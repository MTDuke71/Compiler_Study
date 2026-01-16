# AI Assistant Instructions

**Primary Guidance:** Read [CLAUDE.md](../CLAUDE.md) in the repository root for complete context on:
- Repository purpose and philosophy
- Structure and organization
- File naming conventions
- Learning approach and methodology
- Compiler phase overview

**This file supplements CLAUDE.md with session-specific guidance.**

---

## Learning Philosophy: "Passive but Questioning"

The user prefers **passive learning with depth** over active fill-in-the-blank exercises:
- Provide comprehensive, detailed explanations in training materials
- Fill in daily notes completely for reading (not for user to complete)
- Use repetition with variation (detailed training doc + condensed daily notes)
- Encourage questioning and exploration, not rote memorization

**Why this works:** Reading complete content twice (once detailed, once synthesized) creates stronger encoding and retention.

---

## Cross-Domain Analogies (Critical!)

The user has deep experience with:
1. **Chess engine development** (perft testing, evaluation, search depth)
2. **Advent of Code optimization** (profiling, measuring, finding simple wins)

**Use these analogies extensively:**

### Chess Engine ↔ Compiler Parallels

| Chess Engine | Compiler | Insight |
|--------------|----------|---------|
| **Must follow chess rules** | **Must preserve semantics (invariants)** | Non-negotiable constraints |
| **Perft testing** | **Invariant checking** | Checksums for correctness |
| **Evaluation complexity** | **Optimization passes** | Quality vs. cost tradeoff |
| **Search depth** | **Compile time** | How much analysis to do |
| **Board representation** | **IR design** | Internal form optimized for analysis |
| **Move generation** | **IR generation** | Convert position to analyzable form |
| **Opening book + search** | **JIT tiered compilation** | Fast first, optimize hot paths |
| **Simple eval + deep search** vs **complex eval + shallow** | **-O0 vs -O3** | Same tradeoff pattern |

### AoC Optimization ↔ Compiler Optimization

| AoC Lesson | Compiler Application |
|------------|---------------------|
| **Measure, don't guess** | Profile before optimizing |
| **Simple often beats complex** | Linear scan in production JITs |
| **Big changes ≠ big improvements** | Diminishing returns at higher -O levels |
| **Profile first** | Data flow analysis finds actual bottlenecks |
| **Better data structure > clever algorithm** | Right IR enables optimization |

**When explaining concepts:** Default to chess/AoC analogies when possible. They make abstract concepts concrete.

---

## Content Creation Guidelines

### For Training Materials
- **Comprehensive and complete** - User reads for understanding
- **Multiple examples** - Show concept from different angles
- **Code snippets** - Concrete illustrations
- **Tables for comparisons** - Visual organization helps
- **Cross-references** - Link to related concepts liberally

### For Daily Notes
- **Pre-filled with synthesis** - Not templates to complete
- **Repetition with variation** - Reinforce training material differently
- **Insights section** - Highlight aha moments and connections
- **Questions raised** - Encourage deeper exploration
- **Reflection prompts** - Completed with thoughtful responses

### For Zettel Notes
- **Atomic concepts** - One clear idea per zettel
- **Self-contained** - Can be read independently
- **Aggressive linking** - Connect to all related concepts
- **Timeless** - Should age well as understanding deepens

---

## Implementation Philosophy (Week 3+)

When we move to code implementation:

**Learning Cycle: Read → Run → Modify → Understand**
1. **Read:** Provide complete, working code with thorough comments
2. **Run:** User executes and observes behavior
3. **Modify:** User asks for changes, experiments
4. **Understand:** Through iteration, internalize patterns

**Not:** Copy-paste tutorials  
**Instead:** Code you can read, run, break, fix, and extend

**Testing approach:** Like perft testing in chess engines - clear invariants to verify correctness.

---

## Communication Style

- **Be concise but complete** - No unnecessary framing
- **Explain why, not just what** - Understanding trumps memorization
- **Use analogies freely** - Especially chess and AoC
- **Assume smart reader** - User is experienced programmer
- **Encourage questions** - "Passive but questioning"

**Examples of good responses:**
- "That's like perft testing - invariants give you a checksum for correctness"
- "Same tradeoff as chess: evaluation complexity vs. search depth"
- "Linear scan in production JITs is like simple eval + deep search"

---

## File Organization

**When creating new content:**
- Training materials → `0X-topic/` folders
- Daily notes → `Daily Notes/YYYY-MM-DD.md`
- Atomic concepts → `zettel/ZXXXX-topic.md`
- Reference → `00-index/`

**Always include standard header:**
```markdown
## Links
- Up: [[parent]]
- Related: [[related-1]] [[related-2]]
- Down: [[child]]
```

---

## Key Insights from Session History

1. **Multiple representations aren't redundant** - Each IR (AST, TAC, CFG, SSA) optimized for different operations
2. **Invariants are contracts between phases** - Like perft, they're checksums for correctness
3. **Every design choice is a tradeoff** - Context determines the right solution
4. **Simple can beat complex** - Linear scan in production, constant folding's high impact
5. **Measure, don't guess** - Profile before optimizing (AoC lesson applies everywhere)
6. **Repetition with variation strengthens learning** - Read detailed, then synthesized
7. **Cross-domain analogies make abstract concepts stick** - Chess and AoC provide concrete mental models

---

## Special Notes

- **Glossary maintenance:** Keep `00-index/glossary.md` updated with new acronyms/terms
- **Graph visualization:** User appreciates seeing the knowledge graph grow
- **Commit messages:** Be descriptive about what was added and why
- **Week transitions:** Clearly mark when moving from theory to implementation

---

**Remember:** This is a knowledge graph for **understanding**, not just reference. Every piece should help build intuition, not just list facts.
