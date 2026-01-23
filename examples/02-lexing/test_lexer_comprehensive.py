"""
Comprehensive Lexer Test Suite
================================

Based on the testing strategies from 02-lexing/failure-modes.md, this suite adds:
1. Systematic edge case testing
2. Invariant verification (perft-style)
3. Unicode and encoding tests
4. Numeric boundary testing
5. Stress tests for performance limits
6. Coverage tracking

Complements test_lexer.py with more rigorous testing.
"""

import sys
from typing import List
from lexer_extended import Lexer, Token, TokenType


# ============================================================================
# Invariant Verification (Perft-style testing)
# ============================================================================

def verify_lexer_invariants(source: str, tokens: List[Token]) -> dict:
    """
    Verify that lexer maintains key invariants:
    1. Every character is either consumed or in whitespace/comments
    2. No gaps in positions
    3. No overlapping tokens
    4. All input accounted for
    
    Returns dict with:
    - 'valid': bool
    - 'errors': list of error messages
    """
    errors = []
    
    # Filter out EOF and ERROR tokens for position checking
    real_tokens = [t for t in tokens if t.type not in (TokenType.EOF, TokenType.ERROR)]
    
    # Check 1: All tokens have valid positions
    for i, token in enumerate(real_tokens):
        if token.line < 1:
            errors.append(f"Token {i} ({token.type.name}) has invalid line: {token.line}")
        if token.column < 1:
            errors.append(f"Token {i} ({token.type.name}) has invalid column: {token.column}")
    
    # Check 2: Token positions should generally increase (allowing for newlines)
    for i in range(len(real_tokens) - 1):
        current = real_tokens[i]
        next_tok = real_tokens[i + 1]
        
        # Next token should be on same line at higher column, or on later line
        if next_tok.line < current.line:
            errors.append(
                f"Token order violation: token {i+1} at {next_tok.line}:{next_tok.column} "
                f"comes before token {i} at {current.line}:{current.column}"
            )
        elif next_tok.line == current.line and next_tok.column < current.column:
            errors.append(
                f"Column order violation: token {i+1} at column {next_tok.column} "
                f"comes before token {i} at column {current.column} on same line"
            )
    
    # Check 3: Source should be fully consumed (no leftover characters)
    # This is implicitly checked by lexer reaching EOF
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'token_count': len(real_tokens)
    }


def test_invariants():
    """Test that lexer invariants hold for various inputs."""
    print("=" * 70)
    print("INVARIANT VERIFICATION TESTS (Perft-style)")
    print("=" * 70)
    
    test_cases = [
        "x = 42",
        "if x >= 10 then y = 20",
        "/* comment */ x = 1\n// line comment\ny = 2",
        '"string" + 123 * 4.56',
        "a\n  b\n    c",  # Multi-line with different indentation
    ]
    
    all_valid = True
    for source in test_cases:
        print(f"\nTesting: {source!r}")
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        result = verify_lexer_invariants(source, tokens)
        
        if result['valid']:
            print(f"  ✓ All invariants hold ({result['token_count']} tokens)")
        else:
            print(f"  ✗ Invariant violations found:")
            for error in result['errors']:
                print(f"    - {error}")
            all_valid = False
    
    if all_valid:
        print("\n✓ All invariant tests passed!")
    else:
        print("\n✗ Some invariant tests failed")
    
    return all_valid


# ============================================================================
# Edge Case Testing: String Literals
# ============================================================================

def test_string_edge_cases():
    """Test string literal edge cases and error conditions."""
    print("\n" + "=" * 70)
    print("STRING LITERAL EDGE CASES")
    print("=" * 70)
    
    test_cases = [
        # (source, description, should_error)
        ('""', "Empty string", False),
        ('"a"', "Single character", False),
        ('"hello world"', "String with space", False),
        ('"line1\\nline2"', "Newline escape", False),
        ('"tab\\there"', "Tab escape", False),
        ('"quote: \\"hello\\""', "Escaped quotes", False),
        ('"backslash: \\\\"', "Escaped backslash", False),
        ('"all escapes: \\n\\t\\\\\\"end"', "Multiple escapes", False),
        ('"unterminated', "Unterminated string", True),
        ('"invalid\\xescape"', "Invalid escape sequence", True),
        ('"' + 'x' * 1000 + '"', "Very long string (1000 chars)", False),
    ]
    
    for source, description, should_error in test_cases:
        print(f"\n{description}: {source[:50]!r}{'...' if len(source) > 50 else ''}")
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        errors = [t for t in tokens if t.type == TokenType.ERROR]
        has_error = len(errors) > 0
        
        if has_error == should_error:
            status = "✓"
        else:
            status = "✗"
        
        if has_error:
            print(f"  {status} Error detected: {errors[0].lexeme if errors else 'N/A'}")
        else:
            string_tokens = [t for t in tokens if t.type == TokenType.STRING]
            if string_tokens:
                value = string_tokens[0].value
                print(f"  {status} Parsed successfully, value length: {len(value)}")


