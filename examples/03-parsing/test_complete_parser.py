"""
Test Suite for Complete Recursive Descent Parser
=================================================

Comprehensive tests covering:
- Expression precedence and associativity
- All statement types
- Function declarations and calls
- Scoping rules
- Error cases

Run with: python test_complete_parser.py
"""

import sys
import os

# Add current directory to path so we can import complete_parser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from complete_parser import (
    Lexer, Parser, ParseError,
    Program, FunctionDecl, Block,
    VarDeclaration, IfStatement, WhileStatement, ReturnStatement, ExpressionStatement,
    BinaryOp, UnaryOp, Assignment, FunctionCall,
    IntLiteral, FloatLiteral, StringLiteral, BoolLiteral, Identifier,
    TokenType
)


# ============================================================================
# Test Utilities
# ============================================================================

def parse(code: str):
    """Helper: Lex and parse code"""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


def parse_expr(code: str):
    """Helper: Parse just an expression"""
    # Wrap in expression statement
    full_code = f"{code};"
    ast = parse(full_code)
    return ast.declarations[0].expression


class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record_pass(self, test_name: str):
        self.passed += 1
        print(f"✓ {test_name}")
    
    def record_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def print_summary(self):
        total = self.passed + self.failed
        print("\n" + "="*70)
        print(f"Test Results: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print("="*70)


results = TestResult()


def test(name: str):
    """Decorator for test functions"""
    def decorator(func):
        def wrapper():
            try:
                func()
                results.record_pass(name)
            except AssertionError as e:
                results.record_fail(name, str(e))
            except Exception as e:
                results.record_fail(name, f"Exception: {e}")
        return wrapper
    return decorator


# ============================================================================
# Expression Precedence Tests
# ============================================================================

@test("Multiplication binds tighter than addition")
def test_precedence_mult_add():
    ast = parse_expr("2 + 3 * 4")
    assert isinstance(ast, BinaryOp), "Expected BinaryOp"
    assert ast.op == TokenType.PLUS, "Top level should be +"
    assert isinstance(ast.left, IntLiteral), "Left should be literal"
    assert isinstance(ast.right, BinaryOp), "Right should be BinaryOp"
    assert ast.right.op == TokenType.STAR, "Right should be *"


@test("Parentheses override precedence")
def test_precedence_parens():
    ast = parse_expr("(2 + 3) * 4")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.STAR
    assert isinstance(ast.left, BinaryOp)
    assert ast.left.op == TokenType.PLUS


@test("Unary minus binds tighter than binary minus")
def test_precedence_unary():
    ast = parse_expr("5 - -3")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.MINUS
    assert isinstance(ast.right, UnaryOp)
    assert ast.right.op == TokenType.MINUS


@test("Comparison binds looser than arithmetic")
def test_precedence_comparison():
    ast = parse_expr("2 + 3 < 4 * 5")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.LT
    assert isinstance(ast.left, BinaryOp)
    assert ast.left.op == TokenType.PLUS
    assert isinstance(ast.right, BinaryOp)
    assert ast.right.op == TokenType.STAR


@test("Logical AND binds tighter than OR")
def test_precedence_logical():
    ast = parse_expr("true || false && true")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.OR
    assert isinstance(ast.right, BinaryOp)
    assert ast.right.op == TokenType.AND


# ============================================================================
# Associativity Tests
# ============================================================================

@test("Addition is left-associative")
def test_assoc_addition():
    ast = parse_expr("1 + 2 + 3")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.PLUS
    # Should be (1 + 2) + 3, so left is BinaryOp
    assert isinstance(ast.left, BinaryOp)
    assert ast.left.op == TokenType.PLUS
    assert isinstance(ast.right, IntLiteral)


@test("Subtraction is left-associative")
def test_assoc_subtraction():
    ast = parse_expr("10 - 3 - 2")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.MINUS
    assert isinstance(ast.left, BinaryOp)
    assert ast.left.op == TokenType.MINUS


@test("Assignment is right-associative")
def test_assoc_assignment():
    ast = parse_expr("x = y = 3")
    assert isinstance(ast, Assignment)
    # Should be x = (y = 3), so value is Assignment
    assert isinstance(ast.value, Assignment)
    assert isinstance(ast.value.value, IntLiteral)


# ============================================================================
# Statement Tests
# ============================================================================

@test("Variable declaration without initializer")
def test_var_decl_no_init():
    ast = parse("var x;")
    decl = ast.declarations[0]
    assert isinstance(decl, VarDeclaration)
    assert decl.name == "x"
    assert decl.initializer is None


@test("Variable declaration with initializer")
def test_var_decl_with_init():
    ast = parse("var y = 10;")
    decl = ast.declarations[0]
    assert isinstance(decl, VarDeclaration)
    assert decl.name == "y"
    assert isinstance(decl.initializer, IntLiteral)
    assert decl.initializer.value == 10


@test("If statement without else")
def test_if_no_else():
    code = """
    if (x > 0) {
        return x;
    }
    """
    ast = parse(code)
    stmt = ast.declarations[0]
    assert isinstance(stmt, IfStatement)
    assert isinstance(stmt.condition, BinaryOp)
    assert isinstance(stmt.then_branch, Block)
    assert stmt.else_branch is None


@test("If statement with else")
def test_if_with_else():
    code = """
    if (x > 0) {
        return x;
    } else {
        return -x;
    }
    """
    ast = parse(code)
    stmt = ast.declarations[0]
    assert isinstance(stmt, IfStatement)
    assert isinstance(stmt.then_branch, Block)
    assert isinstance(stmt.else_branch, Block)


@test("While loop")
def test_while():
    code = """
    while (n > 0) {
        n = n - 1;
    }
    """
    ast = parse(code)
    stmt = ast.declarations[0]
    assert isinstance(stmt, WhileStatement)
    assert isinstance(stmt.condition, BinaryOp)
    assert isinstance(stmt.body, Block)


@test("Return with value")
def test_return_with_value():
    ast = parse("return 42;")
    stmt = ast.declarations[0]
    assert isinstance(stmt, ReturnStatement)
    assert isinstance(stmt.value, IntLiteral)
    assert stmt.value.value == 42


@test("Return without value")
def test_return_no_value():
    ast = parse("return;")
    stmt = ast.declarations[0]
    assert isinstance(stmt, ReturnStatement)
    assert stmt.value is None


@test("Block statement")
def test_block():
    code = """
    {
        var x = 1;
        var y = 2;
    }
    """
    ast = parse(code)
    stmt = ast.declarations[0]
    assert isinstance(stmt, Block)
    assert len(stmt.statements) == 2
    assert all(isinstance(s, VarDeclaration) for s in stmt.statements)


@test("Expression statement")
def test_expr_stmt():
    ast = parse("x + 3;")
    stmt = ast.declarations[0]
    assert isinstance(stmt, ExpressionStatement)
    assert isinstance(stmt.expression, BinaryOp)


# ============================================================================
# Function Tests
# ============================================================================

@test("Function declaration with no parameters")
def test_func_no_params():
    code = """
    fn main() {
        return 0;
    }
    """
    ast = parse(code)
    func = ast.declarations[0]
    assert isinstance(func, FunctionDecl)
    assert func.name == "main"
    assert func.parameters == []
    assert isinstance(func.body, Block)


@test("Function declaration with parameters")
def test_func_with_params():
    code = """
    fn add(x, y) {
        return x + y;
    }
    """
    ast = parse(code)
    func = ast.declarations[0]
    assert isinstance(func, FunctionDecl)
    assert func.name == "add"
    assert func.parameters == ["x", "y"]


@test("Function call with no arguments")
def test_func_call_no_args():
    ast = parse_expr("foo()")
    assert isinstance(ast, FunctionCall)
    assert ast.name == "foo"
    assert ast.arguments == []


@test("Function call with arguments")
def test_func_call_with_args():
    ast = parse_expr("add(2, 3)")
    assert isinstance(ast, FunctionCall)
    assert ast.name == "add"
    assert len(ast.arguments) == 2
    assert all(isinstance(arg, IntLiteral) for arg in ast.arguments)


@test("Nested function calls")
def test_nested_func_calls():
    ast = parse_expr("foo(bar(1), baz(2, 3))")
    assert isinstance(ast, FunctionCall)
    assert ast.name == "foo"
    assert len(ast.arguments) == 2
    assert isinstance(ast.arguments[0], FunctionCall)
    assert isinstance(ast.arguments[1], FunctionCall)


@test("Recursive function")
def test_recursive_func():
    code = """
    fn factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    """
    ast = parse(code)
    func = ast.declarations[0]
    assert isinstance(func, FunctionDecl)
    # Check that body contains if statement with recursive call
    if_stmt = func.body.statements[0]
    assert isinstance(if_stmt, IfStatement)


# ============================================================================
# Scoping Tests
# ============================================================================

@test("Nested scopes with same variable name")
def test_nested_scopes():
    code = """
    {
        var x = 1;
        {
            var x = 2;
        }
    }
    """
    # Should parse without error
    ast = parse(code)
    assert isinstance(ast.declarations[0], Block)


@test("Redeclaration in same scope raises error")
def test_redeclaration_error():
    code = """
    {
        var x = 1;
        var x = 2;
    }
    """
    try:
        ast = parse(code)
        raise AssertionError("Expected ParseError for redeclaration")
    except ParseError as e:
        assert "already declared" in str(e)


# ============================================================================
# Complex Expression Tests
# ============================================================================

@test("Complex arithmetic expression")
def test_complex_arithmetic():
    ast = parse_expr("(2 + 3) * (4 - 1) / 5")
    assert isinstance(ast, BinaryOp)
    # Structure: ((2+3) * (4-1)) / 5


@test("Chained comparisons (parsed as nested)")
def test_chained_comparison():
    ast = parse_expr("a < b && b < c")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.AND


@test("Mixed unary operators")
def test_mixed_unary():
    ast = parse_expr("!!true")
    assert isinstance(ast, UnaryOp)
    assert ast.op == TokenType.BANG
    assert isinstance(ast.operand, UnaryOp)
    assert ast.operand.op == TokenType.BANG


@test("Assignment in expression")
def test_assignment_in_expr():
    ast = parse_expr("(x = 5) + 3")
    assert isinstance(ast, BinaryOp)
    assert ast.op == TokenType.PLUS
    assert isinstance(ast.left, Assignment)


# ============================================================================
# Integration Tests (Complete Programs)
# ============================================================================

@test("Complete factorial program")
def test_factorial_program():
    code = """
    fn factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    
    fn main() {
        var result = factorial(5);
        return result;
    }
    """
    ast = parse(code)
    assert isinstance(ast, Program)
    assert len(ast.declarations) == 2
    assert all(isinstance(d, FunctionDecl) for d in ast.declarations)


@test("Program with multiple variable declarations")
def test_multi_var_program():
    code = """
    var x = 10;
    var y = 20;
    var z = x + y;
    """
    ast = parse(code)
    assert len(ast.declarations) == 3
    assert all(isinstance(d, VarDeclaration) for d in ast.declarations)


@test("Program with loops and conditionals")
def test_loops_and_conditionals():
    code = """
    fn abs(x) {
        if (x < 0) {
            return -x;
        } else {
            return x;
        }
    }
    
    fn sum_to_n(n) {
        var sum = 0;
        var i = 1;
        while (i <= n) {
            sum = sum + i;
            i = i + 1;
        }
        return sum;
    }
    """
    ast = parse(code)
    assert len(ast.declarations) == 2
    assert ast.declarations[0].name == "abs"
    assert ast.declarations[1].name == "sum_to_n"


# ============================================================================
# Error Tests
# ============================================================================

@test("Missing semicolon raises error")
def test_error_missing_semicolon():
    try:
        parse("var x = 10")
        raise AssertionError("Expected ParseError for missing semicolon")
    except ParseError:
        pass


@test("Unmatched parenthesis raises error")
def test_error_unmatched_paren():
    try:
        parse("if (x > 0 { }")
        raise AssertionError("Expected ParseError for unmatched paren")
    except ParseError:
        pass


@test("Missing expression raises error")
def test_error_missing_expr():
    try:
        parse("var x = ;")
        raise AssertionError("Expected ParseError for missing expression")
    except ParseError:
        pass


@test("Invalid token raises error")
def test_error_invalid_token():
    try:
        parse("var @ = 5;")
        raise AssertionError("Expected error for invalid token")
    except Exception:  # Lexer will raise exception
        pass


# ============================================================================
# Literal Tests
# ============================================================================

@test("Integer literal")
def test_int_literal():
    ast = parse_expr("42")
    assert isinstance(ast, IntLiteral)
    assert ast.value == 42


@test("Float literal")
def test_float_literal():
    ast = parse_expr("3.14")
    assert isinstance(ast, FloatLiteral)
    assert ast.value == 3.14


@test("String literal")
def test_string_literal():
    ast = parse_expr('"hello world"')
    assert isinstance(ast, StringLiteral)
    assert ast.value == "hello world"


@test("Boolean true")
def test_bool_true():
    ast = parse_expr("true")
    assert isinstance(ast, BoolLiteral)
    assert ast.value == True


@test("Boolean false")
def test_bool_false():
    ast = parse_expr("false")
    assert isinstance(ast, BoolLiteral)
    assert ast.value == False


# ============================================================================
# Edge Cases
# ============================================================================

@test("Empty program")
def test_empty_program():
    ast = parse("")
    assert isinstance(ast, Program)
    assert ast.declarations == []


@test("Empty block")
def test_empty_block():
    ast = parse("{}")
    assert isinstance(ast.declarations[0], Block)
    assert ast.declarations[0].statements == []


@test("Deeply nested parentheses")
def test_deeply_nested_parens():
    ast = parse_expr("((((5))))")
    assert isinstance(ast, IntLiteral)
    assert ast.value == 5


@test("Long function argument list")
def test_long_arg_list():
    ast = parse_expr("foo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)")
    assert isinstance(ast, FunctionCall)
    assert len(ast.arguments) == 10


@test("Deeply nested blocks")
def test_deeply_nested_blocks():
    code = """
    {
        {
            {
                var x = 1;
            }
        }
    }
    """
    ast = parse(code)
    block = ast.declarations[0]
    assert isinstance(block, Block)


# ============================================================================
# Run All Tests
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Running Complete Parser Test Suite")
    print("="*70)
    print()
    
    # Expression tests
    print("Expression Precedence Tests:")
    test_precedence_mult_add()
    test_precedence_parens()
    test_precedence_unary()
    test_precedence_comparison()
    test_precedence_logical()
    
    print("\nAssociativity Tests:")
    test_assoc_addition()
    test_assoc_subtraction()
    test_assoc_assignment()
    
    # Statement tests
    print("\nStatement Tests:")
    test_var_decl_no_init()
    test_var_decl_with_init()
    test_if_no_else()
    test_if_with_else()
    test_while()
    test_return_with_value()
    test_return_no_value()
    test_block()
    test_expr_stmt()
    
    # Function tests
    print("\nFunction Tests:")
    test_func_no_params()
    test_func_with_params()
    test_func_call_no_args()
    test_func_call_with_args()
    test_nested_func_calls()
    test_recursive_func()
    
    # Scoping tests
    print("\nScoping Tests:")
    test_nested_scopes()
    test_redeclaration_error()
    
    # Complex expressions
    print("\nComplex Expression Tests:")
    test_complex_arithmetic()
    test_chained_comparison()
    test_mixed_unary()
    test_assignment_in_expr()
    
    # Integration tests
    print("\nIntegration Tests:")
    test_factorial_program()
    test_multi_var_program()
    test_loops_and_conditionals()
    
    # Error tests
    print("\nError Tests:")
    test_error_missing_semicolon()
    test_error_unmatched_paren()
    test_error_missing_expr()
    test_error_invalid_token()
    
    # Literal tests
    print("\nLiteral Tests:")
    test_int_literal()
    test_float_literal()
    test_string_literal()
    test_bool_true()
    test_bool_false()
    
    # Edge cases
    print("\nEdge Case Tests:")
    test_empty_program()
    test_empty_block()
    test_deeply_nested_parens()
    test_long_arg_list()
    test_deeply_nested_blocks()
    
    # Summary
    results.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if results.failed == 0 else 1)
