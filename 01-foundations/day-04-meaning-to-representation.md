# Day 4 (60 minutes): From Meaning to Representation

## Links

- Up: [[01-foundations/README]]
- Related:
  - [[01-foundations/day-03-structure-to-meaning]]
  - [[01-foundations/ambiguity-and-phases]]
  - [[05-ir/why-ast-is-not-enough]]
  - [[05-ir/three-address-code]]
  - [[05-ir/cfg]]
  - [[zettel/Z0003-representation]]
- Down: [[05-ir/why-ast-is-not-enough]]

## Goal
Understand why semantic analysis alone is insufficient for optimization and code generation.
By the end, you should know what **Intermediate Representation (IR)** is, why it exists, and what problems it solves that the AST cannot.

## The problem: AST is designed for validation, not transformation

After semantic analysis, you have a well-formed, type-checked AST.
Every name is resolved. Every constraint is satisfied. The program is **valid**.

But the AST has a problem: **it preserves source-level structure**.

This structure is great for humans and great for error reporting.
But it is terrible for:

- **Optimization** (too much irrelevant detail)
- **Code generation** (wrong level of abstraction)
- **Analysis** (control flow is implicit, not explicit)

## What the AST knows vs. what the compiler needs

### The AST knows:
- The syntactic structure of the source
- The types and names of all expressions
- The nesting of blocks and statements

### The compiler needs:
- The **order of execution** (control flow)
- The **dependencies between values** (data flow)
- A **uniform representation** of operations (no special cases)
- A form that is **easy to analyze and transform**

The AST provides the first list. IR provides the second.

## Concrete example: loops and control flow

Source:
```txt
while (x < 10) {
  x = x + 1
}
```

AST (semantic analysis output):
```txt
WhileLoop(
  condition = Less(Ident("x"), Int(10)),
  body = Block([
    Assign("x", Add(Ident("x"), Int(1)))
  ])
)
```

This is accurate, but:
- The control flow is **implicit** in the `WhileLoop` node.
- You cannot easily see where execution jumps.
- Optimization requires pattern-matching on tree structure.

IR (control-flow graph):
```txt
entry:
  goto loop_header

loop_header:
  t1 = x < 10
  if t1 goto loop_body else goto exit

loop_body:
  t2 = x + 1
  x = t2
  goto loop_header

exit:
  ...
```

Now:
- Control flow is **explicit** (labeled blocks and jumps).
- Each operation is **atomic** (single assignment per line).
- The loop structure is **decomposed** into basic blocks.

This form is easy to analyze, transform, and optimize.

## Wait, goto is good now?

**If you learned that "goto is harmful," you're right—but only for source code written by humans.**

The confusion:
- **1960s-1980s:** goto was common in BASIC, early C, FORTRAN
- **1968:** Dijkstra's "Go To Statement Considered Harmful" 
- **Modern wisdom:** Use structured control flow (if/while/for) in source code
- **But now:** Compilers use goto everywhere in IR

**Why goto is bad in source code:**
- Makes code hard to read and follow for humans
- Creates "spaghetti code" with arbitrary jumps
- Breaks mental models of program flow
- Makes debugging and maintenance difficult
- Obscures intent (is this a loop? a conditional? error handling?)

**Why goto is good in IR:**
- Makes control flow **explicit** and **analyzable** by the compiler
- Provides a **uniform primitive** that all control structures lower to
- Enables optimization: the compiler can see all possible execution paths
- Simplifies code generation: every control structure is just labels and jumps
- Is **never read by humans** (only by compiler passes)

**The key insight:**
- High-level code (`while`, `if`, `for`) is for **humans** to write and understand
- Low-level code (goto, labels) is the **reality** of how CPUs execute
- The compiler's job is to translate human-friendly → machine-friendly

Your C64 BASIC instincts were right for that context! goto is the natural way CPUs think.
Modern programming languages hide goto behind structured constructs to make code easier for humans.
But inside the compiler, it all becomes goto again—because that's what the machine actually does.

**Analogy:**
- Writing source code with goto: like writing directions as "turn at mile marker 47.3"
- Writing source code with `while`: like writing "turn at the red barn"
- The compiler converts both to absolute addresses (goto) because that's what the CPU needs

You're not going backwards—you're seeing what was always happening under the hood! 🎯

## Why IR exists: uniformity and simplicity

The AST has dozens of node types:
- `IfStatement`, `WhileLoop`, `ForLoop`, `SwitchCase`, `TernaryExpr`, etc.

Each has different semantics. Each requires different optimization rules.

IR reduces all of these to a small set of primitives:
- **Assignment** (`x = y + z`)
- **Conditional jump** (`if cond goto label`)
- **Unconditional jump** (`goto label`)
- **Function call** (`result = func(arg1, arg2)`)

Every high-level construct is **lowered** into these primitives.

This makes optimization **modular**: one optimization pass can improve all loops, all conditionals, all expressions—because they all use the same IR operations.

## Two common IR forms

### 1. Three-Address Code (TAC)
Each instruction has at most three operands:

```txt
t1 = a + b
t2 = t1 * c
x = t2
```

- Simple and uniform
- Easy to generate
- Maps naturally to most assembly languages

### 2. Static Single Assignment (SSA)
Each variable is assigned **exactly once**:

```txt
t1 = a + b
t2 = t1 * c
x1 = t2
```

- Enables powerful optimizations (dead code elimination, constant propagation)
- Makes data flow explicit
- Requires phi nodes for merging control flow

Most modern compilers use SSA internally.

## What IR enables

### Optimization
Because IR is uniform and explicit, optimizations become simple transformations:

- **Constant folding:** `t1 = 3 + 4` → `t1 = 7`
- **Dead code elimination:** If `t1` is never used, delete the assignment.
- **Common subexpression elimination:** If `t1 = a + b` appears twice, compute it once.
- **Loop-invariant code motion:** If `t1 = a + b` is computed in a loop but `a` and `b` never change, move it outside the loop.

These are hard to implement on the AST because syntax obscures data flow.

### Code generation
IR is closer to machine code than the AST.

Translating IR to assembly is straightforward:
- Each IR instruction maps to one or more machine instructions.
- Register allocation operates on IR temporaries.
- Calling conventions are applied to IR function calls.

Translating AST directly to assembly requires re-implementing control flow logic for every construct.

## Key insight: IR is the compiler's "working representation"

- **AST** is for understanding the program (source-oriented).
- **IR** is for transforming the program (machine-oriented).
- **Machine code** is the final output (hardware-oriented).

The AST is a bridge from source to meaning.
The IR is a bridge from meaning to execution.

## Why AST cannot be skipped

You might ask: why not generate IR directly from tokens?

Because:
- **Name resolution** requires scope, which comes from nesting (AST structure).
- **Type checking** requires expression shape (AST structure).
- **Control flow lowering** requires knowing what loops and conditionals mean (semantic analysis).

You cannot build IR until you have meaning. You cannot have meaning without structure.

The phases are ordered because each depends on the guarantees of the previous one.

## What comes next (preview)

Once IR exists, the compiler can:

1. **Analyze** the program (data flow, control flow, liveness)
2. **Optimize** the program (constant folding, dead code elimination, inlining)
3. **Generate code** (instruction selection, register allocation)

These phases operate on IR, not on the AST.

The AST's job is done. From here on, everything is transformation.

Next note: [[05-ir/why-ast-is-not-enough]]

## Success criteria for Day 4

- You can explain why the AST is insufficient for optimization.
- You can describe the difference between AST and IR.
- You understand that IR makes control flow and data flow explicit.
- You recognize that IR exists to enable transformation, not validation.
