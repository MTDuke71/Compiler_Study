/* Token definitions for Flex lexer */

#ifndef TOKENS_H
#define TOKENS_H

/* Token types */
enum TokenType {
    NUMBER = 256,
    IDENTIFIER,
    IF,
    ELSE,
    WHILE,
    PLUS,
    MINUS,
    STAR,
    SLASH,
    EQUAL,
    EQUAL_EQUAL,
    ERROR,
    END_OF_FILE
};

#endif /* TOKENS_H */
