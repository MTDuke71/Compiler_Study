"""
Regex-Based Lexer
=================

Extremely simple tokenizer using Python's regex library.

Pros:
- Very concise (~30 lines)
- No dependencies
- Easy to understand

Cons:
- Poor error messages
- Harder to track positions accurately
- Not suitable for complex languages
"""

import re

# Combined regex pattern with named groups
TOKEN_REGEX = r'''
    (?P<NUMBER>\d+)|
    (?P<KEYWORD>if|while|else)|
    (?P<IDENTIFIER>[a-zA-Z_]\w*)|
    (?P<EQUAL_EQUAL>==)|
    (?P<EQUAL>=)|
    (?P<PLUS>\+)|
    (?P<MINUS>-)|
    (?P<STAR>\*)|
    (?P<SLASH>/)|
    (?P<WHITESPACE>\s+)|
    (?P<ERROR>.)
'''

def tokenize(code):
    """
    Tokenize source code using regex.
    
    Yields tuples of (token_type, value, position)
    """
    line_num = 1
    line_start = 0
    
    for match in re.finditer(TOKEN_REGEX, code, re.VERBOSE):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1
        
        # Skip whitespace but track newlines
        if kind == 'WHITESPACE':
            newlines = value.count('\n')
            if newlines:
                line_num += newlines
                line_start = match.end()
            continue
        
        # Report errors but continue
        if kind == 'ERROR':
            print(f"Error at line {line_num}, col {column}: Invalid character '{value}'")
            continue
        
        yield (kind, value, line_num, column)


def main():
    """Demonstrate regex-based tokenization."""
    
    test_cases = [
        "if x == 42 + 7",
        "while y = 10 - 3",
        "foo = bar * 2",
        "x @ y # z",  # With errors
        """x = 1
y = 2
z = x + y""",  # Multi-line
    ]
    
    for source in test_cases:
        print(f"\nInput: {source!r}")
        print("-" * 60)
        
        tokens = list(tokenize(source))
        
        for kind, value, line, col in tokens:
            value_display = f"'{value}'"
            print(f"{kind:15} {value_display:10} @ {line}:{col}")


if __name__ == "__main__":
    main()
