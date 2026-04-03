//! Runs each compiler phase on a .lox file and writes intermediate
//! representations to disk so you can inspect the full pipeline.
//!
//! Usage:  cargo run --bin dump_pipeline -- examples/demo.lox
//!
//! Produces (in output/):
//!   0_source.lox      — copy of the original source
//!   1_tokens.txt      — token stream from the scanner
//!   2_ast.txt         — AST from the parser (pretty-printed)
//!   3_execution.txt   — interpreter output (print stmts go to stdout,
//!                        which is tee'd to the file)

use std::fmt::Write as FmtWrite;
use std::fs;
use std::path::Path;

use lox_rs::ast::{Expr, Stmt};
use lox_rs::interpreter::Interpreter;
use lox_rs::parser::Parser;
use lox_rs::scanner::Scanner;
use lox_rs::token::Token;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: dump_pipeline <script.lox>");
        std::process::exit(64);
    }

    let source = fs::read_to_string(&args[1]).unwrap_or_else(|e| {
        eprintln!("Could not read '{}': {e}", args[1]);
        std::process::exit(66);
    });

    let out_dir = Path::new("output");
    fs::create_dir_all(out_dir).unwrap();

    // ── Phase 0: Copy source ──────────────────────────────────
    fs::write(out_dir.join("0_source.lox"), &source).unwrap();

    // ── Phase 1: Scanning ─────────────────────────────────────
    eprintln!("=== Phase 1: Scanning (characters -> tokens) ===");
    let mut scanner = Scanner::new(&source);
    let tokens = scanner.scan_tokens();
    if scanner.had_error {
        eprintln!("Scanner errors — aborting.");
        std::process::exit(65);
    }
    let token_count = tokens.len();
    let tokens_text = format_tokens(&tokens);
    fs::write(out_dir.join("1_tokens.txt"), &tokens_text).unwrap();
    eprintln!("  {token_count} tokens -> output/1_tokens.txt");

    // ── Phase 2: Parsing ──────────────────────────────────────
    eprintln!("\n=== Phase 2: Parsing (tokens -> AST) ===");
    let mut parser = Parser::new(tokens);
    let statements = parser.parse();
    if parser.had_error {
        eprintln!("Parser errors — aborting.");
        std::process::exit(65);
    }
    let stmt_count = statements.len();
    let ast_text = format_ast(&statements);
    fs::write(out_dir.join("2_ast.txt"), &ast_text).unwrap();
    eprintln!("  {stmt_count} top-level statements -> output/2_ast.txt");

    // ── Phase 3: Interpretation ───────────────────────────────
    eprintln!("\n=== Phase 3: Interpretation (AST -> runtime output) ===");

    // The interpreter uses println! so we run it and the shell
    // captures stdout to 3_execution.txt.
    let mut interpreter = Interpreter::new();
    interpreter.interpret(&statements);

    if interpreter.had_runtime_error {
        eprintln!("  Runtime error occurred.");
        std::process::exit(70);
    }

    eprintln!("\n=== Pipeline complete ===");
    eprintln!("  output/0_source.lox    — original source");
    eprintln!("  output/1_tokens.txt    — token stream ({token_count} tokens)");
    eprintln!("  output/2_ast.txt       — abstract syntax tree ({stmt_count} stmts)");
    eprintln!("  output/3_execution.txt — execution results (stdout)");
}

// ── Token formatter ──────────────────────────────────────────

fn format_tokens(tokens: &[Token]) -> String {
    let mut out = String::new();
    writeln!(out, "TOKEN STREAM").unwrap();
    writeln!(out, "{}", "=".repeat(70)).unwrap();
    writeln!(out, "{:<6} {:<16} {:<20} {}",
        "Line", "Type", "Lexeme", "Literal").unwrap();
    writeln!(out, "{}", "-".repeat(70)).unwrap();

    for tok in tokens {
        let lit = match &tok.literal {
            Some(l) => format!("{l}"),
            None => "-".to_string(),
        };
        writeln!(out, "{:<6} {:<16} {:<20} {}",
            tok.line,
            format!("{:?}", tok.token_type),
            format!("{:?}", tok.lexeme),
            lit,
        ).unwrap();
    }
    writeln!(out, "{}", "-".repeat(70)).unwrap();
    writeln!(out, "Total: {} tokens", tokens.len()).unwrap();
    out
}

// ── AST pretty-printer ──────────────────────────────────────

