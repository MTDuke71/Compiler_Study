## Links
- Up: [[zettel/Z0005-compiler-phases]]
- Related: [[02-lexing/tokens-vs-characters]] [[zettel/Z0001-state]] [[02-lexing/regular-languages]] [[02-lexing/hand-written-lexer]]
- Down: 

---

# Z0006: Tokens — The Currency of Parsing

## Core Concept

A **token** is a categorized sequence of characters representing a meaningful unit in a programming language.

**Tokens are the interface between lexer and parser.**

## Anatomy of a Token

Every token has:

1. **Type** — Category (IF, IDENTIFIER, NUMBER, PLUS, etc.)
2. **Value** — Semantic data (only when needed)
3. **Position** — Source location (line, column)
4. **Lexeme** — Original text from source

```
Token(type=IDENTIFIER, value="count", line=3, column=5, lexeme="count")
Token(type=NUMBER, value=42, line=3, column=14, lexeme="42")
Token(type=GTE, value=None, line=3, column=11, lexeme=">=")
```

## The Transformation

**Characters (ambiguous):**
```
if x >= 10 then
```

**Tokens (unambiguous):**
```
[IF, IDENTIFIER("x"), GTE, NUMBER(10), THEN]
```

**What happened:**
- Multi-character operators recognized as units (`>=` not `>` + `=`)
- Keywords distinguished from identifiers
- Numbers parsed to values
- Whitespace filtered (but position preserved)
- Token boundaries made explicit

## Why Tokens Exist

### 1. Parser Doesn't Want Characters

The parser works at a higher abstraction level. It thinks in terms of "if statement" and "comparison expression," not "i, f, space, x."

**Without tokens:** Parser makes decisions on every character (O(n²) behavior)  
**With tokens:** Parser makes decisions on meaningful units (O(n))

### 2. Position Must Be Preserved

Error messages need source locations:

**Bad:** `Syntax error`  
**Good:** `Error at line 3, column 15: Type mismatch`

Tokens carry this metadata.

### 3. Lexical Decisions Made Once

The lexer commits to interpretations:
- Is this `>=` or `>` followed by `=`? → **Decide once**
- Is `if` a keyword or variable name? → **Decide once**
- Is `0xFF` the number 255? → **Decide once**

Parser receives **clean, unambiguous data** with all lexical ambiguity resolved.

## Token Types vs. Token Values

Not all tokens need values:

| Token | Type Needed? | Value Needed? | Example |
|-------|--------------|---------------|---------|
| `if` | Yes (IF) | No | `Token(IF, None, ...)` |
| `>=` | Yes (GTE) | No | `Token(GTE, None, ...)` |
| `42` | Yes (NUMBER) | Yes (42) | `Token(NUMBER, 42, ...)` |
| `x` | Yes (IDENTIFIER) | Yes ("x") | `Token(IDENTIFIER, "x", ...)` |
| `"hello"` | Yes (STRING) | Yes ("hello") | `Token(STRING, "hello", ...)` |

**Rule:** Value is needed when the **specific data** matters to downstream phases, not just the category.

## Invariants

1. **Every token knows its source location** — Non-negotiable for error reporting
2. **Token boundaries are unambiguous** — No overlap, no gaps (except whitespace)
3. **Token stream is flat** — No nesting (structure comes from parser)
4. **Token stream is sequential** — Processed left-to-right
5. **Token stream ends with EOF** — Explicit end marker

## The Contract

**Lexer promises:**
- I will give you tokens, not characters
- I will resolve all lexical ambiguity (maximal munch, keyword recognition)
- I will preserve position for error messages
- I will filter noise (whitespace, comments)

**Parser promises:**
- I will work with tokens, not characters
- I will trust your lexical decisions
- I will use position information for diagnostics
- I will build structure from your flat stream

## Analogies

**Chess:** Tokens are to characters as **piece positions** are to **pixels**. You don't evaluate a chess position by analyzing RGB values — you first tokenize the image into "white knight on f3, black pawn on e6," then analyze.

**AoC:** Like parsing input files — first split on delimiters (lexing → tokens), then validate structure (parsing). Trying to do both at once creates spaghetti code.

**Currency:** Tokens are the **currency of parsing**. The parser trades in tokens, not raw characters. Just as you don't buy groceries with atoms of gold (too fine-grained), you don't parse with characters.

## Key Insight

**Tokens transform ambiguous character sequences into well-formatted, unambiguous data.**

This is the **first transformation** in the compiler's progressive ambiguity removal pipeline:

```
Characters (chaos) → Tokens (structure) → AST (meaning) → IR (analysis) → Assembly (execution)
```

At each step, ambiguity decreases and structure increases.

## When Tokens Are Not Enough

Tokens handle **regular patterns** (recognized by finite automata):
- Keywords and identifiers
- Numbers and strings
- Operators and punctuation

They **cannot** handle:
- Nested structures (balanced parentheses, nested comments)
- Context-dependent meaning (`x` as variable vs. type name)
- Syntax rules (expression vs. statement)

**Those are the parser's job.** Tokens are the interface between the two phases.

## Why "Token"?

The term comes from **discrete unit passed between components** (like token ring networks). In compiling:
- Characters flow continuously
- Tokens are **discrete, indivisible units** extracted from that flow
- Each token is **atomic** to the parser

## Cross-References

- [[zettel/Z0005-compiler-phases]] — Lexing as first phase
- [[02-lexing/tokens-vs-characters]] — Detailed comparison
- [[02-lexing/regular-languages]] — What patterns tokens can recognize
- [[zettel/Z0001-state]] — Tokens as state transformation
- [[00-index/invariants]] — Token invariants

## Summary

Tokens are **categorized character sequences** that:
- Carry type, value, and position information
- Form the interface between lexer and parser
- Eliminate lexical ambiguity
- Enable O(n) parsing
- Preserve source location for diagnostics

**The essential transformation:** Characters → Tokens removes the first layer of ambiguity in the compiler pipeline.
