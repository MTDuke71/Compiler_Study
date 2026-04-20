# Z0024 — Sum Types and the Expression Problem

## Links
- Up: [[03-parsing/trees-vs-structure]]
- Related: [[zettel/Z0020-ast-design]] [[zettel/Z0003-representation]] [[00-index/glossary]]
- Down: —

---

## Core Principle

A language without **sum types + pattern matching** cannot express recursive tree consumers without the **Visitor pattern**. The Visitor pattern is a monument to a missing language feature.

Algebraic Data Types (ADTs) collapse ~40 lines of Java scaffolding into one `match`.

---

## The Expression Problem (Wadler)

Every compiler-like program has two axes of extension:

1. **New data variants** — add `Ternary` expression, add `Match` statement, add `ClassDecl`
2. **New operations** — add `interpret`, add `resolve`, add `type_check`, add `compile_to_rv32`

No mainstream language makes *both* axes cheap. The shape of the language picks one, and the other becomes awkward. The question is which axis matters most for your problem.

---

## Java's Native Shape: Types Easy, Operations Hard

Class hierarchy (OOP without pattern matching) makes axis 1 trivial:

```java
class Binary extends Expr { ... }    // new variant? one new class.
```

But adding axis 2 (a new operation) means touching *every subclass*. There's no way to add behavior from outside the hierarchy.

**The Visitor pattern is the workaround.** It inverts the problem via double dispatch:

```java
interface Visitor<R> {
    R visitBinary(Binary b);
    R visitUnary(Unary u);
    // ... one method per variant
}

class Binary {
    <R> R accept(Visitor<R> v) { return v.visitBinary(this); }
}
```

Now adding an operation = writing one `Visitor` class. But adding a variant means modifying every existing `Visitor`. You traded one pain for the other.

For a compiler this trade is correct — operations (print, resolve, interpret, optimize, codegen) come and go, but AST variants are mostly fixed after the language is designed. The problem isn't the trade, it's that you have to **build the scaffold yourself** every time.

---

## Rust's Native Shape: Both Cheap

```rust
enum Expr {
    Binary { left: Box<Expr>, op: Token, right: Box<Expr> },
    Unary  { op: Token, right: Box<Expr> },
    Literal { value: Literal },
    // ... one line per variant
}

fn interpret(e: &Expr) -> Value {
    match e {
        Expr::Binary { .. } => ...,
        Expr::Unary { .. }  => ...,
        Expr::Literal { .. } => ...,
    }
}
```

- **Add a new operation:** write a new function with a `match`. Exhaustiveness checker forces you to handle every variant.
- **Add a new variant:** add a line to the enum. The compiler walks you to every `match` that needs updating — same pain as Java, but mechanized.

No visitor interface. No accept methods. No codegen tool. The pattern match IS the dispatch.

This is the "expression problem solved (mostly)" sweet spot that every ADT-language gets for free — Haskell, OCaml, Rust, Swift, Scala, Kotlin, C# 9+, TypeScript unions.

---

## ADT — What It Actually Is

**Algebraic Data Type** = a type built by composing two operations:

- **Sum** (variant): a value is *one of* several alternatives. `enum` in Rust, `variant` in ML.
- **Product** (record): a value has *all of* several fields. `struct` or tuple.

"Algebraic" because value counts follow real algebra:
- Product: `(bool, bool)` has 2 × 2 = **4** values
- Sum: `enum E { A(bool), B(u8) }` has 2 + 256 = **258** values

That's not a cute name — it's why the typechecker can *prove* `match` is exhaustive. It knows the finite set of shapes.

**Note on the two ADTs:** In older CS literature, ADT means *Abstract Data Type* (Stack, Queue, Map — a type defined by its operations). Modern FP/Rust usage means *Algebraic*. Same acronym, different meaning.

---

## Why This Matters for Compilers

Every compiler IR is a sum of products:

| IR | Shape |
|---|---|
| Tokens | `enum Token { LeftParen, Number(f64), Identifier(String), ... }` |
| AST | `enum Expr { Binary{..}, Literal{..}, ... }` |
| TAC / three-address code | `enum Instr { Add{..}, Load{..}, Branch{..}, ... }` |
| SSA / MIR | Same shape, phi-functions added |
| Target instructions | `enum RV32 { Add{rd, rs1, rs2}, Jal{rd, imm}, ... }` |

Every phase is `fn phase(input: InputIR) -> OutputIR { match ... }`. The match arms ARE the phase logic. This is the whole pipeline shape.

Java's missing ADT support is why GCC and LLVM are written in C++ with hand-rolled tagged unions + `switch` on an enum field, and why rustc is written in Rust. The tool picks the shape that fits the problem.

---

## Concrete Example: AstPrinter

The Crafting Interpreters Ch5 AstPrinter in Java:

