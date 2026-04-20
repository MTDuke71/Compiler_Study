//! Pedagogical AstPrinter — the Crafting Interpreters Chapter 5 exercise.
//!
//! In Java (the book) this is a `Visitor<String>` implementation with an
//! `accept()` method on every Expr subclass — ~40 lines of dispatch scaffold
//! before you write a single character of output logic.
//!
//! In Rust it's a single `match` on the `Expr` enum. The pattern match IS
//! the visitor dispatch. No trait, no accept, no GenerateAst.
//!
//! Run with:
//!   cargo run --bin ast_printer
//!
//! Output format is S-expression (Lisp-style), matching the book:
//!   1 + 2 * 3        =>  (+ 1 (* 2 3))
//!   (1 + 2) * 3      =>  (* (group (+ 1 2)) 3)
//!   -123 * (45.67)   =>  (* (- 123) (group 45.67))

use lox_rs::ast::{Expr, Stmt};
use lox_rs::parser::Parser;
use lox_rs::scanner::Scanner;
use lox_rs::token::{Literal, Token, TokenType};

/// Pretty-print an Expr as an S-expression. The whole visitor pattern,
/// reduced to one function with exhaustive pattern matching.
///
/// Compare to the Java book's AstPrinter class: ~40 lines of Visitor
/// scaffold + ~15 lines of actual print logic. Here the scaffold disappears.
fn pretty(e: &Expr) -> String {
    match e {
        // ── Ch 5 variants ────────────────────────────────────────
        Expr::Literal { value } => value.to_string(),

        Expr::Grouping { expression } => format!("(group {})", pretty(expression)),

        Expr::Unary { operator, right } => {
            format!("({} {})", operator.lexeme, pretty(right))
        }

        Expr::Binary { left, operator, right } => {
            format!("({} {} {})", operator.lexeme, pretty(left), pretty(right))
        }

        // ── Ch 8+ variants (exhaustiveness forces us to handle them) ──
        // In the book's Ch5 AstPrinter these don't exist yet. Rust's match
        // checker doesn't let us skip them, which is actually the point —
        // when you later add a new Expr variant, the compiler walks you to
        // every consumer that needs updating. No silent gaps.
        Expr::Variable { name } => name.lexeme.clone(),

        Expr::Assign { name, value } => {
            format!("(= {} {})", name.lexeme, pretty(value))
        }

        Expr::Logical { left, operator, right } => {
            format!("({} {} {})", operator.lexeme, pretty(left), pretty(right))
        }

        Expr::Call { callee, arguments, .. } => {
            let args: Vec<String> = arguments.iter().map(pretty).collect();
            if args.is_empty() {
                format!("(call {})", pretty(callee))
            } else {
                format!("(call {} {})", pretty(callee), args.join(" "))
            }
        }
    }
}

fn main() {
    // ─── Part 1: the book's exact Ch5 example, built by hand ────────────
    // The book constructs this AST manually (before the parser exists) to
    // demonstrate that the tree representation works independently of how
    // you build it. Parser in Ch6, evaluator in Ch7 — this is just trees.
    //
    // Source equivalent: -123 * (45.67)
    let manual = Expr::Binary {
        left: Box::new(Expr::Unary {
            operator: tok(TokenType::Minus, "-"),
            right: Box::new(Expr::Literal {
                value: Literal::Number(123.0),
            }),
        }),
        operator: tok(TokenType::Star, "*"),
        right: Box::new(Expr::Grouping {
            expression: Box::new(Expr::Literal {
                value: Literal::Number(45.67),
            }),
        }),
    };

    println!("─── Hand-built AST (the book's Ch5 listing) ────────────────");
    println!("  -123 * (45.67)");
    println!("  => {}", pretty(&manual));
    println!();

    // ─── Part 2: let the real parser build the ASTs ─────────────────────
    // These feed source through scanner → parser → ast_printer. The
    // precedence cascade in parser.rs is what decides the tree shape;
    // the printer just reads it back. If the parenthesization here
    // matches your intuition, parser.rs's grammar is correct.
    let samples = [
        "1 + 2 * 3;",      // precedence: * binds tighter than +
        "(1 + 2) * 3;",    // explicit grouping overrides
        "-a * b + c;",     // unary, then factor, then term
        "!true == false;", // unary bang, then equality
        "1 < 2 == 3 > 4;", // comparison feeds equality
        "a = b = 5;",      // assignment is right-associative (Ch 8)
        "a and b or c;",   // or has lower precedence than and (Ch 9)
        "foo(1, 2 + 3);",  // call with argument list (Ch 10)
    ];

    println!("─── Parser-built ASTs (source → scanner → parser → print) ──");
    for src in samples {
        let tokens = Scanner::new(src).scan_tokens();
        let mut parser = Parser::new(tokens);
        let stmts = parser.parse();

        // Each sample is a single expression statement. Unwrap it back to
        // the Expr so we can print with our Ch5 pretty function.
        if let Some(Stmt::Expression { expression }) = stmts.first() {
            println!("  {src:22}  =>  {}", pretty(expression));
        } else {
            println!("  {src:22}  =>  (not a bare expression)");
        }
    }
}

/// Build a throwaway Token for the hand-built AST demo.
/// Real tokens come from the scanner; this is only for Part 1.
fn tok(token_type: TokenType, lexeme: &str) -> Token {
    Token {
        token_type,
        lexeme: lexeme.to_string(),
        literal: None,
        line: 1,
    }
}
