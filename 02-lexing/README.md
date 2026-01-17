# 02-lexing

## Links
- Up: [[README]]
- Related: [[02-lexing/hand-written-lexer]] [[02-lexing/regular-languages]]
- Down: [[02-lexing/regular-languages]]

---

## Overview

Lexical analysis is the **first phase of compilation**, transforming a stream of characters into a stream of tokens. This phase removes ambiguity at the character level—whitespace becomes irrelevant, keywords are distinguished from identifiers, and syntactic structure begins to emerge.

**Core insight:** Lexing is pattern recognition over characters, which is why regular expressions (and finite automata) are the perfect tool.

---

## 6-Day Lexing Curriculum

### Week Overview

This week covers lexical analysis from theory to implementation. By Saturday, you'll have built a working lexer for a subset of COOL and understand the mathematical foundations (regular languages, finite automata) that make lexing tractable.

**Learning pattern:** 
- **Days 1-2:** Foundations (what, why, regular languages)
- **Day 3:** Theory (DFA/NFA, regex to automata)
- **Days 4-5:** Implementation (hand-written lexer, real code)
- **Day 6:** Integration and edge cases

---

### Monday: Lexical Analysis Foundations

**Theme:** What is lexing and why is it a separate phase?

**Topics:**
- **Tokens vs. characters** - Why we need abstraction
- **Lexer responsibilities** - Whitespace, comments, keywords vs. identifiers
- **Lexer output** - Token stream with types, values, positions
- **Why separate lexing from parsing?** - Separation of concerns, tool specialization

**Key questions:**
- Why not parse directly from characters?
- What information must the lexer preserve (positions for error messages)?
- How does lexing "remove ambiguity"?

**Deliverables:**
- Training document: "Lexical Analysis Foundations"
- Daily note: Synthesis with chess/AoC analogies
- Zettel: Update or create tokens/lexer concepts

**Chess/AoC connection:** 
- Lexing is like reading chess notation (Nf3, e4) → recognizing piece types, squares, special symbols
- AoC input parsing: recognizing numbers, splitting on delimiters, handling special characters

**Estimated time:** 2-3 hours (reading, note-taking, questioning)

---

### Tuesday: Regular Languages

**Theme:** The mathematical foundation - why regular expressions work for lexing

**Topics:**
- **Regular languages** - Definition and closure properties
- **Regular expressions** - Syntax and semantics
- **Why regular languages?** - Just powerful enough for token recognition
- **Limitations** - What regular languages cannot express (balanced parentheses, nested structures)
- **Context-free vs. regular** - Why we need parsing for structure

**Key questions:**
- Why can't regex handle nested comments?
- What makes a language "regular"?
- How do we know our token patterns are regular?

**Deliverables:**
- Training document: "Regular Languages and Lexing"
- Daily note: Examples of regular vs. non-regular patterns
- Zettel: Regular languages, closure properties

**Chess/AoC connection:**
- Regular patterns in PGN notation (each move follows a pattern)
- AoC: When line-by-line regex works vs. when you need parsing

**Estimated time:** 3-4 hours (more theoretical, may need re-reading)

---

### Wednesday: Finite Automata - The Lexer's Engine

**Theme:** From regular expressions to executable code

**Topics:**
- **Deterministic Finite Automata (DFA)** - States, transitions, acceptance
- **Non-deterministic Finite Automata (NFA)** - Multiple transitions, epsilon moves
- **Regex → NFA → DFA** - Thompson's construction, subset construction
- **DFA minimization** - Hopcroft's algorithm (conceptual, not implementation)
- **Why DFA for lexers?** - Efficient, predictable, easy to implement

**Key questions:**
- Why does a DFA run in O(n) time?
- What's the cost of converting NFA → DFA? (exponential in worst case, polynomial in practice)
- How does lexer performance relate to DFA size?

