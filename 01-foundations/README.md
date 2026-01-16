# 01-foundations — Map of Content

**Purpose:** Foundational concepts that underpin all compiler design and implementation.

**Scope:** Weeks 1-2 of the curriculum — conceptual understanding before implementation begins.

## Links
- Up: [[README]]
- Related: [[00-index/compiler-map]] [[00-index/invariants]]

---

## Overview

This folder contains the fundamental concepts you need before writing any code. Think of it as the mental model that guides all implementation decisions.

**Core Themes:**
- What compilers do and why they exist
- How programs are represented at different stages
- Properties that must be preserved through transformations
- Design decisions and their tradeoffs

---

## The Four-Day Introduction (Week 1)

### [[01-foundations/day-01-what-is-a-compiler]]
**Day 1 — What Is a Compiler?**

The big picture: what compilers do and why they matter.

**Key concepts:**
- Translation vs. interpretation
- Why compilation is multi-stage
- The contract: preserve meaning, produce executable code

**Read this first** — establishes the foundation for everything else.

---

### [[01-foundations/day-02-from-text-to-structure]]
**Day 2 — From Text to Structure**

How source code becomes a tree (lexing and parsing).

**Key concepts:**
- Lexing: characters → tokens
- Parsing: tokens → AST
- Why syntax matters

**Introduces:** The first two phases of compilation.

---

### [[01-foundations/day-03-structure-to-meaning]]
**Day 3 — Structure to Meaning**

How syntax becomes semantics (type checking and analysis).

**Key concepts:**
- Semantic analysis: what syntax can't express
- Type systems as constraints
- Symbol tables and scopes

**Introduces:** The third phase — where compilers catch logical errors.

---

### [[01-foundations/day-04-meaning-to-representation]]
**Day 4 — Meaning to Representation**

How semantics become executable form (IR and code generation).

**Key concepts:**
- Intermediate representations (IR)
- Why multiple representations exist
- Code generation overview

**Introduces:** Phases 4-6 at a high level (detailed in Week 2).

---

## Deep Concepts (Week 2)

### [[01-foundations/language-as-state]]
**Programs as State Machines**

Understanding programs as state transformations.

**Key concepts:**
- State: what the program knows at any point
- Control flow: how state changes over time
- Observable behavior vs. implementation details

**Why it matters:** This perspective makes control flow graphs and optimization intuitive.

**Cross-references:** [[zettel/Z0001-state]] [[zettel/Z0002-control-flow]]

---

### [[01-foundations/ambiguity-and-phases]]
**Why Compilation Has Phases**

Understanding why we can't do everything at once.

**Key concepts:**
- Separation of concerns
- Each phase has specific responsibilities
- Phases communicate through invariants

**Why it matters:** Explains the pipeline structure, not just what it is.

**Cross-references:** [[zettel/Z0005-compiler-phases]] [[00-index/invariants]]

---

### [[01-foundations/design-tradeoffs]]
**Design Tradeoffs in Compilers**

**Day 8 Topic** — No perfect design exists.

**Key concepts:**
- Compile time vs. runtime performance
- Memory vs. speed
- Simplicity vs. generality
- Early detection vs. flexibility
- Representation choices (AST vs. IR vs. machine code)

**Why it matters:** Every implementation decision is a tradeoff. Understanding these helps you make informed choices, not just copy patterns.

**Analogies:**
- Chess engines: depth vs. evaluation complexity
- AoC optimization: measure first, simple often wins

**Cross-references:** [[05-ir/why-ast-is-not-enough]] [[zettel/Z0003-representation]]

---

### [[01-foundations/representation-to-optimization]]
**From Representation to Optimization**

**Day 9 Topic** — Completing the six-phase mental model.

