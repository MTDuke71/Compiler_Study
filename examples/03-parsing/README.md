# Recursive Descent Implementation Basics

**Training Document — Week 5, Day 2**  
**Date:** January 27, 2026  
**Topic:** Grammar to Code Translation

---

## Overview

This document covers the **mechanical translation** of grammar rules into working parser code. By the end, you'll understand how each grammar construct maps to a specific code pattern.

**Key principle:** Recursive descent parsing is **systematic**, not magical. Follow the patterns, and the code writes itself.

---

## The Core Patterns

### Pattern 1: Non-Terminal → Function

**Grammar rule:**
```
Expr → Term (('+' | '-') Term)*
```

**Code:**
```python
def parse_expr(self):
    """Expr → Term (('+' | '-') Term)*"""
    # Implementation here
```

**Convention:**
- Function name: `parse_` + lowercase(non-terminal)
- Docstring: grammar rule for reference
- Returns: AST node representing this construct

---

### Pattern 2: Terminal → match() + advance()

**Grammar fragment:** `'+'`

**Code:**
```python
if self.match(PLUS):
    self.advance()
```

**For required terminals:**
```python
self.expect(PLUS)  # match + advance + error if no match
```

**Key methods:**
- `match(type)`: Check current token type (lookahead), don't consume
- `advance()`: Consume current token, move to next
- `expect(type)`: Match + advance in one step, error if doesn't match

---

### Pattern 3: Sequence (α β γ) → Sequential Calls

**Grammar:** `'if' '(' Expr ')' Block`

**Code:**
```python
self.expect(IF)          # α: 'if'
self.expect(LPAREN)      # β: '('
cond = self.parse_expr() # γ: Expr
self.expect(RPAREN)      # δ: ')'
body = self.parse_block()# ε: Block
return IfStatement(cond, body)
```

**Pattern:** Process left to right, building components.

---

### Pattern 4: Choice (α | β | γ) → if/elif/else

**Grammar:** `Factor → INT | ID | '(' Expr ')'`

**Code:**
```python
def parse_factor(self):
    if self.match(INT):        # First alternative
        # Parse INT
    elif self.match(ID):       # Second alternative
        # Parse ID
    elif self.match(LPAREN):   # Third alternative
        # Parse '(' Expr ')'
    else:                      # No alternative matched
        self.error("Expected factor")
```

**Decision:** Based on lookahead (first token of each alternative).

**Requirement:** Alternatives must have disjoint first sets (LL(1) property).

---

### Pattern 5: Repetition (α*) → while Loop

**Grammar:** `(('+' | '-') Term)*`

**Code:**
```python
while self.match(PLUS) or self.match(MINUS):
    op = self.current_token.value
    self.advance()
    right = self.parse_term()
    left = BinaryOp(op, left, right)  # Build AST
```

**Pattern:**
- Loop condition: lookahead matches start of repeated element
- Loop body: parse one instance of repeated element
- Exit: when lookahead doesn't match

**Left-associativity trick:** Reassign `left` each iteration to build left-associative tree.

---

### Pattern 6: Optional (α?) → if Statement

**Grammar:** `ElsePart → 'else' Block | ε`

**Code:**
```python
else_block = None  # Default (ε case)
if self.match(ELSE):
    self.expect(ELSE)
    else_block = self.parse_block()
```

**Pattern:** Check if optional part present; if so, parse it. Otherwise, use default (often `None`).

---

## Complete Example: Expression Parser

### Grammar

```
Expr   → Term (('+' | '-') Term)*
Term   → Factor (('*' | '/') Factor)*
Factor → INT | ID | '(' Expr ')'
```

**Properties:**
- No left recursion (safe for RD)
- Precedence: Factor > Term > Expr (multiplication before addition)
- Associativity: Left (via iteration)

---

### Parser Implementation

