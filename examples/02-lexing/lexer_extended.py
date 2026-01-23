"""
Extended Hand-Written Lexer
============================

Extends the minimal lexer with:
- String literals with escape sequences (\n, \t, \\, \")
- Floating-point numbers (3.14, 1e10, 2.5e-3)
- Line comments (//)
- Block comments (/* ... */)
- Additional operators (>, >=, <, <=, !=)

This demonstrates:
- Bounded and unbounded lookahead
- Error recovery (unterminated strings/comments)
- Escape sequence processing
- Multiple token types requiring similar patterns
"""

from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Literals
    NUMBER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    
    # Punctuation
    SEMICOLON = auto()
    
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
    value: any = None


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
        
        if char == '\n':
            self.line += 1
            self.column = 1
            
        return char
    
    def skip_whitespace(self):
        """Consume whitespace without producing tokens."""
        while self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_line_comment(self):
        """Consume line comment (//)."""
        # '//' already consumed
        while self.current_char() not in '\n\0':
            self.advance()
    
    def skip_block_comment(self) -> bool:
        """Consume block comment (/* ... */). Returns False if unterminated."""
        # '/*' already consumed
        
        while True:
            if self.current_char() == '\0':
                return False  # Unterminated
            
            if self.current_char() == '*' and self.peek(1) == '/':
                self.advance()  # Consume '*'
                self.advance()  # Consume '/'
                return True
            
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
    
    def scan_string(self) -> Token:
        """Scan a string literal with escape sequences."""
        # Opening " already consumed
        chars = []
        
        while True:
            char = self.current_char()
            
            # End of input before closing quote
            if char == '\0':
                return Token(
                    type=TokenType.ERROR,
                    lexeme='unterminated string',
                    line=self.token_start_line,
                    column=self.token_start_column
                )
            
            # Closing quote
            if char == '"':
                self.advance()
                break
            
            # Escape sequence
            if char == '\\':
                self.advance()
                next_char = self.current_char()
                
                if next_char == 'n':
                    chars.append('\n')
                elif next_char == 't':
                    chars.append('\t')
                elif next_char == '\\':
                    chars.append('\\')
                elif next_char == '"':
                    chars.append('"')
                else:
                    # Invalid escape - just include backslash and char
                    chars.append('\\')
                    chars.append(next_char)
                
                self.advance()
            else:
                # Regular character
                chars.append(char)
                self.advance()
        
        value = ''.join(chars)
        return self.make_token(TokenType.STRING, value)
    
    def scan_number(self) -> Token:
        """Scan numeric literal (integer or float)."""
        is_float = False
        
        # Integer part
        while self.current_char().isdigit():
            self.advance()
        
        # Decimal part
        if self.current_char() == '.' and self.peek(1).isdigit():
            is_float = True
            self.advance()  # Consume '.'
            while self.current_char().isdigit():
                self.advance()
        
        # Exponent part
        if self.current_char() in 'eE':
            is_float = True
            self.advance()
            
            # Optional sign
            if self.current_char() in '+-':
                self.advance()
            
            # Exponent digits
            if not self.current_char().isdigit():
                return self.make_token(TokenType.ERROR)  # Malformed exponent
            
            while self.current_char().isdigit():
                self.advance()
        
        lexeme = self.source[self.token_start_pos:self.position]
        
        if is_float:
            value = float(lexeme)
            return self.make_token(TokenType.FLOAT, value)
        else:
            value = int(lexeme)
            return self.make_token(TokenType.NUMBER, value)
    
    def scan_identifier(self) -> Token:
        """Scan identifier or keyword."""
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
        
        # Division or comment
        elif char == '/':
            if self.current_char() == '/':
                self.advance()
                self.skip_line_comment()
                return self.next_token()  # Skip comment, get next token
            elif self.current_char() == '*':
                self.advance()
                if not self.skip_block_comment():
                    return Token(
                        type=TokenType.ERROR,
                        lexeme='unterminated comment',
                        line=self.token_start_line,
                        column=self.token_start_column
                    )
                return self.next_token()  # Skip comment, get next token
            else:
                return self.make_token(TokenType.SLASH)
        
        # Comparison operators
        elif char == '=':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.EQUAL_EQUAL)
            else:
                return self.make_token(TokenType.EQUAL)
        
        elif char == '!':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.BANG_EQUAL)
            else:
                return self.make_token(TokenType.ERROR)
        
        elif char == '<':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.LESS_EQUAL)
            else:
                return self.make_token(TokenType.LESS)
        
        elif char == '>':
            if self.current_char() == '=':
                self.advance()
                return self.make_token(TokenType.GREATER_EQUAL)
            else:
                return self.make_token(TokenType.GREATER)
        
        # Semicolon
        elif char == ';':
            return self.make_token(TokenType.SEMICOLON)
        
        # String literals
        elif char == '"':
            return self.scan_string()
        
        # Numbers
        elif char.isdigit():
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()
            return self.scan_number()
        
        # Identifiers and keywords
        elif char.isalpha() or char == '_':
            self.position = self.token_start_pos
            self.column = self.token_start_column
            self.advance()
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
    """Demonstrate extended lexer features."""
    test_cases = [
        # Strings
        '"hello world"',
        '"line1\\nline2"',
        '"He said \\"hi\\""',
        '"unterminated',
        
        # Floats
        '3.14',
        '1e10',
        '2.5e-3',
        '0.5',
        
        # Comments
        'x = 42 // line comment',
        'y = /* block comment */ 10',
        'z = /* unterminated',
        
        # Comparison operators
        'if x >= 10',
        'while y != 0',
        'x < y <= z',
        
        # Combined
        '''x = "test" // assign string
        y = 3.14 /* pi */
        if x != y''',
    ]
    
    for source in test_cases:
        print(f"\nInput: {source!r}")
        print("-" * 60)
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            value_str = f" (value={token.value!r})" if token.value is not None else ""
            print(f"{token.type.name:15} {token.lexeme!r:15} @ {token.line}:{token.column}{value_str}")


if __name__ == "__main__":
    main()
