## Links
- Up: [[03-parsing/README]]
- Related: [[03-parsing/trees-vs-structure]] [[03-parsing/precedence-and-associativity]]
- Down: [[zettel/Z0021-recursive-descent-pattern]]

---

# Recursive Descent Parsing

## Overview

**Recursive descent** is the most straightforward parsing technique: each non-terminal in the grammar becomes a function, and parsing is just calling those functions in the right order.

**Key insight:** The call stack **is** the parse tree. Recursion mirrors grammar structure.

**Properties:**
- Top-down parsing (start from root, expand to leaves)
- Requires LL(1) or LL(k) grammar (left-to-right, leftmost derivation, k-token lookahead)
- Predictive (decides which production to use by looking ahead)
- Easy to implement by hand
- Direct grammar-to-code translation

---

## The Core Idea

### Grammar as Blueprint

**Grammar:**
```
Expr → Term ('+' Term)*
Term → Factor ('*' Factor)*
Factor → INT | ID | '(' Expr ')'
```

**Code:**
```python
def parse_expr(self):
    # Expr → Term ('+' Term)*
    node = self.parse_term()
    while self.match('+'):
        self.advance()
        right = self.parse_term()
        node = BinaryOp('+', node, right)
    return node

def parse_term(self):
    # Term → Factor ('*' Factor)*
    node = self.parse_factor()
    while self.match('*'):
        self.advance()
        right = self.parse_factor()
        node = BinaryOp('*', node, right)
    return node

def parse_factor(self):
    # Factor → INT | ID | '(' Expr ')'
    if self.match(INT):
        value = self.current_token.value
        self.advance()
        return IntLiteral(value)
    elif self.match(ID):
        name = self.current_token.value
        self.advance()
        return Identifier(name)
    elif self.match('('):
        self.advance()
        node = self.parse_expr()  # Recursion!
        self.expect(')')
        return node
    else:
        self.error("Expected factor")
```

**Notice:**
- Each non-terminal (`Expr`, `Term`, `Factor`) → one function
- Terminals checked with `match()` or `expect()`
- Recursion when grammar is recursive (Factor calls Expr)
- Choice (|) becomes if/elif
- Repetition (*) becomes while loop
- Sequence (α β) becomes sequential calls

---

## The Recursive Descent Algorithm

### Input
- Token stream from lexer
- Grammar suitable for recursive descent (no left recursion, left-factored)

### Output
- Abstract Syntax Tree (AST)

### State
- `current_token`: Current position in token stream
- `tokens`: Complete token list
- `position`: Index into token list

### Operations

#### 1. Match (Lookahead)
```python
def match(self, token_type):
    """Check if current token matches type without consuming"""
    return self.current_token.type == token_type
```

#### 2. Advance (Consume)
```python
def advance(self):
    """Move to next token"""
    self.position += 1
    if self.position < len(self.tokens):
        self.current_token = self.tokens[self.position]
    else:
        self.current_token = Token(EOF, None)
```

#### 3. Expect (Match + Advance + Error)
```python
def expect(self, token_type):
    """Consume token if it matches, else error"""
    if not self.match(token_type):
        self.error(f"Expected {token_type}, got {self.current_token.type}")
    self.advance()
```

#### 4. Error (Abort or Recover)
```python
def error(self, message):
    """Report error with location and stop"""
    raise ParseError(f"{message} at line {self.current_token.line}")
```

---

## Grammar Translation Patterns

### Pattern 1: Sequence (α β γ)

**Grammar:** `A → B C D`

**Code:**
```python
def parse_A(self):
    b = self.parse_B()
    c = self.parse_C()
    d = self.parse_D()
    return ANode(b, c, d)
```

**Linear execution** — parse in order.

---

### Pattern 2: Choice (α | β | γ)

**Grammar:** `A → B | C | D`

**Code (LL(1) — disjoint first sets):**
```python
def parse_A(self):
    if self.first_of_B():
        return self.parse_B()
    elif self.first_of_C():
        return self.parse_C()
    elif self.first_of_D():
        return self.parse_D()
    else:
        self.error("Expected A")
```

**Decision based on lookahead** — each alternative has distinct starting token(s).

---

### Pattern 3: Optional (α?)

**Grammar:** `A → B C?`

**Code:**
```python
def parse_A(self):
    b = self.parse_B()
    c = None
    if self.match_first_of_C():
        c = self.parse_C()
    return ANode(b, c)
```

**Optional field** in AST (None if absent).

---

### Pattern 4: Repetition (α*)

**Grammar:** `A → B C*`

**Code:**
```python
def parse_A(self):
    b = self.parse_B()
    c_list = []
    while self.match_first_of_C():
        c_list.append(self.parse_C())
    return ANode(b, c_list)
```

