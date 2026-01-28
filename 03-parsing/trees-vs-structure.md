## Links
- Up: [[03-parsing/README]]
- Related: [[03-parsing/recursive-descent]] [[03-parsing/ambiguity]] [[03-parsing/precedence-and-associativity]]
- Down: [[zettel/Z0020-ast-design]]

---

# Trees vs. Structure: CST and AST

## Overview

Parsing produces a **tree representation** of source code, but not all trees are created equal. Understanding the distinction between **Concrete Syntax Trees (CST)** and **Abstract Syntax Trees (AST)** is fundamental to compiler design.

**Key insight:** The parser's job isn't to preserve every detail of the source—it's to extract the **meaning** while discarding irrelevant syntax.

---

## The Two Trees

### Concrete Syntax Tree (CST)

Also called a **parse tree**, the CST is a faithful representation of **every step** taken during parsing according to the grammar.

**Properties:**
- One node per grammar production
- Includes all terminals (tokens) and non-terminals
- Preserves syntactic details: parentheses, commas, semicolons, keywords
- Often very deep and verbose
- Direct correspondence to grammar structure

**Example:** Parse `3 + 4 * 5` with grammar:
```
Expr → Term ExprTail
ExprTail → '+' Term ExprTail | ε
Term → Factor TermTail
TermTail → '*' Factor TermTail | ε
Factor → INT
```

**CST:**
```
              Expr
             /    \
          Term    ExprTail
           |      /   |   \
        Factor  '+'  Term ExprTail
           |          |      |
          INT(3)   Factor   ε
                      |
                   TermTail
                   /  |  \
                 '*' Factor TermTail
                        |      |
                      INT(4)  ExprTail
                              / |  \
                           '*' Factor TermTail
                                  |      |
                                INT(5)   ε
```

**Notice:**
- Every non-terminal from grammar appears as node
- Empty productions (ε) are present
- Operators are leaf nodes alongside numbers
- Tree depth matches grammar nesting

### Abstract Syntax Tree (AST)

The AST is a **distilled** representation preserving only **semantically relevant** structure.

**Properties:**
- One node per semantic construct
- Omits punctuation, keywords (when meaning is captured structurally)
- Flattens unnecessary intermediate nodes
- Focused on meaning, not syntax
- Optimized for subsequent compiler phases

**Example:** Same expression `3 + 4 * 5`

**AST:**
```
       +
      / \
     3   *
        / \
       4   5
```

**Notice:**
- Only operators and operands
- No ExprTail, TermTail, or Factor nodes
- Precedence encoded by tree structure (× deeper than +)
- Drastically simpler than CST

---

## Side-by-Side Comparison

| Feature | CST | AST |
|---------|-----|-----|
| **Purpose** | Represents parsing process | Represents program structure |
| **Grammar fidelity** | Exact match to productions | Independent of grammar details |
| **Depth** | Deep (all non-terminals) | Shallow (semantic constructs only) |
| **Terminals** | All tokens present | Only semantically relevant ones |
| **Parentheses** | Explicit nodes | Implicit in tree shape |
| **Size** | Large, verbose | Compact, focused |
| **Use case** | Debugging parsers, error recovery | Semantic analysis, optimization, codegen |
| **Construction** | Natural output of parser | Requires deliberate design |

---

## Why AST Wins for Compilers

### 1. Smaller Memory Footprint

CST for `a + b * c + d` might have 20+ nodes; AST has 7.

**Impact:** Large programs with millions of lines produce manageable ASTs but unwieldy CSTs.

### 2. Easier to Traverse

Semantic analysis, type checking, optimization—all walk the tree repeatedly.

**CST traversal:**
```python
def eval_expr(node):
    if node.type == "Expr":
        return eval_term(node.children[0]) + eval_exprtail(node.children[1])
    # Many cases for non-terminals...
```

**AST traversal:**
```python
def eval(node):
    if isinstance(node, BinaryOp):
        return apply(node.op, eval(node.left), eval(node.right))
    elif isinstance(node, IntLiteral):
        return node.value
```

Simpler logic → fewer bugs.

### 3. Grammar-Independent

If you refactor the grammar (e.g., eliminate left recursion), CST changes shape; AST stays the same.

**Example:** These two grammars produce different CSTs but identical ASTs:

**Grammar 1 (left-recursive):**
```
Expr → Expr '+' Term | Term
```

**Grammar 2 (right-recursive):**
```
Expr → Term ExprTail
ExprTail → '+' Term ExprTail | ε
```

**Both produce AST:**
```
   +
  / \
 a   +
    / \
   b   c
```

**Benefit:** AST is the **contract** between parser and later phases. Grammar can evolve without breaking downstream code.

### 4. Precedence and Associativity Are Structural

In CST, operators are tokens; precedence is implicit in grammar structure.

In AST, operators are **nodes**, and precedence is explicit in tree depth.

**CST:** "Why is `*` evaluated before `+`? Because Factor is nested inside Term which is nested inside Expr."

**AST:** "Why is `*` evaluated before `+`? Because it's deeper in the tree."

The AST makes evaluation order **obvious**.