**Key concepts:**
- Why IR enables optimization (AST doesn't)
- What optimization does (transform while preserving semantics)
- What code generation produces (instruction selection, register allocation, scheduling)
- The complete pipeline with invariants

**Why it matters:** Ties together all six phases. You're ready to implement after understanding this.

**Prepares for:** Week 3 lexer implementation.

**Cross-references:** [[05-ir/README]] [[06-optimization/README]] [[07-codegen/README]]

---

## Conceptual Organization

### By Learning Path

**Start here:**
1. [[01-foundations/day-01-what-is-a-compiler]] — The 50,000-foot view
2. [[01-foundations/day-02-from-text-to-structure]] — First two phases
3. [[01-foundations/day-03-structure-to-meaning]] — Third phase
4. [[01-foundations/day-04-meaning-to-representation]] — Phases 4-6 intro

**Then deepen:**
5. [[01-foundations/language-as-state]] — Conceptual foundation
6. [[01-foundations/ambiguity-and-phases]] — Why the pipeline exists
7. [[01-foundations/design-tradeoffs]] — How to make decisions
8. [[01-foundations/representation-to-optimization]] — Complete model

### By Concept

**Understanding Programs:**
- [[01-foundations/language-as-state]] — Programs as state machines
- [[01-foundations/day-01-what-is-a-compiler]] — What compilers do
- [[01-foundations/representation-to-optimization]] — How transformations work

**Understanding Phases:**
- [[01-foundations/day-02-from-text-to-structure]] — Lex & Parse
- [[01-foundations/day-03-structure-to-meaning]] — Semantic analysis
- [[01-foundations/day-04-meaning-to-representation]] — IR & Codegen
- [[01-foundations/ambiguity-and-phases]] — Why phases exist
- [[01-foundations/representation-to-optimization]] — How phases connect

**Understanding Design:**
- [[01-foundations/design-tradeoffs]] — No perfect solution
- [[01-foundations/representation-to-optimization]] — Representation choices

---

## Key Takeaways

After completing this folder, you should understand:

**✓ What compilers do:**
- Translate source code to executable form
- Preserve semantics while improving performance
- Catch errors at compile time when possible

**✓ Why compilation has phases:**
- Separation of concerns
- Each phase assumes invariants from previous
- Different representations optimize for different tasks

**✓ The six-phase pipeline:**
1. Lexing: characters → tokens
2. Parsing: tokens → AST
3. Semantics: AST → annotated AST + types
4. IR Generation: AST → intermediate representation
5. Optimization: IR → better IR
6. Code Generation: IR → machine code

**✓ Design principles:**
- Every choice is a tradeoff
- Context determines the right approach
- Simple often beats complex
- Measure, don't guess

**✓ Mental models:**
- Programs as state machines
- Invariants as contracts between phases
- Multiple representations serve different purposes
- Chess engine parallels (rules, tradeoffs, representations)

---

## Where to Go Next

**Week 3 (Implementation begins):**
- [[02-lexing/README]] — Build your first compiler component
- [[02-lexing/regular-languages]] — Theory behind lexing
- [[02-lexing/hand-written-lexer]] — Actual implementation

**Related Conceptual Material:**
- [[00-index/invariants]] — Properties to preserve
- [[00-index/compiler-map]] — Visual overview
- [[zettel/Z0001-state]] through [[zettel/Z0005-compiler-phases]] — Core concepts

**Review Material:**
- [[Daily Notes/2026-01-01]] through [[Daily Notes/2026-01-16]] — Your learning journey
- [[Weekly Notes/2026-W01]] and [[Weekly Notes/2026-W03]] — Week summaries

---

## Notes on This Folder

**Completion status:** ✅ Complete for initial learning

**Usage:**
- **First time:** Read in order (day-01 through representation-to-optimization)
- **Reference:** Use as MOC to find specific concepts
- **Review:** Come back when implementing to reinforce understanding

**Next content creation:** Week 3+ focuses on implementation with theory as needed.

---

## Related Maps of Content

- [[00-index/README]] — Project organization and roadmaps
- [[02-lexing/README]] — Lexical analysis (Week 3)
- [[03-parsing/README]] — Syntax analysis (Weeks 4-5)
- [[04-semantics/README]] — Semantic analysis (Weeks 6-7)
- [[05-ir/README]] — Intermediate representation (Weeks 8-9)
- [[06-optimization/README]] — Optimization techniques (Weeks 9-10)
- [[07-codegen/README]] — Code generation (Weeks 11-12)