**Collect into list** — keep parsing until lookahead doesn't match.

---

### Pattern 5: One or More (α+)

**Grammar:** `A → B+`

**Code:**
```python
def parse_A(self):
    b_list = [self.parse_B()]
    while self.match_first_of_B():
        b_list.append(self.parse_B())
    return ANode(b_list)
```

**At least one** required, then repeat.

---

### Pattern 6: Right Recursion

**Grammar:** `A → B A | ε`

**Code:**
```python
def parse_A(self):
    if self.match_first_of_B():
        b = self.parse_B()
        a = self.parse_A()  # Recursive call
        return ANode(b, a)
    else:
        return None  # ε case
```

**Recursion mirrors grammar** — call stack grows with nesting depth.

---

## Handling Left Recursion

### The Problem

**Grammar:** `Expr → Expr '+' Term | Term`

**Naive code:**
```python
def parse_expr(self):
    if self.match_first_of_expr():
        left = self.parse_expr()  # Infinite recursion!
        self.expect('+')
        right = self.parse_term()
        return BinaryOp('+', left, right)
    else:
        return self.parse_term()
```

**Problem:** `match_first_of_expr()` checks if current token can start an `Expr`, which includes `Expr` itself → always true → infinite loop.

### The Solution: Eliminate Left Recursion

**Original (left-recursive):**
```
Expr → Expr '+' Term | Term
```

**Transformed (right-recursive with tail):**
```
Expr → Term ExprTail
ExprTail → '+' Term ExprTail | ε
```

**Code:**
```python
def parse_expr(self):
    left = self.parse_term()
    return self.parse_expr_tail(left)

def parse_expr_tail(self, left):
    if self.match('+'):
        self.advance()
        right = self.parse_term()
        node = BinaryOp('+', left, right)
        return self.parse_expr_tail(node)  # Right recursion
    else:
        return left  # ε case
```

**Better (iterative):**
```python
def parse_expr(self):
    left = self.parse_term()
    while self.match('+'):
        self.advance()
        right = self.parse_term()
        left = BinaryOp('+', left, right)  # Left-associative
    return left
```

**Insight:** Right recursion via tail calls → easily converted to iteration. This is **standard pattern** for left-associative operators.

---

## Handling Left Factoring

### The Problem

**Grammar:**
```
Stmt → 'if' '(' Expr ')' Block
     | 'if' '(' Expr ')' Block 'else' Block
```

Common prefix: `'if' '(' Expr ')' Block`

**Naive approach:** Parse prefix twice (inefficient) or look ahead arbitrarily far (impractical).

### The Solution: Factor Common Prefix

**Transformed:**
```
Stmt → 'if' '(' Expr ')' Block ElsePart
ElsePart → 'else' Block | ε
```

**Code:**
```python
def parse_stmt(self):
    if self.match('if'):
        self.expect('if')
        self.expect('(')
        condition = self.parse_expr()
        self.expect(')')
        then_block = self.parse_block()
        else_block = self.parse_else_part()
        return IfStatement(condition, then_block, else_block)
    # ... other statements

def parse_else_part(self):
    if self.match('else'):
        self.expect('else')
        return self.parse_block()
    else:
        return None  # ε case
```

**Benefit:** Parse common prefix once, decide on tail with 1-token lookahead.

---

## Building AST During Parsing

### Strategy: Return Nodes from Functions

Each parsing function returns an AST node (or None for ε).

**Example: Binary Operators**

```python
def parse_expr(self):
    """Expr → Term ('+' Term | '-' Term)*"""
    left = self.parse_term()
    while self.match('+') or self.match('-'):
        op = self.current_token.value
        line, col = self.current_token.line, self.current_token.col
        self.advance()
        right = self.parse_term()
        left = BinaryOp(op, left, right, line, col)
    return left
```

**Key points:**
- `parse_term()` returns AST node
- Loop builds left-associative tree (reassigning `left`)
- Track source location for errors

**Example: Statements**

```python
def parse_block(self):
    """Block → '{' Stmt* '}'"""
    self.expect('{')
    statements = []
    while not self.match('}'):
        statements.append(self.parse_stmt())
    self.expect('}')
    return Block(statements)

def parse_stmt(self):
    """Stmt → IfStmt | WhileStmt | ReturnStmt | ExprStmt"""
    if self.match('if'):
        return self.parse_if_stmt()
    elif self.match('while'):
        return self.parse_while_stmt()
    elif self.match('return'):
        return self.parse_return_stmt()
    else:
        return self.parse_expr_stmt()
```

**Pattern:** Dispatcher function uses lookahead to choose which specialized function to call.

---

## Complete Example: Expression Parser

### Grammar (LL(1), left-factored, no left recursion)

