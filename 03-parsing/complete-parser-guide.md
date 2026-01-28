## Links
- Up: [[03-parsing/README]]
- Related: [[03-parsing/recursive-descent]] [[03-parsing/precedence-and-associativity]] [[04-semantics/scope]]
- Down: Implementation: [[examples/03-parsing/complete-parser.py]]

---

# Complete Recursive Descent Parser

**Training Document — Week 5, Day 3**

## Overview

This document walks through building a **production-ready recursive descent parser** for a complete programming language, not just expressions. We'll extend the basic expression parser to handle:

- **Statements:** Variable declarations, assignments, if/while/return, blocks
- **Functions:** Declarations with parameters, calls with arguments
- **Scoping:** Block-level scope tracking (minimal version)
- **Full precedence hierarchy:** 9 expression levels

**Key insight:** The jump from "toy calculator" to "real language" is **mechanical**—more grammar rules, same patterns.

**Learning approach:** Read the complete implementation, run it on examples, then modify to add features.

---

## Architecture Overview

### The Complete Pipeline

```
Source Code
    ↓
Lexer (tokenize)
    ↓
Token Stream
    ↓
Parser (this document)
    ↓
Abstract Syntax Tree
    ↓
Semantic Analysis (next phase)
```

### Parser Structure

```python
class Parser:
    # State
    tokens: List[Token]       # Input token stream
    position: int             # Current position
    current_token: Token      # Current token
    scopes: List[Dict]        # Scope stack (minimal tracking)
    
    # Entry point
    def parse(self) -> Program
    
    # Statement parsers
    def parse_statement(self) -> Statement
    def parse_var_declaration(self) -> VarDeclaration
    def parse_if_statement(self) -> IfStatement
    def parse_while_statement(self) -> WhileStatement
    def parse_return_statement(self) -> ReturnStatement
    def parse_block(self) -> Block
    def parse_expression_statement(self) -> ExpressionStatement
    
    # Expression parsers (stratified by precedence)
    def parse_expression(self) -> Expression
    def parse_assignment(self) -> Expression
    def parse_logical_or(self) -> Expression
    def parse_logical_and(self) -> Expression
    def parse_equality(self) -> Expression
    def parse_comparison(self) -> Expression
    def parse_addition(self) -> Expression
    def parse_multiplication(self) -> Expression
    def parse_unary(self) -> Expression
    def parse_primary(self) -> Expression
    
    # Function parsers
    def parse_function_decl(self) -> FunctionDecl
    def parse_function_call(self, name) -> FunctionCall
    
    # Utilities
    def match(self, *types) -> bool
    def advance(self) -> Token
    def expect(self, token_type) -> Token
    def error(self, message)
```

**Total:** ~600 lines of code for complete parser.

---

## The Complete Grammar

### Stratified by Precedence

```
// Program structure
Program      → (FunctionDecl | Statement)*
FunctionDecl → 'fn' ID '(' ParamList? ')' Block
ParamList    → ID (',' ID)*

// Statements (no precedence, just dispatch)
Statement    → VarDecl
             | IfStmt
             | WhileStmt
             | ReturnStmt
             | Block
             | ExprStmt

VarDecl      → 'var' ID ('=' Expression)? ';'
IfStmt       → 'if' '(' Expression ')' Statement ('else' Statement)?
WhileStmt    → 'while' '(' Expression ')' Statement
ReturnStmt   → 'return' Expression? ';'
Block        → '{' Statement* '}'
ExprStmt     → Expression ';'

// Expressions (stratified by precedence, lowest to highest)
Expression     → Assignment                                    // Level 1 (lowest)
Assignment     → LogicalOr ('=' Assignment)?                   // Level 2
LogicalOr      → LogicalAnd ('||' LogicalAnd)*                // Level 3
LogicalAnd     → Equality ('&&' Equality)*                    // Level 4
Equality       → Comparison (('==' | '!=') Comparison)*       // Level 5
Comparison     → Addition (('<' | '>' | '<=' | '>=') Addition)* // Level 6
Addition       → Multiplication (('+' | '-') Multiplication)* // Level 7
Multiplication → Unary (('*' | '/') Unary)*                  // Level 8
Unary          → ('!' | '-') Unary | Primary                 // Level 9
Primary        → Literal | ID | FunctionCall | '(' Expression ')' // Level 10 (highest)

// Function calls
FunctionCall → ID '(' ArgList? ')'
ArgList      → Expression (',' Expression)*

// Literals
Literal → INT | FLOAT | STRING | BOOL
```

