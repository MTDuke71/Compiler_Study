use crate::token::{Literal, Token, TokenType};

pub struct Scanner {
    source: Vec<char>,
    tokens: Vec<Token>,
    start: usize,
    current: usize,
    line: usize,
    pub had_error: bool,
}

impl Scanner {
    pub fn new(source: &str) -> Self {
        Scanner {
            source: source.chars().collect(),
            tokens: Vec::new(),
            start: 0,
            current: 0,
            line: 1,
            had_error: false,
        }
    }

    pub fn scan_tokens(&mut self) -> Vec<Token> {
        while !self.is_at_end() {
            self.start = self.current;
            self.scan_token();
        }

        self.tokens.push(Token {
            token_type: TokenType::Eof,
            lexeme: String::new(),
            literal: None,
            line: self.line,
        });

        self.tokens.clone()
    }

    fn scan_token(&mut self) {
        let c = self.advance();
        match c {
            '(' => self.add_token(TokenType::LeftParen),
            ')' => self.add_token(TokenType::RightParen),
            '{' => self.add_token(TokenType::LeftBrace),
            '}' => self.add_token(TokenType::RightBrace),
            ',' => self.add_token(TokenType::Comma),
            '.' => self.add_token(TokenType::Dot),
            '-' => self.add_token(TokenType::Minus),
            '+' => self.add_token(TokenType::Plus),
            ';' => self.add_token(TokenType::Semicolon),
            '*' => self.add_token(TokenType::Star),
            '!' => {
                let tt = if self.match_char('=') { TokenType::BangEqual } else { TokenType::Bang };
                self.add_token(tt);
            }
            '=' => {
                let tt = if self.match_char('=') { TokenType::EqualEqual } else { TokenType::Equal };
                self.add_token(tt);
            }
            '<' => {
                let tt = if self.match_char('=') { TokenType::LessEqual } else { TokenType::Less };
                self.add_token(tt);
            }
            '>' => {
                let tt = if self.match_char('=') { TokenType::GreaterEqual } else { TokenType::Greater };
                self.add_token(tt);
            }
            '/' => {
                if self.match_char('/') {
                    // Comment — skip to end of line
                    while self.peek() != '\n' && !self.is_at_end() {
                        self.advance();
                    }
                } else {
                    self.add_token(TokenType::Slash);
                }
            }
            ' ' | '\r' | '\t' => {}
            '\n' => self.line += 1,
            '"' => self.string(),
            c if c.is_ascii_digit() => self.number(),
            c if c.is_ascii_alphabetic() || c == '_' => self.identifier(),
            _ => {
                self.error(self.line, &format!("Unexpected character: {c}"));
            }
        }
    }

    fn string(&mut self) {
        while self.peek() != '"' && !self.is_at_end() {
            if self.peek() == '\n' {
                self.line += 1;
            }
            self.advance();
        }

        if self.is_at_end() {
            self.error(self.line, "Unterminated string.");
            return;
        }

        // Closing "
        self.advance();

        let value: String = self.source[self.start + 1..self.current - 1].iter().collect();
        self.add_token_literal(TokenType::String, Some(Literal::String(value)));
    }

    fn number(&mut self) {
        while self.peek().is_ascii_digit() {
            self.advance();
        }

        if self.peek() == '.' && self.peek_next().is_ascii_digit() {
            self.advance(); // consume the '.'
            while self.peek().is_ascii_digit() {
                self.advance();
            }
        }

        let text: String = self.source[self.start..self.current].iter().collect();
        let value: f64 = text.parse().unwrap();
        self.add_token_literal(TokenType::Number, Some(Literal::Number(value)));
    }

    fn identifier(&mut self) {
        while self.peek().is_ascii_alphanumeric() || self.peek() == '_' {
            self.advance();
        }

        let text: String = self.source[self.start..self.current].iter().collect();
        let token_type = Self::keyword(&text).unwrap_or(TokenType::Identifier);
        self.add_token(token_type);
    }

    fn keyword(text: &str) -> Option<TokenType> {
        match text {
            "and" => Some(TokenType::And),
            "class" => Some(TokenType::Class),
            "else" => Some(TokenType::Else),
            "false" => Some(TokenType::False),
            "for" => Some(TokenType::For),
            "fun" => Some(TokenType::Fun),
            "if" => Some(TokenType::If),
            "nil" => Some(TokenType::Nil),
            "or" => Some(TokenType::Or),
            "print" => Some(TokenType::Print),
            "return" => Some(TokenType::Return),
            "super" => Some(TokenType::Super),
            "this" => Some(TokenType::This),
            "true" => Some(TokenType::True),
            "var" => Some(TokenType::Var),
            "while" => Some(TokenType::While),
            _ => None,
        }
    }

    fn advance(&mut self) -> char {
        let c = self.source[self.current];
        self.current += 1;
        c
    }

    fn match_char(&mut self, expected: char) -> bool {
        if self.is_at_end() || self.source[self.current] != expected {
            return false;
        }
        self.current += 1;
        true
    }

