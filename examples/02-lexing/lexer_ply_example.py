"""
PLY-Based Lexer
===============

Lexer using PLY (Python Lex-Yacc).

Installation:
    pip install ply

Pros:
- Pythonic syntax
- Built-in position tracking
- No separate build step
- Good error messages

Cons:
- Slower than C-based lexers
- Requires external package
- More verbose than pure regex
"""

try:
    import ply.lex as lex
except ImportError:
    print("Error: PLY not installed. Run: pip install ply")
    exit(1)


# Token list - must be named 'tokens'
tokens = [
    'NUMBER',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'STAR',
    'SLASH',
    'EQUAL',
    'EQUAL_EQUAL',
]

# Reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
}

# Add reserved words to tokens list
tokens = tokens + list(reserved.values())


# Token rules (simple tokens)
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_SLASH = r'/'
t_EQUAL_EQUAL = r'=='
t_EQUAL = r'='

# Ignored characters (whitespace)
t_ignore = ' \t'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check if it's a reserved word
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    """Handle invalid characters."""
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def tokenize(source):
    """
    Tokenize source code and return list of tokens.
    
    Returns list of tuples: (type, value, line, column)
    """
    lexer.input(source)
    tokens = []
    
    for tok in lexer:
        # Calculate column (PLY doesn't track this automatically)
        # This is simplified - a production lexer would track this better
        tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
    
    return tokens


def main():
    """Demonstrate PLY-based tokenization."""
    
    test_cases = [
        "if x == 42 + 7",
        "while y = 10 - 3",
        "foo = bar * 2",
        "if else while",  # All keywords
        "x @ y",  # With error
        """x = 1
y = 2
z = x + y""",  # Multi-line
    ]
    
    for source in test_cases:
        print(f"\nInput: {source!r}")
        print("-" * 60)
        
        lexer.input(source)
        
        for tok in lexer:
            value_str = f" (value={tok.value})" if isinstance(tok.value, int) else ""
            print(f"{tok.type:15} '{tok.value}'{value_str:15} @ line {tok.lineno}")


if __name__ == "__main__":
    main()
