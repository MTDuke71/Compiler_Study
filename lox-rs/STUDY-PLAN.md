# lox-rs Study Plan

## Links
- Up: [[README]]
- Related: [[00-index/curriculum-roadmap]] [[00-index/invariants]]

## Purpose

A hands-on study plan for completing the **lox-rs** tree-walk interpreter, following *Crafting Interpreters* Part II (Chapters 4-13). The goal is not just to get code working, but to **understand the design decisions** and connect them back to the compiler theory in the knowledge graph.

This plan follows the Read -> Run -> Modify -> Understand cycle from the curriculum.

---

## Current State (as of 2026-04-02)

### What's Built

| File | What It Does | CI Chapter | Status |
|------|-------------|------------|--------|
| `token.rs` | Token types, Literal enum | Ch 4 | Complete |
| `scanner.rs` | Hand-written lexer, all Lox tokens | Ch 4 | Complete |
| `ast.rs` | Expr and Stmt enums | Ch 5-8 | Partial — has Call/Function/Return nodes, missing class nodes |
| `parser.rs` | Recursive descent, expressions through functions | Ch 6-8 | Complete for current feature set |
| `environment.rs` | HashMap-based scopes, clone for nesting | Ch 8 | Works but needs rethinking for closures |
| `interpreter.rs` | Tree-walk eval, variables, control flow, blocks | Ch 7-9 | Core works; function calls and closures are stubs |
| `main.rs` | REPL + file runner | Ch 4 | Complete |

### What's Stubbed

- `Stmt::Function` — parser handles it, interpreter just defines name as `Nil`
- `Expr::Call` — parser handles it, interpreter returns error
- `Stmt::Return` — parser handles it, interpreter uses hacky `__return__` string unwinding

### Test Coverage

53 tests across scanner (13), parser (12), interpreter (28). All green.

---

## The Plan

### Phase 1: Functions and Closures (Ch 10)

**The big one.** This is where lox-rs goes from "calculator with variables" to "real language." Think of it like adding search to a chess engine that can only do move generation — suddenly the whole thing has a purpose.

#### Step 1A: LoxCallable Trait and Native Functions

**Goal:** Define what it means to be "callable" in Lox.

**Read first:** Crafting Interpreters Ch 10, sections on "Function Calls" and "Native Functions."

**What to build:**
- A `LoxCallable` trait (or enum) with `call()` and `arity()` methods
- A `LoxFunction` type that wraps `Stmt::Function` data
- Extend `Literal` enum to hold callable values (e.g. `Literal::Function(...)`)
- Implement `clock()` as a real native function (not a Nil placeholder)

**Key design decision:** How to represent functions as values. Crafting Interpreters uses a Java interface; in Rust you'll need to choose between:
- Trait objects (`Box<dyn LoxCallable>`) — most faithful to CI
- An enum variant on `Literal` — simpler, avoids dynamic dispatch
- `Rc<dyn LoxCallable>` — needed if functions are first-class values that get cloned

**Connect to theory:**
- [[zettel/Z0005-compiler-phases]]: Functions don't change the *phases* (scan, parse, interpret), but they change what each phase must handle
- [[04-semantics/scope]]: Function parameters create a new scope — same mechanism as blocks, but parameterized

**Tests to write:**
- `clock()` returns a number
- Calling a non-function is a runtime error
- Wrong number of arguments is a runtime error

#### Step 1B: Function Declarations and Calls

**Goal:** `fun add(a, b) { return a + b; } print add(1, 2);` prints `3`.

**What to build:**
- Implement `Expr::Call` evaluation in the interpreter
- Evaluate arguments, check arity, bind parameters to a new environment
- Execute function body in that environment
- Handle `return` properly (replace the `__return__` string hack with a proper control flow mechanism)

