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

2) **Parsing** turns tokens into structure.  
   It defines grouping and operator binding.

3) **Semantic analysis** adds meaning to structure.  
   It resolves names, checks scopes, and enforces rules such as type constraints.

4) **Intermediate representation (IR)** converts meaning into a form that is easy to analyze and transform.  
   It standardizes control flow and data flow.

5) **Optimization** improves efficiency without changing meaning.  
   It removes waste and simplifies computation.

6) **Code generation** turns the IR into machine-level instructions.  
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
