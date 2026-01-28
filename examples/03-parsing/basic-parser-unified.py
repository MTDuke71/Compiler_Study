"""
Basic Recursive Descent Parser - Expression Grammar
Week 5, Day 2 - January 27, 2026

Grammar:
    Expr   → Term (('+' | '-') Term)*
    Term   → Factor (('*' | '/') Factor)*
    Factor → INT | ID | '(' Expr ')'

This parser demonstrates:
- Mechanical grammar-to-code translation
- AST construction during parsing
- Left-associative operator handling
- Precedence via grammar stratification

NOW USES UNIFIED TOKEN TYPES - Compatible across all compiler phases!
"""

import sys
from pathlib import Path

# Add parent directory to path to import shared token_types
sys.path.insert(0, str(Path(__file__).parent.parent))
from token_types import Token, TokenType


class ParseError(Exception):
    """Raised when parsing fails"""
    pass


# ============================================================================
# AST Node Classes
# ============================================================================

class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, line, col):
        self.line = line
        self.col = col


class IntLiteral(ASTNode):
    """Integer literal: 42"""
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value
    
    def __repr__(self):
        return f"IntLiteral({self.value})"


class Identifier(ASTNode):
    """Variable reference: x"""
    def __init__(self, name, line, col):
        super().__init__(line, col)
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name!r})"


class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    def __init__(self, op, left, right, line, col):
        super().__init__(line, col)
        self.op = op
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.op!r}, {self.left}, {self.right})"


# ============================================================================
# Recursive Descent Parser
# ============================================================================

class RecursiveDescentParser:
    """
    Recursive descent parser for arithmetic expressions.
    
    Uses unified token_types.Token format for compatibility with all phases.
    
    Key methods:
        - match(*types): Check if current token matches any type (lookahead)
        - advance(): Consume token and move to next
        - expect(type): Match + advance, or error
        - parse_expr/term/factor(): Grammar production functions
    """
    
    def __init__(self, tokens, trace=False):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, None, '', 0, 0)
        self.trace = trace
        self.indent_level = 0
    
    def _trace(self, message):
        """Print trace message if tracing enabled"""
        if self.trace:
            indent = "  " * self.indent_level
            print(f"{indent}{message}")
    
    def match(self, *types):
        """Check if current token matches any of the given types"""
        return self.current_token.type in types
    
    def advance(self):
        """Consume current token and move to next"""
        self._trace(f"advance() consumed {self.current_token}")
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(TokenType.EOF, None, '', 0, 0)
    
    def expect(self, token_type):
        """Consume token if it matches, else raise error"""
        if not self.match(token_type):
            raise ParseError(
                f"Expected {token_type.name}, got {self.current_token.type.name} "
                f"at line {self.current_token.line}, col {self.current_token.column}"
            )
        self.advance()
    
    def error(self, message):
        """Report parse error with location"""
        raise ParseError(
            f"{message}\n"
            f"  at line {self.current_token.line}, col {self.current_token.column}\n"
            f"  got: {self.current_token.type.name} = {self.current_token.value!r}"
        )
    
    # Grammar production functions
    
    def parse_expr(self):
        """
        Expr → Term (('+' | '-') Term)*
        
        Handles addition and subtraction (lowest precedence).
        Builds left-associative tree via iteration.
        """
        self._trace("parse_expr() called")
        self.indent_level += 1
        
        # Parse first term
        left = self.parse_term()
        self._trace(f"parse_expr() got left term: {left}")
        
        # Parse remaining (op term) pairs
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.lexeme
            line, col = self.current_token.line, self.current_token.column
            self._trace(f"parse_expr() found operator: {op}")
            self.advance()
            
            right = self.parse_term()
            self._trace(f"parse_expr() got right term: {right}")
            
            # Build left-associative tree
            left = BinaryOp(op, left, right, line, col)
            self._trace(f"parse_expr() built: {left}")
        
        self.indent_level -= 1
        self._trace(f"parse_expr() returning: {left}")
        return left
    
    def parse_term(self):
        """
        Term → Factor (('*' | '/') Factor)*
        
        Handles multiplication and division (higher precedence).
        Builds left-associative tree via iteration.
        """
        self._trace("parse_term() called")
        self.indent_level += 1
        
        # Parse first factor
        left = self.parse_factor()
        self._trace(f"parse_term() got left factor: {left}")
        
        # Parse remaining (op factor) pairs
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.current_token.lexeme
            line, col = self.current_token.line, self.current_token.column
            self._trace(f"parse_term() found operator: {op}")
            self.advance()
            
            right = self.parse_factor()
            self._trace(f"parse_term() got right factor: {right}")
            
            # Build left-associative tree
            left = BinaryOp(op, left, right, line, col)
            self._trace(f"parse_term() built: {left}")
        
        self.indent_level -= 1
        self._trace(f"parse_term() returning: {left}")
        return left
    
    def parse_factor(self):
        """
        Factor → INT | ID | '(' Expr ')'
        
        Handles literals, identifiers, and parenthesized expressions.
        """
        self._trace("parse_factor() called")
        self.indent_level += 1
        
        # INT - integer literal
        if self.match(TokenType.NUMBER):
            token = self.current_token
            self._trace(f"parse_factor() found NUMBER: {token.value}")
            self.advance()
            result = IntLiteral(token.value, token.line, token.column)
            self.indent_level -= 1
            return result
        
        # ID - identifier
        if self.match(TokenType.IDENTIFIER):
            token = self.current_token
            self._trace(f"parse_factor() found IDENTIFIER: {token.lexeme}")
            self.advance()
            result = Identifier(token.lexeme, token.line, token.column)
            self.indent_level -= 1
            return result
        
        # '(' Expr ')' - parenthesized expression
        if self.match(TokenType.LPAREN):
            self._trace("parse_factor() found LPAREN, parsing subexpression")
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            self.indent_level -= 1
            return expr
        
        # Error - unexpected token
        self.indent_level -= 1
        self.error(f"Expected NUMBER, IDENTIFIER, or LPAREN")
    
    def parse(self):
        """Parse the entire input and return the AST"""
        ast = self.parse_expr()
        if not self.match(TokenType.EOF):
            self.error("Expected EOF after expression")
        return ast