    fn peek(&self) -> char {
        if self.is_at_end() { '\0' } else { self.source[self.current] }
    }

    fn peek_next(&self) -> char {
        if self.current + 1 >= self.source.len() {
            '\0'
        } else {
            self.source[self.current + 1]
        }
    }

    fn is_at_end(&self) -> bool {
        self.current >= self.source.len()
    }

    fn add_token(&mut self, token_type: TokenType) {
        self.add_token_literal(token_type, None);
    }

    fn add_token_literal(&mut self, token_type: TokenType, literal: Option<Literal>) {
        let text: String = self.source[self.start..self.current].iter().collect();
        self.tokens.push(Token {
            token_type,
            lexeme: text,
            literal,
            line: self.line,
        });
    }

    fn error(&mut self, line: usize, message: &str) {
        eprintln!("[line {line}] Error: {message}");
        self.had_error = true;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::token::{Literal, TokenType};

    fn token_types(source: &str) -> Vec<TokenType> {
        let mut scanner = Scanner::new(source);
        scanner.scan_tokens().into_iter().map(|t| t.token_type).collect()
    }

    #[test]
    fn single_char_tokens() {
        let types = token_types("(){},.-+;/*");
        assert_eq!(
            types,
            vec![
                TokenType::LeftParen,
                TokenType::RightParen,
                TokenType::LeftBrace,
                TokenType::RightBrace,
                TokenType::Comma,
                TokenType::Dot,
                TokenType::Minus,
                TokenType::Plus,
                TokenType::Semicolon,
                TokenType::Slash,
                TokenType::Star,
                TokenType::Eof,
            ]
        );
    }

    #[test]
    fn two_char_tokens() {
        let types = token_types("!= == >= <=");
        assert_eq!(
            types,
            vec![
                TokenType::BangEqual,
                TokenType::EqualEqual,
                TokenType::GreaterEqual,
                TokenType::LessEqual,
                TokenType::Eof,
            ]
        );
    }

    #[test]
    fn single_without_second_char() {
        // Each should produce the single-char version, not the two-char version
        let types = token_types("! = > <");
        assert_eq!(
            types,
            vec![
                TokenType::Bang,
                TokenType::Equal,
                TokenType::Greater,
                TokenType::Less,
                TokenType::Eof,
            ]
        );
    }

    #[test]
    fn string_literal_value() {
        let mut scanner = Scanner::new(r#""hello""#);
        let tokens = scanner.scan_tokens();
        assert!(!scanner.had_error);
        assert_eq!(tokens[0].token_type, TokenType::String);
        assert_eq!(tokens[0].literal, Some(Literal::String("hello".to_string())));
    }

    #[test]
    fn number_integer() {
        let mut scanner = Scanner::new("42");
        let tokens = scanner.scan_tokens();
        assert_eq!(tokens[0].token_type, TokenType::Number);
        assert_eq!(tokens[0].literal, Some(Literal::Number(42.0)));
    }

    #[test]
    fn number_float() {
        let mut scanner = Scanner::new("3.14");
        let tokens = scanner.scan_tokens();
        assert_eq!(tokens[0].literal, Some(Literal::Number(3.14)));
    }

    #[test]
    fn keywords_recognised() {
        let types = token_types("and class else false for fun if nil or print return true var while");
        assert_eq!(
            types,
            vec![
                TokenType::And,
                TokenType::Class,
                TokenType::Else,
                TokenType::False,
                TokenType::For,
                TokenType::Fun,
                TokenType::If,
                TokenType::Nil,
                TokenType::Or,
                TokenType::Print,
                TokenType::Return,
                TokenType::True,
                TokenType::Var,
                TokenType::While,
                TokenType::Eof,
            ]
        );
    }

    #[test]
    fn keyword_prefix_is_identifier() {
        // "andx" and "classy" share prefixes with keywords but are identifiers
        let types = token_types("andx classy");
        assert_eq!(types, vec![TokenType::Identifier, TokenType::Identifier, TokenType::Eof]);
    }

    #[test]
    fn comment_is_skipped() {
        let types = token_types("// this whole line is a comment");
        assert_eq!(types, vec![TokenType::Eof]);
    }

    #[test]
    fn whitespace_is_skipped() {
        let types = token_types("   \t  \n  ");
        assert_eq!(types, vec![TokenType::Eof]);
    }

    #[test]
    fn multiline_tracks_line_number() {
        let mut scanner = Scanner::new("1\n2\n3");
        let tokens = scanner.scan_tokens();
        assert_eq!(tokens[0].line, 1);
        assert_eq!(tokens[1].line, 2);
        assert_eq!(tokens[2].line, 3);
    }

    #[test]
    fn unterminated_string_sets_error() {
        let mut scanner = Scanner::new(r#""oops"#);
        scanner.scan_tokens();
        assert!(scanner.had_error);
    }

    #[test]
    fn unexpected_char_sets_error() {
        let mut scanner = Scanner::new("@");
        scanner.scan_tokens();
        assert!(scanner.had_error);
    }
}
