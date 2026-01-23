## Links
- Up: [[02-lexing/README]]
- Related: [[02-lexing/tokens-vs-characters]] [[02-lexing/hand-written-lexer]]
- Down: [[02-lexing/hand-written-lexer]]

# Lexer Failure Modes: Testing, Performance, and Edge Cases

## Purpose

Making a lexer that **works** is easy. Making a lexer that **works correctly in production** requires systematic testing, performance awareness, and careful handling of edge cases.

This note covers:
1. How to test lexers comprehensively
2. What performance characteristics matter
3. Common failure modes and how to handle them
4. Error recovery strategies

**Chess analogy:** Like perft testing in chess engines—you need invariants to verify correctness at every step.

**AoC analogy:** Measure before optimizing. Simple often beats complex. Profile first.

---

## The Testing Problem

### What Does "Correct" Mean?

A lexer is correct if it:
1. **Recognizes valid tokens:** All legal input produces expected tokens
2. **Rejects invalid tokens:** Illegal input produces errors, not garbage tokens
3. **Preserves position information:** Line/column tracking is accurate
4. **Maintains invariants:** Token stream is complete and unambiguous
5. **Handles edge cases:** Unicode, EOF, maximum length strings, etc.

**Like perft testing:** You need a checksum. For lexers, the checksum is:
- Input string fully consumed OR error reported
- Every character accounted for in tokens or whitespace
- No gaps, no overlaps in source positions

### Types of Tests

**1. Unit Tests (Token Recognition)**

Test individual token patterns in isolation:

```
Input: "42"
Expected: NUMBER(42, line=1, col=1)

Input: "identifier_123"
Expected: IDENTIFIER("identifier_123", line=1, col=1)

Input: ">="
Expected: GREATER_EQUAL(line=1, col=1)
NOT: GREATER(line=1, col=1), EQUAL(line=1, col=3)
```

**2. Sequence Tests (Maximal Munch)**

Ensure longest match wins:

```
Input: ">=>"
Expected: GREATER_EQUAL, GREATER
NOT: GREATER, EQUAL, GREATER

Input: "123.456"
Expected: FLOAT(123.456)
NOT: NUMBER(123), DOT, NUMBER(456)
```

**3. Error Cases (Recovery)**

Verify proper error reporting:

```
Input: "unterminated string
Expected: ERROR("Unterminated string literal", line=1, col=1)

Input: "999999999999999999999"
Expected: ERROR("Number literal too large", line=1, col=1)
OR: NUMBER with overflow flag

Input: "invalid\x00byte"
Expected: ERROR("Invalid character: 0x00", line=1, col=8)
```

**4. Position Tracking**

Verify line/column accuracy:

```
Input:
"line 1
line 2
  line 3"

Expected token positions:
IDENTIFIER("line", line=1, col=1)
NUMBER(1, line=1, col=6)
IDENTIFIER("line", line=2, col=1)
NUMBER(2, line=2, col=6)
IDENTIFIER("line", line=3, col=3)
NUMBER(3, line=3, col=8)
```

**5. Stress Tests (Performance and Limits)**

Test behavior at extremes:

```
- 1MB identifier (should error with max length)
- 10,000 nested parens (lexer should handle, parser might not)
- 100MB file (memory usage acceptable?)
- Unicode edge cases (emoji, combining characters, RTL text)
```

### Test Organization Strategy

**Partition by token type:**
```
test_numbers()
  - integers: 0, 42, -17, 999999
  - floats: 0.0, 3.14, 1e10, .5
  - edge cases: leading zeros, max value, overflow
  
test_strings()
  - simple: "hello"
  - escapes: "hello\nworld", "quote: \""
  - edge cases: "", max length, unterminated, invalid escape
  
test_operators()
  - single char: +, -, *, /
  - multi char: ==, !=, <=, >=
  - maximal munch: >= vs > and =
```

**Partition by failure mode:**
```
test_invalid_input()
test_position_tracking()
test_unicode_handling()
test_performance_large_input()
```

**AoC lesson:** Start with simple cases, add complexity incrementally. Each test should verify ONE thing.

---

## Common Failure Modes

### 1. Maximal Munch Violations

**Problem:** Lexer commits too early, doesn't recognize longer token.

