## Links
- Up: [[02-lexing/README]]
- Related: [[02-lexing/regular-languages]] [[02-lexing/tokens-vs-characters]] [[02-lexing/failure-modes]]
- Down:

---

# Hand-Written Lexer Implementation

**Purpose:** Understand lexer construction by building one from scratch.

**Learning mode:** Read → Run → Modify → Understand

> **📁 Runnable Code:** Complete implementations are in [`examples/02-lexing/`](../../examples/02-lexing/)  
> - [`lexer_minimal.py`](../../examples/02-lexing/lexer_minimal.py) - Basic lexer (~200 lines)  
> - [`lexer_extended.py`](../../examples/02-lexing/lexer_extended.py) - With strings, floats, comments  
> - [`test_lexer.py`](../../examples/02-lexing/test_lexer.py) - Comprehensive test suite  
> - [`README.md`](../../examples/02-lexing/README.md) - Usage guide and experiments  
>
> **Run immediately:** `cd examples/02-lexing && python lexer_minimal.py`

---

## Overview

A **hand-written lexer** is a lexical analyzer implemented directly in code rather than generated from a specification. This approach gives you:

1. **Complete control** over token recognition logic
2. **Direct visibility** into the state machine execution
3. **Easier debugging** (it's just code you wrote)
4. **Performance tuning** (optimize hot paths)

**The tradeoff:** More code to write and maintain vs. declarative specification.

**When to hand-write:**
- Language is simple (< 50 token types)
- Performance is critical (tight inner loop)
- Need custom error recovery
- Learning compiler internals

**When to generate:**
- Language is complex (100+ token types)
- Syntax changes frequently
- Team prefers declarative specifications
- Standard patterns suffice

---

## Alternatives to Hand-Written Lexers

While this document focuses on hand-written lexers, there are several alternatives worth understanding:

### 1. Lexer Generators (Most Common Alternative)

**Tools that generate lexer code from declarative specifications:**

**Flex (Fast Lexical Analyzer)**
- Most popular, C/C++ output
- Specification: regular expressions + actions
- Used by: GCC, many Unix tools
- Example spec:
  ```flex
  %%
  [0-9]+          { return NUMBER; }
  "if"            { return IF; }
  [a-zA-Z_][a-zA-Z0-9_]*  { return IDENTIFIER; }
  [ \t\n]         { /* skip whitespace */ }
  ```

**re2c**
- Generates very fast C code
- Used by: PHP, Ninja build system
- Known for excellent performance (often faster than hand-written)
- Focuses on speed over features

**Ragel**
- State machine compiler
- Generates C, C++, Java, Ruby, Go, etc.
- More powerful than Flex (can handle some context-sensitive patterns)
- Steeper learning curve

**PLY (Python Lex-Yacc)**
- Python implementation of lex/yacc
- Specification embedded in Python code
- Good for prototyping
- Example:
  ```python
  def t_NUMBER(t):
      r'\d+'
      t.value = int(t.value)
      return t
  ```

**ANTLR**
- Generates lexer + parser together
- Java-based but outputs multiple languages
- Popular in academia and industry
- Includes excellent tooling (grammar visualization, debugging)

**Comparison:**

| Tool | Language | Speed | Learning Curve | Best For |
|------|----------|-------|----------------|----------|
| **Flex** | C/C++ | Fast | Medium | Production C/C++ projects |
| **re2c** | C | Very Fast | Medium | Performance-critical code |
| **Ragel** | Many | Fast | Steep | Complex state machines |
| **PLY** | Python | Slow | Easy | Python projects, prototypes |
| **ANTLR** | Many | Medium | Medium | Full compiler pipelines |

### 2. Regular Expression Libraries

**For simple tokenization:**

```python
import re

token_patterns = [
    (r'\d+', 'NUMBER'),
    (r'if|while|for', 'KEYWORD'),
    (r'[a-zA-Z_]\w*', 'IDENTIFIER'),
    (r'[+\-*/]', 'OPERATOR'),
    (r'\s+', None),  # Skip whitespace
]

def tokenize(code):
    combined = '|'.join(f'(?P<{name}>{pattern})' 
                        for pattern, name in token_patterns if name)
    for match in re.finditer(combined, code):
        kind = match.lastgroup
        value = match.group()
        yield (kind, value)
```

**Pros:**
- Extremely concise
- Leverages standard library
- No build step

**Cons:**
- Poor error messages
- Hard to track positions
- Slower than custom lexers
- Limited error recovery

**Good for:** Quick scripts, DSLs, prototypes

### 3. Parser Combinators (Blur Lexing/Parsing)

**Tools like Parsec (Haskell), nom (Rust), pyparsing (Python):**

These often skip the separate lexing phase entirely, parsing directly from characters.

```python
# pyparsing example
from pyparsing import Word, alphas, nums

identifier = Word(alphas, alphas + nums + "_")
number = Word(nums)
```

**Pros:**
- Single unified grammar
- Very composable
- Great for DSLs

**Cons:**
- Can be slower
- Harder to optimize
- Backtracking can be complex

### 4. PEG Parsers (Parsing Expression Grammars)

**Tools like PEG.js, pest (Rust), parsimonious (Python):**

These also blur lexing and parsing boundaries.

```
// PEG.js example
number = digits:[0-9]+ { return parseInt(digits.join(""), 10); }
identifier = first:[a-z] rest:[a-z0-9]* { return first + rest.join(""); }
```

**Pros:**
- Deterministic (no ambiguity)
- Straightforward to write
- Good error recovery possible

**Cons:**
- Can be slow without memoization
- Limited operator precedence handling
- Not suitable for all grammars

---

## When to Use Each Approach

### Hand-Written Lexer

**✅ Choose when:**
- Performance is critical (tight loop in hot path)
- Need custom error recovery with detailed messages
- Language lexical syntax is stable
- Want complete control over implementation
- Learning compiler internals (educational value)

**❌ Avoid when:**
- Prototyping with rapidly changing syntax
- Team lacks compiler experience
- Many similar token patterns (tedious to hand-code)

**Real-world examples:**
- Clang (C/C++ compiler) - hand-written
- Go compiler - hand-written
- V8 JavaScript engine - hand-written
- Rust compiler - hand-written

### Lexer Generator (Flex/re2c)

**✅ Choose when:**
- Many token types (100+)
- Syntax changes frequently during development
- Want proven, well-tested lexer logic
- Team familiar with lex/flex patterns
- Prototyping a new language

**❌ Avoid when:**
- Need very specific error messages
- Performance is absolutely critical
- Integration with custom infrastructure is complex

**Real-world examples:**
- GCC - uses Flex (though considering hand-written)
- Ruby - uses Flex
- PostgreSQL - uses Flex
- Most academic compilers

### Regular Expression Library

**✅ Choose when:**
- Building a simple DSL or config file parser
- Prototyping quickly
- Token patterns are simple
- Performance doesn't matter

**❌ Avoid when:**
- Need good error messages with positions
- Language has complex lexical rules
- Performance matters
- Handling ambiguous patterns

**Real-world examples:**
- Log parsers
- Config file readers
- Simple DSLs (JSON subset, etc.)

### Parser Combinators / PEG

**✅ Choose when:**
- Lexing and parsing boundaries are unclear
- Building a DSL with tight integration
- Want composable, modular grammar
- Functional programming style preferred

**❌ Avoid when:**
- Performance is critical
- Need to match standard compiler architecture
- Debugging generated code is required

**Real-world examples:**
- Domain-specific languages
- Configuration languages
- Markdown parsers
- Some scripting languages

---

## The Spectrum: Control vs. Convenience

```
Hand-Written          Lexer Generator       Regex Library      Parser Combinators
    |                      |                     |                    |
    |                      |                     |                    |
High Control          Balanced             High Convenience    Unified Approach
High Performance      Good Performance     Lower Performance   Variable Performance
More Code             Less Code            Minimal Code        Functional Style
Custom Errors         Generic Errors       Poor Errors         Custom Errors
Hard to Change        Easy to Change       Very Easy           Very Easy
```

**The key insight:** There's no universally "best" approach. Your choice depends on:
1. Performance requirements
2. Development velocity needs
3. Team expertise
4. Language stability
5. Error message quality requirements
6. Integration constraints

**For learning:** Hand-write first to understand what the generators are doing. Then use generators for production if appropriate.

---

## Why This Document Focuses on Hand-Written

**Three reasons:**

1. **Understanding:** You can't appreciate what Flex generates until you've written a lexer by hand
2. **Control:** Production compilers often hand-write for performance and error handling
3. **Foundation:** The concepts (maximal munch, position tracking, DFA walking) apply to all approaches

**After understanding hand-written lexers**, you'll be able to:
- Read and understand Flex specifications
- Debug generated lexer code
- Make informed tool choices
- Optimize lexer performance
- Implement custom lexer features when needed

**Think of it like chess:** You learn basic tactics before using chess engines. You learn lexing fundamentals before using lexer generators.

---

## Core Lexer Structure

A hand-written lexer is fundamentally a **DFA walker implemented as code**. Each branch in your code corresponds to a state transition.

### The Three Essential Components

**1. State Management**
```
- Current position in input
- Lookahead buffer (peek without consuming)
- Line and column tracking (for error messages)
- Token start position
```

**2. Token Recognition**
```
- Pattern matching (if/else or switch)
- Maximal munch (always take longest match)
- Token construction (type, value, position)
```

**3. Error Recovery**
```
- Invalid character handling
- Unterminated string/comment
- Continue scanning after errors
```

**Chess engine analogy:** The lexer's internal state (position, lookahead) is like a chess engine's board representation - it's optimized for the operations you perform most frequently (peek, advance, match, backtrack).

---

## Complete Implementation

**📁 See runnable code:** [`examples/02-lexing/`](../../examples/02-lexing/)

The complete implementations are in separate Python files for easy experimentation:
- [`lexer_minimal.py`](../../examples/02-lexing/lexer_minimal.py) - Basic lexer (~200 lines)
- [`lexer_extended.py`](../../examples/02-lexing/lexer_extended.py) - With strings, floats, comments (~350 lines)
- [`test_lexer.py`](../../examples/02-lexing/test_lexer.py) - Comprehensive test suite
- [`README.md`](../../examples/02-lexing/README.md) - Usage guide and experiments

**You can run them immediately:**
```bash
cd examples/02-lexing
python lexer_minimal.py
python test_lexer.py
```

---

## Minimal Lexer Overview

The basic lexer ([`lexer_minimal.py`](../../examples/02-lexing/lexer_minimal.py)) demonstrates core concepts with ~200 lines of code.

**Key structure (simplified):**

```python
from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    
    # Special
    EOF = auto()
    ERROR = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    value: any = None  # For numbers, the actual numeric value

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.token_start_pos = 0
        self.token_start_line = 1
        self.token_start_column = 1
        
    def current_char(self) -> str:
        """Get current character without advancing."""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def peek(self, offset: int = 1) -> str:
        """Look ahead without consuming."""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Consume current character and return it."""
        if self.position >= len(self.source):
            return '\0'
        
        char = self.source[self.position]
        self.position += 1
        self.column += 1
        
        # Track newlines for accurate line/column
        if char == '\n':
            self.line += 1
            self.column = 1
            
        return char
    
    def skip_whitespace(self):
        """Consume whitespace without producing tokens."""
        while self.current_char() in ' \t\r\n':
            self.advance()
    
    def mark_token_start(self):
        """Remember where current token begins."""
        self.token_start_pos = self.position
        self.token_start_line = self.line
        self.token_start_column = self.column
    
    def make_token(self, type: TokenType, value=None) -> Token:
        """Create token from start position to current position."""
        lexeme = self.source[self.token_start_pos:self.position]
        return Token(
            type=type,
            lexeme=lexeme,
            line=self.token_start_line,
            column=self.token_start_column,
            value=value
        )
    
    def scan_number(self) -> Token:
        """Scan a numeric literal."""
        # Already positioned at first digit
        while self.current_char().isdigit():
            self.advance()
        
        lexeme = self.source[self.token_start_pos:self.position]
        value = int(lexeme)
        return self.make_token(TokenType.NUMBER, value)
    
    def scan_identifier(self) -> Token:
        """Scan identifier or keyword."""
        # Already positioned at first letter
        while self.current_char().isalnum() or self.current_char() == '_':
            self.advance()
        
        lexeme = self.source[self.token_start_pos:self.position]
        
        # Check if it's a keyword
        keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
        }
        
        type = keywords.get(lexeme, TokenType.IDENTIFIER)
        return self.make_token(type)
    
    def next_token(self) -> Token:
        """Scan and return the next token."""
        self.skip_whitespace()
        
        if self.position >= len(self.source):
            return Token(TokenType.EOF, '', self.line, self.column)
        
        self.mark_token_start()
        char = self.advance()
        
        # Single character tokens
        if char == '+':
            return self.make_token(TokenType.PLUS)
        elif char == '-':
            return self.make_token(TokenType.MINUS)
        elif char == '*':
            return self.make_token(TokenType.STAR)
        elif char == '/':
            return self.make_token(TokenType.SLASH)
        
        # Lookahead for ==
        elif char == '=':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.EQUAL_EQUAL)
            else:
                return self.make_token(TokenType.EQUAL)
        
        # Numbers
        elif char.isdigit():
            # Back up and rescan from start
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()  # Consume first digit again
            return self.scan_number()
        
        # Identifiers and keywords
        elif char.isalpha() or char == '_':
            # Back up and rescan from start
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()  # Consume first char again
            return self.scan_identifier()
        
        # Invalid character
        else:
            return self.make_token(TokenType.ERROR)
    
    def tokenize(self) -> list[Token]:
        """Scan entire input and return all tokens."""
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
```

**Usage:**
```python
source = "if x == 42 + 7"
lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type.name:15} {token.lexeme!r:10} @ {token.line}:{token.column}")
```

**Output:**
```
IF              'if'       @ 1:1
IDENTIFIER      'x'        @ 1:4
EQUAL_EQUAL     '=='       @ 1:6
NUMBER          '42'       @ 1:9
PLUS            '+'        @ 1:12
NUMBER          '7'        @ 1:14
EOF             ''         @ 1:15
```

---

## Key Implementation Patterns

### 1. Maximal Munch

**Rule:** Always consume the longest token that matches.

**Example:** `>=` should be one token (GREATER_EQUAL), not `>` followed by `=`.

**Implementation:**
```python
elif char == '>':
    if self.current_char() == '=':
        self.advance()  # Consume '='
        return self.make_token(TokenType.GREATER_EQUAL)
    else:
        return self.make_token(TokenType.GREATER)
```

**Why it matters:** Without maximal munch, `>=` would lex as two tokens and break your grammar.

**AoC insight:** This is greedy local optimization. Lexer commits to longest match immediately without looking at broader context.

---

### 2. Lookahead Strategies

**Single-character lookahead (most common):**
```python
if char == '=' and self.current_char() == '=':
    # It's ==
else:
    # It's just =
```

**Bounded lookahead (strings, numbers with exponents):**
```python
# Scan digits
while self.current_char().isdigit():
    self.advance()

# Optional decimal part
if self.current_char() == '.' and self.peek(1).isdigit():
    self.advance()  # Consume '.'
    while self.current_char().isdigit():
        self.advance()

# Optional exponent
if self.current_char() in 'eE':
    self.advance()
    if self.current_char() in '+-':
        self.advance()
    while self.current_char().isdigit():
        self.advance()
```

**Unbounded lookahead (comments, strings):**
```python
# Scan until closing quote or EOF
while self.current_char() != '"' and self.current_char() != '\0':
    if self.current_char() == '\\':
        self.advance()  # Skip escape
        self.advance()  # Skip escaped char
    else:
        self.advance()

if self.current_char() == '\0':
    return self.make_token(TokenType.ERROR)  # Unterminated
else:
    self.advance()  # Consume closing "
    return self.make_token(TokenType.STRING)
```

**Chess engine analogy:** Lookahead is like search depth. Single-char lookahead handles most cases (shallow search). Unbounded lookahead for special cases (deep search where needed).

---

### 3. Position Tracking

**Why it's critical:** Error messages need accurate locations.

**What to track:**
- Absolute position in source
- Current line number
- Current column number
- Token start position/line/column

**Update points:**
- Every character consumed (advance())
- Special handling for newlines (reset column, increment line)
- Mark start of token before scanning

**Common mistakes:**
- Off-by-one errors (0-based vs 1-based)
- Forgetting to update on newlines
- Tab characters (count as 1 column or 8?)
- Unicode (one code point = one column?)

**Practical choice:** Keep it simple. One character = one column. Enhance later if needed.

---

### 4. Error Handling

**Lexer error recovery is simple** compared to parser error recovery.

**Strategy:**
1. **Invalid character:** Create ERROR token, skip character, continue
2. **Unterminated string:** Create ERROR token, report start position, continue from next line
3. **Numeric overflow:** Create WARNING, clamp value, continue

**Key insight:** Lexer produces a token stream even for invalid input. The parser will catch semantic errors later.

**Example:**
```python
# Invalid character
else:
    error_token = self.make_token(TokenType.ERROR)
    # Continue scanning - don't abort
    return error_token
```

**Why this works:** Downstream phases expect a token stream. Better to produce ERROR tokens than to crash.

---

## Extension Exercise: Adding String Literals

Let's extend the minimal lexer to handle string literals with escape sequences.

**Requirements:**
- Strings delimited by `"`
- Support escape sequences: `\n`, `\t`, `\\`, `\"`
- Report error for unterminated strings
- Track multi-line strings correctly

**Implementation:**

```python
def scan_string(self) -> Token:
    """Scan a string literal."""
    # Opening " already consumed
    chars = []
    
    while True:
        char = self.current_char()
        
        # End of input before closing quote
        if char == '\0':
            return Token(
                type=TokenType.ERROR,
                lexeme='unterminated string',
                line=self.token_start_line,
                column=self.token_start_column
            )
        
        # Closing quote
        if char == '"':
            self.advance()
            break
        
        # Escape sequence
        if char == '\\':
            self.advance()
            next_char = self.current_char()
            
            if next_char == 'n':
                chars.append('\n')
            elif next_char == 't':
                chars.append('\t')
            elif next_char == '\\':
                chars.append('\\')
            elif next_char == '"':
                chars.append('"')
            else:
                # Invalid escape - just include backslash and char
                chars.append('\\')
                chars.append(next_char)
            
            self.advance()
        else:
            # Regular character
            chars.append(char)
            self.advance()
    
    value = ''.join(chars)
    return self.make_token(TokenType.STRING, value)

# Add to next_token():
elif char == '"':
    return self.scan_string()
```

**Test cases:**
```python
# Basic string
'"hello"' → STRING("hello")

# With escapes
'"line1\nline2"' → STRING("line1\nline2")

# Unterminated
'"hello' → ERROR

# Empty string
'""' → STRING("")

# Quote in string
'"He said \"hi\""' → STRING('He said "hi"')
```

---

## Extension Exercise: Adding Floating-Point Numbers

**Requirements:**
- Recognize: `3.14`, `0.5`, `.5`, `5.`, `1e10`, `3.14e-5`
- Distinguish: `3.14` (float) vs `3` (int)
- Handle: missing digits, multiple decimals

**Implementation:**

```python
def scan_number(self) -> Token:
    """Scan numeric literal (integer or float)."""
    is_float = False
    
    # Integer part
    while self.current_char().isdigit():
        self.advance()
    
    # Decimal part
    if self.current_char() == '.' and self.peek(1).isdigit():
        is_float = True
        self.advance()  # Consume '.'
        while self.current_char().isdigit():
            self.advance()
    
    # Exponent part
    if self.current_char() in 'eE':
        is_float = True
        self.advance()
        
        # Optional sign
        if self.current_char() in '+-':
            self.advance()
        
        # Exponent digits
        if not self.current_char().isdigit():
            return self.make_token(TokenType.ERROR)  # Malformed exponent
        
        while self.current_char().isdigit():
            self.advance()
    
    lexeme = self.source[self.token_start_pos:self.position]
    
    if is_float:
        value = float(lexeme)
        return self.make_token(TokenType.FLOAT, value)
    else:
        value = int(lexeme)
        return self.make_token(TokenType.NUMBER, value)
```

**Edge cases:**
- `.5` - starts with decimal point (need special case)
- `5.` - ends with decimal point (valid in some languages)
- `1e` - missing exponent digits (error)
- `1e+` - missing exponent digits (error)
- `3.14.159` - multiple decimals (error)

---

## Extension Exercise: Adding Comments

**Two flavors:**

**1. Line comments:** `// comment text` - scan until newline

```python
def skip_line_comment(self):
    """Consume line comment."""
    # '//' already consumed
    while self.current_char() not in '\n\0':
        self.advance()
    # Don't consume the newline - let normal scanning handle it
```

**2. Block comments:** `/* comment */` - scan until closing delimiter

```python
def skip_block_comment(self) -> bool:
    """Consume block comment. Returns False if unterminated."""
    # '/*' already consumed
    
    while True:
        if self.current_char() == '\0':
            return False  # Unterminated
        
        if self.current_char() == '*' and self.peek(1) == '/':
            self.advance()  # Consume '*'
            self.advance()  # Consume '/'
            return True
        
        self.advance()
```

**Challenge: Nested block comments**

Some languages allow `/* /* nested */ */`. This requires counting depth:

```python
def skip_nested_block_comment(self) -> bool:
    """Consume block comment with nesting support."""
    depth = 1  # Already inside one comment
    
    while depth > 0:
        if self.current_char() == '\0':
            return False  # Unterminated
        
        # Opening another level
        if self.current_char() == '/' and self.peek(1) == '*':
            depth += 1
            self.advance()
            self.advance()
        # Closing a level
        elif self.current_char() == '*' and self.peek(1) == '/':
            depth -= 1
            self.advance()
            self.advance()
        else:
            self.advance()
    
    return True
```

**Key insight:** Nested comments are NOT regular! The lexer handles them through explicit depth counting, which is beyond regular languages' capability. This is why most languages don't support nested block comments.

---

## Tracing Execution

Let's trace lexer execution on a simple input to see the state transitions.

**Input:** `x = 42 + y`

**Trace:**

```
Position: 0, Line: 1, Col: 1, Char: 'x'
  → Skip whitespace: none
  → Mark token start: pos=0, line=1, col=1
  → Advance: pos=1, char='x'
  → Current=' ', not alnum, stop identifier scan
  → Lexeme: "x"
  → Token: IDENTIFIER("x") @ 1:1

Position: 1, Line: 1, Col: 2, Char: ' '
  → Skip whitespace: advance to pos=2
  → Mark token start: pos=2, line=1, col=3
  → Advance: pos=3, char='='
  → No lookahead needed
  → Token: EQUAL("=") @ 1:3

Position: 3, Line: 1, Col: 4, Char: ' '
  → Skip whitespace: advance to pos=4
  → Mark token start: pos=4, line=1, col=5
  → Advance: pos=5, char='4'
  → Digit detected, call scan_number()
  → Back up to pos=4, advance again
  → Scan digits: '4', '2'
  → Stop at ' '
  → Lexeme: "42", Value: 42
  → Token: NUMBER("42", value=42) @ 1:5

Position: 7, Line: 1, Col: 8, Char: ' '
  → Skip whitespace: advance to pos=8
  → Mark token start: pos=8, line=1, col=9
  → Advance: pos=9, char='+'
  → Token: PLUS("+") @ 1:9

Position: 9, Line: 1, Col: 10, Char: ' '
  → Skip whitespace: advance to pos=10
  → Mark token start: pos=10, line=1, col=11
  → Advance: pos=11, char='y'
  → Identifier detected
  → Scan: 'y'
  → Stop at EOF
  → Lexeme: "y"
  → Token: IDENTIFIER("y") @ 1:11

Position: 11, Line: 1, Col: 12, Char: '\0'
  → EOF reached
  → Token: EOF("") @ 1:12
```

**Observations:**
- Whitespace consumed without producing tokens
- Position tracking updated on every advance()
- Token start marked before each token scan
- Identifiers and numbers require lookahead scan

**Chess analogy:** This is like tracing perft execution - you see every state transition explicitly.

---

## Performance Considerations

**Hot path:** The lexer runs for every character in the source file.

**Optimization opportunities:**
1. **Minimize allocations** - Reuse token objects if possible
2. **Avoid string copies** - Store start/end indices, extract lexeme only when needed
3. **Fast whitespace skip** - Tight loop, no function calls
4. **Inline common cases** - Single-char tokens don't need helper functions
5. **Bounds checking** - Check once at top of loop, not every peek()

**AoC lesson:** Profile before optimizing. Most lexers spend time in `advance()` and character classification (isdigit, isalpha). Optimize those first.

**Typical measurements:**
- Simple lexer: 1-5 MB/sec
- Optimized hand-written lexer: 50-200 MB/sec
- Flex-generated lexer: 10-50 MB/sec

**For most languages:** Lexing is <5% of compile time, so don't over-optimize.

---

## Comparison: Hand-Written vs Generated

| Aspect | Hand-Written | Generated (Flex/re2c) |
|--------|--------------|----------------------|
| **Code size** | 200-500 lines | 50-100 lines spec |
| **Performance** | 50-200 MB/sec | 10-50 MB/sec |
| **Debuggability** | Easy (it's your code) | Hard (generated code) |
| **Maintainability** | Medium (manual updates) | High (change spec) |
| **Flexibility** | Complete control | Limited by generator |
| **Error messages** | Custom, detailed | Generic |
| **Learning value** | High | Medium |

**Real-world choice:**
- **Hand-write:** C compilers, JavaScript engines, Go compiler
- **Generate:** Most academic compilers, DSLs, prototypes

**Why production compilers hand-write:**
- Performance is critical (tight loop)
- Error recovery needs customization
- Integration with rest of compiler is easier
- Once written, rarely changes

---

## Common Pitfalls

### 1. Forgetting Maximal Munch

**Problem:** `>=` lexes as `>` + `=` instead of `>=`

**Solution:** Always check for longer match first
```python
if char == '>':
    if self.current_char() == '=':  # Check longer first!
        self.advance()
        return GREATER_EQUAL
    return GREATER
```

### 2. Off-by-One in Position Tracking

**Problem:** Error messages report wrong line/column

**Solution:** Test position tracking separately with known inputs

### 3. Infinite Loop on Invalid Input

**Problem:** Lexer gets stuck when encountering unexpected character

**Solution:** Always advance position, even on errors
```python
else:
    # Invalid character - don't get stuck!
    return self.make_token(TokenType.ERROR)
```

### 4. Not Handling EOF

**Problem:** Lexer crashes or infinite loops at end of file

**Solution:** Check for EOF in all loops
```python
while self.current_char() != '\0':
    # ... scanning logic
```

### 5. Losing Token Position Information

**Problem:** Tokens don't remember where they came from

**Solution:** Mark token start before scanning
```python
self.mark_token_start()
char = self.advance()
# ... scan token ...
return self.make_token(type)
```

---

## The Invariants

Hand-written lexers must maintain these guarantees:

1. **Every character consumed** - No infinite loops
2. **Positions always accurate** - Line/column reflect reality
3. **Maximal munch respected** - Longest match wins
4. **Deterministic** - Same input always produces same tokens
5. **Complete** - Every input produces a token stream (even if ERROR tokens)

**Like chess rules:** These are non-negotiable. Violate them and your lexer is incorrect.

---

## Summary

**What you built:** A complete lexer that converts source text into tokens.

**Key patterns:**
- **State management:** position, lookahead, line/column
- **Maximal munch:** greedy longest match
- **Position tracking:** essential for error messages
- **Error recovery:** simple at lexer level (skip and continue)

**What you learned:**
1. Hand-written lexers are explicit DFA walkers
2. Maximal munch is local and greedy
3. Position tracking is trickier than it looks
4. Error handling at lexer level is straightforward

**Cross-domain insights:**
- **Chess:** Lexer state is like board representation - optimized for operations
- **AoC:** Simple cases (single-char lookahead) handle 90% - optimize those

**Next steps:**
- Tomorrow: Testing, performance, edge cases ([[02-lexing/failure-modes]])
- Week 5: Parsing - consuming the tokens you produce

**The big picture:** You've now built the first compiler phase. The tokens you produce are the input to the parser you'll build next week.

---

## Further Reading

- [[02-lexing/regular-languages]] - Mathematical foundation
- [[02-lexing/tokens-vs-characters]] - Why separate lexing
- [[02-lexing/failure-modes]] - Error handling in depth
- [[03-parsing/README]] - Next phase preview

---

*Last updated: 2026-01-21*