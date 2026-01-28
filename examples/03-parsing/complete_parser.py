"""
Complete Recursive Descent Parser
==================================

Full-featured parser for a small programming language with:
- Expressions (stratified by precedence)
- Statements (if, while, return, var declarations, blocks)
- Functions (declarations and calls)
- Minimal scope tracking

Grammar:
--------
Program      → (FunctionDecl | Statement)*
FunctionDecl → 'fn' ID '(' ParamList? ')' Block
ParamList    → ID (',' ID)*

Statement    → VarDecl | IfStmt | WhileStmt | ReturnStmt | Block | ExprStmt
VarDecl      → 'var' ID ('=' Expression)? ';'
IfStmt       → 'if' '(' Expression ')' Statement ('else' Statement)?
WhileStmt    → 'while' '(' Expression ')' Statement
ReturnStmt   → 'return' Expression? ';'
Block        → '{' Statement* '}'
ExprStmt     → Expression ';'

Expression     → Assignment
Assignment     → LogicalOr ('=' Assignment)?
LogicalOr      → LogicalAnd ('||' LogicalAnd)*
LogicalAnd     → Equality ('&&' Equality)*
Equality       → Comparison (('==' | '!=') Comparison)*
Comparison     → Addition (('<' | '>' | '<=' | '>=') Addition)*
Addition       → Multiplication (('+' | '-') Multiplication)*
Multiplication → Unary (('*' | '/') Unary)*
Unary          → ('!' | '-') Unary | Primary
Primary        → INT | FLOAT | STRING | BOOL | ID | FunctionCall | '(' Expression ')'

FunctionCall → ID '(' ArgList? ')'
ArgList      → Expression (',' Expression)*

Usage:
------
from complete_parser import Parser, Lexer

code = '''
fn factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
'''

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print_ast(ast)
"""

import sys
import os
# Import unified token types
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from token_types import Token, TokenType

from dataclasses import dataclass
from typing import List, Optional, Any


# ============================================================================
# AST Node Types
# ============================================================================

# Expression nodes
@dataclass
class IntLiteral:
    value: int

@dataclass
class FloatLiteral:
    value: float

@dataclass
class StringLiteral:
    value: str

@dataclass
class BoolLiteral:
    value: bool

@dataclass
class Identifier:
    name: str

@dataclass
class BinaryOp:
    op: TokenType
    left: Any  # Expression
    right: Any  # Expression

@dataclass
class UnaryOp:
    op: TokenType
    operand: Any  # Expression

@dataclass
class Assignment:
    target: Any  # Expression (usually Identifier)
    value: Any  # Expression

@dataclass
class FunctionCall:
    name: str
    arguments: List[Any]  # List[Expression]


# Statement nodes
@dataclass
class VarDeclaration:
    name: str
    initializer: Optional[Any]  # Optional[Expression]

@dataclass
class ExpressionStatement:
    expression: Any  # Expression

@dataclass
class IfStatement:
    condition: Any  # Expression
    then_branch: Any  # Statement
    else_branch: Optional[Any]  # Optional[Statement]

@dataclass
class WhileStatement:
    condition: Any  # Expression
    body: Any  # Statement

@dataclass
class ReturnStatement:
    value: Optional[Any]  # Optional[Expression]

@dataclass
class Block:
    statements: List[Any]  # List[Statement]


# Program nodes
@dataclass
class FunctionDecl:
    name: str
    parameters: List[str]
    body: Block

@dataclass
class Program:
    declarations: List[Any]  # List[FunctionDecl | Statement]


# ============================================================================
# Lexer
# ============================================================================

