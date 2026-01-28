## Links
- Up: [[03-parsing/README]]
- Related: [[03-parsing/ambiguity]] [[03-parsing/recursive-descent]] [[03-parsing/trees-vs-structure]]
- Down: [[zettel/Z0022-operator-precedence]]

---

# Precedence and Associativity

## Overview

When parsing expressions like `3 + 4 * 5` or `a - b - c`, two questions arise:
1. **Precedence:** Which operator binds tighter? (`*` before `+`)
2. **Associativity:** How do operators of equal precedence group? (`-` left-to-right)

**Key insight:** Grammar structure encodes both. Deeper in grammar = higher precedence. Iteration direction determines associativity.

**Without explicit precedence rules:**
- `3 + 4 * 5` could mean `(3 + 4) * 5 = 35` or `3 + (4 * 5) = 23`
- `a - b - c` could mean `(a - b) - c` or `a - (b - c)`

**With grammar stratification:** Unambiguous parse, no precedence tables.

---

## The Problem: Ambiguity

### Example: Flat Expression Grammar

**Grammar (ambiguous):**
```
Expr → Expr '+' Expr
     | Expr '-' Expr
     | Expr '*' Expr
     | Expr '/' Expr
     | INT
```

**Input:** `2 + 3 * 4`

**Parse tree 1 (wrong):**
```
       +
      / \
     2   *
        / \
       3   4
Result: 2 + (3 * 4) = 14
```

**Parse tree 2 (wrong):**
```
       *
      / \
     +   4
    / \
   2   3
Result: (2 + 3) * 4 = 20
```

**Problem:** Grammar permits multiple parse trees. Parser must **guess**.

---

## Solution 1: Grammar Stratification (Standard Approach)

**Idea:** Layer grammar by operator precedence. Each layer handles one precedence level.

### Precedence Levels (Arithmetic)

| Level | Operators | Precedence | Associativity |
|-------|-----------|------------|---------------|
| 1 | `+`, `-` | Lowest | Left |
| 2 | `*`, `/` | Higher | Left |
| 3 | Atoms | Highest | N/A |

**Grammar (stratified, no left recursion):**
```
Expr   → Term (('+' | '-') Term)*
Term   → Factor (('*' | '/') Factor)*
Factor → INT | ID | '(' Expr ')'
```

**Key properties:**
- `Expr` (lowest precedence) → `Term` (higher) → `Factor` (highest)
- To parse `2 + 3 * 4`:
  - `Expr` parses `Term` (which is `2`), sees `+`, parses another `Term`
  - Second `Term` parses `Factor` (which is `3`), sees `*`, parses another `Factor` (which is `4`)
  - Result: `(* 3 4)` is deeper → evaluates first

**Parse tree:**
```
         Expr
        /    \
      Term    +
       |         \
    Factor      Term
       |        /    \
      INT(2) Factor  *
                |       \
              INT(3)  Factor
                         |
                       INT(4)
```

**AST (simplified):**
```
       +
      / \
     2   *
        / \
       3   4
```

**Multiplication is deeper** → higher precedence encoded structurally.

---

## Encoding Precedence: Deeper = Tighter

### Principle

**Grammar nesting determines evaluation order:**
- Higher precedence operators appear **deeper** in grammar
- To parse expression, start at **lowest** precedence level
- Recursively descend to higher levels

**Example:**

| Grammar Rule | Precedence | Handled Operators |
|--------------|------------|-------------------|
| `Expr → Term ...` | Lowest | `+`, `-` |
| `Term → Factor ...` | Middle | `*`, `/` |
| `Factor → ...` | Highest | Atoms, parentheses |

**Why this works:**
- Parser starts at `Expr` (lowest precedence)
- `Expr` immediately calls `Term` (next level up)
- `Term` immediately calls `Factor` (highest level)
- Parse atoms first, then multiply/divide them, then add/subtract results

**Analogy to order of operations:**
- Elementary school: "PEMDAS" (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction)
- Grammar: Same order, encoded in nesting depth

