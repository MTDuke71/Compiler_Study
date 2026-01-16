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

### Passive but Questioning

The learning philosophy is **passive learning with depth** over active exercises:
- Read comprehensive, detailed explanations
- Daily notes are pre-filled for reading (not templates to complete)
- Use repetition with variation (training document + daily note synthesis)
- Encourage questioning and exploration, not rote memorization

**Why this works:** Reading complete content twice (once detailed, once condensed) creates stronger encoding and retention through spaced repetition with different framing.

### Implementation Cycle (Week 3+)

**Read → Run → Modify → Understand**
1. **Read:** Complete, working code with thorough comments
2. **Run:** Execute and observe behavior
3. **Modify:** Request changes, experiment with variations
4. **Understand:** Through iteration, internalize patterns

Not copy-paste tutorials, but code you can read, run, break, fix, and extend.

### V-Cycle Model

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

## Cross-Domain Analogies

The user has deep expertise in:
1. **Chess engine development** - perft testing, evaluation functions, search depth
2. **Advent of Code optimization** - profiling, measuring, finding simple wins

**Use these analogies extensively** when explaining compiler concepts:

### Chess Engine ↔ Compiler Parallels

| Chess Engine | Compiler | Core Insight |
|--------------|----------|--------------|
| Must follow chess rules | Must preserve semantics (invariants) | Non-negotiable constraints |
| Perft testing | Invariant checking | Checksums for correctness |
| Evaluation complexity | Optimization passes | Quality vs. cost tradeoff |
| Search depth | Compile time | How much analysis to do |
| Board representation | IR design | Internal form optimized for analysis |
| Move generation | IR generation | Convert position to analyzable form |
| Opening book + search | JIT tiered compilation | Fast first, optimize hot paths |
| Simple eval + deep search vs. complex eval + shallow | -O0 vs -O3 | Same tradeoff pattern |

### Advent of Code ↔ Compiler Optimization

| AoC Lesson | Compiler Application |
|------------|---------------------|
| Measure, don't guess | Profile before optimizing |
| Simple often beats complex | Linear scan register allocation in production JITs |
| Big changes ≠ big improvements | Diminishing returns at higher -O levels |
| Profile first | Data flow analysis finds actual bottlenecks |
| Better data structure > clever algorithm | Right IR enables optimization |

**When explaining concepts:** Default to chess/AoC analogies when possible. They make abstract concepts concrete and leverage existing mental models.

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
- Implementation examples will be actual code (Week 3+), not pseudocode
- Training materials are comprehensive; daily notes synthesize
- Repetition with variation is intentional and valuable

## Content Creation Guidelines
 (but will include actual implementation code)
- Not a linear textbook
- Not focused on instant gratification
- Not fill-in-the-blank exercises (passive reading, active questioning)

## Key Session Insights

Patterns that have proven effective:

1. **Multiple representations aren't redundant** - Each IR (AST, TAC, CFG, SSA) is optimized for different operations
2. **Invariants are contracts between phases** - Like perft testing in chess engines, they're checksums for correctness
3. **Every design choice is a tradeoff** - Context determines the right solution; there is no universally best approach
4. **Simple can beat complex** - Linear scan in production compilers, constant folding's high impact despite simplicity
5. **Measure, don't guess** - Profile before optimizing (AoC lesson applies universally)
6. **Repetition with variation strengthens learning** - Read detailed training doc, then condensed daily note
7. **Cross-domain analogies make abstract concepts stick** - Chess and AoC provide concrete mental models

## Special Considerations

- **Glossary maintenance:** Keep `00-index/glossary.md` updated with new acronyms and terms
- **Graph visualization:** User appreciates seeing the knowledge graph grow and densify
- **Commit messages:** Be descriptive about what was added and why
- **Week transitions:** Clearly mark when moving from theory to implementation
- **Testing approach:** Like perft testing - clear invariants to verify correctness
- Code snippets with concrete illustrations
- Tables for visual comparison
- Liberal cross-referencing to related concepts

### For Daily Notes
- Pre-filled with synthesis (not templates to complete)
- Reinforce training material with different framing
- Include insights section (aha moments and connections)
- Questions raised (encourage deeper exploration)
- Reflection prompts completed with thoughtful responses

### For Zettel Notes
- Atomic concepts (one clear idea per zettel)
- Self-contained (can be read independently)
- Aggressive linking (connect to all related concepts)
- Timeless (should age well as understanding deepens)

## What This Repository Is NOT

- Not a "build a compiler in 24 hours" guide
- Not language-specific
- Not a linear textbook
- Not focused on instant gratification
- Implementation code is minimal/pseudocode (this is a knowledge repository, not a code repository)