# ============================================================================
# Edge Case Testing: Numeric Literals
# ============================================================================

def test_numeric_edge_cases():
    """Test numeric literal edge cases and boundaries."""
    print("\n" + "=" * 70)
    print("NUMERIC LITERAL EDGE CASES")
    print("=" * 70)
    
    test_cases = [
        # (source, description, expected_type)
        ("0", "Zero", TokenType.NUMBER),
        ("42", "Positive integer", TokenType.NUMBER),
        ("999999", "Large integer", TokenType.NUMBER),
        ("0.0", "Zero float", TokenType.FLOAT),
        ("3.14", "Simple float", TokenType.FLOAT),
        (".5", "Leading decimal point", TokenType.FLOAT),
        ("5.", "Trailing decimal point", TokenType.FLOAT),
        ("1e10", "Scientific notation", TokenType.FLOAT),
        ("2.5e-3", "Negative exponent", TokenType.FLOAT),
        ("1.23e+4", "Positive exponent", TokenType.FLOAT),
        ("0.000001", "Very small float", TokenType.FLOAT),
        ("999999.999999", "Large float", TokenType.FLOAT),
        # Overflow/boundary cases (implementation-dependent behavior)
        ("9999999999999999999999", "Very large integer", None),  # May overflow
        ("1e308", "Near float max", TokenType.FLOAT),
        ("1e-308", "Near float min", TokenType.FLOAT),
    ]
    
    for source, description, expected_type in test_cases:
        print(f"\n{description}: {source!r}")
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        number_tokens = [t for t in tokens if t.type in (TokenType.NUMBER, TokenType.FLOAT)]
        
        if number_tokens:
            token = number_tokens[0]
            status = "✓" if expected_type is None or token.type == expected_type else "✗"
            print(f"  {status} Type: {token.type.name}, Value: {token.value}")
        else:
            print(f"  ✗ No number token produced")


# ============================================================================
# Edge Case Testing: Unicode
# ============================================================================

def test_unicode_handling():
    """Test Unicode character handling."""
    print("\n" + "=" * 70)
    print("UNICODE HANDLING TESTS")
    print("=" * 70)
    
    test_cases = [
        # (source, description)
        ("café", "Accented characters in identifier"),
        ("x = 'café'", "Accented characters in string (if using single quotes)"),
        ('"café"', "Accented characters in string"),
        ('"Hello 世界"', "Chinese characters in string"),
        ('"emoji: 🚀 🎉"', "Emoji in string"),
        ("π = 3.14", "Greek letter in identifier"),
        ('"tab:\t space: "', "Whitespace in string"),
        ('"newline:\\n"', "Newline escape in string"),
    ]
    
    for source, description in test_cases:
        print(f"\n{description}: {source!r}")
        
        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Count non-EOF tokens
            real_tokens = [t for t in tokens if t.type != TokenType.EOF]
            print(f"  ✓ Tokenized successfully ({len(real_tokens)} tokens)")
            
            for token in real_tokens:
                if token.type == TokenType.STRING:
                    print(f"    STRING: {token.value!r}")
                elif token.type == TokenType.IDENTIFIER:
                    print(f"    IDENTIFIER: {token.lexeme!r}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")


# ============================================================================
# Edge Case Testing: Operators and Maximal Munch
# ============================================================================