**Properties:**
- **LL(1) for statements:** First token uniquely determines type
- **LL(2) for expressions:** Sometimes need 2-token lookahead (assignment vs. expression)
- **No left recursion:** All handled via loops or right recursion
- **Precedence via nesting:** Lower precedence = higher in grammar

---

## Statement Parsing: The Dispatcher Pattern

### Core Principle

**Statements don't compose like expressions.** Each statement type is distinct. We use a **dispatcher** to route to the right parser.

### Implementation

```python
def parse_statement(self):
    """
    Statement → VarDecl | IfStmt | WhileStmt | ReturnStmt | Block | ExprStmt
    
    Dispatcher: Look at first token to determine statement type.
    """
    # Each keyword uniquely identifies statement type (LL(1))
    if self.match(VAR):
        return self.parse_var_declaration()
    
    elif self.match(IF):
        return self.parse_if_statement()
    
    elif self.match(WHILE):
        return self.parse_while_statement()
    
    elif self.match(RETURN):
        return self.parse_return_statement()
    
    elif self.match(LBRACE):  # '{'
        return self.parse_block()
    
    else:
        # Default: expression statement (or assignment)
        return self.parse_expression_statement()
```

**Why this works:**
- Keywords (`var`, `if`, `while`, `return`) are **reserved**—can't be used as identifiers
- First token **uniquely determines** statement type
- No backtracking needed

**Chess analogy:** Like identifying piece type from first letter in algebraic notation (N=knight, B=bishop, etc.).

---

### Variable Declarations

```python
def parse_var_declaration(self):
    """
    VarDecl → 'var' ID ('=' Expression)? ';'
    
    Examples:
        var x;           // No initializer
        var y = 10;      // With initializer
    """
    self.expect(VAR)  # Consume 'var'
    
    name = self.expect(ID).value
    
    # Check for redeclaration in current scope
    if name in self.scopes[-1]:
        self.error(f"Variable '{name}' already declared in this scope")
    
    # Mark as declared
    self.scopes[-1][name] = True
    
    # Optional initializer
    initializer = None
    if self.match(ASSIGN):
        self.advance()
        initializer = self.parse_expression()
    
    self.expect(SEMICOLON)
    
    return VarDeclaration(name, initializer)
```

**Key points:**
- Initializer is **optional** (`('=' Expression)?` in grammar)
- We track declarations in **current scope** to catch redeclarations early
- Semicolon is **required** (unlike some languages with ASI)

---

### If Statements

```python
def parse_if_statement(self):
    """
    IfStmt → 'if' '(' Expression ')' Statement ('else' Statement)?
    
    Examples:
        if (x > 0) { return x; }
        if (x > 0) { return x; } else { return -x; }
    """
    self.expect(IF)
    self.expect(LPAREN)
    
    condition = self.parse_expression()
    
    self.expect(RPAREN)
    
    then_branch = self.parse_statement()
    
    # Optional else clause
    else_branch = None
    if self.match(ELSE):
        self.advance()
        else_branch = self.parse_statement()
    
    return IfStatement(condition, then_branch, else_branch)
```

**Important details:**
- **Parentheses required** around condition (unlike Python, Ruby)
- **No braces required** around branches (can be single statement)
- Else clause is **optional**
- Note: This has the classic **dangling else** ambiguity (see below)

---

### The Dangling Else Problem

**Ambiguous code:**
```
if (a)
    if (b)
        x = 1;
    else
        x = 2;
```

**Question:** Which `if` does the `else` match?

**Possible interpretations:**
```
// Interpretation 1: else matches inner if
if (a) {
    if (b)
        x = 1;
    else
        x = 2;
}

// Interpretation 2: else matches outer if
if (a) {
    if (b)
        x = 1;
}
else
    x = 2;
```

**Resolution:** Our parser **always matches else with nearest if** (greedy matching).

**Why?** When we parse the inner `if` statement, we check for `else` before returning. This means else is consumed by innermost `if`.

**Grammar:** LL(1) grammar **prefers greedy match**. Most languages (C, Java, JavaScript) follow this rule.

**Solution if you want different behavior:** Require braces, or use explicit `fi` / `endif` keywords (like Ruby, Bash).

---

### While Loops

```python
def parse_while_statement(self):
    """
    WhileStmt → 'while' '(' Expression ')' Statement
    
    Example:
        while (n > 0) {
            n = n - 1;
        }
    """
    self.expect(WHILE)
    self.expect(LPAREN)
    
    condition = self.parse_expression()
    
    self.expect(RPAREN)
    
    body = self.parse_statement()
    
    return WhileStatement(condition, body)
```

**Note:** Body is a **statement**, which can be a block. This allows:
```
while (x > 0) {
    x = x - 1;
}
```

