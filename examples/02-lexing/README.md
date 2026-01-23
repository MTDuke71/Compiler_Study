# Hand-Written Lexer Examples

This directory contains runnable Python implementations of the hand-written lexers described in [`02-lexing/hand-written-lexer.md`](../../02-lexing/hand-written-lexer.md).

## Files

### `lexer_minimal.py`
Basic lexer demonstrating core concepts:
- Token recognition with maximal munch
- Position tracking (line, column)
- Single-character lookahead
- Basic error handling

**Supported tokens:**
- Numbers: `42`, `123`
- Identifiers: `x`, `foo`, `bar_123`
- Keywords: `if`, `else`, `while`
- Operators: `+`, `-`, `*`, `/`, `=`, `==`

### `lexer_extended.py`
Extended lexer with additional features:
- String literals with escape sequences (`\n`, `\t`, `\\`, `\"`)
- Floating-point numbers (`3.14`, `1e10`, `2.5e-3`)
- Line comments (`//`)
- Block comments (`/* ... */`)
- Comparison operators (`>`, `>=`, `<`, `<=`, `!=`)

### `test_lexer.py`
Comprehensive test suite demonstrating:
- Edge cases and error handling
- Performance measurement
- Position tracking verification
- Maximal munch demonstration
- Interactive REPL mode

### `COMPARISON.md`
Side-by-side comparison of lexer implementation approaches:
- Hand-written vs Flex vs PLY vs Regex
- When to use each approach
- Performance benchmarks
- Code volume comparisons
- Real-world usage examples
- **Includes runnable examples:** `lexer_regex_example.py`, `lexer_ply_example.py`, `lexer.l`

**📖 Recommended reading** to understand alternatives to hand-written lexers.

## All Files in This Directory

### Working Python Implementations
- ✅ `lexer_minimal.py` - Basic hand-written lexer (~200 lines)
- ✅ `lexer_extended.py` - Extended with strings, floats, comments (~350 lines)
- ✅ `lexer_regex_example.py` - Regex-based tokenizer (~90 lines)
- ✅ `lexer_ply_example.py` - PLY-based lexer (~100 lines, requires `pip install ply`)

### Testing and Documentation
- ✅ `test_lexer.py` - Comprehensive test suite (demonstrations and benchmarks)
- ✅ `test_lexer_comprehensive.py` - **NEW:** Rigorous edge case and invariant testing
- ✅ `TESTING.md` - **NEW:** Complete testing guide and philosophy
- ✅ `COMPARISON.md` - Side-by-side comparison of all approaches
- ✅ `README.md` - This file

### Utilities
- ✅ `token_dumper.py` - **NEW:** Dump token streams to files (human/JSON/CSV formats)

### Flex/Lex Examples (require flex toolchain)
- ✅ `lexer.l` - Flex specification (~70 lines)
- ✅ `tokens.h` - Token definitions for C
- ✅ `test_input.txt` - Sample input file

## Running the Code

### Basic Usage

**Minimal lexer:**
```bash
python lexer_minimal.py
```

**Extended lexer:**
```bash
python lexer_extended.py
```

**Test suites:**
```bash
# Original test suite (demonstrations and benchmarks)
python test_lexer.py

# Comprehensive test suite (edge cases and invariants)
python test_lexer_comprehensive.py
```

**Dump tokens to file:**
```bash
# Human-readable format (default)
python token_dumper.py test_input.txt

# JSON format
python token_dumper.py test_input.txt --format json --output tokens.json

# CSV for spreadsheet analysis
python token_dumper.py test_input.txt --format csv --output tokens.csv

# Compact format (just token types)
python token_dumper.py test_input.txt --format compact
```

### Interactive Mode

To experiment with the lexer interactively, edit `test_lexer.py` and uncomment the `interactive_mode()` call in `main()`, then run:

```bash
python test_lexer.py
```