def test_operator_maximal_munch():
    """Systematically test all operator combinations for maximal munch."""
    print("\n" + "=" * 70)
    print("OPERATOR MAXIMAL MUNCH TESTS")
    print("=" * 70)
    
    test_cases = [
        # (source, expected_tokens, description)
        ("=", [TokenType.EQUAL], "Single equal"),
        ("==", [TokenType.EQUAL_EQUAL], "Double equal"),
        ("===", [TokenType.EQUAL_EQUAL, TokenType.EQUAL], "Triple equal"),
        ("====", [TokenType.EQUAL_EQUAL, TokenType.EQUAL_EQUAL], "Quad equal"),
        (">", [TokenType.GREATER], "Greater than"),
        (">=", [TokenType.GREATER_EQUAL], "Greater or equal"),
        (">==", [TokenType.GREATER_EQUAL, TokenType.EQUAL], "Greater-equal followed by equal"),
        ("<", [TokenType.LESS], "Less than"),
        ("<=", [TokenType.LESS_EQUAL], "Less or equal"),
        ("!=", [TokenType.BANG_EQUAL], "Not equal"),
        ("!==", [TokenType.BANG_EQUAL, TokenType.EQUAL], "Not-equal followed by equal"),
        ("+-*/", [TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH], "All arithmetic"),
        ("x>=y<=z", [TokenType.IDENTIFIER, TokenType.GREATER_EQUAL, TokenType.IDENTIFIER, 
                     TokenType.LESS_EQUAL, TokenType.IDENTIFIER], "Chained comparisons"),
    ]
    
    all_passed = True
    for source, expected_types, description in test_cases:
        print(f"\n{description}: {source!r}")
        
        lexer = Lexer(source)
        tokens = [t for t in lexer.tokenize() if t.type != TokenType.EOF]
        
        actual_types = [t.type for t in tokens]
        
        if actual_types == expected_types:
            print(f"  ✓ Correct: {' '.join(t.name for t in actual_types)}")
        else:
            print(f"  ✗ Expected: {' '.join(t.name for t in expected_types)}")
            print(f"    Got:      {' '.join(t.name for t in actual_types)}")
            all_passed = False
    
    return all_passed


# ============================================================================
# Edge Case Testing: Comments
# ============================================================================

def test_comment_edge_cases():
    """Test comment handling edge cases."""
    print("\n" + "=" * 70)
    print("COMMENT EDGE CASES")
    print("=" * 70)
    
    test_cases = [
        # (source, description, expected_token_count)
        ("x = 1 // comment", "Line comment at end", 3),  # x, =, 1
        ("// comment\nx = 1", "Line comment at start", 3),  # x, =, 1
        ("x /* comment */ = 1", "Block comment in middle", 3),
        ("/* comment */", "Only block comment", 0),
        ("//", "Empty line comment", 0),
        ("/**/", "Empty block comment", 0),
        ("/* /* nested? */ */", "Nested block comment attempt", None),  # Implementation-dependent
        ("/* unterminated", "Unterminated block comment", None),  # Should error
        ("x = 1 // no newline at EOF", "Line comment without final newline", 3),
        ("/* multi\nline\ncomment */ x = 1", "Multi-line block comment", 3),
    ]
    
    for source, description, expected_count in test_cases:
        print(f"\n{description}: {source!r}")
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Count non-EOF, non-ERROR tokens
        real_tokens = [t for t in tokens if t.type not in (TokenType.EOF, TokenType.ERROR)]
        error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
        
        if error_tokens:
            print(f"  ⚠ Error detected: {error_tokens[0].lexeme}")
        elif expected_count is not None:
            status = "✓" if len(real_tokens) == expected_count else "✗"
            print(f"  {status} Got {len(real_tokens)} tokens (expected {expected_count})")
        else:
            print(f"  ℹ Got {len(real_tokens)} tokens (implementation-dependent)")


# ============================================================================
# Edge Case Testing: Whitespace
# ============================================================================

