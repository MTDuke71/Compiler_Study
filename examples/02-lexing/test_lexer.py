"""
Lexer Test Suite
================

Comprehensive test cases for the hand-written lexer demonstrating:
- Edge cases and error handling
- Performance measurement
- Usage patterns
- Debugging techniques
"""

import time
from lexer_minimal import Lexer as MinimalLexer, TokenType as MinimalTokenType
from lexer_extended import Lexer as ExtendedLexer, TokenType as ExtendedTokenType


def test_minimal_lexer():
    """Test the minimal lexer with various inputs."""
    print("=" * 70)
    print("MINIMAL LEXER TESTS")
    print("=" * 70)
    
    test_cases = [
        ("Basic assignment", "x = 42"),
        ("Keywords", "if x == 10 while y"),
        ("Operators", "+ - * / = =="),
        ("Mixed", "if foo == 123 + bar"),
        ("Invalid chars", "x @ y # z"),
        ("Maximal munch", "==="),  # Should be == followed by =
        ("Numbers in identifiers", "x123y456"),
    ]
    
    for name, source in test_cases:
        print(f"\n{name}: {source!r}")
        print("-" * 60)
        
        lexer = MinimalLexer(source)
        tokens = lexer.tokenize()
        
        for token in tokens:
            if token.type == MinimalTokenType.EOF:
                continue
            value_str = f" = {token.value}" if token.value is not None else ""
            print(f"  {token.type.name:15} '{token.lexeme}'{value_str:15} @ {token.line}:{token.column}")


def test_extended_lexer():
    """Test the extended lexer features."""
    print("\n" + "=" * 70)
    print("EXTENDED LEXER TESTS")
    print("=" * 70)
    
    test_cases = [
        ("Basic string", '"hello"'),
        ("String with escapes", '"line1\\nline2\\ttab"'),
        ("Empty string", '""'),
        ("Unterminated string", '"hello'),
        ("Integer", "42"),
        ("Float", "3.14"),
        ("Scientific notation", "1.5e10"),
        ("Negative exponent", "2.5e-3"),
        ("Line comment", "x = 42 // this is a comment"),
        ("Block comment", "y = /* comment */ 10"),
        ("Unterminated comment", "z = /* oops"),
        ("Comparison operators", ">= <= != == < >"),
        ("Multi-line", "x = 1\ny = 2\nz = x + y"),
    ]
    
    for name, source in test_cases:
        print(f"\n{name}: {source!r}")
        print("-" * 60)
        
        lexer = ExtendedLexer(source)
        tokens = lexer.tokenize()
        
        for token in tokens:
            if token.type == ExtendedTokenType.EOF:
                continue
            value_str = f" = {token.value!r}" if token.value is not None else ""
            print(f"  {token.type.name:15} '{token.lexeme}'{value_str:20} @ {token.line}:{token.column}")


def test_position_tracking():
    """Verify line and column tracking is accurate."""
    print("\n" + "=" * 70)
    print("POSITION TRACKING TEST")
    print("=" * 70)
    
    source = """line1
    line2 with indentation
line3"""
    
    print(f"\nSource:\n{source}\n")
    print("Token positions:")
    print("-" * 60)
    
    lexer = MinimalLexer(source)
    tokens = lexer.tokenize()
    
    for token in tokens:
        if token.type == MinimalTokenType.EOF:
            continue
        # Show the exact position in the source
        lines = source.split('\n')
        line_text = lines[token.line - 1] if token.line <= len(lines) else ""
        pointer = " " * (token.column - 1) + "^"
        
        print(f"\n{token.type.name} '{token.lexeme}' @ line {token.line}, col {token.column}")
        print(f"  {line_text}")
        print(f"  {pointer}")


def test_error_recovery():
    """Test that lexer recovers from errors and continues."""
    print("\n" + "=" * 70)
    print("ERROR RECOVERY TEST")
    print("=" * 70)
    
    # Source with multiple errors
    source = "x = @ 42 # + y $ z"
    
    print(f"\nSource: {source!r}")
    print("Expected: ERROR tokens for @, #, $, but continues scanning")
    print("-" * 60)
    
    lexer = MinimalLexer(source)
    tokens = lexer.tokenize()
    
    error_count = 0
    for token in tokens:
        if token.type == MinimalTokenType.ERROR:
            error_count += 1
            print(f"  ERROR: '{token.lexeme}' @ {token.line}:{token.column}")
        elif token.type != MinimalTokenType.EOF:
            print(f"  {token.type.name}: '{token.lexeme}'")
    
    print(f"\nRecovered from {error_count} errors and produced complete token stream")