You'll get a REPL where you can type expressions and see the tokens produced.

### Import and Use

You can also import the lexers in your own code:

```python
from lexer_extended import Lexer, TokenType

source = 'x = 3.14 + "hello"'
lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type.name}: {token.lexeme}")
```

**Dump tokens programmatically:**

```python
from lexer_extended import Lexer
from token_dumper import dump_tokens

source = 'x = 42 + 3.14'
lexer = Lexer(source)
tokens = lexer.tokenize()

# Dump to file
dump_tokens(tokens, 'output.txt', format='human')
dump_tokens(tokens, 'output.json', format='json')
```

## Token Dumper Utility

The `token_dumper.py` utility saves token streams to files for inspection, debugging, and testing.

### Use Cases

**1. Debugging large files:**
```bash
python token_dumper.py large_program.txt --output tokens.txt
# Inspect tokens.txt in your editor
```

**2. Creating test fixtures:**
```bash
python token_dumper.py test_input.txt --format json --output expected_tokens.json
# Use expected_tokens.json to verify lexer output in tests
```

**3. Comparing lexer outputs:**
```bash
python token_dumper.py file1.txt --output tokens1.txt
# ... modify lexer ...
python token_dumper.py file1.txt --output tokens2.txt
diff tokens1.txt tokens2.txt
```

**4. Analyzing token patterns:**
```bash
python token_dumper.py source.txt --format csv --output tokens.csv
# Open tokens.csv in Excel/spreadsheet for analysis
```

### Output Formats

**Human-readable (default):**
```
================================================================================
TOKEN STREAM
================================================================================

[   0] IDENTIFIER      'x'                       @ 1:1
[   1] EQUAL           '='                       @ 1:3
[   2] NUMBER          '42'          = 42        @ 1:5
[   3] PLUS            '+'                       @ 1:8
[   4] FLOAT           '3.14'        = 3.14      @ 1:10
[   5] EOF
```

**JSON:**
```json
[
  {
    "type": "IDENTIFIER",
    "lexeme": "x",
    "value": null,
    "line": 1,
    "column": 1
  },
  ...
]
```

**CSV:**
```csv
index,type,lexeme,value,line,column
0,IDENTIFIER,"x","",1,1
1,EQUAL,"=","",1,3
2,NUMBER,"42","42",1,5
```

**Compact (minimal):**
```
IDENTIFIER
EQUAL
NUMBER
PLUS
FLOAT
```

## Experiments to Try

### 1. Understanding Maximal Munch

Run the lexer on these inputs and observe how `==` is recognized:

```python
from lexer_minimal import Lexer

test_cases = [
    "x = y",      # Single =
    "x == y",     # Double ==
    "x === y",    # Should be == followed by =
]

for source in test_cases:
    lexer = Lexer(source)
    tokens = [t.lexeme for t in lexer.tokenize() if t.type.name != 'EOF']
    print(f"{source:15} → {tokens}")
```

**Expected output:**
```
x = y           → ['x', '=', 'y']
x == y          → ['x', '==', 'y']
x === y         → ['x', '==', '=', 'y']
```

### 2. Position Tracking

See how line and column numbers are tracked:

```python
from lexer_minimal import Lexer

source = """x = 1
y = 2
z = x + y"""

lexer = Lexer(source)
for token in lexer.tokenize():
    if token.type.name != 'EOF':
        print(f"{token.lexeme:10} @ line {token.line}, col {token.column}")
```

### 3. Error Recovery

Test how the lexer handles invalid input:

```python
from lexer_minimal import Lexer

source = "x = @ 42 # + y $ z"
lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type.name:15} {token.lexeme!r}")
```

Notice that the lexer produces ERROR tokens but continues scanning.

### 4. String Escape Sequences

Test the extended lexer's string handling:

