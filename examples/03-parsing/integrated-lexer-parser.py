"""
Integrated Lexer + Parser Example
Week 5, Day 2 - January 27, 2026

This demonstrates integration of:
- Week 4 Lexer (from 02-lexing/lexer_extended.py)
- Week 5 Parser (from 03-parsing/basic-parser.py)

Shows the complete front-end pipeline:
    Source Code → Tokens → AST
"""

import sys
import os

# Add Week 4 directory to path
week4_path = os.path.join(os.path.dirname(__file__), '..', '02-lexing')
if week4_path not in sys.path:
    sys.path.insert(0, week4_path)

# Import Week 4 lexer
from lexer_extended import Lexer as Week4Lexer, TokenType as Week4TokenType

# Import Week 5 parser components - must be in same directory
# We'll import the necessary components directly
import importlib.util
spec = importlib.util.spec_from_file_location("basic_parser", 
    os.path.join(os.path.dirname(__file__), "basic-parser.py"))
basic_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(basic_parser)

# Now extract what we need
RecursiveDescentParser = basic_parser.RecursiveDescentParser
ParserToken = basic_parser.Token
INT = basic_parser.INT
ID = basic_parser.ID
PLUS = basic_parser.PLUS
MINUS = basic_parser.MINUS
STAR = basic_parser.STAR
SLASH = basic_parser.SLASH
LPAREN = basic_parser.LPAREN
RPAREN = basic_parser.RPAREN
EOF = basic_parser.EOF
print_ast = basic_parser.print_ast
evaluate = basic_parser.evaluate


# ============================================================================
# Token Type Mapping: Week 4 Lexer → Week 5 Parser
# ============================================================================

TOKEN_TYPE_MAP = {
    Week4TokenType.NUMBER: INT,
    Week4TokenType.IDENTIFIER: ID,
    Week4TokenType.PLUS: PLUS,
    Week4TokenType.MINUS: MINUS,
    Week4TokenType.STAR: STAR,
    Week4TokenType.SLASH: SLASH,
    Week4TokenType.EOF: EOF,
}


def convert_token(week4_token):
    """
    Convert Week 4 lexer token to Week 5 parser token format.
    
    Args:
        week4_token: Token from lexer_extended.py
    
    Returns:
        ParserToken compatible with basic-parser.py
    """
    # Map token type
    if week4_token.type in TOKEN_TYPE_MAP:
        parser_type = TOKEN_TYPE_MAP[week4_token.type]
    else:
        # Unknown token type - skip or error
        return None
    
    # Get value
    if week4_token.type == Week4TokenType.NUMBER:
        value = week4_token.value  # Already an int
    else:
        value = week4_token.lexeme
    
    # Create parser token
    return ParserToken(
        type=parser_type,
        value=value,
        line=week4_token.line,
        col=week4_token.column
    )


def tokenize_with_week4_lexer(source):
    """
    Tokenize source using Week 4 lexer, return tokens for Week 5 parser.
    
    Args:
        source: Source code string
    
    Returns:
        List of ParserToken objects
    """
    lexer = Week4Lexer(source)
    tokens = []
    
    while True:
        token = lexer.next_token()
        
        # Convert to parser token format
        parser_token = convert_token(token)
        
        if parser_token is not None:
            tokens.append(parser_token)
        
        # Stop at EOF
        if token.type == Week4TokenType.EOF:
            break
    
    return tokens


# ============================================================================
# Integrated Pipeline
# ============================================================================

def compile_expression(source, trace=False):
    """
    Complete front-end: source → tokens → AST.
    
    Args:
        source: Source code string
        trace: Enable parser tracing
    
    Returns:
        AST root node
    """
    print(f"Source: {source!r}\n")
    
    # Phase 1: Lexical Analysis (Week 4)
    print("=" * 60)
    print("PHASE 1: LEXICAL ANALYSIS")
    print("=" * 60)
    tokens = tokenize_with_week4_lexer(source)
    print(f"Tokens ({len(tokens)}):")
    for token in tokens:
        print(f"  {token}")
    print()
    
    # Phase 2: Syntactic Analysis (Week 5)
    print("=" * 60)
    print("PHASE 2: SYNTACTIC ANALYSIS")
    print("=" * 60)
    parser = RecursiveDescentParser(tokens, trace=trace)
    ast = parser.parse()
    print("\nAST:")
    print_ast(ast)
    print()
    
    return ast


def compile_and_evaluate(source, env=None, trace=False):
    """
    Complete pipeline: source → tokens → AST → evaluation.
    
    Args:
        source: Source code string
        env: Variable environment (dict)
        trace: Enable parser tracing
    
    Returns:
        Evaluation result
    """
    ast = compile_expression(source, trace=trace)
    
    # Phase 3: Evaluation (simple interpreter)
    print("=" * 60)
    print("PHASE 3: EVALUATION")
    print("=" * 60)
    result = evaluate(ast, env)
    print(f"Result: {result}")
    print()
    
    return result