**Example:**
```
Input: ">="
Wrong: Lexer sees '>', emits GREATER, then sees '=' and emits EQUAL
Right: Lexer looks ahead, sees ">=", emits GREATER_EQUAL
```

**Detection:** Test all multi-character operators in sequence.

**Fix:** Always peek ahead before committing to a token.

### 2. Position Tracking Errors

**Problem:** Line/column numbers drift from actual source position.

**Common causes:**
- Forgetting to increment line counter on `\n`
- Mixing `\r\n` and `\n` newline styles
- Not resetting column to 0 on newline
- Off-by-one errors in token start position

**Detection:** Test multiline input with known token positions.

**Fix:** Update position on **every** character consumed:
```python
def advance(self):
    ch = self.input[self.pos]
    self.pos += 1
    if ch == '\n':
        self.line += 1
        self.col = 0
    else:
        self.col += 1
    return ch
```

### 3. Unclosed Delimiters

**Problem:** String/comment started but never terminated.

**Example:**
```
Input: "unterminated string
```

**Bad behavior:** Lexer scans to EOF, returns string token with entire rest of file as value.

**Good behavior:** Error at end of line or EOF with helpful message.

**Detection:** Test strings/comments without closing delimiter.

**Fix:** Check for newline/EOF while scanning string:
```python
def scan_string(self):
    start_line = self.line
    value = ""
    while self.peek() != '"':
        if self.peek() in ('\n', '\0'):  # EOF or newline
            error(f"Unterminated string starting at line {start_line}")
        value += self.advance()
    self.advance()  # closing quote
    return Token(STRING, value)
```

### 4. Escape Sequence Handling

**Problem:** Incorrectly processing `\n`, `\t`, `\\`, `\"` in strings.

**Example:**
```
Input: "hello\nworld"
Wrong: String value is literal backslash-n (2 chars)
Right: String value contains newline character (1 char)
```

**Detection:** Test strings with all standard escapes.

**Fix:** Process escapes during scanning:
```python
def scan_string(self):
    value = ""
    while self.peek() != '"':
        if self.peek() == '\\':
            self.advance()  # consume backslash
            escape = self.advance()
            if escape == 'n':
                value += '\n'
            elif escape == 't':
                value += '\t'
            elif escape == '\\':
                value += '\\'
            elif escape == '"':
                value += '"'
            else:
                error(f"Invalid escape sequence: \\{escape}")
        else:
            value += self.advance()
    return Token(STRING, value)
```

### 5. Unicode and Character Encoding

**Problem:** Assuming ASCII, breaking on Unicode input.

**Example:**
```
Input: "café" or "🚀" (emoji)
```

**Bad behavior:** Treats multi-byte UTF-8 sequences as separate characters, produces garbage.

**Good behavior:** Correctly handles Unicode identifiers and string literals.

**Detection:** Test with non-ASCII input (accented chars, emoji, etc.)

**Fix:** Use language's proper string/char handling (Python 3 strings are Unicode by default, C requires explicit UTF-8 handling).

### 6. Numeric Overflow

**Problem:** Number literal too large to fit in target type.

**Example:**
```
Input: "99999999999999999999999999"
```

**Options:**
1. **Error during lexing:** "Number literal exceeds maximum value"
2. **Return token with overflow flag:** Parser decides what to do
3. **Use arbitrary precision:** Store as string, convert later

