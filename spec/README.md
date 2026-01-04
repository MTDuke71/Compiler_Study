# Language Specification

## Links

- Up: [[README]]
- Related: [[00-index/curriculum-roadmap]]

---

## Overview

This folder contains the **Decaf language specification**—the implementation target for this compiler study project.

Decaf is a pedagogical language designed for compiler construction courses. It's small enough to implement completely while being large enough to cover all major compiler phases.

---

## Contents

- **`decaf_spec.pdf`** — Official language specification from MIT 6.035
- **`decaf-summary.md`** *(optional)* — Summary notes and key points

---

## Source

**Decaf Language Specification**  
MIT 6.035: Computer Language Engineering (Fall 2005)  
Available under MIT OpenCourseWare  
Source: [MIT-OCW Decaf Spec](https://ocw.mit.edu/courses/6-035-computer-language-engineering-sma-5502-fall-2005/resources/decaf_spec/)

Licensed under Creative Commons for educational use.

---

## Why Decaf

- **Complete but constrained**: All compiler phases required, minimal complexity
- **Well-specified**: Unambiguous grammar and semantics
- **Educational design**: Created specifically for learning compiler construction
- **Proven**: Used in multiple university compiler courses
- **Balanced scope**: Not toy (like calculator), not industrial (like C)

---

## Key Language Features

From the specification:

- **Types**: `int`, `boolean`, arrays
- **Control flow**: `if`, `while`, `for`, `break`, `continue`
- **Functions**: Declaration, calls, recursion
- **Operators**: Arithmetic, logical, relational
- **Scoping**: Block-scoped variables
- **I/O**: Basic input/output primitives

---

## Implementation Phases

The Decaf compiler will be built progressively:

1. **Lexer**: Tokenize Decaf source
2. **Parser**: Build AST from tokens
3. **Semantic analysis**: Type checking, scope resolution
4. **IR generation**: Lower to intermediate representation
5. **Optimization**: Basic optimizations (constant folding, DCE)
6. **Code generation**: Target assembly or bytecode

See [[00-index/curriculum-roadmap]] for detailed timeline.

---

## Usage

Place the downloaded `decaf_spec.pdf` in this folder.  
Refer to it when implementing each compiler phase.

All implementation code is original work—this specification is used purely as a language definition, not as a source for compiler implementation details.