And also (though usually bad style):
```
while (x > 0)
    x = x - 1;
```

---

### Return Statements

```python
def parse_return_statement(self):
    """
    ReturnStmt → 'return' Expression? ';'
    
    Examples:
        return;          // Return from void function
        return 42;       // Return value
    """
    self.expect(RETURN)
    
    # Optional return value
    value = None
    if not self.match(SEMICOLON):
        value = self.parse_expression()
    
    self.expect(SEMICOLON)
    
    return ReturnStatement(value)
```

**Design choice:** Allow `return;` with no value (for void functions).

**Alternative:** Require `return void;` or `return null;` explicitly.

---

### Blocks and Scoping

```python
def parse_block(self):
    """
    Block → '{' Statement* '}'
    
    Creates new scope for contained statements.
    """
    self.expect(LBRACE)
    
    # Enter new scope
    self.enter_scope()
    
    statements = []
    while not self.match(RBRACE) and not self.at_end():
        statements.append(self.parse_statement())
    
    self.expect(RBRACE)
    
    # Exit scope
    self.exit_scope()
    
    return Block(statements)

def enter_scope(self):
    """Push new scope onto stack"""
    self.scopes.append({})

def exit_scope(self):
    """Pop current scope from stack"""
    self.scopes.pop()
```

**Scope tracking:**
- Each block creates **new scope**
- Variable declarations add to **current scope** (top of stack)
- When block exits, scope is **popped** (variables go out of scope)

**What this enables:**
```python
{
    var x = 1;
    {
        var x = 2;  // OK! Different scope
    }
    // x is still 1 here
}
```

**What it prevents:**
```python
{
    var x = 1;
    var x = 2;  // ERROR! Already declared in this scope
}
```

**Limitation:** We only track **declarations**, not **usage**. Full semantic analysis (later phase) will check for undefined variables.

---

### Expression Statements

```python
def parse_expression_statement(self):
    """
    ExprStmt → Expression ';'
    
    Examples:
        x + 3;           // Expression statement (weird but legal)
        foo();           // Function call
        x = 5;           // Assignment (assignment is expression!)
    """
    expr = self.parse_expression()
    self.expect(SEMICOLON)
    return ExpressionStatement(expr)
```

**Key insight:** In our language, **assignments are expressions**, not statements. This means:
```python
x = y = z = 0;  // Chain assignments (right-associative)
if ((x = getInput()) != 0) { ... }  // Assignment in condition
```

**Trade-off:**
- **Pro:** Flexible, expressive (like C, Java)
- **Con:** Easy to write `if (x = 0)` when you meant `if (x == 0)` (assignment vs. comparison)

**Alternative:** Make assignment a statement (like Pascal, Go). Forces clearer code but less flexible.

---

## Expression Parsing: Stratification in Practice

### The Precedence Ladder

**Lowest precedence (binds loosely):**
```
Assignment     =
LogicalOr      ||
LogicalAnd     &&
Equality       == !=
Comparison     < > <= >=
Addition       + -
Multiplication * /
Unary          ! -
Primary        literals, identifiers, function calls, grouping
```
**Highest precedence (binds tightly)**

**Each level:**
1. Calls next level down (higher precedence)
2. Handles its own operators
3. Returns result

**Example call chain for `2 + 3 * 4`:**
```
parse_expression()
  → parse_assignment()
    → parse_logical_or()
      → parse_logical_and()
        → parse_equality()
          → parse_comparison()
            → parse_addition()
              [handles '+']
              → parse_multiplication() [left side]
                → parse_unary()
                  → parse_primary()  [returns 2]
              → parse_multiplication() [right side]
                [handles '*']
                → parse_unary()
                  → parse_primary()  [returns 3]
                → parse_unary()
                  → parse_primary()  [returns 4]
                [returns 3 * 4]
              [returns 2 + (3 * 4)]
```

**Result:** Multiplication parsed first (tighter binding), then addition. ✓

---

### Level 1: Assignment (Right-Associative)

```python
def parse_assignment(self):
    """
    Assignment → LogicalOr ('=' Assignment)?
    
    Right-associative! x = y = 3 means x = (y = 3)
    """
    node = self.parse_logical_or()
    
    if self.match(ASSIGN):
        self.advance()
        # Right recursion for right associativity
        right = self.parse_assignment()
        node = Assignment(node, right)
    
    return node
```

**Why right recursion?**

Compare left-associative (loop):
```python
while self.match(PLUS):
    # x + y + z → (x + y) + z
```

Versus right-associative (recursion):
```python
if self.match(ASSIGN):
    right = self.parse_assignment()
    # x = y = z → x = (y = z)
```