def benchmark_lexer(lexer_class, source: str, iterations: int = 1000):
    """Measure lexer performance."""
    start_time = time.time()
    
    for _ in range(iterations):
        lexer = lexer_class(source)
        tokens = lexer.tokenize()
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Calculate throughput
    total_chars = len(source) * iterations
    chars_per_sec = total_chars / elapsed
    mb_per_sec = chars_per_sec / (1024 * 1024)
    
    return {
        'iterations': iterations,
        'elapsed': elapsed,
        'chars_per_sec': chars_per_sec,
        'mb_per_sec': mb_per_sec,
        'token_count': len(tokens)
    }


def test_performance():
    """Benchmark lexer performance."""
    print("\n" + "=" * 70)
    print("PERFORMANCE TEST")
    print("=" * 70)
    
    # Generate a test program
    source = "\n".join([
        f"x{i} = {i} + {i+1} * {i+2}" 
        for i in range(100)
    ])
    
    print(f"\nSource: {len(source)} characters, {len(source.split())} words")
    print(f"Running 1000 iterations...\n")
    
    # Benchmark minimal lexer
    print("Minimal Lexer:")
    results = benchmark_lexer(MinimalLexer, source, iterations=1000)
    print(f"  Time: {results['elapsed']:.3f} seconds")
    print(f"  Throughput: {results['mb_per_sec']:.2f} MB/sec")
    print(f"  Tokens produced: {results['token_count']}")
    
    # Benchmark extended lexer
    print("\nExtended Lexer:")
    results = benchmark_lexer(ExtendedLexer, source, iterations=1000)
    print(f"  Time: {results['elapsed']:.3f} seconds")
    print(f"  Throughput: {results['mb_per_sec']:.2f} MB/sec")
    print(f"  Tokens produced: {results['token_count']}")
    
    print("\nNote: Extended lexer is slightly slower due to comment checking")


def test_maximal_munch():
    """Demonstrate maximal munch principle."""
    print("\n" + "=" * 70)
    print("MAXIMAL MUNCH DEMONSTRATION")
    print("=" * 70)
    
    test_cases = [
        ("x>=42", "Should be: IDENTIFIER GREATER_EQUAL NUMBER"),
        ("x>=y", "Should be: IDENTIFIER GREATER_EQUAL IDENTIFIER"),
        ("===", "Should be: EQUAL_EQUAL EQUAL (not three separate EQUAL)"),
        ("!==", "Should be: BANG_EQUAL EQUAL (extended lexer)"),
    ]
    
    for source, expected in test_cases:
        print(f"\n{source!r} - {expected}")
        print("-" * 60)
        
        # Try with extended lexer (has >= and !=)
        lexer = ExtendedLexer(source)
        tokens = [t for t in lexer.tokenize() if t.type != ExtendedTokenType.EOF]
        
        print("  Tokens:", " ".join(f"{t.type.name}" for t in tokens))


def interactive_mode():
    """Interactive REPL for testing the lexer."""
    print("\n" + "=" * 70)
    print("INTERACTIVE LEXER (type 'quit' to exit)")
    print("=" * 70)
    
    lexer_class = ExtendedLexer
    
    while True:
        try:
            source = input("\n> ")
            if source.strip().lower() in ['quit', 'exit', 'q']:
                break
            
            lexer = lexer_class(source)
            tokens = lexer.tokenize()
            
            for token in tokens:
                if token.type == ExtendedTokenType.EOF:
                    continue
                value_str = f" = {token.value!r}" if token.value is not None else ""
                print(f"  {token.type.name:15} '{token.lexeme}'{value_str}")
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Run all tests."""
    test_minimal_lexer()
    test_extended_lexer()
    test_position_tracking()
    test_error_recovery()
    test_performance()
    test_maximal_munch()
    
    # Uncomment to enable interactive mode
    # interactive_mode()
    
    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
