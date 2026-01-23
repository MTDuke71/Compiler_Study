"""
Minimal Hand-Written Lexer
===========================

A complete lexer for a tiny language demonstrating core concepts:
- Token recognition with maximal munch
- Position tracking (line, column)
- Single-character lookahead
- Basic error handling

Supported tokens:
- Numbers: 42, 123
- Identifiers: x, foo, bar_123
- Keywords: if, else, while
- Operators: +, -, *, /, =, ==
"""

from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    
    # Special
    EOF = auto()
    ERROR = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
    value: any = None  # For numbers, the actual numeric value


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.token_start_pos = 0
        self.token_start_line = 1
        self.token_start_column = 1
        
    def current_char(self) -> str:
        """Get current character without advancing."""
        if self.position >= len(self.source):
            return '\0'
        return self.source[self.position]
    
    def peek(self, offset: int = 1) -> str:
        """Look ahead without consuming."""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Consume current character and return it."""
        if self.position >= len(self.source):
            return '\0'
        
        char = self.source[self.position]
        self.position += 1
        self.column += 1
        
        # Track newlines for accurate line/column
        if char == '\n':
            self.line += 1
            self.column = 1
            
        return char
    
    def skip_whitespace(self):
        """Consume whitespace without producing tokens."""
        while self.current_char() in ' \t\r\n':
            self.advance()
    
    def mark_token_start(self):
        """Remember where current token begins."""
        self.token_start_pos = self.position
        self.token_start_line = self.line
        self.token_start_column = self.column
    
    def make_token(self, type: TokenType, value=None) -> Token:
        """Create token from start position to current position."""
        lexeme = self.source[self.token_start_pos:self.position]
        return Token(
            type=type,
            lexeme=lexeme,
            line=self.token_start_line,
            column=self.token_start_column,
            value=value
        )
    
    def scan_number(self) -> Token:
        """Scan a numeric literal."""
        # Already positioned at first digit
        while self.current_char().isdigit():
            self.advance()
        
        lexeme = self.source[self.token_start_pos:self.position]
        value = int(lexeme)
        return self.make_token(TokenType.NUMBER, value)
    
    def scan_identifier(self) -> Token:
        """Scan identifier or keyword."""
        # Already positioned at first letter
        while self.current_char().isalnum() or self.current_char() == '_':
            self.advance()
        
        lexeme = self.source[self.token_start_pos:self.position]
        
        # Check if it's a keyword
        keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
        }
        
        type = keywords.get(lexeme, TokenType.IDENTIFIER)
        return self.make_token(type)
    
    def next_token(self) -> Token:
        """Scan and return the next token."""
        self.skip_whitespace()
        
        if self.position >= len(self.source):
            return Token(TokenType.EOF, '', self.line, self.column)
        
        self.mark_token_start()
        char = self.advance()
        
        # Single character tokens
        if char == '+':
            return self.make_token(TokenType.PLUS)
        elif char == '-':
            return self.make_token(TokenType.MINUS)
        elif char == '*':
            return self.make_token(TokenType.STAR)
        elif char == '/':
            return self.make_token(TokenType.SLASH)
        
        # Lookahead for ==
        elif char == '=':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.EQUAL_EQUAL)
            else:
                return self.make_token(TokenType.EQUAL)
        
        # Numbers
        elif char.isdigit():
            # Back up and rescan from start
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()  # Consume first digit again
            return self.scan_number()
        
        # Identifiers and keywords
        elif char.isalpha() or char == '_':
            # Back up and rescan from start
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()  # Consume first char again
            return self.scan_identifier()
        
        # Invalid character
        else:
            return self.make_token(TokenType.ERROR)
    
    def tokenize(self) -> list[Token]:
        """Scan entire input and return all tokens."""
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


def main():
    """Demonstrate basic lexer usage."""
    test_cases = [
        "if x == 42 + 7",
        "while y = 10 - 3",
        "foo = bar * 2",
        "if else while",  # All keywords
        "123 + 456",      # Numbers
        "x123y456",       # Identifier with numbers
        "=====",          # Multiple equals
        "@ # $",          # Invalid characters
    ]
    
    for source in test_cases:
        print(f"\nInput: {source!r}")
        print("-" * 60)
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            value_str = f" (value={token.value})" if token.value is not None else ""
            print(f"{token.type.name:15} {token.lexeme!r:10} @ {token.line}:{token.column}{value_str}")


if __name__ == "__main__":
    main()
