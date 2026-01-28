"""
Unified token types for all compiler phases.

This module defines the token format used across lexing, parsing, and all
subsequent phases. Having a single source of truth prevents the need for
adapters or converters between phases.

Design decisions:
- Use Enum for type safety and IDE autocomplete
- Include both 'value' (parsed) and 'lexeme' (original text)
- Track source location (line, column) for error messages
- value is None for punctuation/keywords, actual value for literals
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """Token types for the expression language.
    
    This will be extended as we add more language features in later weeks:
    - Week 5: Expressions only (arithmetic, identifiers)
    - Week 6: Statements (if, while, return, etc.)
    - Week 7: Functions and declarations
    """
    # Literals
    NUMBER = auto()      # Integer or float literals
    IDENTIFIER = auto()  # Variable names
    STRING = auto()      # String literals (future)
    
    # Arithmetic operators
    PLUS = auto()        # +
    MINUS = auto()       # -
    STAR = auto()        # *
    SLASH = auto()       # /
    PERCENT = auto()     # % (modulo, future)
    
    # Comparison operators (future)
    EQUAL_EQUAL = auto()    # ==
    NOT_EQUAL = auto()      # !=
    LESS = auto()           # <
    LESS_EQUAL = auto()     # <=
    GREATER = auto()        # >
    GREATER_EQUAL = auto()  # >=
    
    # Logical operators (future)
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !
    
    # Grouping
    LPAREN = auto()      # (
    RPAREN = auto()      # )
    LBRACE = auto()      # { (future)
    RBRACE = auto()      # } (future)
    LBRACKET = auto()    # [ (future)
    RBRACKET = auto()    # ] (future)
    
    # Punctuation (future)
    SEMICOLON = auto()   # ;
    COMMA = auto()       # ,
    DOT = auto()         # .
    ASSIGN = auto()      # =
    
    # Keywords (future)
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    FUNCTION = auto()
    VAR = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()
    
    # Special
    EOF = auto()         # End of input
    ERROR = auto()       # Lexer error token


@dataclass
class Token:
    """A single token from the source code.
    
    Attributes:
        type: The token type (from TokenType enum)
        value: Parsed value (int for NUMBER, None for operators/keywords)
        lexeme: Original text from source code
        line: Line number (1-based)
        column: Column number (1-based)
    
    Examples:
        >>> Token(TokenType.NUMBER, 42, "42", 1, 1)
        >>> Token(TokenType.PLUS, None, "+", 1, 3)
        >>> Token(TokenType.IDENTIFIER, None, "foo", 2, 5)
    """
    type: TokenType
    value: Any
    lexeme: str
    line: int
    column: int
    
    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"
        return f"Token({self.type.name}, {self.line}:{self.column})"
    
    def is_type(self, *types):
        """Check if token matches any of the given types."""
        return self.type in types
    
    def is_literal(self):
        """Check if token is a literal value."""
        return self.type in (TokenType.NUMBER, TokenType.STRING, 
                            TokenType.TRUE, TokenType.FALSE, TokenType.NULL)
    
    def is_operator(self):
        """Check if token is an operator."""
        return self.type in (TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
                            TokenType.SLASH, TokenType.PERCENT,
                            TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL,
                            TokenType.LESS, TokenType.LESS_EQUAL,
                            TokenType.GREATER, TokenType.GREATER_EQUAL,
                            TokenType.AND, TokenType.OR, TokenType.NOT)
