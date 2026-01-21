## Links
- Up: [[02-lexing/README]]
- Related: [[02-lexing/regular-languages]] [[02-lexing/failure-modes]] [[02-lexing/hand-written-lexer]]
- Down: [[02-lexing/hand-written-lexer]]

---

# Tokens vs. Characters: The First Abstraction

## The Core Problem

A compiler's input is a sequence of characters:

```
if x >= 10 then
```

But the parser doesn't want to think at character level. It wants to work with meaningful units:

```
[IF, IDENTIFIER("x"), GREATER_OR_EQUAL, NUMBER(10), THEN]
```

**The lexer's job:** Transform characters → tokens.

This is the first phase of **progressive ambiguity removal** in the compiler pipeline.

---

## Why Not Parse Characters Directly?

### Performance

At character level, the parser would make decisions on every single character:

```
i... is this 'i' alone or 'if' or 'int' or 'identifier'?
f... okay, 'if' keyword, but wait, maybe 'ifconfig'?
 ... space means end of keyword
x... new identifier starting
 ... space again
>... is this GT or GTE or RSHIFT?
=... ah, it was GTE
```

**Every decision requires lookahead.** This is O(n²) behavior in the worst case.

With tokens, the parser makes one decision per token, not per character. This is O(n).

### Clarity

Compare these two error messages:

**Character-level:** `Expected 't' at position 47`  
**Token-level:** `Expected THEN but found END at line 3, column 12`

The token-level message is actionable. The character-level message is gibberish.

### Separation of Concerns

The parser shouldn't care about:
- Whitespace handling (is it significant or noise?)
- Comment filtering (block vs. line, nested or not)
- String escape sequences (`\n` vs. `\\n`)
- Numeric formats (`0xFF` vs. `255`)
- Keyword recognition (`if` vs. identifier named `if`)

**All of these are lexical concerns,** not grammatical ones.

---

## What Is a Token?

A token is a **categorized sequence of characters** with:

1. **Type:** What kind of token (keyword, identifier, number, operator)
2. **Value:** The actual data (if needed)
3. **Position:** Where in the source (file, line, column)

### Token Structure (Conceptual)

```python
class Token:
    type: TokenType        # IF, IDENTIFIER, NUMBER, etc.
    value: Any             # "x", 42, None
    line: int              # Line number
    column: int            # Column number
    lexeme: str            # Original text ("if", "42", ">=")
```

### Example Tokenization

**Input:**
```c
if (count >= 100) {
    return true;
}
```

**Output:**
```
Token(IF, None, 1, 1, "if")
Token(LPAREN, None, 1, 4, "(")
Token(IDENTIFIER, "count", 1, 5, "count")
Token(GTE, None, 1, 11, ">=")
Token(NUMBER, 100, 1, 14, "100")
Token(RPAREN, None, 1, 17, ")")
Token(LBRACE, None, 1, 19, "{")
Token(RETURN, None, 2, 5, "return")
Token(TRUE, True, 2, 12, "true")
Token(SEMICOLON, None, 2, 16, ";")
Token(RBRACE, None, 3, 1, "}")
Token(EOF, None, 3, 2, "")
```

Notice:
- Whitespace and indentation are **gone** (filtered out)
- Position information is **preserved** (for error messages)
- Keywords are **distinguished** from identifiers
- Operators are **recognized** as single units (`>=` not `>` + `=`)

---

## Character-Level vs. Token-Level Parsing

### Chess Analogy: Pixels vs. Pieces

Imagine trying to evaluate a chess position from a photograph:

**Pixel-Level (Character-Level):**
- "These pixels at (342, 187) form a curve..."
- "Adjacent white pixels suggest a light piece..."
- "Pattern matching indicates this might be a knight..."

**Piece-Level (Token-Level):**
- "White knight on f3"
- "Black pawn on e6"
- "White king on g1"

You don't analyze the photograph pixel-by-pixel. You **first convert** the image to piece positions (tokenization), **then** evaluate the position (parsing/semantics).

**The lexer is the OCR for source code.**

---

## What Information Must the Lexer Preserve?

Despite filtering noise, the lexer must maintain:

### 1. Position Information

**Why:** Error messages must point to the original source.

```
Error: Type mismatch at line 42, column 15
   if x >= "hello" then
             ^^^^^^^
   cannot compare number with string
```