```python
class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else Token(EOF, None, 0, 0)
    
    # Core operations
    
    def match(self, token_type):
        """Check if current token matches type (lookahead)"""
        return self.current_token.type == token_type
    
    def advance(self):
        """Consume current token and move to next"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(EOF, None, 0, 0)
    
    def expect(self, token_type):
        """Consume token if it matches, else error"""
        if not self.match(token_type):
            raise ParseError(f"Expected {token_type}, got {self.current_token.type}")
        self.advance()
    
    # Grammar productions
    
    def parse_expr(self):
        """Expr → Term (('+' | '-') Term)*"""
        left = self.parse_term()
        
        while self.match(PLUS) or self.match(MINUS):
            op = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self.advance()
            right = self.parse_term()
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_term(self):
        """Term → Factor (('*' | '/') Factor)*"""
        left = self.parse_factor()
        
        while self.match(STAR) or self.match(SLASH):
            op = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(op, left, right, line, col)
        
        return left
    
    def parse_factor(self):
        """Factor → INT | ID | '(' Expr ')'"""
        if self.match(INT):
            value = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self.advance()
            return IntLiteral(value, line, col)
        
        elif self.match(ID):
            name = self.current_token.value
            line, col = self.current_token.line, self.current_token.col
            self.advance()
            return Identifier(name, line, col)
        
        elif self.match(LPAREN):
            self.advance()
            expr = self.parse_expr()  # Recursion!
            self.expect(RPAREN)
            return expr
        
        else:
            raise ParseError("Expected factor (INT, ID, or '(')")
```

---

## Execution Trace: Understanding the Flow

### Input: `3 + 4 * 5`

**Tokens:**
```
[INT(3), PLUS, INT(4), STAR, INT(5), EOF]
```

**Execution steps:**

```
parse_expr()
│
├─ parse_term()  ← Parse first operand
│  ├─ parse_factor()
│  │  └─ match(INT) → IntLiteral(3)
│  └─ match(STAR/SLASH) → no
│  return IntLiteral(3)
│
├─ match(PLUS/MINUS) → yes (PLUS)
├─ advance() → consume PLUS
│
├─ parse_term()  ← Parse second operand
│  │
│  ├─ parse_factor()
│  │  └─ match(INT) → IntLiteral(4)
│  │
│  ├─ match(STAR/SLASH) → yes (STAR)
│  ├─ advance() → consume STAR
│  │
│  ├─ parse_factor()
│  │  └─ match(INT) → IntLiteral(5)
│  │
│  └─ Build: BinaryOp('*', IntLiteral(4), IntLiteral(5))
│  return BinaryOp('*', ...)
│
└─ Build: BinaryOp('+', IntLiteral(3), BinaryOp('*', ...))
return BinaryOp('+', ...)
```

**Resulting AST:**
```
       BinaryOp(+)
       /          \
  IntLiteral(3)  BinaryOp(*)
                 /          \
            IntLiteral(4)  IntLiteral(5)
```

**Key observations:**
1. **Precedence enforced by depth:** `*` parsed inside `Term`, deeper than `+`
2. **Left-to-right execution:** First term (3) parsed before seeing `+`
3. **Recursion:** `parse_expr` → `parse_term` → `parse_factor`
4. **AST built bottom-up:** Leaves (literals) created first, then combined into operators

---

## Building AST Nodes: The Return Pattern

**Key principle:** Each parse function returns an AST node.

**Flow:**
1. Parse components (call sub-functions)
2. Each sub-function returns AST node
3. Combine components into parent node
4. Return parent node (propagates up call stack)

**Example:**

```python
def parse_term(self):
    # 1. Parse left operand
    left = self.parse_factor()  # Returns ASTNode
    
    # 2. Loop for remaining operands
    while self.match(STAR) or self.match(SLASH):
        op = self.current_token.value
        line, col = self.current_token.line, self.current_token.col
        self.advance()
        
        # 3. Parse right operand
        right = self.parse_factor()  # Returns ASTNode
        
        # 4. Build parent node
        left = BinaryOp(op, left, right, line, col)
        # Reassigning 'left' builds left-associative tree
    
    # 5. Return result
    return left
```

**Why reassign `left`?**
- First iteration: `left = (a * b)`
- Second iteration: `left = ((a * b) * c)`
- Third iteration: `left = (((a * b) * c) * d)`

**Builds left-associative tree without explicit stack manipulation.**

---

## Backtracking: When LL(1) Isn't Enough

**Scenario:** Grammar has ambiguous lookahead.

**Example:**
```
Stmt → ID '=' Expr ';'    // Assignment
     | ID '(' Args ')'     // Function call
```

Both start with `ID`. Need to look further ahead to decide.

### Solution 1: Left-Factor (Preferred)

```
Stmt → ID StmtTail
StmtTail → '=' Expr ';' | '(' Args ')'
```

