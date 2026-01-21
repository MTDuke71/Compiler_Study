## Links
- Up: [[zettel/README]]
- Related: [[01-foundations/day-01-what-is-a-compiler]] [[zettel/Z0001-state]] [[zettel/Z0006-tokens]]
- Down: [[zettel/Z0001-state]] [[zettel/Z0006-tokens]]

---

# Z0005: Compiler Phases — Progressive Ambiguity Removal

## Core Principle

A compiler transforms text into behavior while preserving meaning.

**Each phase exists because the next phase needs more precise input.**

The compiler is a **pipeline that progressively removes ambiguity**:

```
Characters → Tokens → AST → Semantics → IR → Optimized IR → Assembly → Machine Code
(chaos)      (units)  (structure) (meaning) (analysis) (improved) (target) (execution)
```

At each step:
- **Ambiguity decreases**
- **Structure increases**
- **Information is preserved** (or explicitly discarded)

## The Phases

### 1. Lexing — Define Tokens

**Input:** Stream of characters  
**Output:** Stream of tokens  
**Removes:** Lexical ambiguity

#### What Lexing Resolves

**Character-level ambiguities:**
```
> = 1 0
```

Questions at character level:
- Is `>` one token or part of `>=`?
- Does the space matter?
- Is `10` one number or two digits?

**Token-level clarity:**
```
[GT, ASSIGN, NUMBER(10)]
```

All ambiguity resolved:
- `>` is standalone GT operator
- Spaces are irrelevant (filtered)
- `10` is one numeric literal with value 10

#### Lexer Responsibilities

1. **Recognize token boundaries** (maximal munch: `>=` not `>` + `=`)
2. **Distinguish keywords from identifiers** (`if` vs. variable named `if`)
3. **Parse numeric and string literals** (`0xFF` → 255, `"hello\n"` → string with newline)
4. **Filter whitespace and comments** (noise to parser)
5. **Preserve position information** (line, column for error messages)
6. **Detect lexical errors** (unclosed strings, invalid characters)

#### What Lexing Cannot Do

Tokens handle **regular patterns** only:
- ✅ Keywords, identifiers, numbers, operators
- ❌ Nested structures (balanced parentheses)
- ❌ Context-dependent meaning (is `x` a type or variable?)
- ❌ Syntax validation (is this a valid expression?)

**Why:** Regular languages (recognized by finite automata) cannot count or nest. That's the parser's job.

#### The Output Contract

The lexer produces **well-formatted, unambiguous data:**

```
Input:  if x>=10 then y=20
Output: [IF, IDENTIFIER("x"), GTE, NUMBER(10), THEN, IDENTIFIER("y"), ASSIGN, NUMBER(20)]
```

**Guarantees:**
- Token types are unambiguous
- Multi-character operators recognized as units
- Keywords distinguished from identifiers
- Position information attached
- Whitespace filtered (but not lost — positions preserved)

**Parser receives clean data** with all lexical decisions already made.

#### Chess Analogy

Like converting a board photograph to piece positions:
- **Pixels → Pieces** (lexing)
- **Pieces → Position evaluation** (parsing/semantics)

You don't analyze the photograph pixel-by-pixel. You first tokenize it into "white knight on f3, black pawn on e6," then analyze the position.

#### AoC Analogy

Like parsing input files:
1. **First:** Split on delimiters (lexing)
2. **Then:** Validate structure (parsing)

Trying to do both at once creates unmaintainable spaghetti code.

#### Key Insight

**Lexing is about commitment.** The lexer makes irreversible decisions:
- This is `>=`, not `>` followed by `=`
- This is keyword `if`, not identifier `if`
- This is number `42`, not string `"42"`

Downstream phases trust these decisions.

#### Common Lexer Techniques

**Maximal munch (longest match):**
```
Input: >=
Choices: > (GT) or >= (GTE)
Decision: >= (longer wins)
```

**Keyword table:**
```python
keywords = {"if": IF, "while": WHILE, "return": RETURN}
# Scan identifier, then check if it's a keyword
```

**Position tracking:**
```python
line = 1
column = 1
# Update on every character (newlines reset column)
```

