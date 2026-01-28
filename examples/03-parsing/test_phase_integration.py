"""
Integration test: Verify complete_parser works with lexer_extended
Demonstrates phase compatibility per INTERFACES.md
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import lexer from Week 4
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02-lexing'))
from lexer_extended import Lexer

# Import parser from Week 5
from complete_parser import Parser, print_ast

# Test code
code = '''
fn add(x, y) {
    return x + y;
}

var result = add(10, 20);
'''

print("="*70)
print("Integration Test: Lexer (Week 4) → Parser (Week 5)")
print("="*70)
print("\nSource code:")
print(code)

# Phase 1: Lex with Week 4 lexer
print("\n" + "="*70)
print("Phase 1: Lexing (using lexer_extended.py)")
print("="*70)

lexer = Lexer(code)
tokens = []
while True:
    token = lexer.next_token()
    tokens.append(token)
    if token.type.name == 'EOF':
        break

print(f"Generated {len(tokens)} tokens")
print("\nFirst 10 tokens:")
for i, tok in enumerate(tokens[:10]):
    print(f"  {i+1}. {tok}")

# Phase 2: Parse with Week 5 parser
print("\n" + "="*70)
print("Phase 2: Parsing (using complete_parser.py)")
print("="*70)

try:
    parser = Parser(tokens)
    ast = parser.parse()
    
    print("\n[SUCCESS] Phases are compatible!")
    print("\nAbstract Syntax Tree:")
    print("="*70)
    print_ast(ast)
    
except Exception as e:
    print(f"\n[FAILED] Incompatibility detected: {e}")
    import traceback
    traceback.print_exc()