```
Expr   → Term (('+' | '-') Term)*
Term   → Factor (('*' | '/') Factor)*
Factor → INT | ID | '(' Expr ')'
```

### AST Node Classes

```python
class ASTNode:
    def __init__(self, line, col):
        self.line = line
        self.col = col

class BinaryOp(ASTNode):
    def __init__(self, op, left, right, line, col):
        super().__init__(line, col)
        self.op = op
        self.left = left
        self.right = right

class IntLiteral(ASTNode):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name, line, col):
        super().__init__(line, col)
        self.name = name
```

### Parser Implementation

```python
class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else Token(EOF, None)
    
    def match(self, token_type):
        return self.current_token.type == token_type
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(EOF, None)
    
    def expect(self, token_type):
        if not self.match(token_type):
            raise ParseError(
                f"Expected {token_type}, got {self.current_token.type} "
                f"at line {self.current_token.line}"
            )
        self.advance()
    
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
            node = self.parse_expr()
            self.expect(RPAREN)
            return node
        else:
            raise ParseError(
                f"Expected factor, got {self.current_token.type} "
                f"at line {self.current_token.line}"
            )
    
    def parse(self):
        """Entry point"""
        ast = self.parse_expr()
        self.expect(EOF)
        return ast
```

### Execution Trace: `3 + 4 * 5`

**Tokens:** `[INT(3), PLUS, INT(4), STAR, INT(5), EOF]`

**Call trace:**
```
parse()
  parse_expr()
    parse_term()
      parse_factor()
        match(INT) → IntLiteral(3)
    match(PLUS) → yes
    advance() → PLUS consumed
    parse_term()
      parse_factor()
        match(INT) → IntLiteral(4)
      match(STAR) → yes
      advance() → STAR consumed
      parse_factor()
        match(INT) → IntLiteral(5)
      return BinaryOp('*', IntLiteral(4), IntLiteral(5))
    return BinaryOp('+', IntLiteral(3), BinaryOp('*', ...))
  expect(EOF) → success
```

**Resulting AST:**
```
       +
      / \
     3   *
        / \
       4   5
```

**Key observations:**
- `parse_expr` calls `parse_term` twice
- First `parse_term` returns `3`, second returns `(4 * 5)`
- Multiplication binds tighter because `Term` is nested inside `Expr`
- Call stack depth mirrors grammar nesting

---

## Backtracking (When LL(1) Fails)

Sometimes lookahead isn't enough. **Backtracking** tries alternatives, undoing on failure.

### Example: Ambiguous Grammar (needs backtracking)

**Grammar:**
```
Expr → ID '(' ArgList ')' | ID
ArgList → Expr (',' Expr)*
```

**Problem:** Both alternatives start with `ID`. Need to look past ID to decide.

**Solution 1:** Left-factor (best)
```
Expr → ID ExprTail
ExprTail → '(' ArgList ')' | ε
```

**Solution 2:** Backtracking (if refactoring not possible)

```python
def parse_expr(self):
    saved_pos = self.position
    try:
        return self.parse_call_expr()
    except ParseError:
        self.position = saved_pos
        self.current_token = self.tokens[self.position]
        return self.parse_id_expr()
```

**Pros:** Handles non-LL(1) grammars
**Cons:** Slow (exponential worst-case), complex control flow

**Advice:** Use backtracking sparingly. Usually better to refactor grammar.

---

## Error Handling

### Panic Mode Recovery

**Goal:** Report error, synchronize to known point, continue parsing.

**Strategy:** Skip tokens until "synchronization point" (e.g., `;`, `}`, keyword).

```python
def parse_stmt(self):
    try:
        if self.match('if'):
            return self.parse_if_stmt()
        elif self.match('while'):
            return self.parse_while_stmt()
        # ... other statements
        else:
            return self.parse_expr_stmt()
    except ParseError as e:
        self.report_error(e)
        self.synchronize()  # Skip to safe point
        return ErrorNode()  # Placeholder

def synchronize(self):
    """Skip tokens until synchronization point"""
    while not self.match(EOF):
        if self.current_token.type in [SEMICOLON, RBRACE]:
            self.advance()
            return
        if self.current_token.type in [IF, WHILE, RETURN]:
            return
        self.advance()
```

**Benefits:**
- Report multiple errors in one pass (not just first)
- Continue parsing to find more issues
- Better user experience

**Tradeoffs:**
- May produce invalid AST (needs error nodes)
- Cascading errors (first error causes many follow-ons)

---

## Advantages of Recursive Descent

1. **Simple to implement** — direct grammar translation
2. **Easy to understand** — control flow matches grammar
3. **Flexible** — can embed semantic actions anywhere
4. **Good error messages** — full context available
5. **Fast** — no table lookups, just function calls
6. **Debuggable** — standard debugger works (set breakpoints in parse functions)