Without position tracking, this becomes: `Error: Type mismatch` (useless).

### 2. Original Lexeme

**Why:** Error messages should quote the actual source text.

```
Error: Unknown identifier 'cout' (did you mean 'count'?)
```

Not: `Error: Unknown identifier TOKEN_IDENTIFIER_137`

### 3. Token Value (When Semantic)

**Why:** The parser needs the actual data, not just the category.

- `NUMBER` token needs value `42`, not just "this is a number"
- `STRING` token needs value `"hello"`, not just "this is a string"
- `IDENTIFIER` token needs value `"x"`, not just "this is an identifier"

### 4. Token Type (Always)

**Why:** The parser's grammar is defined over token types.

Grammar rule: `if_stmt := IF LPAREN expr RPAREN stmt`

The parser matches against `IF` and `LPAREN`, not against the strings `"if"` and `"("`.

---

## Lexer Responsibilities

The lexer is responsible for:

### 1. Token Recognition (Maximal Munch)

When multiple tokens could match, choose the **longest** match:

```
>      → GT
>=     → GTE     (not GT followed by ASSIGN)
>>=    → RSHIFT_ASSIGN (not GT followed by GTE)
```

This is called **maximal munch** or **longest match**.

**AoC Parallel:** Like parsing `"123-456"` - do you get `123`, `-456` or `123`, `-`, `456`? The lexer commits to an interpretation.

### 2. Whitespace Handling

Different languages have different rules:

| Language | Whitespace | Example |
|----------|-----------|---------|
| C/Java | Noise (filtered) | `int x=5;` same as `int x = 5;` |
| Python | Significant (indentation) | Indentation creates blocks |
| Haskell | Mostly noise, but layout | Indentation creates blocks |
| Makefile | Tabs vs. spaces matter | Must use tabs for rules |

The lexer must know **which whitespace to preserve vs. discard**.

### 3. Comment Filtering

Comments are noise to the parser, but the lexer must handle them:

```c
// Line comment
/* Block comment */
/* Nested? /* maybe */ */
```

**Key Question:** Are comments allowed to nest?
- C: No (`/* /* */ */` is an error - the first `*/` closes the comment)
- Pascal: Yes (recursive block comments allowed)

This affects whether comments can be recognized by regular expressions (hint: nested comments require more power than regex provides).

### 4. Keyword vs. Identifier

Is `if` a keyword or an identifier named `"if"`?

**Solution:** Reserved word table. The lexer checks:
1. Is this a sequence of letters/digits?
2. Yes → Check if it's in the keyword table
3. If yes → Keyword token (IF, WHILE, etc.)
4. If no → Identifier token (value = the name)

```python
keywords = {"if", "while", "return", "true", "false"}

def make_identifier_or_keyword(lexeme):
    if lexeme in keywords:
        return Token(lexeme.upper(), None, ...)
    else:
        return Token(IDENTIFIER, lexeme, ...)
```

### 5. String and Character Escapes

The lexer processes escape sequences:

```python
"hello\nworld"  →  Token(STRING, "hello\nworld", ...)
# The value contains actual newline, not backslash-n
```

This means the lexer must:
- Recognize escape sequences (`\n`, `\t`, `\\`, `\"`, etc.)
- Handle invalid escapes (`\q` is an error)
- Detect unclosed strings (EOF before closing `"`)

### 6. Numeric Formats

Different bases and formats:

```
42      → NUMBER(42)
0x2A    → NUMBER(42)    # Hexadecimal
052     → NUMBER(42)    # Octal (in C)
0b101010 → NUMBER(42)   # Binary (in some languages)
3.14    → FLOAT(3.14)
1e-3    → FLOAT(0.001)  # Scientific notation
```

The lexer converts all these to their actual values.

---

## How Lexing Removes Ambiguity

At **character level,** everything is ambiguous:

```
> = 1 0
```

Questions:
- Is `>` one token or part of `>=`?
- Does the space after `>` matter?
- Is `10` one number or two?

At **token level,** ambiguity is resolved:

```
[GT, ASSIGN, NUMBER(10)]
```

Now it's clear:
- `>` is a standalone GT token
- Space is irrelevant (filtered)
- `10` is one number

**The lexer commits to interpretations so the parser doesn't have to.**