```java
class AstPrinter implements Expr.Visitor<String> {
    String print(Expr expr) { return expr.accept(this); }

    @Override public String visitBinaryExpr(Binary expr) {
        return parenthesize(expr.operator.lexeme, expr.left, expr.right);
    }
    @Override public String visitGroupingExpr(Grouping expr) {
        return parenthesize("group", expr.expression);
    }
    @Override public String visitLiteralExpr(Literal expr) {
        if (expr.value == null) return "nil";
        return expr.value.toString();
    }
    @Override public String visitUnaryExpr(Unary expr) {
        return parenthesize(expr.operator.lexeme, expr.right);
    }
    // + parenthesize() helper with varargs
}
```

Plus the `Visitor<R>` interface declaration. Plus `accept()` method on every `Expr` subclass. Roughly 40 lines across multiple files before a single character of output logic.

The Rust equivalent ([lox-rs/src/bin/ast_printer.rs](../lox-rs/src/bin/ast_printer.rs)):

```rust
fn pretty(e: &Expr) -> String {
    match e {
        Expr::Literal { value } => value.to_string(),
        Expr::Grouping { expression } => format!("(group {})", pretty(expression)),
        Expr::Unary { operator, right } =>
            format!("({} {})", operator.lexeme, pretty(right)),
        Expr::Binary { left, operator, right } =>
            format!("({} {} {})", operator.lexeme, pretty(left), pretty(right)),
        // ... other variants
    }
}
```

One function. No interface. No accept. Same output:

```
-123 * (45.67)  =>  (* (- 123) (group 45.67))
1 + 2 * 3       =>  (+ 1 (* 2 3))
a = b = 5       =>  (= a (= b 5))
```

---

## Chess Engine Analogy

Same shape as **mailbox vs bitboard** board representation. Neither is universally better — the question is which operations dominate.

- Mailbox makes "what piece is on e4?" easy and "all squares attacked by white" hard
- Bitboard flips it

Java's class hierarchy picks "easy to add piece types, hard to add operations." A chess engine wants the opposite — operations (move gen, eval, attack detection) dominate. So does a compiler.

Rust enums give you the chess-engine-shaped answer natively. That's why engines like Stockfish-in-Rust ports exist, and why rustc itself leans hard on enum + match.

---

## Related Concepts

- **Exhaustiveness checking** — the typechecker enforces that `match` handles every variant. Missing case = compile error. This is what makes ADTs safer than class hierarchies: "remember to update every Visitor when you add a variant" is a manual discipline in Java; it's a compile-time guarantee in Rust.

- **Boxing for recursion** — `Box<Expr>` in the recursive positions of `Expr` is Rust-required, not optional. Enums need a known size at compile time; infinite recursion in types would have no size. Java doesn't have this problem because every object is a heap reference by default. This is a representation cost ADT-languages pay for the clean shape.

- **Arena allocation alternative** — production compilers (rustc, Roslyn, Zig stage2) typically use `Vec<Node>` + `NodeId(u32)` indices instead of `Box`. Better cache locality, cheaper serialization, nodes can share subtrees. Same ADT discipline, different backing store.

- **GenerateAst as a symptom** — Nystrom's metaprogram in Ch5 exists only because Java requires ~10 lines of boilerplate per AST variant (constructors, final fields, equals, hashCode, accept). Rust's `#[derive(Debug, Clone)]` + enum variant syntax collapses that to one line. When you find yourself writing a codegen tool to patch around your language's verbosity, that's a signal.

---

## Takeaways

1. **The Visitor pattern is not a good idea — it's a workaround.** It exists because Java's type system can't express recursive tree consumers directly.

2. **ADTs = sum + product + pattern matching.** The three together are what collapse the Visitor scaffold.

3. **Compilers want "operations easy" not "variants easy."** ADT languages are well-matched to compiler work. That's not a coincidence — the ML family (SML, OCaml, Haskell, F#) was literally designed around type-theoretic compiler construction, and modern production compilers (rustc, Scala's compiler, the Roslyn type provider in C#) use them because the match arms *are* the compiler phase logic.

4. **Exhaustiveness turns axis-2 extension from discipline into mechanism.** In Java, adding a new `Expr` subclass means "remember to touch every Visitor." In Rust, the compiler lists them for you.

5. **Every IR you will write for the Lox→RV32 capstone will be an ADT.** Tokens, AST, TAC (if you add it), SSA (if you go that far), RV32 instructions. The enum + match shape repeats at every level of the pipeline.

---

## References

- Philip Wadler, "The Expression Problem" (1998) — the original formulation
- Crafting Interpreters, Chapter 5 — introduces the AST, the Visitor pattern, and the GenerateAst metaprogram
- [[../lox-rs/src/ast.rs]] — the `Expr` enum
- [[../lox-rs/src/bin/ast_printer.rs]] — match-as-visitor demonstration
- [[00-index/glossary]] — ADT entry in TLA section
