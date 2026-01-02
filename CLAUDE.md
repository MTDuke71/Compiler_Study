# CLAUDE.md

## Links
- Up: [[README]]
- Related: [[00-index/README]] [[00-index/curriculum-roadmap]] [[00-index/invariants]]

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **knowledge graph for compiler construction** designed as a Zettelkasten using Obsidian. It is:
- textbook-agnostic
- implementation-oriented
- concept-driven rather than chapter-driven
- intentionally unfinished and evolving

The goal: understand **why all real compilers eventually take the shape they do**.

## Core Philosophy

A compiler is a **pipeline that progressively removes ambiguity**.

Guiding invariants:
- Syntax describes structure, not meaning
- Semantics constrain behavior, not syntax
- Optimization never creates meaning
- All representations are tradeoffs
- Complexity cannot be eliminated, only relocated

## Repository Structure

### Two Complementary Layers

1. **Structured Notes (Narrative)**: `01-foundations/`, `02-lexing/`, `03-parsing/`, `04-semantics/`, `05-ir/`, `06-optimization/`, `07-codegen/`
   - Explain ideas in context
   - Capture learning sessions (e.g., Day 1-4)
   - Approachable to readers
   - Evolve over time

2. **Zettels (Atomic Concepts)**: `/zettel/`
   - Each captures **one idea**
   - Self-contained
   - Links aggressively using `[[wikilinks]]`
   - Designed to age well
   - Examples: `Z0001-state.md`, `Z0005-compiler-phases.md`

3. **Index**: `/00-index/`
   - `compiler-map.md`: Overview of compiler concepts
   - `invariants.md`: Core principles that don't change
   - `learning-log.md`: Progress tracking
   - `curriculum-roadmap.md`: 12-16 week structured learning path

4. **Daily/Weekly Notes**: Track progress and reflections
   - `Daily Notes/YYYY-MM-DD.md`
   - `Weekly Notes/YYYY-Wnn.md`

## Working with This Repository

### Obsidian Integration
This repository is designed to be opened directly in Obsidian:
- Graph view enabled
- Backlinks enabled
- Unlinked mentions enabled
- Use `[[wikilinks]]` freely

### File Naming Conventions
- Structured notes: lowercase with hyphens (e.g., `day-01-what-is-a-compiler.md`)
- Zettels: `Z####-topic.md` format (e.g., `Z0001-state.md`)
- All markdown files use `.md` extension

### Link Structure
Every note includes a "Links" section at the top:
```markdown
## Links
- Up: [[parent-note]]
- Related: [[related-note-1]] [[related-note-2]]
- Down: [[child-note]]
```

## Learning Approach

Follows a **V-cycle learning model**:
1. Start with top-down mental model
2. Descend into concrete mechanisms
3. Ascend back to abstraction through validation

Theory is introduced **when code demands it**, not before.

## Key Compiler Phases (from Z0005)

Each phase removes specific ambiguity:
1. **Lexing**: defines tokens from characters
2. **Parsing**: defines structure from tokens
3. **Semantics**: defines meaning and legality
4. **IR**: defines stable form for analysis
5. **Optimization**: improves performance without changing meaning
6. **Codegen**: targets the machine

The pipeline is not optional; it is the minimum sequence that makes execution possible.

## Recommended Progression

See `00-index/curriculum-roadmap.md` for full 12-16 week plan.

Quick overview:
- **Weeks 1-2**: Foundations and mental models
- **Weeks 3-4**: Lexing
- **Weeks 5-6**: Parsing
- **Week 7**: Semantics
- **Weeks 8-9**: Intermediate Representation
- **Week 10**: Optimization
- **Weeks 11-12**: Code Generation
- **Weeks 13-16**: Integration and extension

## Navigation Strategy

When helping with this repository:

1. **For concept questions**: Check both structured notes AND zettels
2. **For learning path**: Refer to `curriculum-roadmap.md`
3. **For philosophy**: Check `README.md` and `invariants.md`
4. **For specific phases**: Navigate to numbered directories (`01-foundations/`, etc.)

## Content Characteristics

- Non-linear growth expected
- Topics revisited multiple times
- Earlier notes may be contradicted (and resolved) by later ones
- Links accumulate faster than pages
- Implementation examples use pseudocode or are described conceptually (no specific language)

## What This Repository Is NOT

- Not a "build a compiler in 24 hours" guide
- Not language-specific
- Not a linear textbook
- Not focused on instant gratification
- Implementation code is minimal/pseudocode (this is a knowledge repository, not a code repository)