---

## Encoding Associativity: Left vs. Right

### Left-Associative Operators

Most operators are **left-associative**: `a - b - c` means `(a - b) - c`, not `a - (b - c)`.

**Grammar (right-recursive, but wrong associativity):**
```
Expr → Term '+' Expr | Term
```

**Parse of `1 + 2 + 3`:**
```
     +
    / \
   1   +
      / \
     2   3
Result: 1 + (2 + 3) — RIGHT-associative
```

**Problem:** Right recursion gives right-associativity.

**Solution: Iteration (left-associative):**
```
Expr → Term ('+' Term)*
```

**Code:**
```python
def parse_expr(self):
    left = self.parse_term()
    while self.match('+'):
        self.advance()
        right = self.parse_term()
        left = BinaryOp('+', left, right)  # Reassign left
    return left
```

**Execution on `1 + 2 + 3`:**
```
Iteration 1: left = 1, right = 2 → left = (+ 1 2)
Iteration 2: left = (+ 1 2), right = 3 → left = (+ (+ 1 2) 3)
Result: ((1 + 2) + 3) — LEFT-associative
```

**Key:** Loop reassigns `left`, building left-associative tree.

---

### Right-Associative Operators

Some operators are **right-associative**: `a = b = c` means `a = (b = c)` (assign c to b, then result to a).

**Grammar:**
```
Assign → ID '=' Assign | Expr
```

**Right recursion is correct here:**
```python
def parse_assign(self):
    if self.match(ID) and self.peek_ahead() == '=':
        name = self.current_token.value
        self.advance()  # ID
        self.expect('=')
        value = self.parse_assign()  # Recursive call
        return Assignment(name, value)
    else:
        return self.parse_expr()
```

**Execution on `a = b = 5`:**
```
parse_assign() for 'a'
  sees ID 'a', lookahead '='
  recursively parse_assign() for 'b'
    sees ID 'b', lookahead '='
    recursively parse_assign() for '5'
      parse_expr() → IntLiteral(5)
    return Assignment('b', IntLiteral(5))
  return Assignment('a', Assignment('b', IntLiteral(5)))
```

**AST:**
```
      =
     / \
    a   =
       / \
      b   5
Result: a = (b = 5) — RIGHT-associative
```

**Key:** Recursion naturally builds right-associative tree.

---

## Complete Example: Arithmetic with Precedence & Associativity

### Operator Precedence Table

| Precedence | Operators | Associativity |
|------------|-----------|---------------|
| 1 (lowest) | `+`, `-` | Left |
| 2 | `*`, `/` | Left |
| 3 | `**` (exponentiation) | Right |
| 4 (highest) | Unary `-`, `!` | Right |

### Grammar

```
Expr       → AddExpr
AddExpr    → MultExpr (('+' | '-') MultExpr)*
MultExpr   → PowExpr (('*' | '/') PowExpr)*
PowExpr    → UnaryExpr ('**' PowExpr)?
UnaryExpr  → ('-' | '!') UnaryExpr | Primary
Primary    → INT | ID | '(' Expr ')'
```

**Notice:**
- Each precedence level has its own production
- Left-associative: iteration (`(...)* `)
- Right-associative: recursion (`... PowExpr?`)
- Unary operators: right-recursive (apply right-to-left)

### Parsing Examples

#### Example 1: `2 + 3 * 4`

**Call stack:**
```
parse_expr()
  parse_addexpr()
    parse_multexpr()
      parse_powexpr()
        parse_unaryexpr()
          parse_primary() → 2
    sees '+', parse_multexpr()
      parse_powexpr()
        parse_unaryexpr()
          parse_primary() → 3
      sees '*', parse_powexpr()
        parse_unaryexpr()
          parse_primary() → 4
      return (* 3 4)
    return (+ 2 (* 3 4))
```

**AST:**
```
       +
      / \
     2   *
        / \
       3   4
```

