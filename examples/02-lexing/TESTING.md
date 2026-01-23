# Testing Overview

## Two Test Suites

### `test_lexer.py` - Demonstrations and Benchmarks
**Purpose:** Educational demonstrations of lexer features

**What it covers:**
- Basic token recognition examples
- Interactive REPL mode for experimentation
- Position tracking visualization
- Error recovery demonstration
- Performance benchmarking
- Maximal munch examples

**Best for:** Learning how the lexer works, experimenting, quick validation

**Run:** `python test_lexer.py`

---

### `test_lexer_comprehensive.py` - Edge Cases and Invariants
**Purpose:** Rigorous testing based on [`02-lexing/failure-modes.md`](../../02-lexing/failure-modes.md)

**What it covers:**
- Invariant verification (perft-style testing)
- Systematic edge case testing:
  - String literals (escapes, unterminated, long strings)
  - Numeric literals (overflow, scientific notation, boundaries)
  - Unicode handling (accented chars, emoji, multi-byte)
  - Operator maximal munch (all combinations)
  - Comment edge cases (unterminated, nested, EOF)
  - Whitespace variations (tabs, newlines, line endings)
- Stress testing:
  - Large input files (1000+ lines)
  - Very long tokens (1000+ chars)
  - Performance measurement

**Best for:** Verifying correctness, finding bugs, production readiness

**Run:** `python test_lexer_comprehensive.py`

---

## Testing Philosophy (From Failure Modes Doc)

### Invariants to Verify

Like perft testing in chess engines, lexer tests verify that transformations preserve correctness:

1. **Every character consumed:** No gaps, no overlaps
2. **Positions monotonic:** Line/column always increase (or stay same)
3. **Complete token stream:** All input accounted for
4. **Error recovery:** Lexer continues after errors

### Test Categories

| Category | Purpose | Example |
|----------|---------|---------|
| **Unit tests** | Individual token patterns | `"42"` → `NUMBER(42)` |
| **Sequence tests** | Maximal munch | `">="` → `GREATER_EQUAL` not `GREATER, EQUAL` |
| **Error cases** | Recovery and messages | Unterminated string → error + continue |
| **Position tracking** | Line/column accuracy | Multi-line input positions correct |
| **Stress tests** | Performance and limits | 1MB input, 1000-char identifiers |

### Performance Targets (From Failure Modes)

**Hand-written lexer (like ours):**
- Throughput: 50-200 MB/sec typical
- Memory: O(1) space (streaming)
- Scaling: O(n) time with input size

**Context matters:**
- Batch compiler: 100 MB/sec is plenty (lexing ~5-10% of compile time)
- Interactive tools: Latency < 100ms matters more than throughput
- JIT compiler: Every millisecond counts

---

## Quick Start

### Run Both Test Suites

```bash
# Educational demonstrations
python test_lexer.py

# Comprehensive edge case testing
python test_lexer_comprehensive.py
```

### Interactive Experimentation

Edit `test_lexer.py`, uncomment `interactive_mode()` in `main()`, then:

```bash
python test_lexer.py
# Type expressions at the prompt to see tokens
```

### Run Specific Test Category

Open `test_lexer_comprehensive.py`, comment out unwanted tests in `main()`, or grep output:

```bash
python test_lexer_comprehensive.py | grep "STRING EDGE"
```

---

## What Each Test Suite Tests

### test_lexer.py

- ✅ Basic functionality demos
- ✅ Keyword recognition
- ✅ Operator recognition
- ✅ Position tracking visualization
- ✅ Error recovery example
- ✅ Performance benchmark
- ✅ Maximal munch demo

### test_lexer_comprehensive.py

- ✅ **Invariant verification** (perft-style)
- ✅ **String edge cases** (10 variations)
- ✅ **Numeric edge cases** (15 variations)
- ✅ **Unicode handling** (8 test cases)
- ✅ **Operator maximal munch** (14 combinations)
- ✅ **Comment edge cases** (10 scenarios)
- ✅ **Whitespace handling** (9 variations)
- ✅ **Stress: Large input** (1000 lines)
- ✅ **Stress: Deep nesting** (100 levels)
- ✅ **Stress: Long tokens** (1000 chars)

---

## Adding Your Own Tests

### To test_lexer.py (Demonstrations)

Add a new test function:

```python
def test_my_feature():
    print("\n" + "=" * 70)
    print("MY FEATURE TEST")
    print("=" * 70)
    
    source = "test input"
    lexer = ExtendedLexer(source)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(f"{token.type.name}: {token.lexeme}")

# Add to main()
def main():
    # ... existing tests ...
    test_my_feature()
```

### To test_lexer_comprehensive.py (Edge Cases)

Follow the pattern in existing test functions:

```python
def test_my_edge_cases():
    """Test description."""
    print("\n" + "=" * 70)
    print("MY EDGE CASES")
    print("=" * 70)
    
    test_cases = [
        ("input1", "description1", expected1),
        ("input2", "description2", expected2),
    ]
    
    for source, description, expected in test_cases:
        print(f"\n{description}: {source!r}")
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Verify behavior
        # Print ✓ or ✗ based on result
```

---

## Common Test Failures and Fixes

### Position Tracking Off

**Symptom:** Invariant tests fail with position violations

**Cause:** Not updating line/column on every character

**Fix:** Check `advance()` method updates position correctly

### Maximal Munch Wrong

**Symptom:** `">="` becomes `GREATER, EQUAL` instead of `GREATER_EQUAL`

**Cause:** Not looking ahead before committing

**Fix:** Always peek at next character for multi-char operators

### Unicode Errors

**Symptom:** Exception or garbage tokens on non-ASCII input

**Cause:** Assuming one byte = one character

**Fix:** Use Python's string handling (already Unicode-aware in Python 3)

### String Escape Issues

**Symptom:** `\n` stored as two characters instead of newline

**Cause:** Not processing escapes during scanning

**Fix:** Check `scan_string()` converts escape sequences

---

## Next Steps

After running both test suites:

1. **Fix any failures** in comprehensive tests
2. **Add tests** for any custom tokens you added
3. **Measure performance** on your expected workload
4. **Read** [`02-lexing/failure-modes.md`](../../02-lexing/failure-modes.md) for more context
5. **Move to parsing** (Week 5) - consuming these tokens to build trees

---

## References

- [`02-lexing/failure-modes.md`](../../02-lexing/failure-modes.md) - Theory behind these tests
- [`02-lexing/hand-written-lexer.md`](../../02-lexing/hand-written-lexer.md) - Implementation guide
- [`COMPARISON.md`](COMPARISON.md) - Alternative lexer approaches
- [`README.md`](README.md) - Complete documentation
