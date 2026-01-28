# Z0021 — Recursive Descent Pattern

## Links
- Up: [[03-parsing/recursive-descent]]
- Related: [[zettel/Z0020-ast-design]] [[zettel/Z0005-compiler-phases]]
- Down: [[examples/03-parsing/basic-parser.py]]

---

## Core Pattern

**One grammar rule → One function**

Each function:
1. Checks lookahead (what token is next?)
2. Decides which production to apply
3. Parses components recursively
4. Builds and returns AST node

---

## The Six Translation Rules

### Rule 1: Non-Terminal → Function

```
Grammar: Expr → ...
Code:    def parse_expr(self): ...
```

### Rule 2: Terminal → match() + advance()

```
Grammar: '+'
Code:    self.expect(PLUS)
```

### Rule 3: Sequence → Sequential Calls

```
Grammar: 'if' '(' Expr ')' Block
Code:    
    self.expect(IF)
    self.expect(LPAREN)
    cond = self.parse_expr()
    self.expect(RPAREN)
    body = self.parse_block()
```

### Rule 4: Choice → if/elif

```
Grammar: A → B | C | D
Code:
    if self.match_first_of_B():
        return self.parse_B()
    elif self.match_first_of_C():
        return self.parse_C()
    else:
        return self.parse_D()
```

### Rule 5: Repetition → while Loop

```
Grammar: A → B*
Code:
    while self.match_first_of_B():
        self.parse_B()
```

### Rule 6: Optional → if Statement

```
Grammar: A → B?
Code:
    if self.match_first_of_B():
        self.parse_B()
```

---

## Left-Associativity Trick

**Pattern for left-associative operators:**

```python
def parse_expr(self):
    left = self.parse_term()
    
    while self.match(PLUS):
        self.advance()
        right = self.parse_term()
        left = BinaryOp('+', left, right)  # Reassign!
    
    return left
```

**Key:** Reassigning `left` in loop builds left-associative tree:
- Iteration 1: `left = (a + b)`
- Iteration 2: `left = ((a + b) + c)`
- Iteration 3: `left = (((a + b) + c) + d)`

**Alternative (right-associative):** Recursion instead of iteration
```python
def parse_assign(self):
    left = self.parse_expr()
    if self.match(ASSIGN):
        self.advance()
        right = self.parse_assign()  # Recursive call
        return AssignOp(left, right)
    return left
```

Builds: `a = (b = (c = d))` (right-associative)

---

## The Three Core Operations

### 1. match(type) — Lookahead

```python
def match(self, token_type):
    """Check if current token matches type WITHOUT consuming"""
    return self.current_token.type == token_type
```

**Use:** Decision making (which production to apply?)

### 2. advance() — Consume

```python
def advance(self):
    """Consume current token and move to next"""
    self.position += 1
    self.current_token = self.tokens[self.position]
```

**Use:** After deciding, consume token and move forward

### 3. expect(type) — Match + Advance + Error

```python
def expect(self, token_type):
    """Match and consume, or error if no match"""
    if not self.match(token_type):
        raise ParseError(f"Expected {token_type}")
    self.advance()
```

**Use:** Required terminals (guaranteed to be present)

---

## AST Construction Pattern

**Each parse function returns AST node:**

```python
def parse_factor(self):
    if self.match(INT):
        value = self.current_token.value
        line, col = self.current_token.line, self.current_token.col
        self.advance()
        return IntLiteral(value, line, col)  # Return AST node
    
    elif self.match(LPAREN):
        self.advance()
        expr = self.parse_expr()  # Get AST from recursive call
        self.expect(RPAREN)
        return expr  # Return AST node
```

**Pattern:**
1. Parse components (recursive calls)
2. Each returns AST node
3. Combine into parent node
4. Return parent

**Call stack = implicit tree structure**

---

## Error Pattern

```python
def error(self, message):
    raise ParseError(
        f"{message} at line {self.current_token.line}, "
        f"col {self.current_token.col}"
    )
```

**Always include:**
- Error message (what went wrong)
- Location (line, column)
- Context (what token was found)

---

## Checklist: Implementing New Production

When adding grammar rule `A → α β γ`:

1. ☐ Create `parse_a()` function
2. ☐ Add docstring with grammar rule
3. ☐ For each terminal: `expect()` or `match() + advance()`
4. ☐ For each non-terminal: call `parse_x()`
5. ☐ For choices: use `if/elif` based on lookahead
6. ☐ For repetition: use `while` loop
7. ☐ Build AST node from components
8. ☐ Capture `line, col` from tokens
9. ☐ Return AST node
10. ☐ Add error handling (else clause for choices)

---

## Common Bugs

### Bug 1: Infinite Loop

**Cause:** Left recursion in grammar
```
Expr → Expr '+' Term  // parse_expr calls parse_expr immediately
```

**Fix:** Eliminate left recursion
```
Expr → Term ('+' Term)*
```

### Bug 2: Forgetting advance()

**Cause:** Check token but don't consume
```python
if self.match(PLUS):
    # Missing: self.advance()
    right = self.parse_term()
```

**Result:** Parser stuck on same token forever

**Fix:** Always `advance()` after `match()`

### Bug 3: Wrong Associativity

**Cause:** Recursion instead of iteration for left-assoc operator

**Fix:** Use while loop + reassignment for left-assoc

---

## Summary

**Recursive descent = systematic translation:**

| Grammar | Code |
|---------|------|
| Non-terminal | Function |
| Terminal | expect() |
| Sequence | Sequential calls |
| Choice | if/elif |
| Repetition | while |
| Optional | if |

**Key insight:** Grammar structure directly determines code structure. No interpretation, just translation.

---

## Related

- [[03-parsing/recursive-descent]] — Full theory
- [[zettel/Z0020-ast-design]] — What AST nodes to build
- [[03-parsing/precedence-and-associativity]] — Grammar stratification for operators