class Lexer:
    """
    Simple lexer for our language.
    Tokenizes source code into token stream.
    """
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        self.keywords = {
            'var': TokenType.VAR,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN,
            'fn': TokenType.FUNCTION,  # Using unified FUNCTION
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }
    
    def current_char(self) -> Optional[str]:
        """Get current character without consuming"""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset=1) -> Optional[str]:
        """Look ahead at character"""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        """Consume current character"""
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self):
        """Skip whitespace and comments"""
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()
    
    def read_number(self) -> Token:
        """Read integer or float literal"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break  # Second dot, stop here
                is_float = True
            num_str += self.current_char()
            self.advance()
        
        value = float(num_str) if is_float else int(num_str)
        return Token(TokenType.NUMBER, value, num_str, start_line, start_col)
    
    def read_string(self) -> Token:
        """Read string literal"""
        start_line = self.line
        start_col = self.column
        
        opening_quote_pos = self.position - 1  # We already advanced past opening quote
        self.advance()  # Skip opening quote
        string = ''
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    string += '\n'
                elif self.current_char() == 't':
                    string += '\t'
                elif self.current_char() == '"':
                    string += '"'
                elif self.current_char() == '\\':
                    string += '\\'
                else:
                    string += self.current_char()
                self.advance()
            else:
                string += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()  # Skip closing quote
        
        # lexeme includes the quotes
        lexeme = self.source[opening_quote_pos:self.position]
        return Token(TokenType.STRING, string, lexeme, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        ident = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(ident, TokenType.IDENTIFIER)
        # Keywords and identifiers have None value per contract
        value = None
        
        return Token(token_type, value, ident, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize entire source code"""
        self.tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            ch = self.current_char()
            line = self.line
            col = self.column
            
            # Numbers
            if ch.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif ch == '"':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif ch.isalpha() or ch == '_':
                self.tokens.append(self.read_identifier())
            
            # Two-character operators
            elif ch == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL_EQUAL, None, '==', line, col))
                self.advance()
                self.advance()
            
            elif ch == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, None, '!=', line, col))
                self.advance()
                self.advance()
            
            elif ch == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, None, '<=', line, col))
                self.advance()
                self.advance()
            
            elif ch == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, None, '>=', line, col))
                self.advance()
                self.advance()
            
            elif ch == '&' and self.peek_char() == '&':
                self.tokens.append(Token(TokenType.AND, None, '&&', line, col))
                self.advance()
                self.advance()
            
            elif ch == '|' and self.peek_char() == '|':
                self.tokens.append(Token(TokenType.OR, None, '||', line, col))
                self.advance()
                self.advance()
            
            # Single-character operators and delimiters
            elif ch == '+':
                self.tokens.append(Token(TokenType.PLUS, None, '+', line, col))
                self.advance()
            elif ch == '-':
                self.tokens.append(Token(TokenType.MINUS, None, '-', line, col))
                self.advance()
            elif ch == '*':
                self.tokens.append(Token(TokenType.STAR, None, '*', line, col))
                self.advance()
            elif ch == '/':
                self.tokens.append(Token(TokenType.SLASH, None, '/', line, col))
                self.advance()
            elif ch == '!':
                self.tokens.append(Token(TokenType.NOT, None, '!', line, col))
                self.advance()
            elif ch == '=':
                self.tokens.append(Token(TokenType.ASSIGN, None, '=', line, col))
                self.advance()
            elif ch == '<':
                self.tokens.append(Token(TokenType.LESS, None, '<', line, col))
                self.advance()
            elif ch == '>':
                self.tokens.append(Token(TokenType.GREATER, None, '>', line, col))
                self.advance()
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, None, '(', line, col))
                self.advance()
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, None, ')', line, col))
                self.advance()
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, None, '{', line, col))
                self.advance()
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, None, '}', line, col))
                self.advance()
            elif ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, None, ';', line, col))
                self.advance()
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, None, ',', line, col))
                self.advance()
            else:
                raise Exception(f"Unexpected character '{ch}' at line {line}, column {col}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, '', self.line, self.column))
        
        return self.tokens


# ============================================================================
# Parser
# ============================================================================

class ParseError(Exception):
    """Parse error exception"""
    pass


class Parser:
    """
    Recursive descent parser for our language.
    Builds Abstract Syntax Tree from token stream.
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else Token(TokenType.EOF, None, '', 0, 0)
        self.scopes = [{}]  # Stack of scopes (for minimal tracking)
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    def at_end(self) -> bool:
        """Check if at end of token stream"""
        return self.current_token.type == TokenType.EOF
    
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of given types"""
        return self.current_token.type in types
    
    def advance(self) -> Token:
        """Consume current token and move to next"""
        prev_token = self.current_token
        if not self.at_end():
            self.position += 1
            self.current_token = self.tokens[self.position]
        return prev_token
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume token of expected type, or raise error"""
        if not self.match(token_type):
            self.error(f"Expected {token_type.name}, got {self.current_token.type.name}")
        return self.advance()
    
    def error(self, message: str):
        """Raise parse error with context"""
        raise ParseError(
            f"Parse error at line {self.current_token.line}, "
            f"column {self.current_token.column}: {message}"
        )
    
    # ========================================================================
    # Scope Tracking (Minimal)
    # ========================================================================
    
    def enter_scope(self):
        """Enter new block scope"""
        self.scopes.append({})
    
    def exit_scope(self):
        """Exit current block scope"""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def declare_variable(self, name: str):
        """Declare variable in current scope"""
        if name in self.scopes[-1]:
            self.error(f"Variable '{name}' already declared in this scope")
        self.scopes[-1][name] = True
    
    # ========================================================================
    # Entry Point
    # ========================================================================
    
    def parse(self) -> Program:
        """
        Program → (FunctionDecl | Statement)*
        
        Parse entire program.
        """
        declarations = []
        
        while not self.at_end():
            if self.match(TokenType.FUNCTION):
                declarations.append(self.parse_function_decl())
            else:
                declarations.append(self.parse_statement())
        
        return Program(declarations)
    
    # ========================================================================
    # Function Parsing
    # ========================================================================
    
    def parse_function_decl(self) -> FunctionDecl:
        """
        FunctionDecl → 'fn' ID '(' ParamList? ')' Block
        ParamList → ID (',' ID)*
        """
        self.expect(TokenType.FUNCTION)
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.lexeme  # Use lexeme per contract
        
        self.expect(TokenType.LPAREN)
        
        # Parse parameter list
        parameters = []
        if not self.match(TokenType.RPAREN):
            param_token = self.expect(TokenType.IDENTIFIER)
            parameters.append(param_token.lexeme)
            while self.match(TokenType.COMMA):
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                parameters.append(param_token.lexeme)
        
        self.expect(TokenType.RPAREN)
        
        # Function body (always a block)
        body = self.parse_block()
        
        return FunctionDecl(name, parameters, body)
    
    def parse_function_call(self, name: str) -> FunctionCall:
        """
        FunctionCall → ID '(' ArgList? ')'
        ArgList → Expression (',' Expression)*
        
        Called from parse_primary when we've seen ID '('.
        """
        self.expect(TokenType.LPAREN)
        
        # Parse argument list
        arguments = []
        if not self.match(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        
        return FunctionCall(name, arguments)
    
    # ========================================================================
    # Statement Parsing
    # ========================================================================
    
    def parse_statement(self):
        """
        Statement → VarDecl | IfStmt | WhileStmt | ReturnStmt | Block | ExprStmt
        
        Dispatcher: Look at first token to determine statement type.
        """
        if self.match(TokenType.VAR):
            return self.parse_var_declaration()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_block()
        else:
            return self.parse_expression_statement()
    
    def parse_var_declaration(self) -> VarDeclaration:
        """
        VarDecl → 'var' ID ('=' Expression)? ';'
        """
        self.expect(TokenType.VAR)
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.lexeme  # Use lexeme per contract
        
        # Track declaration in current scope
        self.declare_variable(name)
        
        # Optional initializer
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        
        return VarDeclaration(name, initializer)
    
    def parse_if_statement(self) -> IfStatement:
        """
        IfStmt → 'if' '(' Expression ')' Statement ('else' Statement)?
        """
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        
        condition = self.parse_expression()
        
        self.expect(TokenType.RPAREN)
        
        then_branch = self.parse_statement()
        
        # Optional else clause
        else_branch = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_branch = self.parse_statement()
        
        return IfStatement(condition, then_branch, else_branch)
    
    def parse_while_statement(self) -> WhileStatement:
        """
        WhileStmt → 'while' '(' Expression ')' Statement
        """
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        
        condition = self.parse_expression()
        
        self.expect(TokenType.RPAREN)
        
        body = self.parse_statement()
        
        return WhileStatement(condition, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        """
        ReturnStmt → 'return' Expression? ';'
        """
        self.expect(TokenType.RETURN)
        
        # Optional return value
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        
        return ReturnStatement(value)
    
    def parse_block(self) -> Block:
        """
        Block → '{' Statement* '}'
        
        Creates new scope.
        """
        self.expect(TokenType.LBRACE)
        
        # Enter new scope
        self.enter_scope()
        
        statements = []
        while not self.match(TokenType.RBRACE) and not self.at_end():
            statements.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE)
        
        # Exit scope
        self.exit_scope()
        
        return Block(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        """
        ExprStmt → Expression ';'
        """
        expr = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    # ========================================================================
    # Expression Parsing (Stratified by Precedence)
    # ========================================================================
    
    def parse_expression(self):
        """
        Expression → Assignment
        
        Entry point for expression parsing.
        """
        return self.parse_assignment()
    
    def parse_assignment(self):
        """
        Assignment → LogicalOr ('=' Assignment)?
        
        Right-associative: x = y = 3 means x = (y = 3)
        """
        node = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            # Right recursion for right associativity
            value = self.parse_assignment()
            node = Assignment(node, value)
        
        return node
    
    def parse_logical_or(self):
        """
        LogicalOr → LogicalAnd ('||' LogicalAnd)*
        
        Left-associative via loop.
        """
        node = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            op = self.current_token.type
            self.advance()
            right = self.parse_logical_and()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_logical_and(self):
        """
        LogicalAnd → Equality ('&&' Equality)*
        """
        node = self.parse_equality()
        
        while self.match(TokenType.AND):
            op = self.current_token.type
            self.advance()
            right = self.parse_equality()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_equality(self):
        """
        Equality → Comparison (('==' | '!=') Comparison)*
        """
        node = self.parse_comparison()
        
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            op = self.current_token.type
            self.advance()
            right = self.parse_comparison()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_comparison(self):
        """
        Comparison → Addition (('<' | '>' | '<=' | '>=') Addition)*
        """
        node = self.parse_addition()
        
        while self.match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            op = self.current_token.type
            self.advance()
            right = self.parse_addition()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_addition(self):
        """
        Addition → Multiplication (('+' | '-') Multiplication)*
        """
        node = self.parse_multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.advance()
            right = self.parse_multiplication()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_multiplication(self):
        """
        Multiplication → Unary (('*' | '/') Unary)*
        """
        node = self.parse_unary()
        
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.current_token.type
            self.advance()
            right = self.parse_unary()
            node = BinaryOp(op, node, right)
        
        return node
    
    def parse_unary(self):
        """
        Unary → ('!' | '-') Unary | Primary
        
        Right-associative via recursion.
        """
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.current_token.type
            self.advance()
            operand = self.parse_unary()  # Right recursion
            return UnaryOp(op, operand)
        
        return self.parse_primary()
    
    def parse_primary(self):
        """
        Primary → Literal | Identifier | FunctionCall | '(' Expression ')'
        Literal → INT | FLOAT | STRING | BOOL
        """
        # Number literal (int or float)
        if self.match(TokenType.NUMBER):
            value = self.current_token.value
            self.advance()
            # Check if it's int or float
            if isinstance(value, int):
                return IntLiteral(value)
            else:
                return FloatLiteral(value)
        
        # String literal
        if self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
        
        # Boolean literals
        if self.match(TokenType.TRUE):
            self.advance()
            return BoolLiteral(True)
        
        if self.match(TokenType.FALSE):
            self.advance()
            return BoolLiteral(False)
        
        # Identifier or function call
        if self.match(TokenType.IDENTIFIER):
            name = self.current_token.lexeme  # Use lexeme per contract
            self.advance()
            
            # Check for function call (LL(2) - look ahead 1 token)
            if self.match(TokenType.LPAREN):
                return self.parse_function_call(name)
            else:
                return Identifier(name)
        
        # Grouping
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()  # Full recursion
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Expected expression, got {self.current_token.type.name}")


# ============================================================================
# AST Printer (for debugging)
# ============================================================================

def print_ast(node, indent=0):
    """Pretty-print AST for debugging"""
    prefix = "  " * indent
    
    if isinstance(node, Program):
        print(f"{prefix}Program")
        for decl in node.declarations:
            print_ast(decl, indent + 1)
    
    elif isinstance(node, FunctionDecl):
        print(f"{prefix}FunctionDecl: {node.name}")
        print(f"{prefix}  Parameters: {node.parameters}")
        print(f"{prefix}  Body:")
        print_ast(node.body, indent + 2)
    
    elif isinstance(node, Block):
        print(f"{prefix}Block")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    
    elif isinstance(node, VarDeclaration):
        print(f"{prefix}VarDeclaration: {node.name}")
        if node.initializer:
            print(f"{prefix}  Initializer:")
            print_ast(node.initializer, indent + 2)
    
    elif isinstance(node, IfStatement):
        print(f"{prefix}IfStatement")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Then:")
        print_ast(node.then_branch, indent + 2)
        if node.else_branch:
            print(f"{prefix}  Else:")
            print_ast(node.else_branch, indent + 2)
    
    elif isinstance(node, WhileStatement):
        print(f"{prefix}WhileStatement")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        print_ast(node.body, indent + 2)
    
    elif isinstance(node, ReturnStatement):
        print(f"{prefix}ReturnStatement")
        if node.value:
            print_ast(node.value, indent + 1)
    
    elif isinstance(node, ExpressionStatement):
        print(f"{prefix}ExpressionStatement")
        print_ast(node.expression, indent + 1)
    
    elif isinstance(node, Assignment):
        print(f"{prefix}Assignment")
        print(f"{prefix}  Target:")
        print_ast(node.target, indent + 2)
        print(f"{prefix}  Value:")
        print_ast(node.value, indent + 2)
    
    elif isinstance(node, BinaryOp):
        print(f"{prefix}BinaryOp: {node.op.name}")
        print(f"{prefix}  Left:")
        print_ast(node.left, indent + 2)
        print(f"{prefix}  Right:")
        print_ast(node.right, indent + 2)
    
    elif isinstance(node, UnaryOp):
        print(f"{prefix}UnaryOp: {node.op.name}")
        print_ast(node.operand, indent + 1)
    
    elif isinstance(node, FunctionCall):
        print(f"{prefix}FunctionCall: {node.name}")
        print(f"{prefix}  Arguments:")
        for arg in node.arguments:
            print_ast(arg, indent + 2)
    
    elif isinstance(node, IntLiteral):
        print(f"{prefix}IntLiteral: {node.value}")
    
    elif isinstance(node, FloatLiteral):
        print(f"{prefix}FloatLiteral: {node.value}")
    
    elif isinstance(node, StringLiteral):
        print(f"{prefix}StringLiteral: \"{node.value}\"")
    
    elif isinstance(node, BoolLiteral):
        print(f"{prefix}BoolLiteral: {node.value}")
    
    elif isinstance(node, Identifier):
        print(f"{prefix}Identifier: {node.name}")
    
    else:
        print(f"{prefix}Unknown node: {type(node)}")


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example program
    code = '''
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
    '''
    
    print("Source code:")
    print(code)
    print("\n" + "="*70 + "\n")
    
    # Lex
    print("Lexing...")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"Generated {len(tokens)} tokens\n")
    
    # Parse
    print("Parsing...")
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parse successful!\n")
    
    print("="*70)
    print("Abstract Syntax Tree:")
    print("="*70)
    print_ast(ast)
