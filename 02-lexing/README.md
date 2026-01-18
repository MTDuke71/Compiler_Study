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

## 5-Day Lexing Curriculum

### Week Overview

This week covers lexical analysis from theory to implementation. By Friday, you'll have built a working lexer and understand the mathematical foundations (regular languages, finite automata) that make lexing tractable.

**Learning pattern:** 
- **Days 1-2:** Foundations and theory (what, why, regular languages, automata)
- **Days 3-5:** Implementation (hand-written lexer, extension, integration)

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

### Tuesday: Regular Languages + Finite Automata

**Theme:** Mathematical foundations - from theory to execution

**Topics:**
- **Regular languages** - Definition and closure properties
- **Regular expressions** - Syntax and semantics
- **Why regular languages?** - Just powerful enough for token recognition
- **Limitations** - What regular languages cannot express (balanced parentheses, nested structures)
- **Deterministic Finite Automata (DFA)** - States, transitions, acceptance
- **Non-deterministic Finite Automata (NFA)** - Multiple transitions, epsilon moves
- **Regex → NFA → DFA** - Thompson's construction, subset construction

**Key questions:**
- Why can't regex handle nested comments?
- What makes a language "regular"?
- Why does a DFA run in O(n) time?
- What's the cost of converting NFA → DFA?

**Deliverables:**
- Training document: "Regular Languages and Finite Automata"
- Daily note: Examples of regular vs. non-regular patterns, DFA traces
- Zettel: Regular languages, DFA/NFA, Thompson's construction

**Chess/AoC connection:**
- Regular patterns in PGN notation
- DFA state machine like chess engine state (position → legal moves → next position)
- AoC state machines (2D grid navigation, game of life patterns)

**Estimated time:** 4-5 hours (combines theory from old Tuesday + Wednesday)

---

### Wednesday: Hand-Written Lexer Implementation

**Theme:** **Read → Run → Modify** - Complete lexer from scratch to extension

**Topics:**
- **Lexer structure** - Main loop, character lookahead, token emission
- **Token representation** - Type, lexeme, line/column tracking
- **Keyword vs. identifier** - Reserved word tables
- **Whitespace and comments** - Skip vs. preserve (for formatting tools)
- **Error handling** - Invalid characters, unclosed strings
- **Adding token types** - Strings, floats, comments
- **Maximal munch** - Longest match principle (>= vs. >, =)

**Implementation:**
- **Provided:** Complete hand-written lexer for simple language (variables, numbers, operators, keywords)
- **Activity:** Read code, run on test inputs, observe token streams
- **Trace execution:** Step through identifier recognition, number parsing
- **Extend:** Add string literals, multi-line comments, floating-point numbers

**Key questions:**
- How does lookahead work? (peek without consuming)
- When does lexer backtrack vs. commit?
- How are line/column positions maintained?
- How do you handle escape sequences in strings?
- What happens with unclosed comments?

**Deliverables:**
- Training document: "Hand-Written Lexer Implementation"
- Annotated source code with comments
- Extended lexer with new features
- Daily note: Key insights from implementation
- Test inputs and their token streams

**Chess/AoC connection:**
- Lexer lookahead like chess engine move generation
- Extending lexer like adding move types (castling, en passant)
- Maintaining position like tracking state in AoC simulations

**Estimated time:** 5-6 hours (combines old Thursday + Friday)

---

### Thursday: Testing, Performance & Edge Cases

**Theme:** Making the lexer robust and production-ready

**Topics:**
- **Comprehensive testing** - Valid inputs, edge cases, malformed inputs
- **Error recovery** - How to handle invalid tokens gracefully
- **Performance measurement** - Profiling lexer on large inputs
- **Edge cases** - Unicode, very long identifiers, number overflow
- **Failure modes** - What can go wrong and how to detect it

**Implementation:**
- **Test suite:** Create comprehensive tests covering:
  - All token types
  - Boundary cases (empty input, single character, very long)
  - Malformed input (unclosed strings, invalid escapes, bad numbers)
  - Position tracking (multi-line, tabs, mixed whitespace)
- **Performance:** Measure lexer speed on various input sizes
- **Error messages:** Ensure clear, helpful error reporting

**Key questions:**
- How do you know your lexer is correct?
- What makes a good error message?
- When is performance good enough?
- What edge cases did you miss initially?

**Deliverables:**
- Comprehensive test suite with coverage analysis
- Performance measurements and profiling results
- Daily note: Edge cases discovered, lessons learned
- Documentation of error handling strategy

**Chess/AoC connection:**
- Testing like perft validation (exhaustive correctness checking)
- Performance measurement like AoC optimization (measure, don't guess)
- Edge cases like chess special moves (often forgotten, always tested)

**Estimated time:** 4-5 hours (testing, debugging, documentation)

---

### Friday: Lexer Generators & Real-World Integration

**Theme:** Tools, tradeoffs, and integration with the rest of the compiler

**Topics:**
- **Lex/Flex** - Declarative lexer specification
- **Regex → Lexer** - How generators work (conceptual)
- **Hand-written vs. generated** - Tradeoffs
  - Generated: Fast development, provably correct
  - Hand-written: Better error messages, special-case optimization
- **Lexer-parser interface** - Token stream protocol
- **Real-world issues** - Unicode, encodings, performance in production
- **Week synthesis** - From theory to working code

**Implementation:**
- **Compare:** Hand-written lexer vs. Flex-generated lexer
- **Measure:** Performance differences on large inputs
- **Integrate:** Connect lexer output to dummy parser (prints token stream)
- **Document:** Decision framework for tool selection

**Key questions:**
- When should you hand-write vs. generate?
- How does lexer performance impact overall compile time?
- What happens when lexical rules are ambiguous?
- What did you learn this week that surprised you?

**Deliverables:**
- Training document: "Lexer Generators and Practical Considerations"
- Performance comparison (hand-written vs. generated)
- Daily note: Week synthesis, key insights, open questions
- Updated knowledge graph showing lexing connections
- Integration example with parser interface

**Chess/AoC connection:**
- Tool selection like choosing perft implementation (speed vs. clarity)
- Performance measurement like AoC optimization (profile first!)
- Integration testing like connecting chess engine components

**Estimated time:** 4-5 hours (tool exploration, comparison, synthesis)

---

## Week Deliverables

By end of Friday, you should have:

### Code
- ✅ Working hand-written lexer (extensible, well-tested)
- ✅ Flex-based lexer (for comparison)
- ✅ Comprehensive test suite with edge cases
- ✅ Integration with token stream consumer
- ✅ Performance measurements

### Documentation
- ✅ 5 training documents (one per day)
- ✅ 5 daily notes (synthesis, reflections)
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

### Stanford Lectures (Weekend)
- Week 3 Stanford lectures (Saturday-Sunday to reinforce and extend week's learning)

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

- **Flexible pacing:** Some days may take longer (especially Tuesday/Wednesday). That's fine—understanding matters more than schedule.
- **Weekend Stanford lectures:** Will provide another perspective on same material (repetition with variation).
- **Questions encouraged:** Note anything unclear for discussion.
- **Implementation language:** Choose what you're comfortable with (Python for clarity, C/Rust for performance, whatever fits your learning style).

**Remember:** Lexing is the most straightforward compiler phase. If you understand this deeply, harder phases will feel more approachable.