**Error recovery:**
```python
# Unclosed string detected
error("Unterminated string at line 3, column 15")
# Skip to next quote or end of line
```

#### Why Lexing Is Separate

**Performance:** Lexer is character-by-character (fine-grained); parser works with higher-level structures. Separating allows independent optimization.

**Simplicity:** Parser doesn't care about whitespace, comments, or escape sequences.

**Reusability:** Same lexer for different parsing strategies (recursive descent vs. LR).

**Modularity:** Can test and profile each phase independently.

---

### 2. Parsing — Define Structure

**Input:** Stream of tokens  
**Output:** Abstract Syntax Tree (AST)  
**Removes:** Structural ambiguity

*(To be expanded)*

- Parsing defines structure.

---

### 3. Semantics — Define Meaning and Legality

**Input:** Abstract Syntax Tree  
**Output:** Annotated AST (with types, symbols)  
**Removes:** Semantic ambiguity

*(To be expanded)*

- Semantics defines meaning and legality.

---

### 4. IR — Define Stable Form for Analysis

**Input:** Annotated AST  
**Output:** Intermediate Representation (TAC, SSA, etc.)  
**Removes:** Language-specific details

*(To be expanded)*

- IR defines a stable form for analysis.

---

### 5. Optimization — Improve Performance Without Changing Meaning

**Input:** IR  
**Output:** Optimized IR  
**Removes:** Inefficiencies

*(To be expanded)*

- Optimization improves performance without changing meaning.

---

### 6. Codegen — Target the Machine

**Input:** Optimized IR  
**Output:** Assembly or machine code  
**Removes:** Abstraction

*(To be expanded)*

- Codegen targets the machine.

---

## Why This Pipeline Is Not Optional

Each phase has a **specific job** that cannot be skipped:

1. **Cannot parse characters directly** — Too many decisions per character (O(n²))
2. **Cannot skip AST** — Need structure before meaning
3. **Cannot skip semantics** — Syntax alone doesn't catch type errors
4. **Cannot skip IR** — Need stable form for optimization
5. **Cannot skip optimization entirely** — Even -O0 does some (constant folding)
6. **Cannot skip codegen** — Must eventually target actual hardware

**The pipeline is the minimum sequence that makes execution possible.**

## The Progression Pattern

Each phase follows the same pattern:

```
Phase N receives: Data with ambiguity X removed
Phase N removes:  Ambiguity Y
Phase N produces: Data with ambiguity X and Y removed
```

**Example:**
- Lexer receives: Characters (all ambiguity present)
- Lexer removes: Lexical ambiguity (token boundaries, keywords)
- Lexer produces: Tokens (lexical ambiguity removed, structural ambiguity remains)

- Parser receives: Tokens (lexical ambiguity removed)
- Parser removes: Structural ambiguity (precedence, associativity)
- Parser produces: AST (structural ambiguity removed, semantic ambiguity remains)

## Invariants Across Phases

1. **Meaning is preserved** — No phase changes what the program does (except optimization, which preserves observable behavior)
2. **Position is preserved** — Every phase maintains source location for error reporting
3. **Errors are detected as early as possible** — Lexical errors in lexer, syntax errors in parser, type errors in semantic analysis
4. **Each phase produces well-formed output** — Or reports an error and stops

## Summary

The compiler phases exist to **progressively remove ambiguity**:

1. **Lexing** defines tokens from characters
2. **Parsing** defines structure from tokens  
3. **Semantics** defines meaning and legality from structure
4. **IR** defines stable form for analysis
5. **Optimization** improves performance without changing meaning
6. **Codegen** targets the machine

**The pipeline is not optional; it is the minimum sequence that makes execution possible.**

Each phase removes a specific class of ambiguity, making the next phase's job simpler and more focused.

## Cross-References

- [[zettel/Z0001-state]] — Phases as state transformations
- [[zettel/Z0006-tokens]] — Lexing output in detail
- [[01-foundations/ambiguity-and-phases]] — Why phases exist
- [[02-lexing/tokens-vs-characters]] — Lexing phase details
- [[00-index/invariants]] — What phases must preserve
