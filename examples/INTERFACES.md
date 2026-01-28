# Compiler Phase Interfaces

## Purpose

This document defines the **contracts between compiler phases**. Each phase:
- Has clear **inputs** and **outputs**
- Makes **guarantees** about what it produces
- Has **requirements** about what it accepts

Following these contracts ensures phases can be developed, tested, and replaced independently.

---

## Token Format (Lexer → Parser)

**File:** `token_types.py`

### Contract

```python
@dataclass
class Token:
    type: TokenType      # REQUIRED: Token classification
    value: Any           # REQUIRED: Parsed value or None
    lexeme: str          # REQUIRED: Original source text
    line: int            # REQUIRED: 1-based line number
    column: int          # REQUIRED: 1-based column number
```

### Lexer Guarantees

A conforming lexer **MUST**:
1. **Produce valid Token objects** with all 5 fields populated
2. **Set type** to a value from the `TokenType` enum
3. **Set value correctly**:
   - For `NUMBER`: integer or float value (e.g., `42`, `3.14`)
   - For `IDENTIFIER`: None (lexeme contains the name)
   - For operators/punctuation: None
   - For `STRING`: the parsed string (escape sequences processed)
4. **Set lexeme** to the exact characters from source
5. **Track location accurately** (1-based line and column)
6. **End with EOF token** when source is exhausted
7. **Return same EOF repeatedly** if `next_token()` called after exhaustion
8. **Use ERROR token** for lexical errors (invalid characters, unterminated strings)

### Parser Requirements

A conforming parser **MUST**:
1. **Accept any sequence of Token objects** matching the contract
2. **Check token.type** using `TokenType` enum (not strings)
3. **Handle EOF gracefully** (not treat it as an error)
4. **Use token.line and token.column** for error messages
5. **Not modify tokens** (treat as immutable)

### Examples

**Valid NUMBER token:**
```python
Token(TokenType.NUMBER, 42, "42", 1, 5)
```

**Valid IDENTIFIER token:**
```python
Token(TokenType.IDENTIFIER, None, "count", 2, 10)
```

**Valid EOF token:**
```python
Token(TokenType.EOF, None, "", 10, 1)
```

**Invalid tokens (violate contract):**
```python
Token("INT", 42, "42", 1, 5)           # ❌ type must be TokenType enum
Token(TokenType.NUMBER, "42", "42", 1, 5)  # ❌ value should be int, not string
Token(TokenType.PLUS, None, "+", 0, 5)     # ❌ line must be >= 1
```

---

## AST Format (Parser → Semantic Analysis)

**File:** `basic-parser-unified.py` (AST node definitions)

### Contract

All AST nodes are **dataclasses** with:
- `line: int` and `column: int` for source location
- Type-specific fields for semantic content

### Parser Guarantees

A conforming parser **MUST**:
1. **Produce valid AST nodes** matching the grammar
2. **Preserve source locations** from tokens
3. **Build correct tree structure** (left-associative for same-precedence operators)
4. **Include all operands** (no implicit operands)
5. **Reject invalid syntax** with clear error messages

### AST Node Types

#### Literals

```python
@dataclass
class IntLiteral:
    value: int
    line: int
    column: int
```

#### Identifiers

```python
@dataclass
class Identifier:
    name: str
    line: int
    column: int
```

#### Binary Operations

```python
@dataclass
class BinaryOp:
    operator: str    # One of: '+', '-', '*', '/'
    left: ASTNode    # Left operand (another AST node)
    right: ASTNode   # Right operand (another AST node)
    line: int
    column: int
```

### Semantic Analyzer Requirements

