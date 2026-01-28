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
"""

# Token types
INT = 'INT'
ID = 'ID'
PLUS = 'PLUS'
MINUS = 'MINUS'
STAR = 'STAR'
SLASH = 'SLASH'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'


class Token:
    """Represents a single token from the lexer"""
    def __init__(self, type, value, line=1, col=0):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.col})"


class ParseError(Exception):
    """Raised when parsing fails"""
    pass


# ============================================================================
# AST Node Classes
# ============================================================================

class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, line=0, col=0):
        self.line = line
        self.col = col
    
    def __repr__(self):
        return self.__class__.__name__


class IntLiteral(ASTNode):
    """Integer literal: 42"""
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value
    
    def __repr__(self):
        return f"IntLiteral({self.value})"


class Identifier(ASTNode):
    """Variable name: x, foo, bar123"""
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
    
    Key methods:
        - match(type): Check if current token matches type (lookahead)
        - advance(): Consume token and move to next
        - expect(type): Match + advance, or error
        - parse_expr/term/factor(): Grammar production functions
    """
    
    def __init__(self, tokens, trace=False):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else Token(EOF, None, 0, 0)
        self.trace = trace
        self.indent_level = 0
    
    def _trace(self, message):
        """Print trace message if tracing enabled"""
        if self.trace:
            indent = "  " * self.indent_level
            print(f"{indent}{message}")
    
    def match(self, token_type):
        """Check if current token matches type without consuming"""
        return self.current_token.type == token_type
    
    def advance(self):
        """Consume current token and move to next"""
        self._trace(f"advance() consumed {self.current_token}")
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(EOF, None, 0, 0)
    
    def expect(self, token_type):
        """Consume token if it matches, else raise error"""
        if not self.match(token_type):
            raise ParseError(
                f"Expected {token_type}, got {self.current_token.type} "
                f"at line {self.current_token.line}, col {self.current_token.col}"
            )
        self.advance()
    
    def error(self, message):
        """Report parse error with location"""
        raise ParseError(
            f"{message}\n"
            f"  at line {self.current_token.line}, col {self.current_token.col}\n"
            f"  got: {self.current_token.type} = {self.current_token.value!r}"
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
        while self.match(PLUS) or self.match(MINUS):
            op = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
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
        while self.match(STAR) or self.match(SLASH):
            op = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
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
        
        Handles atoms (integers, identifiers) and parenthesized expressions.
        Parentheses allow nested expressions (recursion).
        """
        self._trace("parse_factor() called")
        self.indent_level += 1
        
        # Case 1: Integer literal
        if self.match(INT):
            value = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self._trace(f"parse_factor() found INT: {value}")
            self.advance()
            result = IntLiteral(value, line, col)
        
        # Case 2: Identifier
        elif self.match(ID):
            name = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self._trace(f"parse_factor() found ID: {name}")
            self.advance()
            result = Identifier(name, line, col)
        
        # Case 3: Parenthesized expression
        elif self.match(LPAREN):
            self._trace("parse_factor() found '('")
            self.advance()
            result = self.parse_expr()  # Recursion!
            self._trace("parse_factor() expecting ')'")
            self.expect(RPAREN)
        
        # Case 4: None of the above → error
        else:
            self.error("Expected factor (INT, ID, or '(')")
        
        self.indent_level -= 1
        self._trace(f"parse_factor() returning: {result}")
        return result
    
    def parse(self):
        """
        Entry point: parse expression and expect EOF.
        
        Returns:
            AST root node
        """
        self._trace("parse() called")
        self._trace(f"Tokens: {self.tokens}")
        ast = self.parse_expr()
        self.expect(EOF)
        self._trace(f"parse() complete, AST: {ast}")
        return ast


# ============================================================================
# Simple Lexer (for testing)
# ============================================================================

def tokenize(source):
    """
    Simple lexer for testing parser.
    Splits source into tokens.
    
    Note: This is a minimal lexer for demonstration.
    Production lexer would be more robust (see Week 4).
    """
    tokens = []
    i = 0
    line = 1
    col = 0
    
    while i < len(source):
        char = source[i]
        
        # Skip whitespace
        if char.isspace():
            if char == '\n':
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue
        
        # Integer literal
        if char.isdigit():
            start = i
            start_col = col
            while i < len(source) and source[i].isdigit():
                i += 1
                col += 1
            value = int(source[start:i])
            tokens.append(Token(INT, value, line, start_col))
            continue
        
        # Identifier
        if char.isalpha() or char == '_':
            start = i
            start_col = col
            while i < len(source) and (source[i].isalnum() or source[i] == '_'):
                i += 1
                col += 1
            name = source[start:i]
            tokens.append(Token(ID, name, line, start_col))
            continue
        
        # Single-character tokens
        token_map = {
            '+': PLUS,
            '-': MINUS,
            '*': STAR,
            '/': SLASH,
            '(': LPAREN,
            ')': RPAREN,
        }
        
        if char in token_map:
            tokens.append(Token(token_map[char], char, line, col))
            i += 1
            col += 1
            continue
        
        # Unknown character
        raise ParseError(f"Unknown character '{char}' at line {line}, col {col}")
    
    # Add EOF
    tokens.append(Token(EOF, None, line, col))
    return tokens


# ============================================================================
# AST Utilities
# ============================================================================

def print_ast(node, indent=0):
    """Pretty-print AST tree structure"""
    prefix = "  " * indent
    if isinstance(node, IntLiteral):
        print(f"{prefix}IntLiteral({node.value})")
    elif isinstance(node, Identifier):
        print(f"{prefix}Identifier({node.name!r})")
    elif isinstance(node, BinaryOp):
        print(f"{prefix}BinaryOp({node.op!r})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    else:
        print(f"{prefix}{node}")


def evaluate(node, env=None):
    """
    Evaluate AST (simple interpreter).
    
    Args:
        node: AST node to evaluate
        env: Environment (dict mapping variable names to values)
    
    Returns:
        Evaluation result (integer)
    """
    if env is None:
        env = {}
    
    if isinstance(node, IntLiteral):
        return node.value
    
    elif isinstance(node, Identifier):
        if node.name not in env:
            raise RuntimeError(f"Undefined variable: {node.name}")
        return env[node.name]
    
    elif isinstance(node, BinaryOp):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left // right  # Integer division
        else:
            raise RuntimeError(f"Unknown operator: {node.op}")
    
    else:
        raise RuntimeError(f"Unknown node type: {type(node)}")


# ============================================================================
# Test Cases
# ============================================================================

def run_test(source, expected_result=None, trace=False, env=None):
    """Run a single test case"""
    print(f"\n{'='*60}")
    print(f"Input: {source!r}")
    print(f"{'='*60}")
    
    # Tokenize
    tokens = tokenize(source)
    print(f"Tokens: {[str(t) for t in tokens]}")
    
    # Parse
    parser = RecursiveDescentParser(tokens, trace=trace)
    ast = parser.parse()
    
    print(f"\nAST:")
    print_ast(ast)
    
    # Evaluate
    if expected_result is not None:
        result = evaluate(ast, env)
        print(f"\nResult: {result}")
        print(f"Expected: {expected_result}")
        assert result == expected_result, f"Test failed: {result} != {expected_result}"
        print("✓ Test passed")
    
    return ast


def main():
    """Run all test cases"""
    print("Recursive Descent Parser - Test Suite")
    print("=" * 60)
    
    # Test 1: Simple addition
    run_test("3 + 5", expected_result=8)
    
    # Test 2: Precedence (multiplication before addition)
    run_test("2 + 3 * 4", expected_result=14)
    
    # Test 3: Precedence (another order)
    run_test("2 * 3 + 4", expected_result=10)
    
    # Test 4: Parentheses override precedence
    run_test("(2 + 3) * 4", expected_result=20)
    
    # Test 5: Left associativity
    run_test("5 - 3 - 1", expected_result=1)  # (5 - 3) - 1 = 1
    
    # Test 6: Complex expression
    run_test("1 + 2 * 3 + 4", expected_result=11)  # 1 + 6 + 4 = 11
    
    # Test 7: Identifiers
    run_test("x + y", env={'x': 10, 'y': 20}, expected_result=30)
    
    # Test 8: Mixed
    run_test("x * 2 + y", env={'x': 5, 'y': 3}, expected_result=13)  # 10 + 3
    
    # Test 9: Deeply nested
    run_test("((1 + 2) * (3 + 4))", expected_result=21)  # 3 * 7 = 21
    
    # Test 10: Division
    run_test("10 / 2 + 3", expected_result=8)  # 5 + 3 = 8
    
    print(f"\n{'='*60}")
    print("All tests passed! ✓")
    print(f"{'='*60}")
    
    # Demonstrate tracing
    print("\n\nDemonstrating execution trace for: '3 + 4 * 5'")
    print("=" * 60)
    run_test("3 + 4 * 5", expected_result=23, trace=True)


if __name__ == "__main__":
    main()
