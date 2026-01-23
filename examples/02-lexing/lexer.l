%{
/*
 * Flex Lexer Specification
 * ========================
 * 
 * To build and run:
 *   flex lexer.l
 *   gcc lex.yy.c -o lexer -lfl
 *   ./lexer < input.txt
 * 
 * Or on Windows with MinGW:
 *   flex lexer.l
 *   gcc lex.yy.c -o lexer.exe
 *   lexer.exe < input.txt
 */

#include "tokens.h"
#include <stdio.h>

int line_num = 1;
int column = 1;

#define YY_USER_ACTION column += yyleng;
%}

/* Options */
%option noyywrap

/* Definitions */
DIGIT    [0-9]
LETTER   [a-zA-Z_]
ID       {LETTER}({LETTER}|{DIGIT})*
NUMBER   {DIGIT}+

%%

    /* Skip whitespace */
[ \t]+          { /* do nothing */ }

    /* Track newlines */
\n              { line_num++; column = 1; }

    /* Keywords */
"if"            { printf("IF           'if'         @ %d:%d\n", line_num, column - yyleng); }
"else"          { printf("ELSE         'else'       @ %d:%d\n", line_num, column - yyleng); }
"while"         { printf("WHILE        'while'      @ %d:%d\n", line_num, column - yyleng); }

    /* Identifiers */
{ID}            { printf("IDENTIFIER   '%s'%*s@ %d:%d\n", yytext, (int)(12 - strlen(yytext)), " ", line_num, column - yyleng); }

    /* Numbers */
{NUMBER}        { printf("NUMBER       '%s'%*s@ %d:%d\n", yytext, (int)(12 - strlen(yytext)), " ", line_num, column - yyleng); }

    /* Operators */
"=="            { printf("EQUAL_EQUAL  '=='        @ %d:%d\n", line_num, column - yyleng); }
"="             { printf("EQUAL        '='         @ %d:%d\n", line_num, column - yyleng); }
"+"             { printf("PLUS         '+'         @ %d:%d\n", line_num, column - yyleng); }
"-"             { printf("MINUS        '-'         @ %d:%d\n", line_num, column - yyleng); }
"*"             { printf("STAR         '*'         @ %d:%d\n", line_num, column - yyleng); }
"/"             { printf("SLASH        '/'         @ %d:%d\n", line_num, column - yyleng); }

    /* Error: any other character */
.               { printf("ERROR        '%c'         @ %d:%d\n", yytext[0], line_num, column - yyleng); }

%%

int main(int argc, char **argv) {
    printf("Flex Lexer - Enter input (Ctrl+D or Ctrl+Z to end):\n");
    printf("------------------------------------------------------------\n");
    yylex();
    printf("------------------------------------------------------------\n");
    printf("EOF\n");
    return 0;
}