---

## Token Stream Properties

The token stream has important properties:

### 1. Sequential

Tokens are processed left-to-right, one at a time. This is a **stream,** not random access.

**Chess Parallel:** Like reading a PGN game move-by-move. You process `1. e4 e5 2. Nf3` sequentially, not by jumping around.

### 2. Finite

The token stream always ends with EOF (end-of-file) token.

### 3. Flat (Not Nested)

Tokens don't contain other tokens. Structure is the parser's job:

```
Tokens: [IF, LPAREN, X, GT, TEN, RPAREN, Y, ASSIGN, TWENTY]

Parser builds:
  if_stmt
    condition: (X > 10)
    body: Y = 20
```

### 4. Lossless (With Effort)

Good lexers preserve enough information to **reconstruct the original source** (except comments/whitespace):

```
for token in tokens:
    print(token.lexeme, end=" ")
# Prints something close to original (modulo whitespace)
```

This matters for tools like:
- Pretty printers
- Refactoring tools
- Syntax highlighters

---

## Comparison Table

| Aspect | Characters | Tokens |
|--------|-----------|--------|
| **Count** | Many (100s to millions) | Fewer (~1/6 of characters) |
| **Meaning** | Individual symbols | Semantic units |
| **Whitespace** | Present | Filtered (usually) |
| **Comments** | Present | Filtered |
| **Keywords** | Just letters | Distinguished from identifiers |
| **Operators** | May be multi-char | Single unit (`>=` is one token) |
| **Position** | Implicit (index) | Explicit (line, column) |
| **Error messages** | Useless | Actionable |
| **Parser decisions** | O(n²) potential | O(n) |
| **Structure** | None | Categories (types) |

---

## Edge Cases and Challenges

### 1. Maximal Munch Ambiguity

What if both `=` and `==` are valid tokens?

```
x==y
```

Is this:
- `x` `==` `y` (equality test), or
- `x` `=` `=` `y` (assign = to x, then parse =y)?

**Solution:** Maximal munch always wins. `==` is recognized.

### 2. Backtracking in Lexing

Sometimes the lexer must backtrack:

```
123.456    → FLOAT(123.456)
123.foo    → NUMBER(123), DOT, IDENTIFIER("foo")
```

After seeing `123.`, the lexer must:
1. Look ahead
2. If digit follows → float
3. If letter follows → number, dot, identifier
4. This requires **lookahead** (next section)

### 3. Unclosed Strings

```c
char* s = "hello
```

The lexer must:
- Detect the newline before closing `"`
- Report error with position
- Decide how to recover (skip to next `"`, or end of line, or...?)

### 4. Invalid Characters

```c
int x = 5 ± 2;  // ± is not valid in C
```

The lexer must reject characters not in the language's alphabet.

---

## Lookahead in Lexing

Some tokens require **looking ahead** to decide:

### One-Character Lookahead

```
>     → GT
>=    → GTE

=     → ASSIGN
==    → EQUAL
```

Algorithm:
1. See `>`
2. Peek at next char
3. If `=` → consume it, return GTE
4. Else → return GT

### Two-Character Lookahead (Rare)

```
...   → ELLIPSIS (in C++11)
..    → illegal or DOT DOT
.     → DOT
```

Most lexers keep lookahead to **1 character** for simplicity and speed.

---

## Keywords vs. Identifiers: The Table Approach

Most languages have **reserved words** that cannot be used as identifiers:

```c
int if = 5;  // Error: 'if' is a keyword
```

**Lexer implementation:**

```python
KEYWORDS = {
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'return': TokenType.RETURN,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    # ... etc
}

def scan_identifier(self):
    start = self.position
    while self.is_alnum(self.current_char):
        self.advance()
    
    lexeme = self.source[start:self.position]
    
    # Check if it's a keyword
    token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
    
    return Token(token_type, lexeme, self.line, start)
```

**Alternative:** Some languages allow keywords as identifiers in contexts where they're unambiguous (context-sensitive lexing, more complex).

---

## Position Tracking: The Non-Negotiable Invariant

Without position information, error messages become useless:

**Bad:** `Syntax error`  
**Good:** `Syntax error at line 42, column 15`  
**Better:** 
```
Error at line 42, column 15:
    if x >= "hello" then
              ^^^^^^^
Type mismatch: cannot compare number with string
```