**Best practice:** Lexer recognizes syntax (it's a number), semantic analysis checks range.

**Detection:** Test with INT_MAX + 1, LONG_MAX + 1, etc.

### 7. Ambiguous Lexical Rules

**Problem:** Multiple patterns could match the same input.

**Example:**
```
Input: "if"
Is it: IDENTIFIER("if") or keyword IF?
```

**Resolution:** Keywords take precedence over identifiers.

**Implementation:**
```python
def scan_identifier(self):
    value = ""
    while self.peek().isalnum() or self.peek() == '_':
        value += self.advance()
    
    # Check if identifier is actually a keyword
    if value in KEYWORDS:
        return Token(KEYWORDS[value])  # IF, WHILE, etc.
    else:
        return Token(IDENTIFIER, value)
```

**Detection:** Test all keywords in isolation and in context.

### 8. Whitespace and Comment Handling

**Problem:** Inconsistent treatment of whitespace and comments.

**Options:**
1. **Discard completely:** Most compilers
2. **Preserve for formatter:** Code formatters need original whitespace
3. **Include in token stream:** Parsers that care about indentation (Python)

**Edge cases:**
- Multiple consecutive whitespace
- Comments at EOF without trailing newline
- Mixed tabs and spaces
- Empty lines

**Detection:** Test various whitespace patterns, ensure consistent behavior.

---

## Performance Considerations

### What to Measure

**1. Throughput (MB/sec)**

How fast can lexer scan source code?

**Typical targets:**
- Hand-written lexer: 50-200 MB/sec
- Generated lexer (Flex): 20-100 MB/sec
- Regex-based lexer (Python re): 5-50 MB/sec

**Measurement:**
```python
import time

def benchmark_lexer(input_text):
    start = time.time()
    tokens = lexer.scan(input_text)
    elapsed = time.time() - start
    mb_per_sec = (len(input_text) / 1_000_000) / elapsed
    print(f"Scanned {len(input_text)} bytes in {elapsed:.3f}s ({mb_per_sec:.1f} MB/sec)")
```

**2. Memory Usage**

How much memory does lexer allocate?

**Sources:**
- Token objects (especially if keeping all in memory)
- String values (duplicates for keywords?)
- Lookahead buffers
- Position tracking state

**Optimization:** String interning for keywords/identifiers.

**3. Latency (Time to First Token)**

How quickly can lexer produce first token?

**Matters for:** Interactive tools (IDE autocomplete, REPL)

**4. Scaling Behavior**

Does performance degrade with input size?

**Expected:** O(n) time, O(1) space (streaming)

**Test:** Double input size, expect 2x time, same memory.

### Performance Tradeoffs

**1. Hand-Written vs. Generated**

| Aspect | Hand-Written | Generated (Flex) |
|--------|--------------|------------------|
| **Speed** | Faster (optimized for specific language) | Good (DFA is fast) |
| **Memory** | Lower (no DFA table storage) | Higher (DFA transition tables) |
| **Development Time** | Slower (manual code) | Faster (write regex, generate) |
| **Maintainability** | Harder (more code) | Easier (declarative spec) |
| **Error Messages** | Better (custom) | Generic |

**AoC lesson:** Simple hand-written lexer often beats complex generated one for small languages.

**2. Lookahead Strategy**

**Single character peek:**
- Fast (just array index)
- Sufficient for most tokens
- Example: `if (peek() == '=')` for `>=`

**Unbounded lookahead:**
- Slower (scan until delimiter)
- Necessary for strings, comments, some keywords
- Example: Scan until closing `"`

**Backtracking:**
- Very slow (re-scan input)
- Avoid in production lexers
- DFA eliminates backtracking

**3. Error Handling Cost**

**Fast path (no errors):**
- Minimal overhead
- Direct character classification

**Error path:**
- Building error messages (allocation)
- Position tracking (extra bookkeeping)
- Recovery (scanning to next valid token)

**Optimization:** Don't build detailed error info unless error actually occurs.

### When Is Performance "Good Enough"?

**Context matters:**

**Batch compiler (GCC, Clang):**
- Lexing is 5-10% of total compile time
- 100 MB/sec is plenty fast
- Focus on correctness over speed

**Interactive tools (IDE, REPL):**
- Need low latency (< 100ms for small edits)
- Throughput less important than responsiveness
- Incremental lexing may be needed

**JIT compiler (JavaScript V8, Java HotSpot):**
- Lexing on critical path (startup time)
- Every millisecond counts
- Hand-tuned, SIMD-optimized lexers

**AoC lesson:** Measure first. 10x improvement in lexer speed might give 0.5% faster compile.

---

## Error Recovery Strategies

### Goals of Error Recovery

1. **Continue scanning:** Find as many errors as possible in one pass
2. **Minimize cascading errors:** One mistake shouldn't cause 100 errors
3. **Provide helpful context:** Where did error occur? What was expected?

### Recovery Techniques

**1. Panic Mode (Skip to Synchronization Point)**

When error found, skip characters until reaching a "safe" point:

```python
def recover_from_error(self):
    # Skip until newline, semicolon, or closing brace
    while self.peek() not in ('\n', ';', '}', '\0'):
        self.advance()
    # Now resume normal scanning
```

**Pros:** Simple, fast
**Cons:** May skip valid code

**2. Substitute Token**

Replace invalid input with placeholder token:

```python
if not self.is_valid_char():
    error(f"Invalid character: {self.peek()}")
    self.advance()  # skip it
    return Token(ERROR, "�")  # placeholder
```

**Pros:** Parser can continue
**Cons:** May produce nonsense parse tree

**3. Minimal Distance Correction**

Guess what user meant:

```python
if self.scan_string() found unterminated string:
    error("Unterminated string (expected closing quote)")
    # Pretend we found the closing quote
    return Token(STRING, scanned_value)
```

**Pros:** Allows analysis to continue
**Cons:** Might guess wrong

### Error Message Quality

**Bad:**
```
Error at position 147
```

**Better:**
```
Error at line 5, column 23: Unterminated string literal
```

**Best:**
```
Error at line 5, column 23: Unterminated string literal
    x = "hello world
        ^
Expected closing quote (") before end of line
```

**Key elements:**
1. **Position:** Line and column
2. **Context:** Show the actual source code
3. **Explanation:** What's wrong and why
4. **Suggestion:** How to fix it

---

## Testing Checklist

Use this checklist to verify lexer robustness:

### Basic Functionality
- [ ] All token types recognized correctly
- [ ] Whitespace handled properly
- [ ] Comments ignored
- [ ] Keywords distinguished from identifiers
- [ ] Position tracking accurate

### Maximal Munch
- [ ] Multi-character operators work (`>=`, `==`, `!=`)
- [ ] Longest match always chosen
- [ ] Ambiguous cases resolved correctly

### Edge Cases
- [ ] Empty input produces EOF token
- [ ] Input without newline at EOF
- [ ] Very long tokens (max length handling)
- [ ] Numeric overflow/underflow
- [ ] Unicode input (if supported)
- [ ] All valid escape sequences in strings
- [ ] Invalid escape sequences rejected

### Error Handling
- [ ] Unterminated strings detected
- [ ] Unterminated comments detected (if block comments supported)
- [ ] Invalid characters rejected
- [ ] Error messages include position
- [ ] Recovery allows scanning to continue

### Performance
- [ ] Throughput measured on large input
- [ ] Memory usage reasonable
- [ ] No performance cliff at specific input size
- [ ] Scales linearly with input size

### Integration
- [ ] Lexer produces token stream parser expects
- [ ] EOF token generated correctly
- [ ] Error tokens can be handled by parser
- [ ] Position info sufficient for error reporting

---

## Real-World Example: Testing GCC's Lexer

GCC's C lexer handles:
- Trigraphs (`??=` becomes `#`)
- Line splicing (backslash-newline)
- Multiple character encodings (UTF-8, UTF-16, etc.)
- Preprocessor directives intermixed with tokens
- Very long identifiers (OS limits, not lexer limits)

**Test suite includes:**
- 1000+ individual test cases
- Edge cases from bug reports (real-world failures)
- Performance tests on large files (Linux kernel source)
- Comparison against reference implementation

**Key lesson:** Production lexers are tested against **decades** of edge cases found in the wild.

---

## Summary: Making Lexers Robust

**Correctness:**
- Test all token types thoroughly
- Verify position tracking on multiline input
- Test error cases, not just success cases
- Use perft-style invariants (all input consumed, no gaps/overlaps)

**Performance:**
- Measure actual throughput on representative input
- Simple hand-written often beats complex generated
- Lexing is usually 5-10% of compile time (context dependent)
- Profile before optimizing

**Error Handling:**
- Detect errors close to where they occur
- Provide line/column context
- Recover gracefully to find multiple errors
- Error messages should help user fix problem

**Edge Cases:**
- Unicode handling (if needed)
- Numeric overflow
- Unclosed delimiters
- Escape sequences
- Maximum length inputs
- EOF without trailing newline

**Chess/AoC analogy:** Like perft testing, lexer testing verifies invariants at each step. Measure before optimizing. Simple often wins.

---

## Next Steps

With a robust, tested lexer:
1. **Integration:** Connect to parser (Week 5)
2. **Optimization:** Profile and improve hot paths (if needed)
3. **Documentation:** Describe lexical grammar and error codes
4. **Maintenance:** Update tests as language evolves

**The lexer is done when:**
- All tests pass
- Performance is acceptable
- Error messages are helpful
- Code is maintainable

Not when it's perfect—when it's **good enough for the next phase**.