**Result:**
- `x + y + z` → `((x + y) + z)` — Left-associative via loop
- `x = y = z` → `x = (y = z)` — Right-associative via recursion

---

### Levels 2-6: Binary Operators (Left-Associative)

**Pattern (same for ||, &&, ==, <, +, *):**

```python
def parse_LEVEL(self):
    """
    LEVEL → NEXT_LEVEL (OP NEXT_LEVEL)*
    
    Left-associative via loop.
    """
    node = self.parse_NEXT_LEVEL()
    
    while self.match(OP1, OP2, ...):
        op = self.current_token.type
        self.advance()
        right = self.parse_NEXT_LEVEL()
        node = BinaryOp(op, node, right)
    
    return node
```

**Example: Addition**

```python
def parse_addition(self):
    """
    Addition → Multiplication (('+' | '-') Multiplication)*
    """
    node = self.parse_multiplication()
    
    while self.match(PLUS, MINUS):
        op = self.current_token.type
        self.advance()
        right = self.parse_multiplication()
        node = BinaryOp(op, node, right)
    
    return node
```

**Trace for `2 + 3 - 4`:**
```
node = parse_multiplication() → 2
match(PLUS) → true
  op = PLUS
  right = parse_multiplication() → 3
  node = BinaryOp(PLUS, 2, 3)  → (2 + 3)
match(MINUS) → true
  op = MINUS
  right = parse_multiplication() → 4
  node = BinaryOp(MINUS, (2 + 3), 4)  → ((2 + 3) - 4)
return node
```

**Result:** `((2 + 3) - 4)` — Left-associative ✓

---

### Level 9: Unary Operators

```python
def parse_unary(self):
    """
    Unary → ('!' | '-') Unary | Primary
    
    Right-associative (naturally via recursion).
    """
    if self.match(BANG, MINUS):
        op = self.current_token.type
        self.advance()
        operand = self.parse_unary()  # Right recursion
        return UnaryOp(op, operand)
    
    return self.parse_primary()
```

**Why right-associative?**