Now decision deferred until after parsing `ID`.

### Solution 2: Backtracking (Fallback)

```python
def parse_stmt(self):
    # Save current position
    saved_pos = self.position
    saved_token = self.current_token
    
    try:
        # Try first alternative
        return self.parse_assignment()
    except ParseError:
        # Failed, restore position
        self.position = saved_pos
        self.current_token = saved_token
        
        # Try second alternative
        return self.parse_function_call()
```

**Costs:**
- Re-parsing on failure (slow)
- Complex control flow
- Poor error messages (which attempt failed?)

**Recommendation:** Refactor grammar to avoid backtracking when possible.

---

## Error Handling

### Basic Error Reporting

```python
def error(self, message):
    """Report parse error with location"""
    raise ParseError(
        f"{message}\n"
        f"  at line {self.current_token.line}, col {self.current_token.col}\n"
        f"  got: {self.current_token.type} = {self.current_token.value!r}"
    )
```

**Example output:**
```
ParseError: Expected factor (INT, ID, or '(')
  at line 2, col 10
  got: STAR = '*'
```

### Better: Show Context

```python
def error(self, message):
    # Get surrounding tokens for context
    start = max(0, self.position - 2)
    end = min(len(self.tokens), self.position + 3)
    context = ' '.join(str(t.value) for t in self.tokens[start:end])
    
    raise ParseError(
        f"{message}\n"
        f"  at line {self.current_token.line}, col {self.current_token.col}\n"
        f"  near: ... {context}\n"
        f"  got: {self.current_token.type}"
    )
```

**Output:**
```
ParseError: Expected factor (INT, ID, or '(')
  at line 2, col 10
  near: ... x + * 5 ...
             ^
  got: STAR
```

---

## Testing Strategy

### Test Cases

**1. Simple cases:**
- `3 + 5` → `BinaryOp(+, 3, 5)`
- `x` → `Identifier(x)`

**2. Precedence:**
- `2 + 3 * 4` → `BinaryOp(+, 2, BinaryOp(*, 3, 4))`
- `2 * 3 + 4` → `BinaryOp(+, BinaryOp(*, 2, 3), 4)`

**3. Associativity:**
- `5 - 3 - 1` → `BinaryOp(-, BinaryOp(-, 5, 3), 1)` (left-assoc)

**4. Parentheses:**
- `(2 + 3) * 4` → `BinaryOp(*, BinaryOp(+, 2, 3), 4)`

**5. Complex:**
- `((1 + 2) * (3 + 4))` → deeply nested tree

### Verification Methods

**1. AST structure inspection:**
```python
ast = parser.parse("3 + 4 * 5")
assert isinstance(ast, BinaryOp)
assert ast.op == '+'
assert isinstance(ast.right, BinaryOp)
assert ast.right.op == '*'
```

**2. Evaluation (simple interpreter):**
```python
def evaluate(ast):
    if isinstance(ast, IntLiteral):
        return ast.value
    elif isinstance(ast, BinaryOp):
        left = evaluate(ast.left)
        right = evaluate(ast.right)
        if ast.op == '+': return left + right
        elif ast.op == '*': return left * right
        # ...

assert evaluate(parser.parse("3 + 4 * 5")) == 23
```

**3. Round-trip (parse → print → parse):**
```python
source = "3 + 4 * 5"
ast1 = parser.parse(source)
source2 = ast_to_string(ast1)
ast2 = parser.parse(source2)
assert ast_equal(ast1, ast2)
```

---

## Common Mistakes

### Mistake 1: Not Handling Left Recursion

**Problem:** Grammar has left recursion.
```
Expr → Expr '+' Term  // Infinite loop!
```

**Fix:** Eliminate left recursion.
```
Expr → Term (('+') Term)*
```

### Mistake 2: Forgetting to advance()

**Problem:**
```python
if self.match(PLUS):
    # Forgot to advance!
    right = self.parse_term()
```

**Result:** Parser sees PLUS forever, infinite loop.

**Fix:** Always `advance()` after checking token.

### Mistake 3: Wrong Associativity

**Problem:** Right recursion for left-associative operator.
```python
def parse_expr(self):
    left = self.parse_term()
    if self.match(PLUS):
        self.advance()
        right = self.parse_expr()  # Right recursion!
        return BinaryOp('+', left, right)
    return left
```