# ============================================================================
# Simple Lexer (for standalone testing)
# ============================================================================

def simple_lexer(source):
    """
    Simple lexer for testing. Produces tokens in unified format.
    
    In real usage, you'd use the Week 4 lexer which already produces
    these tokens correctly!
    """
    tokens = []
    pos = 0
    line = 1
    col = 1
    
    while pos < len(source):
        ch = source[pos]
        
        # Skip whitespace
        if ch.isspace():
            if ch == '\n':
                line += 1
                col = 1
            else:
                col += 1
            pos += 1
            continue
        
        # Numbers
        if ch.isdigit():
            start_col = col
            num_str = ''
            while pos < len(source) and source[pos].isdigit():
                num_str += source[pos]
                pos += 1
                col += 1
            tokens.append(Token(TokenType.NUMBER, int(num_str), num_str, line, start_col))
            continue
        
        # Identifiers
        if ch.isalpha() or ch == '_':
            start_col = col
            ident = ''
            while pos < len(source) and (source[pos].isalnum() or source[pos] == '_'):
                ident += source[pos]
                pos += 1
                col += 1
            tokens.append(Token(TokenType.IDENTIFIER, None, ident, line, start_col))
            continue
        
        # Operators and punctuation
        start_col = col
        if ch == '+':
            tokens.append(Token(TokenType.PLUS, None, '+', line, start_col))
        elif ch == '-':
            tokens.append(Token(TokenType.MINUS, None, '-', line, start_col))
        elif ch == '*':
            tokens.append(Token(TokenType.STAR, None, '*', line, start_col))
        elif ch == '/':
            tokens.append(Token(TokenType.SLASH, None, '/', line, start_col))
        elif ch == '(':
            tokens.append(Token(TokenType.LPAREN, None, '(', line, start_col))
        elif ch == ')':
            tokens.append(Token(TokenType.RPAREN, None, ')', line, start_col))
        else:
            raise ValueError(f"Unexpected character '{ch}' at line {line}, col {col}")
        
        pos += 1
        col += 1
    
    tokens.append(Token(TokenType.EOF, None, '', line, col))
    return tokens


# ============================================================================
# AST Evaluator (for testing)
# ============================================================================