**Key design decision:** How to handle `return`. The current `__return__` string prefix is fragile. Options:
- A `Return` struct used as a sentinel error (CI's approach) — already partially there
- A custom `Result` type with `Ok(()) | Return(Literal) | Err(String)`

**The chess analogy:** Return is like a cutoff in alpha-beta search. You're evaluating a position (executing statements), and you hit a condition that says "stop evaluating this branch, I have the answer." The unwinding is the same pattern — propagate upward until someone catches it.

**Tests to write:**
- Simple function call with return value
- Function with no return (implicit nil)
- Recursive function (fibonacci or factorial)
- Function as expression (assign to variable, pass as argument)

#### Step 1C: Closures

**Goal:** Functions capture their enclosing environment.

```lox
fun makeCounter() {
  var i = 0;
  fun count() {
    i = i + 1;
    print i;
  }
  return count;
}
var counter = makeCounter();
counter(); // 1
counter(); // 2
```

**What to build:**
- When a function is declared, snapshot the current environment
- When a function is called, use that snapshot (not the call-site environment)
- This likely means moving from `Environment` cloning to `Rc<RefCell<Environment>>` — the biggest refactor in the project

**Why this is hard:** The current `Environment` is cloned when entering a block. Closures need *shared* environments — two closures over the same variable must see each other's mutations. Clone won't cut it.

**The AoC analogy:** This is like discovering your data structure can't handle Part 2. You built a working solution for Part 1 (blocks with cloned environments), and now the requirements demand shared state. Better data structure > clever algorithm — right `Rc<RefCell<>>` enables closures without algorithmic tricks.

**Connect to theory:**
- [[04-semantics/scope]]: Closures are the most interesting scoping story — lexical scope captured at definition time
- [[01-foundations/language-as-state]]: A closure *is* a state machine: the function body is the transition function, the captured environment is the state

**Tests to write:**
- Closure captures variable from enclosing scope
- Two closures over the same variable share state
- Closure in a loop captures each iteration correctly (or doesn't — Lox has a known footgun here)

---

### Phase 2: Variable Resolution (Ch 11)

**Why this exists:** Without a resolver, variable lookup walks the environment chain at runtime every time. The resolver does a static analysis pass that figures out *how many hops* each variable reference needs — like pre-computing an opening book instead of searching from scratch.

#### Step 2A: The Resolver Pass

**Goal:** A new AST walk that resolves variable references before interpretation.

**What to build:**
- A `Resolver` struct that walks the AST
- For each variable use, compute the "depth" (how many scopes out)
- Store the results in a side table (HashMap from expression to depth)
- Report errors: variable used in its own initializer, local variable never used (optional)

**Key design decision:** How to identify expressions for the side table. CI uses object identity (Java). In Rust, you'll need another approach:
- Assign each `Expr` a unique ID
- Use a `HashMap<*const Expr, usize>` (raw pointer as key)
- Thread resolution depth into the AST nodes themselves

**Connect to theory:**
- [[06-optimization/constant-folding]]: The resolver is an optimization pass — same concept, different target. Instead of folding constants, you're folding scope lookups.
- [[04-semantics/symbol-tables]]: The resolver *is* building a lightweight symbol table. Stanford's scope/symbol-table lectures directly apply here.

**Tests to write:**
- Variable used before declaration in same scope is an error
- Variable in own initializer is an error
- Top-level `return` is an error
- Nested functions resolve to correct depth

#### Step 2B: Integrate Resolver with Interpreter

**Goal:** The interpreter uses resolved depths instead of walking the chain.

**What to build:**
- `Environment::get_at(depth, name)` and `assign_at(depth, name, value)`
- Modify `Interpreter` to consult the resolution table
- Globals remain unresolved (looked up dynamically) — this is intentional

**Tests to write:**
- All existing tests still pass (regression)
- Shadowing works correctly with resolution
- Closures still work after resolution

---

### Phase 3: Classes (Ch 12)

**Where Lox gets object-oriented.** This is a big chapter but the groundwork from Phase 1 (callable trait, closures) makes it tractable.

#### Step 3A: Class Declarations and Instances

**Goal:** `class Foo {} var foo = Foo(); print foo;`

**What to build:**
- New AST nodes: `Expr::Get`, `Expr::Set`, `Stmt::Class`
- Extend parser for `class` keyword, property access (`.`), property assignment
- `LoxClass` type that implements `LoxCallable` (classes are callable — calling creates instances)
- `LoxInstance` type with property storage (HashMap)
- Extend `Literal` to hold class and instance values

**Connect to theory:**
- [[07-codegen/stack-machines]]: Object layout in memory — Stanford's lectures on vtables and dispatch directly preview what's happening here at a higher level
- A class is a factory (callable that produces instances). An instance is a namespace (environment for properties).

**Tests to write:**
- Class declaration and instantiation
- Getting and setting properties
- Accessing undefined property is runtime error

#### Step 3B: Methods and `this`

**Goal:** Classes have methods; `this` binds to the instance.

**What to build:**
- Methods stored on the class (not the instance)
- When a method is accessed on an instance, bind `this` to that instance (create a new environment with `this` defined)
- `init()` method as constructor — called automatically, returns `this`

**The chess analogy:** `this` binding is like the side-to-move in a chess position. Every method "knows" which instance it's operating on, just like every evaluation function knows whose perspective to score from.

**Tests to write:**
- Method call on instance
- `this` refers to the correct instance
- `init` is called on construction
- `init` implicitly returns `this`
- `return` inside `init` returns `this` (not the value)

---

### Phase 4: Inheritance (Ch 13)

**The final chapter.** Lox supports single inheritance with `super`.

#### Step 4A: Superclasses

**Goal:** `class B < A { }` — B inherits A's methods.

**What to build:**
- Extend parser and AST for `< superclass` syntax
- Method resolution: look in subclass first, then superclass chain
- `super.method()` — like `this` but starts lookup in the superclass

**Connect to theory:**
- [[04-semantics/types-as-constraints]]: Inheritance creates a subtype relationship. Stanford's lectures on subtyping (Week 5) formalize exactly this.
- [[00-index/invariants]]: Behavioral substitutability — a subclass instance should work anywhere the superclass is expected.

**Tests to write:**
- Subclass inherits superclass methods
- Subclass can override methods
- `super.method()` calls the superclass version
- Superclass must be a class (not a number, string, etc.)
- Diamond problem doesn't exist (single inheritance)

---

## After Completion

When all four phases are done, lox-rs will be a **complete tree-walk interpreter** for Lox. At that point:

1. **Run the Crafting Interpreters test suite** — Robert Nystrom provides one. Validate against it.
2. **Write a non-trivial Lox program** — something recursive, with closures and classes. A linked list, a simple game, or an expression evaluator (a Lox program that interprets expressions — compilers all the way down).
3. **Reflect on the architecture** — what would you change? Where did Rust fight you vs. help you? Document this in a zettel.
4. **Connect back to the curriculum** — this completes the "hands-on reinforcement" for Weeks 13-14 (lexing + parsing were already done; functions/classes are the meaty part). Update the roadmap.

### Optional Extensions (pick any that interest you)

- **Static methods** — methods that don't need `this`
- **Getters** — properties computed on access
- **Break/continue** in loops
- **Multi-line strings** or **string interpolation**
- **Lambda expressions** — `fun(x) { return x * 2; }` as an expression
- **Error handling** — try/catch or Result-like patterns

---

## Pacing

Each phase is roughly **1-2 weeks** at 60-90 min/day:

| Phase | Estimated Time | Complexity |
|-------|---------------|------------|
| Phase 1: Functions & Closures | 1.5-2 weeks | High (Rc/RefCell refactor) |
| Phase 2: Resolver | 1 week | Medium (new pass, but mechanical) |
| Phase 3: Classes | 1-1.5 weeks | Medium-high (new types, method binding) |
| Phase 4: Inheritance | 0.5-1 week | Medium (builds on Phase 3) |

**Total: ~4-6 weeks** — fits naturally into the curriculum's Weeks 13-18 hands-on reinforcement window.

The hardest part is Phase 1C (closures / `Rc<RefCell<>>` refactor). Everything after that builds incrementally.

---

## How to Use This Plan

1. **Read the relevant CI chapter** before coding
2. **Read the existing lox-rs code** for that module — understand what's already there
3. **Write tests first** for the new feature
4. **Implement** — get tests green
5. **Run the full suite** — no regressions
6. **Reflect** — what compiler concept did this exercise? Create or update a zettel if you had an insight.

This is a living document. Update it as you go.
