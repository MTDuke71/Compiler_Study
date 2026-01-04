# Day 1 (60 minutes): What Exists and Why

## Links

- Up: [[01-foundations/README]]
- Related: [[zettel/Z0005-compiler-phases]] [[01-foundations/ambiguity-and-phases]]
- Down: [[01-foundations/day-02-from-text-to-structure]]

## Core idea

A compiler transforms text into behavior while preserving meaning.  
Each phase removes a specific ambiguity so the next phase can be precise.

## The unavoidable phases (plain facts)

Most compilers have these six phases:

1) **Lexing** turns a stream of characters into tokens.  
   It defines where symbols begin and end.

2) **Parsing** turns tokens into structure (AST).  
   It defines grouping and operator binding.  
   **AST** (Abstract Syntax Tree) is a tree representation of the program's structure where each node represents a construct in the source code (expression, statement, etc.).

3) **Semantic analysis** adds meaning (Annotated AST) to structure.  
   It resolves names, checks scopes, and enforces rules such as type constraints.

4) **Intermediate representation (IR) Translation** converts meaning into a form that is easy to analyze and transform.  
   It standardizes control flow and data flow.

5) **Optimization** improves efficiency without changing meaning.  
   It removes waste and simplifies computation.

6) **Code generation** turns the Optimized IR into machine-level instructions.  
   It targets the calling convention, register set, and architecture.

These phases exist because each one reduces ambiguity that the next cannot afford.

## A minimal language still needs all phases

Even a toy language with integers, variables, `+`, `*`, assignment, and `print` needs:

- **Structure** so the program can be parsed.
- **Meaning** so names and rules are enforced.
- **Representation** so the program can be transformed and executed.

Small languages do not eliminate phases; they only shrink their scope.

## Invariants to anchor the rest of the course

- Syntax is about structure, not meaning.  
- Optimization preserves meaning; it only changes performance.  
- Every representation is a compromise between clarity and efficiency.

## Success criteria for Day 1

- You can describe why phases exist without memorizing their names.  
- Diagrams feel descriptive, not mysterious.  
- You feel oriented rather than informed.

---

## Exercise Answers & Review

### Exercise 1.1.1: Difference between compiler and interpreter

**My Answer:**  
Compiler translates source code to machine code. Interpreter does not generate machine code as the final step.

**Review:**  
✓ Correct that compilers generate machine code while interpreters don't as final output  
💡 **Missing key point**: The behavioral difference—compilers translate the *entire* program first (creating an executable), then run it separately. Interpreters execute source code *directly* without creating a standalone executable.

---

### Exercise 1.1.2: Advantages of compiler vs interpreter

**My Answer:**  
Compiler is faster. Interpreter has better error messages because it executes statement by statement.

**Review:**  
✓ Correct that compiled code runs faster  
✓ Good observation about interpreter error messages  
💡 **Additional advantages**:
- **Compiler advantages**: optimizations, no runtime overhead, can distribute without source code
- **Interpreter advantages**: faster development cycle (no compilation step), better portability, easier debugging, dynamic features

---

### Exercise 1.1.3: Assembly language vs machine language

**My Answer:**  
Assembler can use macros and link with other files easier.

**Review:**  
⚠️ Partially correct, but missing the main point  
💡 **Key advantage**: **Portability**—assembly can be assembled for different target machines, while machine code is architecture-specific. Assembly also provides:
- Symbolic references (labels instead of addresses)
- Macro expansion
- Readable mnemonics vs binary opcodes
- Easier maintenance and debugging

---

### Exercise 1.1.4: C as target language

**My Answer:**  
Can write in easier language like Python, but then do a final compile in lower-level language that would be faster.

**Review:**  
✓ Right direction about using easier source languages  
💡 **Key advantages of C as target**:
- Leverage existing C compilers (portability to many platforms)
- Mature optimization infrastructure (decades of work in C compilers)
- Widespread tooling (debuggers, profilers, linkers)
- Well-understood compilation target
- Don't need to generate machine code directly

---

### Exercise 1.1.5: Tasks of an assembler

**My Answer:**  
Lexing, Parsing, Semantic Analysis, Translation, Optimization, Code Generation.

**Review:**  
❌ **Wrong answer**—these are compiler phases, not assembler tasks!  
**Assembler tasks include**:
- Translate mnemonics (e.g., `MOV`, `ADD`) to machine opcodes
- Resolve symbolic addresses (labels like `loop:` to actual addresses)
- Expand macros
- Handle assembler directives (`.data`, `.text`, etc.)
- Perform two-pass assembly (first pass: build symbol table, second pass: generate code)
- Calculate offsets and addresses
- Generate object files for linking