A conforming semantic analyzer **MUST**:
1. **Accept any valid AST** from the parser
2. **Visit all nodes** (don't skip subtrees)
3. **Use line/column** for error messages
4. **Not modify AST** (create new tree if transforming)
5. **Validate semantics only** (syntax already validated by parser)

---

## Symbol Table (Semantic Analysis → IR Generation)

**Not yet implemented** (Week 7)

Will define:
- Scope structure
- Symbol information (name, type, location)
- Lookup protocol

---

## IR Format (Semantic Analysis → Optimization)

**Not yet implemented** (Week 8-9)

Will define:
- Three-address code format
- Basic block structure
- SSA properties

---

## Design Principles

### 1. Single Source of Truth

**BAD:** Each phase defines its own token type
```python
# lexer.py
class LexerToken:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

# parser.py  
class ParserToken:
    def __init__(self, kind, text, pos):
        self.kind = kind
        self.text = text
        self.pos = pos

# Need adapter:
def convert(lexer_token):
    return ParserToken(lexer_token.type, lexer_token.lexeme, 0)
```

**GOOD:** One definition, everyone imports
```python
# token_types.py
@dataclass
class Token:
    type: TokenType
    value: Any
    lexeme: str
    line: int
    column: int

# lexer.py
from token_types import Token, TokenType

# parser.py
from token_types import Token, TokenType
```

### 2. Design Interfaces First

**Development order:**
1. **Define the contract** (what data passes between phases)
2. **Write tests** using the contract
3. **Implement phases** to satisfy the contract
4. **Verify integration** (no adapters needed!)

**Like chess engine development:**
1. Define board representation (bitboards, mailbox, etc.)
2. Write move generation tests
3. Implement move generator using that representation
4. Write search tests
5. Implement search using same representation

### 3. Make Illegal States Unrepresentable

**BAD:** String-based token types (typos silently accepted)
```python
if token.type == "NUMBER":    # Works
if token.type == "NUMBR":     # Typo! Bug at runtime
```

**GOOD:** Enum enforces valid types
```python
if token.type == TokenType.NUMBER:  # Works
if token.type == TokenType.NUMBR:   # Compile error!
```

### 4. Include Debugging Information

Every interface should include **source location**:
- Tokens have `line` and `column`
- AST nodes have `line` and `column`
- IR instructions will have source mappings

This enables:
- **Error messages:** "Error at line 5, column 12"
- **Debugging:** Step through source, not IR
- **Profiling:** Map hot IR back to source lines

---

## Testing Interfaces

### Lexer Testing

```python
def test_lexer_contract():
    """Verify lexer produces valid tokens."""
    lexer = Lexer("42 + x")
    
    tok1 = lexer.next_token()
    assert isinstance(tok1.type, TokenType)
    assert tok1.value == 42
    assert tok1.lexeme == "42"
    assert tok1.line >= 1
    assert tok1.column >= 1
    
    tok2 = lexer.next_token()
    assert tok2.type == TokenType.PLUS
    assert tok2.value is None
    assert tok2.lexeme == "+"
    
    # ... verify all tokens
    
    eof = lexer.next_token()
    assert eof.type == TokenType.EOF
    
    # Calling again should return same EOF
    eof2 = lexer.next_token()
    assert eof2.type == TokenType.EOF
```

### Parser Testing

```python
def test_parser_contract():
    """Verify parser produces valid AST."""
    tokens = [
        Token(TokenType.NUMBER, 42, "42", 1, 1),
        Token(TokenType.EOF, None, "", 1, 3)
    ]
    
    parser = RecursiveDescentParser(tokens)
    ast = parser.parse()
    
    assert isinstance(ast, IntLiteral)
    assert ast.value == 42
    assert ast.line >= 1
    assert ast.column >= 1
```

### Integration Testing

```python
def test_phase_integration():
    """Verify lexer output works with parser input."""
    source = "2 + 3"
    
    # Phase 1: Lex
    lexer = Lexer(source)
    tokens = []
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.type == TokenType.EOF:
            break
    
    # Phase 2: Parse
    parser = RecursiveDescentParser(tokens)
    ast = parser.parse()
    
    # No adapter needed! Tokens work directly.
    assert isinstance(ast, BinaryOp)
```

---

## Checklist for Adding New Phases

When adding a new compiler phase:

- [ ] **Define the output format** (what data structure it produces)
- [ ] **Document the contract** (guarantees and requirements)
- [ ] **Add to this file** (update INTERFACES.md)
- [ ] **Write interface tests** (verify contract conformance)
- [ ] **Implement the phase** (satisfy the contract)
- [ ] **Test integration** (output works with next phase)

---

## Lessons from Token Unification

**What went wrong:**
- Week 4 and Week 5 developed in isolation
- Each phase defined its own token format
- Integration required adapter pattern
- Adapter was pure overhead (no semantic value)

**What we learned:**
- **Design interfaces first, implement second**
- **One definition, multiple importers**
- **Integration tests catch incompatibilities early**
- **Adapters indicate design failure**

**Chess engine parallel:**
Like choosing board representation (bitboards vs mailbox) - pick one, stick with it throughout. Move generation, search, evaluation all use same format.

**AoC parallel:**
Input parsing defines data structure - all subsequent processing uses that structure. Don't convert between formats mid-solve.

---

## Related Documentation

- [[token_types.py]] - Token format implementation
- [[TOKEN-UNIFICATION.md]] - History of unification work
- [[Daily Notes/2026-01-27]] - Token unification lessons
- [[00-index/invariants]] - Core compiler invariants