fn format_ast(stmts: &[Stmt]) -> String {
    let mut out = String::new();
    writeln!(out, "ABSTRACT SYNTAX TREE").unwrap();
    writeln!(out, "{}", "=".repeat(70)).unwrap();

    for (i, stmt) in stmts.iter().enumerate() {
        writeln!(out, "\n── Statement {i} ──").unwrap();
        fmt_stmt(&mut out, stmt, 0);
    }
    out
}

fn fmt_stmt(out: &mut String, stmt: &Stmt, depth: usize) {
    let pad = "  ".repeat(depth);
    match stmt {
        Stmt::Expression { expression } => {
            writeln!(out, "{pad}ExprStmt").unwrap();
            fmt_expr(out, expression, depth + 1);
        }
        Stmt::Print { expression } => {
            writeln!(out, "{pad}Print").unwrap();
            fmt_expr(out, expression, depth + 1);
        }
        Stmt::Var { name, initializer } => {
            write!(out, "{pad}VarDecl '{}'", name.lexeme).unwrap();
            if let Some(init) = initializer {
                writeln!(out).unwrap();
                fmt_expr(out, init, depth + 1);
            } else {
                writeln!(out, " = nil").unwrap();
            }
        }
        Stmt::Block { statements } => {
            writeln!(out, "{pad}Block").unwrap();
            for s in statements {
                fmt_stmt(out, s, depth + 1);
            }
        }
        Stmt::If { condition, then_branch, else_branch } => {
            writeln!(out, "{pad}If").unwrap();
            writeln!(out, "{pad}  condition:").unwrap();
            fmt_expr(out, condition, depth + 2);
            writeln!(out, "{pad}  then:").unwrap();
            fmt_stmt(out, then_branch, depth + 2);
            if let Some(els) = else_branch {
                writeln!(out, "{pad}  else:").unwrap();
                fmt_stmt(out, els, depth + 2);
            }
        }
        Stmt::While { condition, body } => {
            writeln!(out, "{pad}While").unwrap();
            writeln!(out, "{pad}  condition:").unwrap();
            fmt_expr(out, condition, depth + 2);
            writeln!(out, "{pad}  body:").unwrap();
            fmt_stmt(out, body, depth + 2);
        }
        Stmt::Function { name, params, body } => {
            let ps: Vec<&str> = params.iter().map(|p| p.lexeme.as_str()).collect();
            writeln!(out, "{pad}FunDecl '{}' ({})", name.lexeme, ps.join(", ")).unwrap();
            for s in body {
                fmt_stmt(out, s, depth + 1);
            }
        }
        Stmt::Return { value, .. } => {
            writeln!(out, "{pad}Return").unwrap();
            if let Some(expr) = value {
                fmt_expr(out, expr, depth + 1);
            }
        }
    }
}

fn fmt_expr(out: &mut String, expr: &Expr, depth: usize) {
    let pad = "  ".repeat(depth);
    match expr {
        Expr::Literal { value } => {
            writeln!(out, "{pad}Literal({value})").unwrap();
        }
        Expr::Unary { operator, right } => {
            writeln!(out, "{pad}Unary '{}'", operator.lexeme).unwrap();
            fmt_expr(out, right, depth + 1);
        }
        Expr::Binary { left, operator, right } => {
            writeln!(out, "{pad}Binary '{}'", operator.lexeme).unwrap();
            fmt_expr(out, left, depth + 1);
            fmt_expr(out, right, depth + 1);
        }
        Expr::Grouping { expression } => {
            writeln!(out, "{pad}Grouping").unwrap();
            fmt_expr(out, expression, depth + 1);
        }
        Expr::Variable { name } => {
            writeln!(out, "{pad}Var({})", name.lexeme).unwrap();
        }
        Expr::Assign { name, value } => {
            writeln!(out, "{pad}Assign '{}'", name.lexeme).unwrap();
            fmt_expr(out, value, depth + 1);
        }
        Expr::Logical { left, operator, right } => {
            writeln!(out, "{pad}Logical '{}'", operator.lexeme).unwrap();
            fmt_expr(out, left, depth + 1);
            fmt_expr(out, right, depth + 1);
        }
        Expr::Call { callee, arguments, .. } => {
            writeln!(out, "{pad}Call").unwrap();
            fmt_expr(out, callee, depth + 1);
            for arg in arguments {
                fmt_expr(out, arg, depth + 1);
            }
        }
    }
}