# ============================================================================
# Test Cases
# ============================================================================

def test_basic_integration():
    """Test basic lexer + parser integration"""
    print("\n" + "=" * 60)
    print("TEST 1: Basic Integration")
    print("=" * 60 + "\n")
    
    result = compile_and_evaluate("3 + 4 * 5")
    assert result == 23, f"Expected 23, got {result}"
    print("✓ Test passed\n")


def test_with_spaces():
    """Test that lexer handles whitespace correctly"""
    print("\n" + "=" * 60)
    print("TEST 2: Whitespace Handling")
    print("=" * 60 + "\n")
    
    # Different spacing should produce same result
    sources = [
        "2+3*4",
        "2 + 3 * 4",
        "2  +  3  *  4",
        "  2   +   3   *   4  ",
    ]
    
    for source in sources:
        result = compile_and_evaluate(source)
        assert result == 14, f"Expected 14, got {result}"
        print("✓ Test passed\n")


def test_identifiers():
    """Test that identifiers work through the pipeline"""
    print("\n" + "=" * 60)
    print("TEST 3: Identifiers")
    print("=" * 60 + "\n")
    
    env = {'x': 10, 'y': 5, 'z': 2}
    result = compile_and_evaluate("x + y * z", env=env)
    assert result == 20, f"Expected 20, got {result}"  # 10 + (5 * 2)
    print("✓ Test passed\n")


def test_complex_expression():
    """Test complex expression through pipeline"""
    print("\n" + "=" * 60)
    print("TEST 4: Complex Expression")
    print("=" * 60 + "\n")
    
    source = "1 + 2 * 3 + 4 * 5"
    result = compile_and_evaluate(source)
    assert result == 27, f"Expected 27, got {result}"  # 1 + 6 + 20
    print("✓ Test passed\n")


def test_with_trace():
    """Demonstrate full trace through lexer and parser"""
    print("\n" + "=" * 60)
    print("TEST 5: Full Trace Demonstration")
    print("=" * 60 + "\n")
    
    result = compile_and_evaluate("3 + 4 * 5", trace=True)
    assert result == 23
    print("✓ Test passed\n")


def demo_error_handling():
    """Demonstrate error reporting from lexer and parser"""
    print("\n" + "=" * 60)
    print("DEMO: Error Handling")
    print("=" * 60 + "\n")
    
    # Test 1: Parser error (syntax error)
    print("Test: Syntax Error (missing operand)")
    print("-" * 60)
    try:
        compile_expression("3 + * 5")
        print("❌ Should have raised error!")
    except Exception as e:
        print(f"✓ Caught expected error:\n  {e}\n")
    
    # Test 2: Parser error (unexpected token)
    print("Test: Unexpected Token")
    print("-" * 60)
    try:
        compile_expression("3 + 4)")
        print("❌ Should have raised error!")
    except Exception as e:
        print(f"✓ Caught expected error:\n  {e}\n")


# ============================================================================
# Interactive Mode
# ============================================================================

def repl():
    """Read-Eval-Print Loop for testing expressions"""
    print("=" * 60)
    print("Expression Evaluator (Integrated Lexer + Parser)")
    print("=" * 60)
    print("Enter expressions to evaluate (Ctrl+C to exit)")
    print("Examples:")
    print("  3 + 4 * 5")
    print("  (2 + 3) * 4")
    print("  x + y  (with variables)")
    print()
    
    env = {}
    
    while True:
        try:
            # Read
            source = input(">>> ").strip()
            if not source:
                continue
            
            # Check for variable assignment (simple extension)
            if '=' in source and not any(op in source for op in ['==', '!=', '<=', '>=']):
                # Simple assignment: x = expr
                parts = source.split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    expr = parts[1].strip()
                    
                    # Evaluate expression
                    ast = compile_expression(expr, trace=False)
                    result = evaluate(ast, env)
                    env[var_name] = result
                    print(f"{var_name} = {result}\n")
                    continue
            
            # Compile and evaluate
            result = compile_and_evaluate(source, env=env, trace=False)
            
        except KeyboardInterrupt:
            print("\n\nBye!")
            break
        except EOFError:
            print("\n\nBye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all tests and demonstrations"""
    print("\n")
    print("*" * 60)
    print("INTEGRATED LEXER + PARSER TEST SUITE")
    print("Week 4 Lexer → Week 5 Parser")
    print("*" * 60)
    
    # Run tests
    test_basic_integration()
    test_with_spaces()
    test_identifiers()
    test_complex_expression()
    test_with_trace()
    demo_error_handling()
    
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)
    print()
    
    # Offer REPL
    print("Start interactive mode? (y/n): ", end='')
    choice = input().strip().lower()
    if choice in ['y', 'yes']:
        repl()


if __name__ == "__main__":
    main()