**Result:** `a + b + c` parsed as `a + (b + c)` (right-assoc).

**Fix:** Use iteration, not recursion, for left-assoc.

### Mistake 4: Losing Source Location

**Problem:**
```python
return IntLiteral(value)  # No line/col!
```

**Result:** Error messages say "error somewhere" instead of "error at line 5, col 10".

**Fix:** Always capture location from tokens.
```python
line, col = self.current_token.line, self.current_token.col
return IntLiteral(value, line, col)
```

---

## Summary

**Grammar to code patterns:**

| Grammar Construct | Code Pattern |
|-------------------|--------------|
| Non-terminal `A` | `def parse_a(self):` |
| Terminal `'x'` | `self.expect('x')` or `self.match('x') + self.advance()` |
| Sequence `α β` | Sequential calls |
| Choice `α | β` | `if/elif` based on lookahead |
| Repetition `α*` | `while` loop |
| Optional `α?` | `if` statement |

**Key principles:**
1. **One function per non-terminal**
2. **Lookahead drives decisions** (match without consuming)
3. **Build AST bottom-up** (leaves first, combine upward)
4. **Iteration for left-assoc** (reassign left in loop)
5. **Recursion for nesting** (Factor can call Expr)
6. **Always track location** (line/col in AST nodes)

**Next steps:**
- Extend to statements (if/while/return)
- Add declarations (functions, variables)
- Implement error recovery

---

## Further Reading

- [[03-parsing/recursive-descent]] — Theory and advanced topics
- [[03-parsing/trees-vs-structure]] — AST vs CST
- [[03-parsing/precedence-and-associativity]] — Encoding operator precedence
- [[zettel/Z0020-ast-design]] — AST design patterns
- `examples/03-parsing/basic-parser.py` — Complete working code

---

## Exercises

1. **Add modulo operator (`%`):**
   - Same precedence as `*` and `/`
   - Update grammar and parser
   - Test: `10 % 3` → 1

2. **Add unary minus:**
   - Grammar: `Factor → '-' Factor | INT | ...`
   - Right-associative (naturally from recursion)
   - Test: `-(3 + 4)` → -7

3. **Add exponentiation (`**`):**
   - Higher precedence than multiplication
   - Right-associative (unlike other operators)
   - Test: `2 ** 3 ** 2` → 512 (not 64)

4. **Improve error messages:**
   - Show surrounding code context
   - Suggest fixes ("Did you mean ')'?")
   - Multiple errors in one pass (error recovery)

5. **Add tracing:**
   - Print function entry/exit
   - Show current token at each step
   - Visualize call stack depth

---

# Complete Parser Implementation (January 28, 2026)

## New Files: Production-Ready Parser

This directory now contains a **complete recursive descent parser** for a full programming language.

### complete_parser.py (600 lines)

Full implementation with:
- Complete lexer (all tokens, string escapes, position tracking)
- Full parser (expressions + statements + functions)
- 17 AST node types
- 9 expression precedence levels
- Minimal scope tracking
- Example factorial program

### test_complete_parser.py (500 lines)

Comprehensive test suite: **46 tests, all passing ✓**

Coverage:
- Expression precedence/associativity
- All statement types (var, if, while, return, block)
- Function declarations and calls
- Scoping rules (nested scopes, redeclarations)
- Error handling
- Integration tests (complete programs)

## Quick Start

```bash
# Run the parser
python complete_parser.py

# Run tests (expect: 46/46 passed)
python test_complete_parser.py
```

## Language Features

Supports complete programs like:

```python
fn factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

**Complete feature set:**
- Expressions: binary/unary ops, function calls, 9 precedence levels
- Statements: var, if/else, while, return, blocks
- Functions: declarations with params, calls with args, recursion
- Scoping: block-level with redeclaration detection

## Training Document

See [complete-parser-guide.md](../../03-parsing/complete-parser-guide.md) for comprehensive walkthrough (35+ pages covering grammar design, implementation patterns, testing strategy, design decisions).

## Daily Reflection

Session notes: [Daily Notes/2026-01-28.md](../../Daily Notes/2026-01-28.md)

---

**Status:** Complete parser implementation finished  
**Test coverage:** 46/46 passing  
**Next:** Error recovery and diagnostics (Day 4)
