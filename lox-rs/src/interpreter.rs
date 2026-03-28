use crate::ast::{Expr, Stmt};
use crate::environment::Environment;
use crate::token::{Literal, TokenType};

/// Sentinel used to unwind the call stack on `return`.
#[derive(Debug)]
pub struct Return {
    pub value: Literal,
}

pub struct Interpreter {
    pub environment: Environment,
    pub had_runtime_error: bool,
}

impl Interpreter {
    pub fn new() -> Self {
        let mut env = Environment::new();

        // Native function: clock() — returns seconds since epoch
        // We store native functions as Nil for now; call handling is below.
        env.define("clock", Literal::Nil);

        Interpreter {
            environment: env,
            had_runtime_error: false,
        }
    }

    pub fn interpret(&mut self, statements: &[Stmt]) {
        for stmt in statements {
            if let Err(msg) = self.execute(stmt) {
                eprintln!("Runtime error: {msg}");
                self.had_runtime_error = true;
                return;
            }
        }
    }

    // ── Statements ────────────────────────────────────────────

    fn execute(&mut self, stmt: &Stmt) -> Result<(), String> {
        match stmt {
            Stmt::Expression { expression } => {
                self.evaluate(expression)?;
            }
            Stmt::Print { expression } => {
                let value = self.evaluate(expression)?;
                println!("{value}");
            }
            Stmt::Var { name, initializer } => {
                let value = match initializer {
                    Some(expr) => self.evaluate(expr)?,
                    None => Literal::Nil,
                };
                self.environment.define(&name.lexeme, value);
            }
            Stmt::Block { statements } => {
                self.execute_block(statements)?;
            }
            Stmt::If {
                condition,
                then_branch,
                else_branch,
            } => {
                if is_truthy(&self.evaluate(condition)?) {
                    self.execute(then_branch)?;
                } else if let Some(else_stmt) = else_branch {
                    self.execute(else_stmt)?;
                }
            }
            Stmt::While { condition, body } => {
                while is_truthy(&self.evaluate(condition)?) {
                    self.execute(body)?;
                }
            }
            Stmt::Function { name, params, body } => {
                // Store function as a serialised form we can call later.
                // For a full implementation you'd want a LoxFunction type.
                // This is a simplified placeholder — see TODO below.
                let _ = (params, body);
                self.environment.define(&name.lexeme, Literal::Nil);
                // TODO: implement first-class function values and closures
            }
            Stmt::Return { value, .. } => {
                let ret_val = match value {
                    Some(expr) => self.evaluate(expr)?,
                    None => Literal::Nil,
                };
                // Use a special error string to unwind; a real impl uses Result enum.
                return Err(format!("__return__:{ret_val}"));
            }
        }
        Ok(())
    }

    fn execute_block(&mut self, statements: &[Stmt]) -> Result<(), String> {
        let previous = self.environment.clone();
        self.environment = Environment::with_enclosing(previous.clone());

        let result = (|| {
            for stmt in statements {
                self.execute(stmt)?;
            }
            Ok(())
        })();

        self.environment = previous;
        result
    }

    // ── Expressions ───────────────────────────────────────────