```python
from lexer_extended import Lexer

test_strings = [
    '"hello"',
    '"line1\\nline2"',
    '"tab\\there"',
    '"quote: \\"hi\\""',
    '"unterminated',
]

for s in test_strings:
    lexer = Lexer(s)
    tokens = lexer.tokenize()
    token = tokens[0]
    print(f"{s:25} → {token.type.name:10} value={token.value!r}")
```

### 5. Floating-Point Numbers

See how different number formats are recognized:

```python
from lexer_extended import Lexer

numbers = [
    "42",       # Integer
    "3.14",     # Float
    "1e10",     # Scientific (no decimal)
    "2.5e-3",   # Scientific with negative exponent
    "0.5",      # Leading zero
]

for num in numbers:
    lexer = Lexer(num)
    token = lexer.tokenize()[0]
    print(f"{num:10} → {token.type.name:10} = {token.value}")
```

### 6. Comments

Test comment handling:

```python
from lexer_extended import Lexer

sources = [
    "x = 42 // line comment",
    "y = /* block */ 10",
    "z = /* multi\nline\ncomment */ 5",
]

for source in sources:
    lexer = Lexer(source)
    tokens = [t for t in lexer.tokenize() if t.type.name != 'EOF']
    print(f"{source[:30]:30} → {[t.lexeme for t in tokens]}")
```

### 7. Performance Testing

Measure lexer throughput:

```python
import time
from lexer_extended import Lexer

# Generate a large input
source = "\n".join([f"x{i} = {i} + {i+1}" for i in range(10000)])

start = time.time()
lexer = Lexer(source)
tokens = lexer.tokenize()
end = time.time()

chars_per_sec = len(source) / (end - start)
mb_per_sec = chars_per_sec / (1024 * 1024)

print(f"Scanned {len(source)} chars in {end-start:.3f}s")
print(f"Throughput: {mb_per_sec:.2f} MB/sec")
print(f"Tokens: {len(tokens)}")
```

## Comprehensive Testing (NEW)

The `test_lexer_comprehensive.py` file adds rigorous testing based on [`02-lexing/failure-modes.md`](../../02-lexing/failure-modes.md). It includes:

### 1. Invariant Verification (Perft-style)

Like perft testing in chess engines, verifies that lexer maintains key invariants:
- Every character consumed or accounted for
- No gaps in positions
- No overlapping tokens
- Positions increase monotonically

```bash
python test_lexer_comprehensive.py
```

### 2. Edge Case Categories

**String Literals:**
- Empty strings
- Escape sequences (`\n`, `\t`, `\\`, `\"`)
- Unterminated strings
- Invalid escape sequences
- Very long strings (1000+ characters)

**Numeric Literals:**
- Zero, positive, large integers
- Floats with various formats (`.5`, `5.`, `5.0`)
- Scientific notation (`1e10`, `2.5e-3`)
- Boundary cases (very large/small numbers)
- Overflow conditions

**Unicode:**
- Accented characters (`café`)
- Chinese/Japanese characters
- Emoji in strings (`🚀 🎉`)
- Greek letters (`π`)

**Operators (Maximal Munch):**
- All single-char operators
- All multi-char operators (`>=`, `==`, `!=`)
- Sequences (`===`, `>==`)
- Chained comparisons

**Comments:**
- Line comments with/without newline at EOF
- Block comments (empty, multi-line)
- Comments at various positions
- Unterminated comments

**Whitespace:**
- Spaces, tabs, newlines
- Windows vs Unix line endings
- Mixed whitespace
- Leading/trailing whitespace

### 3. Stress Tests

**Large Input:**
- 1000+ lines of code
- Measures throughput (MB/sec)
- Verifies memory usage stays reasonable

**Deeply Nested:**
- Long expression chains
- Tests that lexer doesn't have depth limits

**Long Tokens:**
- 1000+ character identifiers
- Very long strings
- Tests buffer handling

### Running Specific Test Categories

The comprehensive test suite can be modified to run specific tests:

```python
# Edit test_lexer_comprehensive.py, comment out tests in main() you don't want
# Or run and grep for specific output:
python test_lexer_comprehensive.py | grep "STRING EDGE"
```

### What the Tests Verify

Each test category checks different aspects from the failure-modes doc:

| Test Category | Verifies |
|---------------|----------|
| Invariant Verification | Correctness (like perft) |
| String Edge Cases | Delimiter handling, escapes |
| Numeric Edge Cases | Number parsing, overflow |
| Unicode Handling | Multi-byte character support |
| Operator Maximal Munch | Longest match always chosen |
| Comment Edge Cases | Proper comment stripping |
| Whitespace Edge Cases | Consistent whitespace handling |
| Stress Tests | Performance, scaling, limits |

### Expected Output

When all tests pass, you'll see:

```
✓ Invariant Verification
✓ String Edge Cases
✓ Numeric Edge Cases
✓ Unicode Handling
✓ Operator Maximal Munch
✓ Comment Edge Cases
✓ Whitespace Edge Cases
✓ Stress: Large Input
✓ Stress: Deeply Nested
✓ Stress: Long Identifier

10/10 test suites passed

🎉 All tests passed!
```

## Extending the Lexer


### Add a New Operator

To add `&&` (logical AND):

1. Add to `TokenType` enum:
   ```python
   AND = auto()
   ```

2. Add to `next_token()`:
   ```python
   elif char == '&':
       if self.current_char() == '&':
           self.advance()
           return self.make_token(TokenType.AND)
       else:
           return self.make_token(TokenType.ERROR)  # Single & not allowed
   ```

### Add a New Keyword

To add `for` keyword:

1. Add to `TokenType` enum:
   ```python
   FOR = auto()
   ```

2. Add to keywords dict in `scan_identifier()`:
   ```python
   keywords = {
       'if': TokenType.IF,
       'else': TokenType.ELSE,
       'while': TokenType.WHILE,
       'for': TokenType.FOR,  # ← Add this
   }
   ```

### Add Hexadecimal Numbers

To recognize `0x1A3F`:

Add to `next_token()` before the `isdigit()` check:
```python
# Hex numbers (0x...)
elif char == '0' and self.current_char() in 'xX':
    self.advance()  # Skip 'x'
    if not self.current_char() in '0123456789abcdefABCDEF':
        return self.make_token(TokenType.ERROR)
    
    while self.current_char() in '0123456789abcdefABCDEF':
        self.advance()
    
    lexeme = self.source[self.token_start_pos:self.position]
    value = int(lexeme, 16)
    return self.make_token(TokenType.NUMBER, value)
```

## Learning Path

**Read → Run → Modify → Understand**

1. **Read:** Start with `lexer_minimal.py` - understand the structure
2. **Run:** Execute it and observe the output
3. **Modify:** Try adding a new operator or keyword
4. **Understand:** Run `test_lexer.py` to see comprehensive examples

Then move to `lexer_extended.py` and repeat the cycle.

## Common Issues

**"Module not found" error:**
- Make sure you're in the `examples/02-lexing/` directory
- Or add the directory to your Python path

**Infinite loops:**
- Make sure all scanning loops check for `\0` (EOF)
- Always advance position, even on errors

**Wrong positions:**
- Check that `advance()` updates both position and column
- Check that newlines reset column to 1

**Maximal munch not working:**
- Always check for longer matches first
- Use `current_char()` for lookahead, don't advance until you commit

## Next Steps

After understanding these lexers:
- Read [`02-lexing/failure-modes.md`](../../02-lexing/failure-modes.md) for edge cases
- Move to Week 5: Parsing (consuming these tokens to build trees)
- Compare with generated lexers (Flex, re2c)

---

**Remember:** The goal isn't just to have working code, but to understand **why** lexers work this way. Each design decision (maximal munch, position tracking, error recovery) reflects fundamental constraints of lexical analysis.