**Deliverables:**
- Training document: "Finite Automata for Lexical Analysis"
- Daily note: Trace DFA execution on example inputs
- Zettel: DFA, NFA, Thompson's construction

**Chess/AoC connection:**
- DFA state machine like chess engine state (position → legal moves → next position)
- AoC state machines (2D grid navigation, game of life patterns)

**Estimated time:** 3-4 hours (diagrams help, draw state machines)

---

### Thursday: Hand-Written Lexer (Part 1)

**Theme:** **Read → Run** - Understanding lexer implementation

**Topics:**
- **Lexer structure** - Main loop, character lookahead, token emission
- **Token representation** - Type, lexeme, line/column tracking
- **Keyword vs. identifier** - Reserved word tables
- **Whitespace and comments** - Skip vs. preserve (for formatting tools)
- **Error handling** - Invalid characters, unclosed strings

**Implementation:**
- **Provided:** Complete hand-written lexer for simple language (variables, numbers, operators, keywords)
- **Activity:** Read code, run on test inputs, observe token streams
- **Trace execution:** Step through identifier recognition, number parsing

**Key questions:**
- How does lookahead work? (peek without consuming)
- When does lexer backtrack vs. commit?
- How are line/column positions maintained?

**Deliverables:**
- Training document: "Hand-Written Lexer Walkthrough"
- Annotated source code with comments explaining each section
- Daily note: Key insights from reading implementation
- Test inputs and their token streams

**Chess/AoC connection:**
- Lexer lookahead like chess engine move generation (peek ahead before committing)
- Maintaining position like tracking state in AoC simulations

**Estimated time:** 3-4 hours (code reading, running, tracing)

---

### Friday: Hand-Written Lexer (Part 2)

**Theme:** **Modify → Understand** - Extending the lexer

**Topics:**
- **Adding new token types** - Strings, floats, comments
- **Maximal munch** - Longest match principle (>= vs. >, =)
- **Operator precedence** - Not lexer's job, but must recognize all operators
- **Performance considerations** - Switch vs. if-else, table-driven approaches

**Implementation:**
- **Modify:** Extend Thursday's lexer with:
  - String literals (with escape sequences)
  - Multi-line comments
  - Floating-point numbers
  - Additional operators (++, --, <<, >>)
- **Test:** Create comprehensive test suite
- **Break it:** Try malformed inputs, observe error messages

**Key questions:**
- How do you handle escape sequences in strings?
- What happens with unclosed comments?
- How does maximal munch resolve ambiguity?

**Deliverables:**
- Extended lexer implementation with new features
- Comprehensive test suite
- Daily note: Challenges encountered, solutions applied
- Error handling examples

**Chess/AoC connection:**
- Extending lexer like adding move types to chess engine (castling, en passant)
- Test suite creation like AoC example validation

**Estimated time:** 4-5 hours (implementation, debugging, testing)

---

### Saturday: Lexer Generator Tools & Integration

**Theme:** Real-world lexing - tools, performance, integration with parser

**Topics:**
- **Lex/Flex** - Declarative lexer specification
- **Regex → Lexer** - How generators work (conceptual)
- **Hand-written vs. generated** - Tradeoffs
  - Generated: Fast development, provably correct
  - Hand-written: Better error messages, special-case optimization
- **Lexer-parser interface** - Token stream protocol
- **Lookahead and backtracking** - When lexer needs parser context
- **Real-world issues** - Unicode, encodings, performance

**Implementation:**
- **Compare:** Hand-written lexer vs. Flex-generated lexer
- **Measure:** Performance on large inputs
- **Integrate:** Connect lexer output to dummy parser (prints token stream)

**Key questions:**
- When should you hand-write vs. generate?
- How does lexer performance impact overall compile time? (Usually negligible)
- What happens when lexical rules are ambiguous?

**Deliverables:**
- Training document: "Lexer Generators and Practical Considerations"
- Performance comparison (hand-written vs. generated)
- Daily note: Week synthesis, key insights, open questions
- Updated knowledge graph showing lexing connections