def evaluate(node, env=None):
    """Simple evaluator to test the AST"""
    if env is None:
        env = {}
    
    if isinstance(node, IntLiteral):
        return node.value
    
    if isinstance(node, Identifier):
        if node.name not in env:
            raise NameError(f"Undefined variable: {node.name}")
        return env[node.name]
    
    if isinstance(node, BinaryOp):
        left_val = evaluate(node.left, env)
        right_val = evaluate(node.right, env)
        
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val // right_val  # Integer division
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    
    raise TypeError(f"Unknown node type: {type(node)}")


# ============================================================================
# Test Suite
# ============================================================================

def run_tests():
    """Run comprehensive test suite"""
    tests = [
        # (input, expected_result, description)
        ("2 + 3", 5, "Simple addition"),
        ("5 - 2", 3, "Simple subtraction"),
        ("3 * 4", 12, "Simple multiplication"),
        ("8 / 2", 4, "Simple division"),
        
        # Precedence tests
        ("2 + 3 * 4", 14, "Multiplication has higher precedence than addition"),
        ("2 * 3 + 4", 10, "Multiplication before addition"),
        ("10 - 2 * 3", 4, "Multiplication before subtraction"),
        
        # Associativity tests
        ("5 - 3 - 1", 1, "Left-associative subtraction: (5-3)-1 = 1"),
        ("2 + 3 + 4", 9, "Left-associative addition"),
        ("16 / 4 / 2", 2, "Left-associative division: (16/4)/2 = 2"),
        
        # Parentheses tests
        ("(2 + 3) * 4", 20, "Parentheses override precedence"),
        ("2 * (3 + 4)", 14, "Parentheses create subexpression"),
        ("((2 + 3) * 4)", 20, "Nested parentheses"),
        ("(2 + 3) * (4 + 5)", 45, "Multiple parenthesized subexpressions"),
        
        # Complex expressions
        ("1 + 2 * 3 + 4", 11, "Mixed operators: 1 + (2*3) + 4"),
        ("(1 + 2) * (3 + 4)", 21, "Complex parentheses"),
        ("2 + 3 * 4 - 5", 9, "Three operators with precedence"),
    ]
    
    print("=" * 70)
    print("RUNNING PARSER TESTS")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for source, expected, description in tests:
        try:
            tokens = simple_lexer(source)
            parser = RecursiveDescentParser(tokens)
            ast = parser.parse()
            result = evaluate(ast)
            
            if result == expected:
                print(f"✓ {description}")
                print(f"  Input: {source}")
                print(f"  AST: {ast}")
                print(f"  Result: {result}")
                passed += 1
            else:
                print(f"✗ {description}")
                print(f"  Input: {source}")
                print(f"  Expected: {expected}, Got: {result}")
                print(f"  AST: {ast}")
                failed += 1
        except Exception as e:
            print(f"✗ {description}")
            print(f"  Input: {source}")
            print(f"  Error: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)


def test_with_identifiers():
    """Test parsing with variables"""
    print("\n" + "=" * 70)
    print("TESTING WITH IDENTIFIERS")
    print("=" * 70)
    
    tests = [
        ("x + y", {'x': 10, 'y': 20}, 30),
        ("a * b + c", {'a': 2, 'b': 3, 'c': 4}, 10),
        ("(x + y) * z", {'x': 1, 'y': 2, 'z': 3}, 9),
    ]
    
    for source, env, expected in tests:
        tokens = simple_lexer(source)
        parser = RecursiveDescentParser(tokens)
        ast = parser.parse()
        result = evaluate(ast, env)
        
        status = "✓" if result == expected else "✗"
        print(f"{status} {source} with {env} = {result}")


def test_with_trace():
    """Show execution trace for one example"""
    print("\n" + "=" * 70)
    print("EXECUTION TRACE EXAMPLE: 3 + 4 * 5")
    print("=" * 70)
    
    source = "3 + 4 * 5"
    tokens = simple_lexer(source)
    
    print(f"Source: {source}")
    print(f"Tokens: {[str(t) for t in tokens]}")
    print("\nParsing with trace enabled:\n")
    
    parser = RecursiveDescentParser(tokens, trace=True)
    ast = parser.parse()
    
    print(f"\nFinal AST: {ast}")
    print(f"Result: {evaluate(ast)}")


if __name__ == "__main__":
    run_tests()
    test_with_identifiers()
    test_with_trace()
