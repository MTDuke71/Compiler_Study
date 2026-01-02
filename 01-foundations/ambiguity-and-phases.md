# Ambiguity and Phases

## Links

- Up: [[01-foundations/README]]
- Related:
  - [[01-foundations/day-01-what-is-a-compiler]]
  - [[01-foundations/day-02-from-text-to-structure]]
  - [[01-foundations/day-03-structure-to-meaning]]
  - [[zettel/Z0005-compiler-phases]]
  - [[zettel/Z0004-invariants]]
- Down: [[01-foundations/day-01-what-is-a-compiler]]

## Core principle

**Each compiler phase exists to resolve a specific kind of ambiguity.**

Source code is intentionally compact and human-friendly, which makes it ambiguous.
Compiler phases systematically eliminate ambiguity, transforming the program into forms that are increasingly explicit and machine-executable.

## The pattern: ambiguity → resolution → precision

### Characters are ambiguous about boundaries

Source text: `x=3+4*5`

**Ambiguity:** Where does one symbol end and another begin?
- Is it `x`, `=`, `3`, `+`, `4`, `*`, `5`?
- Or `x=3`, `+4*`, `5`?
- Or something else entirely?

**Resolution:** Lexing
- **Input:** Character stream
- **Output:** Token stream with explicit boundaries
- **Result:** `IDENT(x) EQUALS INT(3) PLUS INT(4) STAR INT(5)`

### Tokens are ambiguous about structure

Token stream: `x EQUALS 3 PLUS 4 STAR 5`

**Ambiguity:** How do operators bind?
- Is it `x = (3 + 4) * 5`? (Result: 35)
- Or `x = 3 + (4 * 5)`? (Result: 23)
- Or `(x = 3) + (4 * 5)`? (Nonsensical)

**Resolution:** Parsing
- **Input:** Token stream
- **Output:** Tree structure with explicit precedence
- **Result:** `Assign(x, Add(Int(3), Mul(Int(4), Int(5))))`

### Structure is ambiguous about meaning

Parse tree:
```
Assign(
  name = "x",
  value = Add(Ident("y"), Int(1))
)
```

**Ambiguity:** What do the names refer to?
- Does `x` exist? Was it declared?
- What is `y`? What type does it have?
- Can you add `y` to an integer?
- Is `x` allowed to be modified?

**Resolution:** Semantic analysis
- **Input:** Parse tree
- **Output:** Annotated tree + symbol table
- **Result:** Names resolved, types checked, constraints validated

### High-level structure is ambiguous about execution

Semantic tree with meaning:
```
Assign(x: int, Add(y: int, Int(1)))
```

**Ambiguity:** How should this execute?
- What is the order of evaluation?
- Are there dependencies between statements?
- Can subexpressions be reordered or eliminated?

**Resolution:** IR translation
- **Input:** Annotated AST
- **Output:** Control-flow graph with explicit data flow
- **Result:** Three-address code or SSA form

### IR is ambiguous about efficiency

Three-address code:
```
t1 = 4 * 5
t2 = 3 + t1
x = t2
```

**Ambiguity:** Is this the fastest representation?
- Can `t2` be eliminated?
- Can constants be folded?
- Are there redundant computations?

**Resolution:** Optimization
- **Input:** IR
- **Output:** Transformed IR (same meaning, better performance)
- **Result:** `x = 23` (constant folded)

### IR is ambiguous about target machine

Optimized IR: `x = 23`

**Ambiguity:** How does this map to machine instructions?
- Which register should hold `23`?
- Where in memory is `x` located?
- What is the exact instruction encoding?

**Resolution:** Code generation
- **Input:** Optimized IR
- **Output:** Machine code
- **Result:** `mov dword ptr [rbp-4], 23`

## Why phases cannot be collapsed

Each phase depends on the guarantees established by the previous one:

- **Parsing requires tokens** because structure depends on knowing where symbols begin and end.
- **Semantics requires structure** because name resolution depends on scope (which comes from nesting).
- **IR requires meaning** because control flow cannot be represented without knowing what operations do.
- **Optimization requires IR** because you cannot eliminate redundancy in source-level syntax.
- **Code generation requires optimization** because register allocation needs to know which values are live.

Skipping a phase does not simplify the compiler—it makes the next phase impossible.

## Key insight: precision has a cost

Each phase trades **conciseness** for **precision**:

- Source code: compact, ambiguous, human-friendly
- Tokens: slightly more verbose, boundaries explicit
- Parse tree: larger still, structure explicit
- Annotated AST: names and types explicit
- IR: control flow and data flow explicit
- Machine code: all decisions explicit, maximum verbosity

This is not accidental. **Ambiguity is compression.** Humans tolerate ambiguity because it makes code shorter and easier to write. Machines require precision because they cannot infer intent.

The compiler is the translator between these two extremes.

## Why this matters

When you encounter a compiler error, the phase tells you what kind of ambiguity failed to resolve:

- **Lexical error:** Character sequence is malformed (e.g., `3.14.15`)
- **Syntax error:** Token sequence does not form a valid structure (e.g., `x = + 3`)
- **Semantic error:** Structure is valid but violates meaning rules (e.g., `x = "hello" + 5`)
- **Optimization error:** IR transformation is unsound (rare; usually a compiler bug)
- **Code generation error:** Target architecture limitation (e.g., `register allocation failed`)

Each error is a different kind of ambiguity the compiler could not resolve.

## Anti-patterns to avoid

### Trying to do semantic analysis during parsing
Parsing builds structure; semantics requires structure to already exist.
Mixing the two creates fragile, order-dependent logic.

### Expecting the compiler to "figure it out"
Compilers enforce rules. They do not guess.
If the language says "`int + string` is illegal," the compiler will reject it—even if a human could infer intent.

### Treating phases as optional
Even the smallest language needs all phases.
You can make phases simpler, but you cannot eliminate them.

## Connection to other notes

- [[01-foundations/day-01-what-is-a-compiler]] explains why phases exist
- [[01-foundations/day-02-from-text-to-structure]] details lexing and parsing
- [[01-foundations/day-03-structure-to-meaning]] details semantic analysis
- [[zettel/Z0005-compiler-phases]] provides a reference map of all phases
- [[zettel/Z0004-invariants]] lists what each phase preserves

## Success criteria

- You can explain why a specific phase exists (what ambiguity it resolves).
- You can predict which phase will catch a given error.
- You understand that phases are not arbitrary—they are forced by the nature of ambiguity.