**Chess/AoC connection:**
- Tool selection like choosing perft implementation (speed vs. clarity)
- Performance measurement like AoC optimization (measure before optimizing)

**Estimated time:** 3-4 hours (tool exploration, comparison, synthesis)

---

## Week Deliverables

By end of Saturday, you should have:

### Code
- ✅ Working hand-written lexer (extensible, well-tested)
- ✅ Flex-based lexer (for comparison)
- ✅ Comprehensive test suite
- ✅ Integration with token stream consumer

### Documentation
- ✅ 6 training documents (one per day)
- ✅ 6 daily notes (synthesis, reflections)
- ✅ Multiple zettels (regular languages, DFA/NFA, lexer structure, etc.)
- ✅ Updated knowledge graph

### Understanding
- ✅ Why lexing is a separate phase
- ✅ Regular languages as the foundation
- ✅ How regex maps to DFA
- ✅ Implementation patterns (lookahead, maximal munch, error handling)
- ✅ Tradeoffs (hand-written vs. generated, performance vs. clarity)

---

## Connection to Compiler Pipeline

**What comes before:** Source code (character stream)

**What lexing does:**
- Character stream → Token stream
- Removes irrelevant details (whitespace, comments)
- Identifies keyword vs. identifier
- Handles literals (numbers, strings)
- Tracks positions (for error messages)

**What comes after:** Parsing (tokens → AST)

**Interface:** Stream of tokens with:
- Type (ID, NUM, KEYWORD, OPERATOR, etc.)
- Value (lexeme, numeric value, string content)
- Position (line, column for error reporting)

---

## Prerequisites

**Before starting this week:**
- ✅ Completed Week 1-2 (Foundations)
- ✅ Understand compiler phases (Z0005)
- ✅ Familiar with state machines (from foundations)

**Skills needed:**
- Basic regex knowledge (or willingness to learn)
- Reading/writing code in chosen implementation language
- Comfort with state machines and automata concepts

---

## Resources

### Within Repository
- [[02-lexing/tokens-vs-characters]]
- [[02-lexing/regular-languages]]
- [[02-lexing/hand-written-lexer]]
- [[02-lexing/failure-modes]]

### External (Optional)
- Dragon Book: Chapter 3 (Lexical Analysis)
- Engineering a Compiler: Chapter 2
- Flex/Lex documentation
- Regex tutorial/reference

### Stanford Lectures (Sunday)
- Lecture on lexical analysis (watch Sunday to reinforce week's learning)

---

## Success Criteria

**You'll know you understand lexing when you can:**

1. ✅ Explain why lexing is separate from parsing
2. ✅ Write regular expressions for common token patterns
3. ✅ Trace DFA execution on input strings
4. ✅ Implement a lexer for a simple language from scratch
5. ✅ Debug lexer issues (wrong tokens, position tracking, edge cases)
6. ✅ Make informed decisions (hand-written vs. generated, performance tradeoffs)
7. ✅ Recognize when a pattern is **not** regular (requires parsing instead)

---

## Next Week Preview

**Week 4: Parsing**
- Context-free grammars
- Top-down parsing (recursive descent)
- Bottom-up parsing (LR, LALR)
- Building abstract syntax trees (ASTs)
- Handling ambiguity and precedence

**The lexer you build this week becomes the input to next week's parser.**

---

## Notes

- **Flexible pacing:** Some days may take longer (especially Wednesday/Thursday). That's fine—understanding matters more than schedule.
- **Sunday Stanford lecture:** Will provide another perspective on same material (repetition with variation).
- **Questions encouraged:** Note anything unclear for Monday discussion.
- **Implementation language:** Choose what you're comfortable with (Python for clarity, C/Rust for performance, whatever fits your learning style).

**Remember:** Lexing is the most straightforward compiler phase. If you understand this deeply, harder phases will feel more approachable.