---

## What Gets Discarded?

When building an AST from a CST, we intentionally drop:

### 1. Punctuation (Usually)

- **Parentheses:** `(a + b)` — meaning captured by tree structure
- **Commas:** `f(a, b, c)` — children array captures argument list
- **Semicolons:** `x = 5; y = 10;` — statement list captures sequence

**Exception:** Sometimes punctuation affects semantics:
- C's ternary operator: `a ? b : c` — might keep `?` and `:` as node type
- Function calls: `f()` vs. `f` — distinguish call from reference

### 2. Keywords (Often)

- **`if`/`else`:** IfStatement node type encodes this
- **`while`:** WhileStatement node
- **`return`:** ReturnStatement node

**Exception:** Keywords that change meaning:
- Storage class specifiers: `static`, `const`
- Access modifiers: `public`, `private`

### 3. Intermediate Non-Terminals

- **ExprTail, TermTail:** Artifacts of grammar transformation
- **StmtList:** Flattened into array of statements
- **ParamList:** Becomes array of parameters

**Heuristic:** If a non-terminal exists only to avoid left recursion or enable factoring, it's probably not in the AST.

### 4. Empty Productions (ε)

`ElsePart → ε` becomes `else_block = None` in AST node.

---

## AST Design Patterns

### Pattern 1: Operators as Interior Nodes

**Structure:**
```python
class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op      # String: '+', '-', '*', '/'
        self.left = left  # ASTNode
        self.right = right # ASTNode
```

**Benefits:**
- Uniform handling of all binary operators
- Easy to extend with new operators
- Visitor pattern works cleanly

### Pattern 2: Statement Lists as Arrays

**Instead of:**
```
Block → '{' StmtList '}'
StmtList → Stmt StmtList | ε
```

**AST:**
```python
class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # list of ASTNode
```

**Benefits:**
- Natural iteration with loops
- Easy to insert/remove statements during optimization
- No recursive list structure

### Pattern 3: Optional Nodes as None

**Grammar:**
```
IfStmt → 'if' '(' Expr ')' Block ElsePart
ElsePart → 'else' Block | ε
```

**AST:**
```python
class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition  # ASTNode
        self.then_block = then_block  # Block
        self.else_block = else_block  # Block or None
```

**Benefits:**
- Clear distinction: presence vs. absence
- No special "empty" node types
- Pythonic (None is idiomatic)

### Pattern 4: Source Locations Always

**Every AST node includes:**
```python
class ASTNode:
    def __init__(self, line, col):
        self.line = line
        self.col = col
```

**Why:**
- Error messages: "Error at line 42, column 15"
- Debugging: trace code back to source
- Refactoring tools: know what to update
- IDE features: jump to definition

**Cost:** Minimal memory overhead, massive benefit.

---

## Construction Strategies

### Strategy 1: Build AST Directly During Parsing

**Approach:** Each parsing function returns an AST node.

**Example (recursive descent):**
```python
def parse_expr(self):
    left = self.parse_term()
    while self.current_token in ['+', '-']:
        op = self.current_token.value
        self.advance()
        right = self.parse_term()
        left = BinaryOp(op, left, right, self.line, self.col)
    return left
```

**Pros:**
- Single pass (efficient)
- No intermediate CST storage
- Natural fit for recursive descent

**Cons:**
- Parsing and AST design tightly coupled
- Harder to change AST structure independently

### Strategy 2: Build CST, Then Transform to AST

**Approach:** Parser produces CST; separate pass converts to AST.

**Example:**
```python
def cst_to_ast(cst_node):
    if cst_node.type == "Expr":
        term = cst_to_ast(cst_node.children[0])
        tail = cst_node.children[1]
        return build_left_assoc(term, tail)
    # ... handle other node types
```

**Pros:**
- Clean separation: parsing vs. representation
- Can experiment with different AST designs
- Easier to debug (inspect CST)

**Cons:**
- Two passes (slower, more memory)
- Extra code to maintain

**When to use:** Parser generators often produce CSTs; you write transformation.

### Strategy 3: Hybrid (Common in Practice)

**Approach:** Most nodes built directly; complex cases use intermediate form.

**Example:**
- Expressions: build AST directly
- Declarations: build intermediate form, resolve later
- Error recovery: produce partial CST, fix up to AST

---

## Chess Engine Analogy

**CST ↔ Move notation**
- CST is like recording every move in long algebraic notation: `Ng1-f3`, `e7-e5`
- Captures every detail of how position evolved
- Useful for move validation and game replay

**AST ↔ Position representation**
- AST is like bitboard or piece-list representation
- Only current state matters, not how we got here
- Optimized for evaluation and search (semantic analysis/optimization)

**Takeaway:** After parsing (move validation), you don't replay the moves; you analyze the position.

---

## Common Mistakes

### Mistake 1: Including Too Much in AST

**Problem:** Keeping semicolons, parentheses, commas as nodes.

**Result:** AST becomes cluttered, traversal code filled with special cases.

**Fix:** Ask "Does this affect **meaning** or just **spelling**?" If spelling, discard.

