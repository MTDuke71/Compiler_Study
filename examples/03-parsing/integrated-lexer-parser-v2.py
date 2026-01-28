"""
Integration: Week 4 Lexer → Week 5 Parser (Unified Token Format)
Week 5, Day 2 - January 27, 2026

This demonstrates the integration using Week 4's FIXED lexer.

Pipeline:
    Source Code → Lexer (Week 4, fixed) → Tokens → Parser (Week 5) → AST → Result
"""

import sys
from pathlib import Path
import importlib.util

# Import unified token types
sys.path.insert(0, str(Path(__file__).parent.parent))
from token_types import Token, TokenType

# Import Week 4 lexer (now fixed!)
week4_lexer_path = Path(__file__).parent.parent / "02-lexing" / "lexer_extended.py"
spec = importlib.util.spec_from_file_location("week4_lexer", week4_lexer_path)
week4_lexer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(week4_lexer)

# Import the parser using unified tokens
parser_path = Path(__file__).parent / "basic-parser-unified.py"
spec = importlib.util.spec_from_file_location("parser", parser_path)
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)


def compile_expression(source, env=None, verbose=False):
    """Complete compilation pipeline using Week 4 lexer"""
    if verbose:
        print(f"\n{'='*70}")
        print(f"COMPILING: {source}")
        print(f"{'='*70}")
    
    # Phase 1: Lexical Analysis (Week 4 - FIXED!)
    if verbose:
        print("\nPhase 1: Lexical Analysis (Week 4 Lexer - Fixed)")
    
    lexer = week4_lexer.Lexer(source)
    tokens = []
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if verbose and token.type != week4_lexer.TokenType.EOF:
            print(f"  {token}")
        if token.type == week4_lexer.TokenType.EOF:
            break
    
    # Phase 2: Syntactic Analysis (Week 5)
    if verbose:
        print("\nPhase 2: Syntactic Analysis (Week 5 Parser)")
    
    parser = parser_module.RecursiveDescentParser(tokens, trace=verbose)
    ast = parser.parse()
    
    if verbose:
        print(f"\nAST: {ast}")
    
    # Phase 3: Evaluation
    if verbose:
        print("\nPhase 3: Evaluation")
    
    result = parser_module.evaluate(ast, env or {})
    
    if verbose:
        print(f"Result: {result}")
    
    return result


def run_integration_tests():
    """Test the complete pipeline"""
    print("=" * 70)
    print("INTEGRATION TESTS: Week 4 Lexer + Week 5 Parser (Unified Tokens)")
    print("=" * 70)
    
    tests = [
        ("2 + 3", {}, 5, "Basic addition"),
        ("3 + 4 * 5", {}, 23, "Precedence"),
        ("(2 + 3) * 4", {}, 20, "Parentheses"),
        ("x + y * z", {'x': 10, 'y': 5, 'z': 2}, 20, "Variables"),
        ("1 + 2 * 3 + 4 * 5", {}, 27, "Complex expression"),
    ]
    
    passed = 0
    for source, env, expected, description in tests:
        try:
            result = compile_expression(source, env)
            if result == expected:
                print(f"✓ {description}: '{source}' = {result}")
                passed += 1
            else:
                print(f"✗ {description}: '{source}' - expected {expected}, got {result}")
        except Exception as e:
            print(f"✗ {description}: '{source}' - {e}")
    
    print(f"\nPassed: {passed}/{len(tests)}")
    
    # Show one with verbose output
    print("\n" + "=" * 70)
    print("DETAILED TRACE: 3 + 4 * 5")
    print("=" * 70)
    compile_expression("3 + 4 * 5", verbose=True)


def interactive_repl():
    """Interactive Read-Eval-Print Loop"""
    print("\n" + "=" * 70)
    print("INTERACTIVE REPL")
    print("=" * 70)
    print("Enter expressions to evaluate (or 'quit' to exit)")
    print("You can set variables: x = 10")
    print()
    
    env = {}
    
    while True:
        try:
            source = input(">>> ").strip()
            
            if source in ('quit', 'exit'):
                break
            
            if not source:
                continue
            
            # Check for variable assignment (simple version)
            if '=' in source and source.count('=') == 1 and not any(op in source for op in ['==', '!=', '<=', '>=']):
                parts = source.split('=')
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    value_expr = parts[1].strip()
                    
                    if var_name.isidentifier():
                        value = compile_expression(value_expr, env)
                        env[var_name] = value
                        print(f"{var_name} = {value}")
                        continue
            
            # Regular expression evaluation
            result = compile_expression(source, env)
            print(f"Result: {result}")
            
        except Exception as e:
            print(f"Error: {e}")


def show_token_compatibility():
    """Demonstrate Week 4 lexer (fixed!) working with Week 5 parser"""
    print("\n" + "=" * 70)
    print("WEEK 4 LEXER (FIXED!) → WEEK 5 PARSER")
    print("=" * 70)
    
    source = "2 + 3"
    
    print(f"\nSource: {source}\n")
    print("Tokens from Week 4 Lexer:")
    
    lexer = week4_lexer.Lexer(source)
    tokens = []
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.type != week4_lexer.TokenType.EOF:
            print(f"  {token}")
        if token.type == week4_lexer.TokenType.EOF:
            break
    
    print(f"\n✓ Week 4 lexer fixed - {len(tokens)} tokens total (no infinite loop!)")
    print("✓ Tokens work directly with Week 5 parser.\n")
    
    # Parse and evaluate
    parser = parser_module.RecursiveDescentParser(tokens)
    ast = parser.parse()
    result = parser_module.evaluate(ast)
    
    print(f"Result: {result}")


if __name__ == "__main__":
    show_token_compatibility()
    run_integration_tests()
    
    # Uncomment to run interactive REPL:
    # interactive_repl()