`!!x` should parse as `!(!x)`, not `(!)!x` (which doesn't make sense).

**Recursion enables:** Chained unary ops bind right-to-left.

---

### Level 10: Primary Expressions

```python
def parse_primary(self):
    """
    Primary → Literal | Identifier | FunctionCall | '(' Expression ')'
    
    Handles atoms and function calls.
    """
    # Literals
    if self.match(INT):
        value = self.current_token.value
        self.advance()
        return IntLiteral(value)
    
    if self.match(FLOAT):
        value = self.current_token.value
        self.advance()
        return FloatLiteral(value)
    
    if self.match(STRING):
        value = self.current_token.value
        self.advance()
        return StringLiteral(value)
    
    if self.match(TRUE, FALSE):
        value = self.current_token.type == TRUE
        self.advance()
        return BoolLiteral(value)
    
    # Identifier or function call
    if self.match(ID):
        name = self.current_token.value
        self.advance()
        
        # Check for function call
        if self.match(LPAREN):
            return self.parse_function_call(name)
        else:
            return Identifier(name)
    
    # Grouping
    if self.match(LPAREN):
        self.advance()
        expr = self.parse_expression()  # Full recursion!
        self.expect(RPAREN)
        return expr
    
    self.error("Expected expression")
```

**Key decision point:** When we see identifier, we peek ahead:
- If next token is `(`, it's a **function call**
- Otherwise, it's just an **identifier**

This is **LL(2)** — we need to look 2 tokens ahead (ID + LPAREN) to distinguish.

---

## Function Parsing

### Function Declarations

```python
def parse_function_decl(self):
    """
    FunctionDecl → 'fn' ID '(' ParamList? ')' Block
    ParamList → ID (',' ID)*
    
    Example:
        fn factorial(n) {
            if (n <= 1) {
                return 1;
            } else {
                return n * factorial(n - 1);
            }
        }
    """
    self.expect(FN)
    
    name = self.expect(ID).value
    
    self.expect(LPAREN)
    
    # Parse parameter list
    params = []
    if not self.match(RPAREN):
        params.append(self.expect(ID).value)
        while self.match(COMMA):
            self.advance()
            params.append(self.expect(ID).value)
    
    self.expect(RPAREN)
    
    # Function body is always a block
    body = self.parse_block()
    
    return FunctionDecl(name, params, body)
```

**Design choices:**
- Function body **must** be block (can't be single expression)
- Parameters are just names (no types—this is dynamically typed language)
- No return type annotation

**Extension:** Could add type annotations: `fn add(x: int, y: int) -> int { ... }`

---

### Function Calls

```python
def parse_function_call(self, name):
    """
    FunctionCall → ID '(' ArgList? ')'
    ArgList → Expression (',' Expression)*
    
    Called from parse_primary when we've seen ID '('.
    
    Examples:
        foo()
        add(2, 3)
        factorial(n - 1)
    """
    self.expect(LPAREN)  # Already matched, now consume
    
    # Parse argument list
    args = []
    if not self.match(RPAREN):
        args.append(self.parse_expression())
        while self.match(COMMA):
            self.advance()
            args.append(self.parse_expression())
    
    self.expect(RPAREN)
    
    return FunctionCall(name, args)
```

**Pattern for comma-separated lists:**
```python
if not empty:
    parse first item
    while match(COMMA):
        advance
        parse next item
```

This pattern works for:
- Function parameters
- Function arguments
- Array initializers
- etc.

---

## Lookahead and Disambiguation

### The Assignment vs. Expression Problem

**Ambiguous input:**
```python
x;       // Just an identifier expression
x = 5;   // Assignment
```

Both start with identifier. How to distinguish?

**Solution: Look ahead after identifier**

```python
def parse_expression_statement(self):
    """Handle expression statements (including assignments)"""
    
    # Check for assignment pattern: ID '='
    if self.match(ID):
        # Save position for potential backtrack
        saved_pos = self.position
        name = self.current_token.value
        self.advance()
        
        if self.match(ASSIGN):
            # It's an assignment!
            self.advance()
            value = self.parse_expression()
            self.expect(SEMICOLON)
            # Assignment is expression, wrap in statement
            return ExpressionStatement(Assignment(Identifier(name), value))
        else:
            # Not assignment, backtrack and parse as expression
            self.position = saved_pos
            self.current_token = self.tokens[self.position]
    
    # Regular expression statement
    expr = self.parse_expression()
    self.expect(SEMICOLON)
    return ExpressionStatement(expr)
```

**Alternative approach:** Since assignment is expression in our grammar, we can parse it in `parse_assignment()` and don't need special case in statement parser.

---

### When to Commit vs. Backtrack

**Guidelines:**

1. **Commit when grammar is LL(1)**
   - First token uniquely determines production
   - No backtracking needed
   - Example: Statement dispatcher (keywords are unique)

2. **Peek when grammar is LL(2)**
   - Need to look ahead 2 tokens to decide
   - Example: ID followed by '(' → function call

3. **Backtrack when LL(k) fails**
   - Try one interpretation, backtrack if wrong
   - Expensive! Avoid in hot paths
   - Example: Some parsers backtrack on assignment vs. expression

**Real compilers:** Most are LL(1) or LR(1), rarely backtrack. If backtracking is needed frequently, grammar needs refactoring.

**Chess analogy:** Like search depth—minimal lookahead (LL(1)) is fast but may miss patterns. Deep lookahead (backtracking) is slow but handles complex positions.

---

## AST Node Definitions

### Expression Nodes

```python
class IntLiteral:
    def __init__(self, value):
        self.value = value  # int

class FloatLiteral:
    def __init__(self, value):
        self.value = value  # float

class StringLiteral:
    def __init__(self, value):
        self.value = value  # string

class BoolLiteral:
    def __init__(self, value):
        self.value = value  # bool

class Identifier:
    def __init__(self, name):
        self.name = name  # string

class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op        # operator type (PLUS, MINUS, etc.)
        self.left = left    # Expression
        self.right = right  # Expression

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op        # operator type (BANG, MINUS)
        self.operand = operand  # Expression

class Assignment:
    def __init__(self, target, value):
        self.target = target  # Expression (usually Identifier)
        self.value = value    # Expression

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name          # string
        self.arguments = arguments  # List[Expression]
```

---

### Statement Nodes

```python
class VarDeclaration:
    def __init__(self, name, initializer):
        self.name = name              # string
        self.initializer = initializer  # Expression or None

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression  # Expression

class IfStatement:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition      # Expression
        self.then_branch = then_branch  # Statement
        self.else_branch = else_branch  # Statement or None

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition  # Expression
        self.body = body            # Statement

class ReturnStatement:
    def __init__(self, value):
        self.value = value  # Expression or None

class Block:
    def __init__(self, statements):
        self.statements = statements  # List[Statement]
```

---

### Program Nodes

```python
class FunctionDecl:
    def __init__(self, name, parameters, body):
        self.name = name            # string
        self.parameters = parameters  # List[string]
        self.body = body            # Block

class Program:
    def __init__(self, functions, statements):
        self.functions = functions    # List[FunctionDecl]
        self.statements = statements  # List[Statement]
```

---

## Complete Example

### Input Program

```python
fn factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() {
    var result = factorial(5);
    return result;
}
```

### Resulting AST (simplified)

```
Program
├─ FunctionDecl: factorial
│  ├─ Parameters: [n]
│  └─ Body: Block
│     └─ IfStatement
│        ├─ Condition: BinaryOp(<=, Identifier(n), IntLiteral(1))
│        ├─ Then: Block
│        │  └─ ReturnStatement(IntLiteral(1))
│        └─ Else: Block
│           └─ ReturnStatement
│              └─ BinaryOp(*,
│                    Identifier(n),
│                    FunctionCall(factorial, [BinaryOp(-, Identifier(n), IntLiteral(1))]))
│
└─ FunctionDecl: main
   ├─ Parameters: []
   └─ Body: Block
      ├─ VarDeclaration: result
      │  └─ Initializer: FunctionCall(factorial, [IntLiteral(5)])
      └─ ReturnStatement(Identifier(result))
```

**Depth:** 9 levels (Program → Function → Block → Statement → Expression → ... → Literal)

**Node count:** ~25 nodes for this small program

---

## Testing Strategy

### Test Categories

1. **Expression tests** — Precedence and associativity
2. **Statement tests** — Each statement type
3. **Function tests** — Declarations and calls
4. **Scoping tests** — Block scopes and shadowing
5. **Error tests** — Malformed input
6. **Integration tests** — Complete programs

---

### Expression Tests

```python
def test_precedence():
    """Verify operator precedence"""
    
    # Multiplication binds tighter than addition
    ast = parse("2 + 3 * 4")
    assert isinstance(ast, BinaryOp)
    assert ast.op == PLUS
    assert isinstance(ast.right, BinaryOp)
    assert ast.right.op == MULT
    
    # Parentheses override precedence
    ast = parse("(2 + 3) * 4")
    assert isinstance(ast, BinaryOp)
    assert ast.op == MULT
    assert isinstance(ast.left, BinaryOp)
    assert ast.left.op == PLUS

def test_associativity():
    """Verify operator associativity"""
    
    # Addition is left-associative
    ast = parse("1 + 2 + 3")
    assert isinstance(ast, BinaryOp)
    assert ast.op == PLUS
    assert isinstance(ast.left, BinaryOp)  # (1 + 2) on left
    
    # Assignment is right-associative
    ast = parse("x = y = 3")
    assert isinstance(ast, Assignment)
    assert isinstance(ast.value, Assignment)  # (y = 3) on right
```

---

### Statement Tests

```python
def test_if_statement():
    code = """
    if (x > 0) {
        return x;
    } else {
        return -x;
    }
    """
    ast = parse(code)
    assert isinstance(ast, IfStatement)
    assert isinstance(ast.condition, BinaryOp)
    assert isinstance(ast.then_branch, Block)
    assert isinstance(ast.else_branch, Block)

def test_while_statement():
    code = """
    while (n > 0) {
        n = n - 1;
    }
    """
    ast = parse(code)
    assert isinstance(ast, WhileStatement)
    assert isinstance(ast.condition, BinaryOp)
    assert isinstance(ast.body, Block)

def test_var_declaration():
    code = "var x = 10;"
    ast = parse(code)
    assert isinstance(ast, VarDeclaration)
    assert ast.name == "x"
    assert isinstance(ast.initializer, IntLiteral)
    assert ast.initializer.value == 10
```

---

### Function Tests

```python
def test_function_declaration():
    code = """
    fn add(x, y) {
        return x + y;
    }
    """
    ast = parse(code)
    assert isinstance(ast, FunctionDecl)
    assert ast.name == "add"
    assert ast.parameters == ["x", "y"]
    assert isinstance(ast.body, Block)

def test_function_call():
    code = "add(2, 3)"
    ast = parse(code)
    assert isinstance(ast, FunctionCall)
    assert ast.name == "add"
    assert len(ast.arguments) == 2
    assert isinstance(ast.arguments[0], IntLiteral)
    assert isinstance(ast.arguments[1], IntLiteral)

def test_recursive_function():
    code = """
    fn factorial(n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }
    """
    ast = parse(code)
    assert isinstance(ast, FunctionDecl)
    # ... verify recursive call in else branch
```

---

### Scoping Tests

```python
def test_nested_scopes():
    code = """
    {
        var x = 1;
        {
            var x = 2;  // OK! Different scope
        }
    }
    """
    ast = parse(code)  # Should succeed

def test_redeclaration_error():
    code = """
    {
        var x = 1;
        var x = 2;  // ERROR! Same scope
    }
    """
    with pytest.raises(ParseError):
        parse(code)
```

---

### Error Tests

```python
def test_missing_semicolon():
    code = "var x = 10"  # Missing semicolon
    with pytest.raises(ParseError):
        parse(code)

def test_unmatched_paren():
    code = "if (x > 0 { }"  # Missing ')'
    with pytest.raises(ParseError):
        parse(code)

def test_unexpected_token():
    code = "if x > 0 { }"  # Missing parens around condition
    with pytest.raises(ParseError):
        parse(code)
```

---

## Design Patterns Summary

### Pattern 1: Grammar Rule → Function

**Every non-terminal becomes a function.**

```
Expr → Term ('+' Term)*
```
↓
```python
def parse_expr(self):
    node = self.parse_term()
    while self.match(PLUS):
        self.advance()
        right = self.parse_term()
        node = BinaryOp(PLUS, node, right)
    return node
```

---

### Pattern 2: Choice → if/elif

**Alternatives become conditional branches.**

```
Factor → INT | ID | '(' Expr ')'
```
↓
```python
def parse_factor(self):
    if self.match(INT):
        ...
    elif self.match(ID):
        ...
    elif self.match(LPAREN):
        ...
```

---

### Pattern 3: Repetition → Loop

**Kleene star becomes while loop.**

```
Expr → Term ('+' Term)*
```
↓
```python
while self.match(PLUS):
    self.advance()
    right = self.parse_term()
    node = BinaryOp(PLUS, node, right)
```

---

### Pattern 4: Optional → if

**Optional element becomes conditional.**

```
IfStmt → 'if' '(' Expr ')' Stmt ('else' Stmt)?
```
↓
```python
if self.match(ELSE):
    self.advance()
    else_branch = self.parse_statement()
```

---

### Pattern 5: Sequence → Sequential Calls

**Concatenation becomes sequential code.**

```
IfStmt → 'if' '(' Expr ')' Stmt
```
↓
```python
self.expect(IF)
self.expect(LPAREN)
expr = self.parse_expr()
self.expect(RPAREN)
stmt = self.parse_statement()
```

---

## Common Pitfalls

### Pitfall 1: Left Recursion

**Problem:**
```
Expr → Expr '+' Term  // Left recursion!
```

**Why it breaks:**
```python
def parse_expr(self):
    node = self.parse_expr()  # Infinite recursion!
    ...
```

**Solution:** Eliminate left recursion:
```
Expr → Term ('+' Term)*
```

---

### Pitfall 2: Ambiguous Grammar

**Problem:**
```
Expr → Expr '+' Expr  // Which way to associate?
```

**Input:** `1 + 2 + 3`

**Ambiguous parse trees:**
```
   +              +
  / \            / \
 1   +    OR    +   3
    / \        / \
   2   3      1   2
```

**Solution:** Use stratified grammar with explicit associativity.

---

### Pitfall 3: Forgetting to Advance

**Problem:**
```python
if self.match(PLUS):
    # Forgot to call advance()!
    right = self.parse_term()
```

**Result:** Infinite loop (keeps matching same PLUS token).

**Solution:** Always `advance()` after `match()`.

---

### Pitfall 4: Wrong Precedence Level

**Problem:**
```python
def parse_addition(self):
    node = self.parse_primary()  # Should call parse_multiplication()!
    while self.match(PLUS):
        ...
```

**Result:** `2 + 3 * 4` parses incorrectly (multiplication not recognized).

**Solution:** Each level calls **next higher precedence** level.

---

## Performance Characteristics

### Time Complexity

**Best case:** O(n) where n = number of tokens
- Each token consumed exactly once
- No backtracking in well-designed LL(1) grammar

**Worst case:** O(n²) or worse
- Excessive backtracking
- Happens when grammar is not LL(k)

**Typical:** O(n) for production parsers

---

### Space Complexity

**Call stack:** O(d) where d = maximum nesting depth
- Each function call adds frame
- Deeply nested expressions → deep call stack

**AST size:** O(n) where n = number of nodes
- Each token typically becomes 1-3 AST nodes
- Linear in program size

**Scope stack:** O(s) where s = maximum scope nesting
- Each block adds scope
- Typically small (< 10 scopes deep)

---

### Optimization Opportunities

1. **Token buffering:** Read tokens in batches (reduces I/O)
2. **AST pooling:** Reuse node objects (reduces allocation)
3. **Lazy evaluation:** Don't build full AST for unused functions
4. **Parallel parsing:** Parse independent functions in parallel (requires careful design)

**Real compilers:** Modern compilers (Rust, Swift) use parallel parsing for speed.

---

## Comparison with Other Parsing Techniques

### Recursive Descent (this document)

**Pros:**
- Simple to implement
- Easy to understand and debug
- Good error messages (know exact context)
- Direct grammar → code mapping

**Cons:**
- Requires LL(k) grammar (no left recursion)
- Manual implementation for each grammar
- Backtracking can be slow

---

### Parser Generators (Yacc, Bison, ANTLR)

**Pros:**
- Generate parser from grammar spec
- Handle LR grammars (more powerful than LL)
- Well-tested implementations

**Cons:**
- Learning curve for grammar syntax
- Generated code is harder to debug
- Error messages can be cryptic
- Less control over AST construction

---

### PEG Parsers (Parsing Expression Grammars)

**Pros:**
- Ordered choice (no ambiguity)
- Support left recursion (with memoization)
- Composable (can define grammar incrementally)

**Cons:**
- Exponential worst case (requires memoization)
- Harder to reason about performance
- Less commonly taught

---

### LR Parsers (Bottom-Up)

**Pros:**
- More powerful (handle more grammars)
- Used in production (GCC, Clang use variants)
- Deterministic

**Cons:**
- Complex to implement by hand
- Usually generated by tool
- Error recovery is harder
- Less intuitive than top-down

---

## Production Use

### Languages Using Recursive Descent

- **Python:** Hand-written recursive descent (since Python 3.9, switched from LL(1) parser generator)
- **Go:** Hand-written recursive descent
- **TypeScript:** Hand-written recursive descent
- **Lua:** Hand-written recursive descent
- **JSON parsers:** Almost all use recursive descent

### Why It's Popular

1. **Simplicity:** Easy to implement and maintain
2. **Performance:** O(n) for well-designed grammars
3. **Error messages:** Direct control over error reporting
4. **Flexibility:** Easy to add custom logic (semantic checks during parsing)

### When to Use Something Else

- Grammar has left recursion that's hard to eliminate
- Need to support ambiguous grammar (use GLR)
- Want to experiment with grammar quickly (use parser generator)
- Performance is critical and grammar is complex (use LR parser)

---

## Exercises

### Exercise 1: Add For Loops

**Extend grammar:**
```
ForStmt → 'for' '(' VarDecl Expr ';' Expr ')' Stmt
```

**Example:**
```
for (var i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Implementation:**
1. Add `parse_for_statement()` function
2. Add ForStatement AST node
3. Update statement dispatcher
4. Add tests

---

### Exercise 2: Add Ternary Operator

**Extend grammar:**
```
Conditional → LogicalOr ('?' Expression ':' Conditional)?
```

**Example:**
```
var max = x > y ? x : y;
```

**Challenge:** Where does ternary fit in precedence hierarchy?

---

### Exercise 3: Add Array Literals

**Extend grammar:**
```
Primary → ... | '[' ExprList? ']'
ExprList → Expr (',' Expr)*
```

**Example:**
```
var nums = [1, 2, 3, 4, 5];
```

**Implementation:**
1. Add ArrayLiteral AST node
2. Handle empty arrays: `[]`
3. Add tests for nested arrays: `[[1, 2], [3, 4]]`

---

### Exercise 4: Add Break/Continue

**Extend grammar:**
```
Statement → ... | BreakStmt | ContinueStmt
BreakStmt → 'break' ';'
ContinueStmt → 'continue' ';'
```

**Challenge:** How to detect `break` outside of loop? (Hint: Track loop nesting depth during parsing.)

---

## Summary

**What we built:**
- Complete recursive descent parser for real programming language
- 600 lines of Python
- 17 AST node types
- 9 expression precedence levels
- Statement types: var, if, while, return, block
- Function declarations and calls
- Minimal scope tracking

**Key techniques:**
- Grammar stratification for precedence
- Dispatcher pattern for statements
- Lookahead for disambiguation
- Recursion for right-associativity
- Loops for left-associativity

**Performance:**
- O(n) time for well-designed grammar
- O(d) space for call stack
- Production-ready

**Next steps:**
- Error recovery (tomorrow)
- Semantic analysis (next week)
- Code generation (Week 8-9)

---

## References

### Books
- **"Crafting Interpreters"** by Robert Nystrom — Excellent recursive descent implementation
- **"Engineering a Compiler"** (Cooper & Torczon) — Chapter 3 on parsing
- **"Modern Compiler Implementation in ML"** (Appel) — Chapter 3 on LL parsing

### Online Resources
- Python grammar: https://docs.python.org/3/reference/grammar.html
- Go grammar: https://go.dev/ref/spec
- TypeScript parser source: https://github.com/microsoft/TypeScript

### Tools
- ANTLR — Parser generator supporting LL(*) grammars
- PEG.js — JavaScript PEG parser generator
- Tree-sitter — Incremental parsing library (used in editors)