**Evaluation:** `2 + (3 * 4) = 2 + 12 = 14` ✓

---

#### Example 2: `2 - 3 - 4` (left-associative)

**Call stack:**
```
parse_addexpr()
  parse_multexpr() → 2
  sees '-', parse_multexpr() → 3
    left = (- 2 3)
  sees '-', parse_multexpr() → 4
    left = (- (- 2 3) 4)
  return (- (- 2 3) 4)
```

**AST:**
```
       -
      / \
     -   4
    / \
   2   3
```

**Evaluation:** `(2 - 3) - 4 = -1 - 4 = -5` ✓

---

#### Example 3: `2 ** 3 ** 4` (right-associative)

**Grammar (PowExpr):**
```
PowExpr → UnaryExpr ('**' PowExpr)?
```

**Call stack:**
```
parse_powexpr()
  parse_unaryexpr() → 2
  sees '**', parse_powexpr() (recursive)
    parse_unaryexpr() → 3
    sees '**', parse_powexpr() (recursive)
      parse_unaryexpr() → 4
      return 4
    return (** 3 4)
  return (** 2 (** 3 4))
```

**AST:**
```
      **
     /  \
    2   **
       /  \
      3    4
```

**Evaluation:** `2 ** (3 ** 4) = 2 ** 81 = huge number` ✓

**If it were left-associative:** `(2 ** 3) ** 4 = 8 ** 4 = 4096` (different!)

---

#### Example 4: `-3 * 4` (unary vs. binary)

**Grammar (UnaryExpr):**
```
UnaryExpr → ('-' | '!') UnaryExpr | Primary
```

**Call stack:**
```
parse_multexpr()
  parse_powexpr()
    parse_unaryexpr()
      sees '-', parse_unaryexpr() (recursive)
        parse_primary() → 3
      return (unary- 3)
  sees '*', parse_powexpr()
    parse_unaryexpr()
      parse_primary() → 4
  return (* (unary- 3) 4)
```

**AST:**
```
       *
      / \
  unary-  4
     |
     3
```

**Evaluation:** `(-3) * 4 = -12` ✓

**Crucial:** Unary `-` parsed as part of `UnaryExpr`, not `AddExpr`.

---

## Precedence Table to Grammar: The Translation

### Step-by-Step Process

**Given precedence table:**

| Precedence | Operators | Associativity |
|------------|-----------|---------------|
| 1 | `||` | Left |
| 2 | `&&` | Left |
| 3 | `==`, `!=` | Left |
| 4 | `<`, `>`, `<=`, `>=` | Left |
| 5 | `+`, `-` | Left |
| 6 | `*`, `/`, `%` | Left |
| 7 | Unary `-`, `!` | Right |
| 8 | Primary | N/A |

**Grammar:**

```
Expr       → OrExpr
OrExpr     → AndExpr ('||' AndExpr)*
AndExpr    → EqExpr ('&&' EqExpr)*
EqExpr     → RelExpr (('==' | '!=') RelExpr)*
RelExpr    → AddExpr (('<' | '>' | '<=' | '>=') AddExpr)*
AddExpr    → MultExpr (('+' | '-') MultExpr)*
MultExpr   → UnaryExpr (('*' | '/' | '%') UnaryExpr)*
UnaryExpr  → ('-' | '!') UnaryExpr | Primary
Primary    → INT | ID | '(' Expr ')'
```

**Pattern:**
1. **One non-terminal per precedence level**
2. **Lowest precedence at top** (Expr → OrExpr)
3. **Each level calls next higher level**
4. **Left-assoc:** `A → B (op B)*` with iteration
5. **Right-assoc:** `A → B op A` with recursion

---

## Common Pitfalls

### Pitfall 1: Precedence Inversion

**Wrong grammar (multiplication at top level):**
```
Expr → Expr '*' Expr | Expr '+' Expr | INT
```

**Problem:** No nesting → ambiguous. Could parse `2 + 3 * 4` as `(2 + 3) * 4`.