**Chess analogy:** Like perft testing—straightforward implementation, easy to verify correctness.

---

## Disadvantages of Recursive Descent

1. **Grammar restrictions** — must be LL(k), no left recursion
2. **Manual maintenance** — grammar changes require code updates
3. **Repetitive code** — similar patterns across functions
4. **Limited error recovery** — panic mode is crude

**When to avoid:**
- Grammar has unavoidable left recursion (use LR parser)
- Frequent grammar changes (use parser generator)
- Need best possible error recovery (LR parsers can be better)

---

## Recursive Descent vs. Parser Generators

| Aspect | Recursive Descent (Hand-Written) | Parser Generator (yacc/ANTLR) |
|--------|----------------------------------|-------------------------------|
| **Implementation effort** | High initially, low maintenance if grammar stable | Low initially, auto-generated |
| **Grammar flexibility** | LL(1) or LL(k) only | LR(1), LALR, LL(*) |
| **Error messages** | Excellent (custom) | Generic (can customize) |
| **Debugging** | Easy (standard debugger) | Harder (generated code) |
| **Performance** | Fast (optimized by hand) | Fast (optimized tables) |
| **Learning curve** | Low (just functions) | Medium (learn tool + grammar syntax) |
| **Integration** | Seamless (part of codebase) | External tool in build pipeline |

**When to use RD:**
- Small to medium languages
- Stable grammar
- Want full control and clarity
- Need excellent error messages

**When to use generator:**
- Large, complex grammar
- Evolving language design
- Need grammar features RD can't handle (left recursion, ambiguity)

---

## Production Compilers Using Recursive Descent

- **GCC** (C/C++ front-end)
- **Clang** (C/C++/Objective-C)
- **Go** (gc compiler)
- **Rust** (rustc)
- **TypeScript** (tsc)

**Reason:** LL grammars for modern languages + desire for great error messages + full control.

**Counter-examples (LR):**
- **Python** (uses PEG parser as of 3.9, previously LL(1) with hacks)
- **Java** (javac uses hand-written recursive descent despite some LR features)

---

## Chess Engine Analogy

**Recursive descent ↔ Recursive search (minimax/negamax)**

- **Grammar productions** ↔ **Move generation** — both define structure
- **Parsing functions** ↔ **Search functions** — mutual recursion
- **Call stack** ↔ **Search tree** — implicit structure
- **Lookahead (k tokens)** ↔ **Search depth** — how far to explore
- **Backtracking** ↔ **Undoing moves** — explore alternatives
- **AST** ↔ **Principal variation** — result of successful parse/search

**Takeaway:** Both use recursion to explore tree-structured space. Parse tree is implicit in call stack, just like search tree.

---

## AoC Analogy

**Recursive descent ↔ Recursive problem solving**

- **Grammar rules** ↔ **Problem structure** — define decomposition
- **Parsing** ↔ **Solving subproblems** — break down and conquer
- **Iteration (while loops)** ↔ **Repetition in input** — process sequences
- **Error recovery** ↔ **Handling edge cases** — robustness

**Example:** Parsing nested structures (JSON, S-expressions) in AoC → natural recursive descent approach.

---

## Summary

**Recursive descent parsing:**
- ✅ Simple and elegant
- ✅ Direct grammar-to-code translation
- ✅ Fast and debuggable
- ✅ Excellent error messages
- ❌ Requires LL(k) grammar (no left recursion)
- ❌ Manual maintenance

**Key patterns:**
- Choice (|) → if/elif
- Sequence (α β) → sequential calls
- Repetition (*) → while loop
- Recursion → function calls

**When to use:** Modern language front-ends, stable grammars, need control and clarity.

**Implementation (Day 28):** Tomorrow we'll write a complete recursive descent parser for the simple language from the weekly plan.

---

## Further Reading

- [[03-parsing/trees-vs-structure]] — Building AST vs. CST
- [[03-parsing/precedence-and-associativity]] — Encoding precedence in grammar
- [[03-parsing/ambiguity]] — Resolving grammar ambiguity
- [[lecture-23-abstract-syntax-trees]] — LL parsing theory
- [[lecture-24-recursive-descent-parsing]] — Recursive descent in detail

---

## Reflection Questions

1. **Why does left recursion cause infinite loops in recursive descent?**
   - What changes when you eliminate it?

2. **How does the call stack represent the parse tree?**
   - Could you visualize it during execution?

3. **When would you choose backtracking over grammar refactoring?**
   - What are the tradeoffs?

4. **How does recursive descent compare to chess search algorithms?**
   - What patterns are shared?

5. **Why do production compilers (GCC, Clang, Rust) use hand-written recursive descent?**
   - What do they gain over parser generators?
