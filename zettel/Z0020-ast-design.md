# Z0020 — AST Design Principles

## Links
- Up: [[03-parsing/trees-vs-structure]]
- Related: [[03-parsing/recursive-descent]] [[05-ir/why-ast-is-not-enough]] [[04-semantics/README]] [[zettel/Z0024-sum-types-and-expression-problem]]
- Down: [[zettel/Z0021-recursive-descent-pattern]] [[zettel/Z0023-ambiguity-resolution]]

---

## Core Principle

An AST node encodes **semantic meaning**, not syntactic detail.

**Question to ask for each node field:** "Will semantic analysis or optimization need this information?"

If yes → include it. If no → discard it (it's syntactic sugar).

---

## Five Design Patterns

### Pattern 1: Operators as Interior Nodes

```python
class BinaryOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op        # String: '+', '-', '*', '/'
        self.left = left    # ASTNode
        self.right = right  # ASTNode
```

**Why:** All binary operators are structurally identical (two operands, one operation). Treating them uniformly:
- Reduces node types (one instead of Add, Subtract, Multiply, Divide)
- Simplifies visitor pattern
- Makes it easy to add new operators

**When to violate:** If operator behavior differs fundamentally (e.g., logical AND short-circuits; arithmetic + doesn't). Then separate nodes may clarify intent.

---

### Pattern 2: Collections as Arrays

**Don't:**
```python
class StmtList(ASTNode):
    def __init__(self, head, tail):
        self.head = head      # Statement
        self.tail = tail      # StmtList or None
```

**Do:**
```python
class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # list of ASTNode
```

**Why:** Arrays are natural for iteration, insertion, manipulation. Linked lists are artificial.

**Cost:** Minimal. Benefit: Vastly simpler traversal and transformation code.

---

### Pattern 3: Optional Fields as None

**Don't:**
```python
class OptionalElse(ASTNode):
    """Represents ElsePart → 'else' Block | ε"""
    def __init__(self, block):
        self.block = block  # Block or None
```

**Do:**
```python
class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition        # ASTNode
        self.then_block = then_block      # Block
        self.else_block = else_block      # Block or None
```

**Why:** Presence/absence is clearer than separate node types. `else_block = None` is idiomatic Python (same pattern in many libraries).

---

### Pattern 4: Source Locations Everywhere

**Don't:**
```python
class IntLiteral(ASTNode):
    def __init__(self, value):
        self.value = value
```

**Do:**
```python
class IntLiteral(ASTNode):
    def __init__(self, value, line, col):
        self.line = line
        self.col = col
        self.value = value
```

**Why:** Error messages and debugging are impossible without location. One bad decision here costs you hours later.

**Base class:**
```python
class ASTNode:
    def __init__(self, line, col):
        self.line = line
        self.col = col
```

**Always propagate from tokens:**
```python
def parse_int(self):
    token = self.current_token
    value = token.value
    line, col = token.line, token.col
    self.advance()
    return IntLiteral(value, line, col)
```

---

### Pattern 5: Type Field Placeholder

**Reserve space for semantic information:**

```python
class ASTNode:
    def __init__(self, line, col):
        self.line = line
        self.col = col
        self.type = None    # Will be filled by semantic analysis
```

**Why:** Don't wait until semantic analysis to add this field. Parser is the natural place to set up the structure.

**Not for:** Runtime type tags. For: Inferred types, resolved types, type annotations.

---

## Design Checklist

For each AST node class, ask:

1. **Does this node represent a semantic construct?**
   - Yes → create node
   - No → it's grammar artifact; merge with parent

2. **What information is necessary to represent this construct?**
   - Include only necessary fields
   - Discard punctuation, keywords (encoded in node type)

3. **What will semantic analysis need?**
   - Type checking → reserve type field
   - Scope resolution → might need symbol table links
   - Optimization → might need metadata (mutable, side-effects, etc.)

4. **What will code generation need?**
   - Target information? → prepare field
   - Register requirements? → metadata

5. **Can two different semantic constructs share a node?**
   - Use operator field (like BinaryOp)
   - Or separate node classes (clearer semantics)

6. **Is this node collection or scalar?**
   - Multiple: use array (like statements list)
   - Single or optional: use scalar with None

7. **Include source location?**
   - Always yes (unless it's truly never needed)

---

## AST for Simple Expression Language

### Complete Example

```python
class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self, line=0, col=0):
        self.line = line
        self.col = col
        self.type = None

# Expressions
class IntLiteral(ASTNode):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name, line, col):
        super().__init__(line, col)
        self.name = name

class BinaryOp(ASTNode):
    def __init__(self, op, left, right, line, col):
        super().__init__(line, col)
        self.op = op        # '+', '-', '*', '/'
        self.left = left
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand, line, col):
        super().__init__(line, col)
        self.op = op        # '-', '!'
        self.operand = operand

class FunctionCall(ASTNode):
    def __init__(self, name, args, line, col):
        super().__init__(line, col)
        self.name = name
        self.args = args    # list of ASTNode

# Statements
class Block(ASTNode):
    def __init__(self, statements, line, col):
        super().__init__(line, col)
        self.statements = statements  # list of ASTNode

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block, line, col):
        super().__init__(line, col)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block  # None if no else

class WhileStatement(ASTNode):
    def __init__(self, condition, body, line, col):
        super().__init__(line, col)
        self.condition = condition
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value, line, col):
        super().__init__(line, col)
        self.value = value  # None if bare 'return'

class ExpressionStatement(ASTNode):
    def __init__(self, expr, line, col):
        super().__init__(line, col)
        self.expr = expr

# Declarations
class FunctionDecl(ASTNode):
    def __init__(self, name, params, body, line, col):
        super().__init__(line, col)
        self.name = name
        self.params = params      # list of strings (parameter names)
        self.body = body          # Block

class Program(ASTNode):
    def __init__(self, functions):
        super().__init__()
        self.functions = functions  # list of FunctionDecl
```

**Properties of this design:**
- ✅ No ExprTail, TermTail (grammar artifacts)
- ✅ Binary operators unified (single BinaryOp class)
- ✅ Collections are arrays (statements, arguments, parameters)
- ✅ Source location on every node
- ✅ Type field ready for semantic analysis
- ✅ Optional fields as None

---

## Anti-Patterns

### Anti-Pattern 1: Grammar Mirroring

**Bad:** AST mirrors grammar exactly.

```python
# Grammar: Expr → Term ExprTail
# Result: ExprTail node in AST (artifact)
class ExprTail(ASTNode):
    def __init__(self, operator, term, tail):
        self.operator = operator
        self.term = term
        self.tail = tail  # ExprTail or None
```

**Problem:** Traversal code must handle ExprTail (which has no semantic meaning).

**Better:** Let iteration in parse function flatten the tree.

---

### Anti-Pattern 2: Excessive Node Types

**Bad:**
```python
class AddExpression(ASTNode): ...
class SubtractExpression(ASTNode): ...
class MultiplyExpression(ASTNode): ...
class DivideExpression(ASTNode): ...
```

**Problem:** Boilerplate. 20+ nearly identical classes.

**Better:** Single BinaryOp with operator field.

---

### Anti-Pattern 3: Losing Information

**Bad:** Parser throws away important info (location, original tokens, comments).

```python
# Lost: which operator in parse of 'a + b'
class BinaryOp(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
```

**Better:** Keep location, operator, and metadata.

---

### Anti-Pattern 4: Mixing Concerns

**Bad:** Type information in parser.

```python
class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
        self.resolved_type = None  # DON'T populate in parser
        self.resolved_symbol = None
```

**Better:** Reserve field, but don't populate:

```python
class Identifier(ASTNode):
    def __init__(self, name, line, col):
        super().__init__(line, col)
        self.name = name
        self.resolved_type = None  # Semantic phase will fill
        self.resolved_symbol = None
```

**Reason:** Separation of concerns. Parser builds structure; semantic phase fills meaning.

---

## Visitor Pattern for AST Traversal

**Standard approach for operating on AST:**

```python
class ASTVisitor:
    """Base visitor for all node types"""
    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise NotImplementedError(f"No visit method for {node.__class__.__name__}")

class EvaluatorVisitor(ASTVisitor):
    """Example: evaluates arithmetic expressions"""
    def visit_IntLiteral(self, node):
        return node.value
    
    def visit_Identifier(self, node):
        return self.environment[node.name]
    
    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        # ...
    
    def visit_IfStatement(self, node):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.then_block)
        elif node.else_block:
            self.visit(node.else_block)
```

**Why:** Separates structure (AST) from operations (visitors).

**Benefit:** Add new operations without modifying AST classes.

---

## Testing AST Design

### Invariant: Structure Preservation

**Property:** Parse, then print AST → should accurately represent program.

```python
def test_ast_structure():
    source = "3 + 4 * 5"
    ast = parser.parse(source)
    
    # Verify structure
    assert isinstance(ast, BinaryOp)
    assert ast.op == '+'
    assert isinstance(ast.left, IntLiteral)
    assert isinstance(ast.right, BinaryOp)  # Multiplication is deeper
```

### Invariant: Complete Information

**Property:** AST contains all information needed for semantic analysis.

```python
def test_ast_location_info():
    ast = parser.parse("x + y")
    walk_ast(ast, lambda node: 
        assert node.line > 0 and node.col >= 0
    )
```

### Invariant: Determinism

**Property:** Same input → same AST structure (not object identity).

```python
def test_ast_determinism():
    source = "if (a) x else y"
    ast1 = parser.parse(source)
    ast2 = parser.parse(source)
    
    assert ast_equal(ast1, ast2)  # Same structure
    assert ast1 is not ast2       # Different objects
```

---

## Evolution: AST to IR

**AST is first representation, not final.**

As program moves through compiler:
1. **Parser** → AST (high-level, grammar-oriented)
2. **Semantic analysis** → annotated AST (types, symbols)
3. **Lowering** → Intermediate Representation (machine-oriented)

**Each step removes more abstraction.**

**AST properties to preserve:**
- Sufficient for semantic analysis
- Clean for common operations (traversal, transformation)
- Not prematurely optimized (keep high-level structure)

---

## Summary

**AST is the **bridge** between syntactic structure (grammar) and semantic meaning (types, symbols, optimization).**

**Design principles:**
1. **Semantic constructs** → nodes
2. **Syntactic artifacts** → discard (already in tree structure)
3. **Operators** → data (field in node)
4. **Collections** → arrays
5. **Optionals** → None
6. **Always** → source location
7. **Placeholder** → type field for semantic phase

**Key insight:** A good AST makes later compiler phases trivial. A bad AST makes them painful.

---

## Related Zettels

- [[zettel/Z0021-recursive-descent-pattern]] — How to build AST during parsing
- [[zettel/Z0005-compiler-phases]] — AST in context of full compilation
- [[zettel/Z0003-representation]] — Representation as central compiler concept