**Fix:** Stratify: addition above multiplication.

---

### Pitfall 2: Wrong Associativity

**Wrong (right-associative subtraction):**
```
Expr → Term '-' Expr | Term
```

**Parses `5 - 3 - 1` as `5 - (3 - 1) = 5 - 2 = 3` (wrong)**

**Fix:** Use iteration for left-associativity:
```
Expr → Term ('-' Term)*
```

---

### Pitfall 3: Mixing Precedence Levels

**Wrong:**
```
Expr → Expr ('+' | '*') Expr | INT
```

**Problem:** `+` and `*` at same level → ambiguous.

**Fix:** Separate levels:
```
Expr → Term ('+' Term)*
Term → Factor ('*' Factor)*
Factor → INT
```

---

## Alternative: Precedence Climbing

**For dynamically adding operators or complex precedence tables, recursive descent can be awkward. Precedence climbing is a hybrid approach.**

### Algorithm

```python
def parse_expr(min_precedence):
    left = parse_primary()
    while is_binop(current_token) and precedence(current_token) >= min_precedence:
        op = current_token
        advance()
        right = parse_expr(precedence(op) + (1 if left_assoc(op) else 0))
        left = BinaryOp(op, left, right)
    return left
```

**Key idea:**
- Parse left operand (primary)
- While operator has sufficient precedence, parse right operand with **higher minimum precedence**
- Associativity: left-assoc increments precedence for right side (forces it to bind tighter)

**Pros:**
- Single parsing function (no stratification)
- Easy to add operators dynamically

**Cons:**
- Less intuitive than stratified grammar
- Requires precedence/associativity tables

**Used in:** Expression parsers for languages with many operators (e.g., C, C++).

---

## Precedence and Parentheses

**Parentheses override precedence** by forcing evaluation order.

**Grammar:**
```
Primary → '(' Expr ')'
```

**Key:** `Primary` is highest precedence level, but contains `Expr` (lowest level via recursion).

**Effect:**
- `(2 + 3) * 4`: Parentheses force `+` to be parsed first (deeper in tree)
- Without stratification, this wouldn't be possible

**Example parse: `(2 + 3) * 4`**

**Call stack:**
```
parse_multexpr()
  parse_primary()
    sees '(', parse_expr()
      parse_addexpr()
        parse_multexpr() → 2
        sees '+', parse_multexpr() → 3
        return (+ 2 3)
    expects ')'
    return (+ 2 3)
  sees '*', parse_primary() → 4
  return (* (+ 2 3) 4)
```

**AST:**
```
       *
      / \
     +   4
    / \
   2   3
```

**Evaluation:** `(2 + 3) * 4 = 5 * 4 = 20` ✓

---

## Grammar Stratification: A Systematic Approach

### Design Process

**1. List all operators with precedence and associativity**

Example:
```
|| (left, precedence 1)
&& (left, precedence 2)
== != (left, precedence 3)
< > <= >= (left, precedence 4)
+ - (left, precedence 5)
* / % (left, precedence 6)
unary -, ! (right, precedence 7)
```

**2. Create one non-terminal per precedence level**

```
Expr (entry point)
OrExpr
AndExpr
EqExpr
RelExpr
AddExpr
MultExpr
UnaryExpr
Primary
```

**3. For each level, write production**

**Left-associative:**
```
A → B (op B)*
```

**Right-associative:**
```
A → B op A | B
```

**Or (cleaner):**
```
A → B (op A)?
```

**4. Link levels: each calls next higher precedence**

```
OrExpr → AndExpr ...
AndExpr → EqExpr ...
EqExpr → RelExpr ...
```

**5. Highest level is atoms**

```
Primary → INT | ID | '(' Expr ')'
```

---

## Testing Precedence and Associativity

### Test Cases

**Precedence:**
- `2 + 3 * 4` → `2 + (3 * 4)` → 14
- `2 * 3 + 4` → `(2 * 3) + 4` → 10
- `2 + 3 + 4 * 5` → `(2 + 3) + (4 * 5)` → 25

