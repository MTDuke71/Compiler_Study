"""
Token Dumper Utility
====================

Utility for dumping token streams to files in various formats.
Useful for debugging, testing, and inspecting large token streams.

Usage:
    python token_dumper.py source_file.txt [--output tokens.txt] [--format json]
    
Or import and use programmatically:
    from token_dumper import dump_tokens
    dump_tokens(tokens, "output.txt", format="human")
"""

import argparse
import json
from pathlib import Path
from typing import List
from lexer_extended import Lexer, Token, TokenType


def dump_tokens_human(tokens: List[Token], output_file: str):
    """Dump tokens in human-readable format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("TOKEN STREAM\n")
        f.write("=" * 80 + "\n\n")
        
        for i, token in enumerate(tokens):
            if token.type == TokenType.EOF:
                f.write(f"\n[{i:4d}] EOF\n")
                continue
            
            value_str = f" = {token.value!r}" if token.value is not None else ""
            f.write(f"[{i:4d}] {token.type.name:15} '{token.lexeme}'{value_str:20} @ {token.line}:{token.column}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Total tokens: {len(tokens)}\n")
        f.write("=" * 80 + "\n")


def dump_tokens_json(tokens: List[Token], output_file: str):
    """Dump tokens in JSON format."""
    token_list = []
    for token in tokens:
        token_list.append({
            'type': token.type.name,
            'lexeme': token.lexeme,
            'value': token.value,
            'line': token.line,
            'column': token.column
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(token_list, f, indent=2)


def dump_tokens_csv(tokens: List[Token], output_file: str):
    """Dump tokens in CSV format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("index,type,lexeme,value,line,column\n")
        
        # Tokens
        for i, token in enumerate(tokens):
            lexeme = token.lexeme.replace('"', '""')  # Escape quotes
            value = str(token.value).replace('"', '""') if token.value is not None else ""
            f.write(f'{i},{token.type.name},"{lexeme}","{value}",{token.line},{token.column}\n')


def dump_tokens_compact(tokens: List[Token], output_file: str):
    """Dump tokens in compact one-line-per-token format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            f.write(f"{token.type.name}\n")


def dump_tokens(tokens: List[Token], output_file: str, format: str = 'human'):
    """
    Dump tokens to file in specified format.
    
    Args:
        tokens: List of Token objects
        output_file: Path to output file
        format: One of 'human', 'json', 'csv', 'compact'
    """
    format = format.lower()
    
    if format == 'human':
        dump_tokens_human(tokens, output_file)
    elif format == 'json':
        dump_tokens_json(tokens, output_file)
    elif format == 'csv':
        dump_tokens_csv(tokens, output_file)
    elif format == 'compact':
        dump_tokens_compact(tokens, output_file)
    else:
        raise ValueError(f"Unknown format: {format}. Use 'human', 'json', 'csv', or 'compact'.")
    
    print(f"✓ Dumped {len(tokens)} tokens to {output_file} ({format} format)")


def main():
    parser = argparse.ArgumentParser(
        description='Dump lexer token stream to file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Human-readable format (default)
  python token_dumper.py input.txt
  
  # JSON format
  python token_dumper.py input.txt --format json
  
  # Custom output file
  python token_dumper.py input.txt --output my_tokens.txt
  
  # CSV for spreadsheet analysis
  python token_dumper.py input.txt --format csv --output tokens.csv

Formats:
  human   - Readable format with alignment (default)
  json    - JSON array of token objects
  csv     - CSV with header row
  compact - One token type per line (minimal)
        """
    )
    
    parser.add_argument('input', help='Source file to tokenize')
    parser.add_argument('-o', '--output', help='Output file (default: tokens.txt)', default='tokens.txt')
    parser.add_argument('-f', '--format', 
                       choices=['human', 'json', 'csv', 'compact'],
                       default='human',
                       help='Output format (default: human)')
    
    args = parser.parse_args()
    
    # Read source file
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"✗ Error: File not found: {args.input}")
        return 1
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return 1
    
    # Tokenize
    print(f"Tokenizing {args.input}...")
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Dump to file
    try:
        dump_tokens(tokens, args.output, args.format)
    except Exception as e:
        print(f"✗ Error writing output: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