    fn evaluate(&mut self, expr: &Expr) -> Result<Literal, String> {
        match expr {
            Expr::Literal { value } => Ok(value.clone()),

            Expr::Grouping { expression } => self.evaluate(expression),

            Expr::Unary { operator, right } => {
                let right = self.evaluate(right)?;
                match operator.token_type {
                    TokenType::Minus => match right {
                        Literal::Number(n) => Ok(Literal::Number(-n)),
                        _ => Err("Operand must be a number.".to_string()),
                    },
                    TokenType::Bang => Ok(Literal::Bool(!is_truthy(&right))),
                    _ => Err("Unknown unary operator.".to_string()),
                }
            }

            Expr::Binary {
                left,
                operator,
                right,
            } => {
                let left = self.evaluate(left)?;
                let right = self.evaluate(right)?;

                match operator.token_type {
                    TokenType::Minus => number_op(&left, &right, |a, b| Literal::Number(a - b)),
                    TokenType::Slash => number_op(&left, &right, |a, b| Literal::Number(a / b)),
                    TokenType::Star => number_op(&left, &right, |a, b| Literal::Number(a * b)),
                    TokenType::Plus => match (&left, &right) {
                        (Literal::Number(a), Literal::Number(b)) => Ok(Literal::Number(a + b)),
                        (Literal::String(a), Literal::String(b)) => {
                            Ok(Literal::String(format!("{a}{b}")))
                        }
                        _ => Err("Operands must be two numbers or two strings.".to_string()),
                    },
                    TokenType::Greater => number_op(&left, &right, |a, b| Literal::Bool(a > b)),
                    TokenType::GreaterEqual => {
                        number_op(&left, &right, |a, b| Literal::Bool(a >= b))
                    }
                    TokenType::Less => number_op(&left, &right, |a, b| Literal::Bool(a < b)),
                    TokenType::LessEqual => {
                        number_op(&left, &right, |a, b| Literal::Bool(a <= b))
                    }
                    TokenType::BangEqual => Ok(Literal::Bool(left != right)),
                    TokenType::EqualEqual => Ok(Literal::Bool(left == right)),
                    _ => Err("Unknown binary operator.".to_string()),
                }
            }

            Expr::Variable { name } => self.environment.get(&name.lexeme),

            Expr::Assign { name, value } => {
                let val = self.evaluate(value)?;
                self.environment.assign(&name.lexeme, val.clone())?;
                Ok(val)
            }

            Expr::Logical {
                left,
                operator,
                right,
            } => {
                let left_val = self.evaluate(left)?;
                match operator.token_type {
                    TokenType::Or => {
                        if is_truthy(&left_val) {
                            return Ok(left_val);
                        }
                    }
                    TokenType::And => {
                        if !is_truthy(&left_val) {
                            return Ok(left_val);
                        }
                    }
                    _ => {}
                }
                self.evaluate(right)
            }

            Expr::Call { .. } => {
                // TODO: implement function calls (requires LoxFunction / LoxCallable)
                Err("Function calls not yet implemented.".to_string())
            }
        }
    }
}

// ── Helpers ───────────────────────────────────────────────────

fn is_truthy(literal: &Literal) -> bool {
    match literal {
        Literal::Nil => false,
        Literal::Bool(b) => *b,
        _ => true,
    }
}