**Associativity (left):**
- `5 - 3 - 1` → `(5 - 3) - 1` → 1 (not `5 - (3 - 1)` → 3)
- `10 / 5 / 2` → `(10 / 5) / 2` → 1 (not `10 / (5 / 2)` → 4)

**Associativity (right):**
- `a = b = 5` → `a = (b = 5)` (both a and b get 5)
- `2 ** 3 ** 2` → `2 ** (3 ** 2)` → 512 (not `(2 ** 3) ** 2` → 64)

**Parentheses:**
- `(2 + 3) * 4` → 20
- `2 + (3 * 4)` → 14
- `((2 + 3) * 4)` → 20

**Unary operators:**
- `-3 * 4` → `(-3) * 4` → -12
- `-(3 * 4)` → `-(12)` → -12
- `!a && b` → `(!a) && b`

### Systematic Verification

**Like perft testing in chess:**
1. Enumerate test cases
2. Calculate expected result
3. Parse and evaluate
4. Compare actual vs. expected

**Property:** Parser must be **deterministic**—same input always produces same AST.

---

## Chess Engine Analogy

**Precedence ↔ Piece values**
- Just as `*` binds tighter than `+`, queen is worth more than pawn
- Evaluation function weights: analogous to precedence levels

**Associativity ↔ Move ordering**
- Left-associative: process moves left-to-right (move ordering heuristic)
- Right-associative: process right-to-left (e.g., PV move first)

**Grammar stratification ↔ Evaluation layers**
- Material → Mobility → King safety → Pawn structure
- Each layer "calls" next layer, just like Expr → Term → Factor

---

## AoC Analogy

**Parsing expressions in AoC puzzles:**
- Day 18 (2020): Math homework with precedence rules
- Day 18 (2015): String evaluation with operators

**Lesson:** Grammar stratification makes evaluation trivial. Parse once, evaluate recursively.

**Pattern:** Transform input into structured form (AST) → process structure (evaluate).

---

## Summary

| Concept | Technique | Effect |
|---------|-----------|--------|
| **Precedence** | Grammar stratification (nesting) | Deeper in grammar = higher precedence |
| **Left-assoc** | Iteration `(op B)*` | Build left-associative tree via loop |
| **Right-assoc** | Recursion `op A` | Natural right-associative tree |
| **Parentheses** | `Primary → '(' Expr ')'` | Override precedence via recursion |
| **Unary operators** | Right-recursive rule | Apply right-to-left |

**Key principles:**
1. **One non-terminal per precedence level**
2. **Lowest precedence at top of grammar**
3. **Each level calls next higher level**
4. **Iteration for left-assoc, recursion for right-assoc**
5. **Atoms at bottom (highest precedence)**

**Benefit:** Grammar **encodes** precedence and associativity. Parser is **mechanical translation**—no special cases, no precedence tables, just follow the structure.

---

## Further Reading

- [[03-parsing/recursive-descent]] — Implementation of stratified grammars
- [[03-parsing/trees-vs-structure]] — AST structure encodes precedence
- [[03-parsing/ambiguity]] — Ambiguity resolution via stratification
- [[Stanford/lecture-24]] — Precedence in parsing theory
- [[zettel/Z0022-operator-precedence]] — Quick reference

---

## Reflection Questions

1. **Why does deeper nesting in grammar mean higher precedence?**
   - Trace through parser execution on `2 + 3 * 4` to see.

2. **What happens if you swap levels (put `*` above `+` in grammar)?**
   - How does AST change? Is result still correct?

3. **How would you add a new operator (e.g., `%` modulo, same precedence as `*`)?**
   - Modify grammar and code.

4. **Why is exponentiation right-associative while most operators are left-associative?**
   - Mathematical convention: `2^3^4 = 2^(3^4)` (not `(2^3)^4`).

5. **Could you implement precedence with a flat grammar + precedence table?**
   - How would associativity work? (Hint: precedence climbing)