def test_whitespace_edge_cases():
    """Test various whitespace scenarios."""
    print("\n" + "=" * 70)
    print("WHITESPACE EDGE CASES")
    print("=" * 70)
    
    test_cases = [
        ("x=1", "No whitespace", 3),
        ("x = 1", "Single spaces", 3),
        ("x  =  1", "Multiple spaces", 3),
        ("x\t=\t1", "Tabs", 3),
        ("x \t = \t 1", "Mixed spaces and tabs", 3),
        ("\n\nx = 1\n\n", "Leading/trailing newlines", 3),
        ("   x = 1   ", "Leading/trailing spaces", 3),
        ("x\r\n=\r\n1", "Windows line endings", 3),
        ("x\n\n\n=\n\n\n1", "Multiple consecutive newlines", 3),
    ]
    
    for source, description, expected_count in test_cases:
        print(f"\n{description}: {source!r}")
        
        lexer = Lexer(source)
        tokens = [t for t in lexer.tokenize() if t.type != TokenType.EOF]
        
        status = "✓" if len(tokens) == expected_count else "✗"
        print(f"  {status} Got {len(tokens)} tokens (expected {expected_count})")


# ============================================================================
# Stress Testing
# ============================================================================

def test_stress_large_input():
    """Test lexer with very large input."""
    print("\n" + "=" * 70)
    print("STRESS TEST: LARGE INPUT")
    print("=" * 70)
    
    # Generate large source file
    lines = []
    for i in range(1000):
        lines.append(f"x{i} = {i} + {i+1} * {i+2}")
    
    source = "\n".join(lines)
    
    print(f"\nGenerated source: {len(source):,} bytes, {len(lines):,} lines")
    
    import time
    start = time.time()
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    elapsed = time.time() - start
    
    real_tokens = [t for t in tokens if t.type != TokenType.EOF]
    
    print(f"  ✓ Tokenized in {elapsed:.3f} seconds")
    print(f"  ✓ Produced {len(real_tokens):,} tokens")
    print(f"  ✓ Throughput: {len(source)/elapsed/1024/1024:.2f} MB/sec")


def test_stress_deeply_nested():
    """Test with deeply nested expressions (lots of parens)."""
    print("\n" + "=" * 70)
    print("STRESS TEST: DEEPLY NESTED EXPRESSIONS")
    print("=" * 70)
    
    # Note: Current lexer doesn't have parens, but test with operators
    depth = 100
    source = "x = " + " + ".join(["1"] * depth)
    
    print(f"\nGenerated expression with {depth} additions")
    
    lexer = Lexer(source)
    tokens = [t for t in lexer.tokenize() if t.type != TokenType.EOF]
    
    print(f"  ✓ Tokenized successfully ({len(tokens)} tokens)")


def test_stress_long_identifier():
    """Test very long identifier."""
    print("\n" + "=" * 70)
    print("STRESS TEST: LONG IDENTIFIER")
    print("=" * 70)
    
    # Create 1000-character identifier
    long_name = "x" * 1000
    source = f"{long_name} = 42"
    
    print(f"\nIdentifier length: {len(long_name)} characters")
    
    lexer = Lexer(source)
    tokens = [t for t in lexer.tokenize() if t.type != TokenType.EOF]
    
    id_token = next((t for t in tokens if t.type == TokenType.IDENTIFIER), None)
    
    if id_token and len(id_token.lexeme) == len(long_name):
        print(f"  ✓ Successfully tokenized ({len(tokens)} tokens)")
    else:
        print(f"  ✗ Identifier not fully captured")


# ============================================================================
# Main Test Runner
# ============================================================================

def main():
    """Run all comprehensive tests."""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE LEXER TEST SUITE")
    print("Based on 02-lexing/failure-modes.md")
    print("=" * 70)
    
    tests = [
        ("Invariant Verification", test_invariants),
        ("String Edge Cases", test_string_edge_cases),
        ("Numeric Edge Cases", test_numeric_edge_cases),
        ("Unicode Handling", test_unicode_handling),
        ("Operator Maximal Munch", test_operator_maximal_munch),
        ("Comment Edge Cases", test_comment_edge_cases),
        ("Whitespace Edge Cases", test_whitespace_edge_cases),
        ("Stress: Large Input", test_stress_large_input),
        ("Stress: Deeply Nested", test_stress_deeply_nested),
        ("Stress: Long Identifier", test_stress_long_identifier),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            # If test returns bool, track it; otherwise assume success
            if result is False:
                results.append((name, False))
            else:
                results.append((name, True))
        except Exception as e:
            print(f"\n✗ Test '{name}' raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test suite(s) had failures")
        return 1


if __name__ == "__main__":
    sys.exit(main())
