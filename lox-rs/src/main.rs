mod ast;
mod environment;
mod interpreter;
mod parser;
mod scanner;
mod token;

use std::io::{self, BufRead, Write};

use interpreter::Interpreter;
use parser::Parser;
use scanner::Scanner;

fn main() {
    let args: Vec<String> = std::env::args().collect();

    match args.len() {
        1 => run_prompt(),
        2 => run_file(&args[1]),
        _ => {
            eprintln!("Usage: lox-rs [script]");
            std::process::exit(64);
        }
    }
}

fn run_file(path: &str) {
    let source = std::fs::read_to_string(path).unwrap_or_else(|e| {
        eprintln!("Could not read file '{path}': {e}");
        std::process::exit(66);
    });

    let mut interpreter = Interpreter::new();
    let exit_code = run(&source, &mut interpreter);

    if exit_code != 0 {
        std::process::exit(exit_code);
    }
}

fn run_prompt() {
    let stdin = io::stdin();
    let mut interpreter = Interpreter::new();

    print!("> ");
    io::stdout().flush().unwrap();

    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if line.is_empty() {
            break;
        }
        run(&line, &mut interpreter);
        print!("> ");
        io::stdout().flush().unwrap();
    }
}

fn run(source: &str, interpreter: &mut Interpreter) -> i32 {
    let mut scanner = Scanner::new(source);
    let tokens = scanner.scan_tokens();

    if scanner.had_error {
        return 65;
    }

    let mut parser = Parser::new(tokens);
    let statements = parser.parse();

    if parser.had_error {
        return 65;
    }

    interpreter.interpret(&statements);

    if interpreter.had_runtime_error {
        return 70;
    }

    0
}