### Mistake 2: Losing Source Information

**Problem:** No line/column numbers in AST nodes.

**Result:** Error messages say "type error" without location. Useless for debugging.

**Fix:** Always include source positions. Always.

### Mistake 3: Grammar-Dependent AST

**Problem:** AST structure mirrors grammar exactly (e.g., separate ExprTail nodes).

**Result:** Grammar refactoring breaks everything downstream.

**Fix:** AST should represent **language semantics**, not grammar productions.

### Mistake 4: Not Planning for Later Phases

**Problem:** AST designed for parsing, not for type checking or optimization.

**Result:** Later phases add hacks or parallel data structures.

**Fix:** Think ahead. What will semantic analysis need? Optimization? Code generation?

---

## Examples: CST vs. AST

### Example 1: Function Call

**Source:** `max(3 + 5, 10)`

**CST (simplified):**
```
        CallExpr
       /    |    \
     ID   ArgList  ')'
    /      /   \
  max     Expr  ArgTail
          /|\    /  |  \
       Term + Term ','  ArgList
        |      |        /     \
     Factor Factor    Expr    ArgTail
        |      |       |        |
       INT    INT     INT       ε
        3      5       10
```

**AST:**
```
    FunctionCall
       /    \
    "max"  [args]
            /    \
          +       10
         / \
        3   5
```

**Transformation:**
- `CallExpr`, `ArgList`, `ArgTail` → `FunctionCall` node
- Argument list → array of expression nodes
- Grammar artifacts gone

---

### Example 2: If Statement

**Source:**
```c
if (x > 0) {
    y = 1;
} else {
    y = -1;
}
```

**CST (simplified):**
```
          IfStmt
        /   |    \     \
      'if'  '('  Expr  Block ElsePart
                  |      |      |
               BinaryOp  {...} 'else' Block
                 / | \            |
               ID '>' INT        {...}
```

**AST:**
```
        IfStatement
       /     |      \
    condition then  else
      |       |      |
      >    [y=1]  [y=-1]
     / \
    x   0
```

**Transformation:**
- Keywords `if`, `else`, parentheses → implicit in node type
- `ElsePart` → `else_block` field (or None if absent)
- Blocks → arrays of statements

---

### Example 3: Operator Precedence

**Source:** `2 + 3 * 4`

**CST (with precedence grammar):**
```
         Expr
        /    \
      Term   ExprTail
       |      /  |  \
    Factor  '+' Term ExprTail
      |          |      |
    INT(2)    Factor   ε
               /   \
              *   TermTail
             / \      |
          INT(3) INT(4)  ε
```

**AST:**
```
     +
    / \
   2   *
      / \
     3   4
```

**Key:** CST encodes precedence through nested non-terminals; AST encodes it through tree depth.

---

## When to Use Each

### Use CST When:

1. **Error recovery matters** — CST preserves all tokens for better error messages
2. **Source transformation tools** — Refactoring, code formatting (need exact syntax)
3. **Parser debugging** — Visualize parse tree to understand grammar behavior
4. **Teaching/visualization** — Show students how parsing works

### Use AST When:

1. **Semantic analysis** — Type checking, scope resolution
2. **Optimization** — Transform code, constant folding, dead code elimination
3. **Code generation** — Translate to IR or machine code
4. **Interpretation** — Directly execute AST
5. **Static analysis** — Linters, security scanners

**In practice:** Most compilers build AST directly or quickly discard CST.

---

## Summary

| Aspect | CST | AST |
|--------|-----|-----|
| **Represents** | Parsing derivation | Program semantics |
| **Size** | Large (all grammar nodes) | Compact (semantic nodes only) |
| **Fidelity** | Exact match to grammar | Independent of grammar |
| **Operators** | Leaf tokens | Interior nodes |
| **Precedence** | Implicit in nesting | Explicit in tree depth |
| **Use in compiler** | Rare (parser debugging) | Standard (all phases after parsing) |

**Key takeaway:** AST is the **language of compilers**. Once parsing completes, everything operates on ASTs (or further lowered IRs). The CST is scaffolding—useful during construction, discarded when building is done.

---

## Further Reading

- [[03-parsing/recursive-descent]] — Building ASTs during parsing
- [[03-parsing/precedence-and-associativity]] — How grammar encodes precedence in AST
- [[03-parsing/ambiguity]] — When grammar produces multiple CSTs
- [[05-ir/why-ast-is-not-enough]] — Why we lower AST to simpler IRs
- [[Z0020-ast-design]] — Design principles for AST nodes

---

## Reflection Questions

1. **Why doesn't the AST include parentheses from `(a + b) * c`?**
   - What does the tree structure encode that makes parentheses redundant?

2. **Could you build a compiler using only CST, never AST?**
   - What would be the tradeoffs?

3. **How would you design AST nodes for C's pointer declarations: `int **p[10]`?**
   - What information must be preserved?

4. **If grammar changes but language semantics don't, should AST change?**
   - What does this tell you about AST vs. CST?

5. **How does AST design affect later phases like type checking?**
   - What information do you wish you'd included earlier?