**Implementation:**

```python
class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
```

**Cost:** Tracking line/column adds overhead, but it's **mandatory** for usable compiler.

**AoC Parallel:** Like tracking coordinates in a grid problem. Extra bookkeeping, but necessary for solving the problem.

---

## Why Tokens Are Named "Tokens"

Historical note: The term "token" comes from **token ring networks** and earlier computing uses where a "token" was a **discrete unit** passed between components.

In lexing:
- Characters flow continuously
- Tokens are **discrete units** extracted from that flow
- Each token is an **indivisible unit** to the parser

Think of tokens as **currency** in the parsing economy: the parser trades in tokens, not in raw characters.

---

## The Lexer's Output: Well-Formatted, Unambiguous Data

At the **end of lexing**, you have a **well-formatted, unambiguous version of the input data** that the parser can work with.

**Input to lexer (ambiguous characters):**
```
if x>=10 then y=20
```

**Output from lexer (unambiguous tokens):**
```
[IF, IDENTIFIER("x"), GTE, NUMBER(10), THEN, IDENTIFIER("y"), ASSIGN, NUMBER(20)]
```

**What has been resolved:**
- ✅ Multi-character operators recognized (`>=` not `>` + `=`)
- ✅ Keywords distinguished from identifiers (`if` and `then` are keywords, not variable names)
- ✅ Numbers parsed (`10` and `20` are numeric literals, not strings)
- ✅ Whitespace normalized (irrelevant spacing removed)
- ✅ Token boundaries clear (no ambiguity about where one token ends and next begins)
- ✅ Position preserved (each token knows its source location)

The parser receives a **clean, standardized stream** where all lexical ambiguity has been eliminated. It can focus solely on **structural** questions (does this sequence of tokens form a valid statement?) without worrying about character-level concerns.

**This is the first transformation in the progressive ambiguity removal pipeline.**

---

## Summary: The Contract Between Lexer and Parser

The lexer promises:
- **I will give you tokens, not characters**
- **I will give you well-formatted, unambiguous data**
- **I will preserve position information**
- **I will filter noise (whitespace, comments)**
- **I will distinguish keywords from identifiers**
- **I will recognize multi-character operators as single tokens**
- **I will handle string escapes and numeric formats**
- **I will detect lexical errors (unclosed strings, invalid chars)**

The parser promises:
- **I will work with tokens, not characters**
- **I will trust that lexical ambiguity has been resolved**
- **I will not worry about whitespace or comments**
- **I will build structure from flat token stream**
- **I will report errors using position information you give me**

This **contract** allows each phase to focus on its core responsibility.

---

## Next Steps

With this understanding of tokens vs. characters, we can now explore:

1. **[[02-lexing/regular-languages]]** - The mathematical foundation (what patterns can lexers recognize?)
2. **[[02-lexing/hand-written-lexer]]** - Implementing a lexer by hand
3. **[[02-lexing/failure-modes]]** - Edge cases and error handling

The token abstraction is **fundamental** to compiler construction. Every compiler has this phase, whether implicit or explicit.

---

## Key Takeaways

1. **Lexing produces well-formatted, unambiguous data** - The parser receives a clean token stream with all lexical ambiguity resolved
2. **Lexing is about commitment** - The lexer makes irreversible decisions (this is `>=`, not `>` followed by `=`)
3. **Tokens are semantic units** - They carry meaning, not just characters
4. **Position is mandatory** - Without it, error messages are useless
5. **Separation enables optimization** - Lexer and parser can be optimized independently
6. **Maximal munch is the rule** - Always take the longest valid token
7. **Whitespace handling is contextual** - Different languages treat it differently
8. **Keywords are checked after identification** - Scan as identifier, then lookup in keyword table

**The Essential Insight:** Lexing transforms messy, ambiguous character sequences into a clean, standardized token stream. The parser receives **formatted data** where character-level decisions have already been made.

**Chess Analogy Recap:** Tokens are to characters as piece positions are to pixels. You don't evaluate a chess position by analyzing image pixels - you first convert to piece positions (tokenization), then analyze (parsing/semantics).

**AoC Analogy Recap:** Like parsing input files - first split on delimiters (lexing), then validate structure (parsing). Trying to do both at once creates unmaintainable code.
