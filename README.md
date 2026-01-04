# Compiler Notes — A Living Knowledge Graph

## Links

- Up: None, This is the Root Note
- Related: [[00-index/README]] [[01-foundations/README]]
- Down: [[00-index/README]]

This repository is a **public, evolving knowledge graph on compiler construction**.

It is:

- textbook-agnostic
- implementation-oriented
- concept-driven rather than chapter-driven
- designed to be navigated as a **Zettelkasten** using **Obsidian**

The goal is not to “finish” compilers.  
The goal is to understand **why all real compilers eventually take the shape they do**.

---

## Core Philosophy

A compiler is not a monolith.  
It is a **pipeline that progressively removes ambiguity**.

Across languages, paradigms, and decades, compilers converge on the same ideas:

- state
- transformation
- choice
- representation
- invariants

This repository treats those ideas as **first-class nodes**, not footnotes in a textbook.

---

## What This Repository Is

- A **map**, not a tutorial
- A **knowledge graph**, not a linear course
- A place where theory and implementation meet
- A record of understanding as it evolves

It is intentionally:

- modular
- cross-linked
- readable out of order
- resilient to partial reading

---

## What This Repository Is Not

- A “build a compiler in 24 hours” guide
- A language-specific walkthrough
- A substitute for formal CS education
- A linear textbook clone

If you want instant gratification, this repo may feel slow.  
If you want durable understanding, it compounds.

---

## Structure Overview

The repository is organized into two complementary layers:

### 1. Structured Notes (Narrative)

These live in numbered folders (`01-foundations`, `02-lexing`, etc.).

They:

- explain ideas in context
- capture learning sessions (e.g. Day 1, Day 2)
- evolve over time
- are approachable to readers

Think: *guided exploration*.

---

### 2. Zettels (Atomic Concepts)

These live in `/zettel/`.

Each zettel:

- captures **one idea**
- is self-contained
- links aggressively to related concepts
- avoids pedagogy and chronology

Think: *conceptual atoms*.

Zettels are designed to age well.

---

## Obsidian Compatibility

This repository is designed to be opened directly in **Obsidian**.

Recommended settings:

- Graph view enabled
- Backlinks enabled
- Unlinked mentions enabled

Use `[[wikilinks]]` freely.  
The graph is a feature, not a side effect.

The dailty notes has a template for consistent structure. [[templates/template-daily-note]]

---

## Learning Approach

This project follows a **V-cycle learning model**:

1. Start with a top-down mental model
2. Descend into concrete mechanisms
3. Ascend back to abstraction through validation

Theory is introduced **when code demands it**, not before.

---

## Guiding Invariants

Some beliefs that shape this repository:

- Syntax describes structure, not meaning
- Semantics constrain behavior, not syntax
- Optimization never creates meaning
- All representations are tradeoffs
- Complexity cannot be eliminated, only relocated

These invariants are revisited and refined over time.

---

## Status

This repository is intentionally **unfinished**.

It is expected to:

- grow non-linearly
- revisit topics multiple times
- contradict earlier notes (and resolve them)
- accumulate links faster than pages

That is not a bug.

---

## Who This Is For

This repository may be useful if you:

- want to understand compilers beyond surface syntax
- enjoy systems thinking and abstraction
- are comfortable learning in non-linear ways
- believe ideas outlive tools

If you’re here just to copy code, you’ll be disappointed.  
If you’re here to build understanding, welcome.

---

## Target Language: Decaf

When moving from concepts to implementation, this repository targets the **Decaf** language specification—a pedagogical language designed for compiler construction courses.

**Decaf Specification:**  
Based on MIT 6.035 (Computer Language Engineering), Fall 2005  
Available under MIT OpenCourseWare: [Decaf Language Specification](https://ocw.mit.edu/courses/6-035-computer-language-engineering-sma-5502-fall-2005/resources/decaf_spec/)

**Why Decaf:**
- Small enough to implement completely
- Large enough to cover all compiler phases
- Well-specified and unambiguous
- Designed explicitly for learning
- Balances simplicity with real-world concepts

The specification is used under the MIT OpenCourseWare Creative Commons license for educational purposes. All compiler implementation code in this repository is original work.

---

## License

Content is provided for learning and exploration.  
Reuse is encouraged. Attribution is appreciated.

**Third-Party Materials:**  
Decaf language specification © MIT OpenCourseWare, used under Creative Commons license for educational purposes.

---

## Closing Note

Compilers are not magic.  
They are bookkeeping systems with strong opinions.

This repository exists to make those opinions visible.