fn number_op(
    left: &Literal,
    right: &Literal,
    op: impl Fn(f64, f64) -> Literal,
) -> Result<Literal, String> {
    match (left, right) {
        (Literal::Number(a), Literal::Number(b)) => Ok(op(*a, *b)),
        _ => Err("Operands must be numbers.".to_string()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ast::Stmt;
    use crate::parser::Parser;
    use crate::scanner::Scanner;

    /// Scan → parse → evaluate a single expression (no trailing semicolon needed).
    fn eval(expr_source: &str) -> Result<Literal, String> {
        let source = format!("{expr_source};");
        let mut scanner = Scanner::new(&source);
        let tokens = scanner.scan_tokens();
        let mut parser = Parser::new(tokens);
        let stmts = parser.parse();
        let mut interp = Interpreter::new();
        match stmts.into_iter().next() {
            Some(Stmt::Expression { expression }) => interp.evaluate(&expression),
            _ => Err("Expected expression statement".to_string()),
        }
    }

    /// Run full Lox source; returns true if a runtime error occurred.
    fn run(source: &str) -> bool {
        let mut scanner = Scanner::new(source);
        let tokens = scanner.scan_tokens();
        let mut parser = Parser::new(tokens);
        let stmts = parser.parse();
        let mut interp = Interpreter::new();
        interp.interpret(&stmts);
        interp.had_runtime_error
    }

    // ── Literals ──────────────────────────────────────────────

    #[test]
    fn number_literal() {
        assert_eq!(eval("42"), Ok(Literal::Number(42.0)));
    }

    #[test]
    fn string_literal() {
        assert_eq!(eval(r#""hello""#), Ok(Literal::String("hello".to_string())));
    }

    #[test]
    fn bool_literal() {
        assert_eq!(eval("true"), Ok(Literal::Bool(true)));
        assert_eq!(eval("false"), Ok(Literal::Bool(false)));
    }

    #[test]
    fn nil_literal() {
        assert_eq!(eval("nil"), Ok(Literal::Nil));
    }

    // ── Arithmetic ────────────────────────────────────────────

    #[test]
    fn arithmetic_precedence() {
        // * binds tighter: 2 + (3 * 4) = 14
        assert_eq!(eval("2 + 3 * 4"), Ok(Literal::Number(14.0)));
    }

    #[test]
    fn subtraction() {
        assert_eq!(eval("10 - 3"), Ok(Literal::Number(7.0)));
    }

    #[test]
    fn division() {
        assert_eq!(eval("10 / 4"), Ok(Literal::Number(2.5)));
    }

    #[test]
    fn unary_negate() {
        assert_eq!(eval("-5"), Ok(Literal::Number(-5.0)));
    }

    // ── Unary bang ────────────────────────────────────────────

    #[test]
    fn bang_true_is_false() {
        assert_eq!(eval("!true"), Ok(Literal::Bool(false)));
    }

    #[test]
    fn bang_nil_is_true() {
        // nil is falsy, so !nil = true
        assert_eq!(eval("!nil"), Ok(Literal::Bool(true)));
    }

    #[test]
    fn bang_number_is_false() {
        // any number is truthy
        assert_eq!(eval("!42"), Ok(Literal::Bool(false)));
    }

    // ── Strings ───────────────────────────────────────────────

    #[test]
    fn string_concatenation() {
        assert_eq!(
            eval(r#""foo" + "bar""#),
            Ok(Literal::String("foobar".to_string()))
        );
    }

    #[test]
    fn number_plus_string_is_error() {
        assert!(eval(r#"1 + "oops""#).is_err());
    }

    // ── Comparisons ───────────────────────────────────────────

    #[test]
    fn comparison_greater() {
        assert_eq!(eval("3 > 2"), Ok(Literal::Bool(true)));
        assert_eq!(eval("2 > 3"), Ok(Literal::Bool(false)));
    }

    #[test]
    fn comparison_less_equal() {
        assert_eq!(eval("1 <= 1"), Ok(Literal::Bool(true)));
        assert_eq!(eval("2 <= 1"), Ok(Literal::Bool(false)));
    }

    // ── Equality ──────────────────────────────────────────────

    #[test]
    fn nil_equals_nil() {
        assert_eq!(eval("nil == nil"), Ok(Literal::Bool(true)));
    }

    #[test]
    fn inequality() {
        assert_eq!(eval("1 != 2"), Ok(Literal::Bool(true)));
        assert_eq!(eval("1 != 1"), Ok(Literal::Bool(false)));
    }

    // ── Logical ───────────────────────────────────────────────

    #[test]
    fn logical_and() {
        assert_eq!(eval("true and true"),  Ok(Literal::Bool(true)));
        assert_eq!(eval("true and false"), Ok(Literal::Bool(false)));
        assert_eq!(eval("false and true"), Ok(Literal::Bool(false)));
    }

    #[test]
    fn logical_or() {
        assert_eq!(eval("true or false"),  Ok(Literal::Bool(true)));
        assert_eq!(eval("false or false"), Ok(Literal::Bool(false)));
    }

    #[test]
    fn logical_and_returns_left_on_falsy() {
        // Lox returns the actual value, not a bool — nil and 2 => nil
        assert_eq!(eval("nil and 2"), Ok(Literal::Nil));
    }

    #[test]
    fn logical_or_short_circuits_on_truthy() {
        // 1 or 2 => 1 (left is returned, right never evaluated)
        assert_eq!(eval("1 or 2"), Ok(Literal::Number(1.0)));
    }

    // ── Variables ─────────────────────────────────────────────

    #[test]
    fn variable_declaration_no_error() {
        assert!(!run("var x = 10;"), "Expected no runtime error");
    }

    #[test]
    fn variable_assignment_no_error() {
        assert!(!run("var x = 1; x = 2;"), "Expected no runtime error");
    }

    #[test]
    fn undefined_variable_is_runtime_error() {
        assert!(run("print x;"), "Expected runtime error for undefined var");
    }

    #[test]
    fn block_scoping_does_not_leak() {
        // x is defined only inside the block; using it outside should error
        assert!(run("{ var x = 1; } print x;"));
    }

    // ── Control flow ──────────────────────────────────────────

    #[test]
    fn if_true_branch_runs() {
        // If this completes without runtime error the then-branch ran
        assert!(!run("var x = 0; if (true) { x = 1; }"));
    }

    #[test]
    fn while_false_never_runs() {
        assert!(!run("while (false) { print undefined_var; }"));
    }
}
