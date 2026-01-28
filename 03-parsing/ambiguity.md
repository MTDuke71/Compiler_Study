## Links
- Up: [[03-parsing/README]]
- Related: [[03-parsing/trees-vs-structure]] [[03-parsing/precedence-and-associativity]] [[03-parsing/recursive-descent]]
- Down: [[zettel/Z0023-ambiguity-resolution]]

---

# Ambiguity in Grammars

## Overview

A grammar is **ambiguous** if a single input string can produce **multiple distinct parse trees**. Ambiguity is problematic for compilers—the parser must choose one interpretation, but which one?

**Key insight:** Ambiguity is a property of the **grammar**, not the language. A language can have both ambiguous and unambiguous grammars.

**Resolution strategies:**
1. **Rewrite grammar** (eliminate ambiguity structurally)
2. **Add precedence/associativity rules** (disambiguate via metadata)
3. **Parser disambiguation** (choose one parse systematically)
4. **Accept ambiguity** (rare; used in some natural language parsers)

---

## Classic Example: The Dangling Else

### The Problem

**Grammar:**
```
Stmt → 'if' '(' Expr ')' Stmt
     | 'if' '(' Expr ')' Stmt 'else' Stmt
     | 'other'
```

**Input:**
```
if (a) if (b) s1 else s2
```

**Question:** Does `else` match the first `if` or the second `if`?

### Parse Tree 1: Else Matches Inner If

```
           Stmt
            |
      if (a) Stmt
              |
        if (b) Stmt else Stmt
                |         |
               s1        s2
```

**Interpretation:**
```
if (a)
    if (b)
        s1
    else
        s2
```

If `a` is true and `b` is false, execute `s2`.

---

### Parse Tree 2: Else Matches Outer If

```
              Stmt
               |
    if (a) Stmt else Stmt
            |         |
       if (b) Stmt   s2
              |
             s1
```

**Interpretation:**
```
if (a)
    if (b)
        s1
else
    s2
```

If `a` is false, execute `s2` (regardless of `b`).

---

### Two Valid Parse Trees → Ambiguous

**Problem:** Grammar permits both interpretations. Parser must guess.

**Convention (most languages):** Else matches **nearest unmatched if** (Parse Tree 1).

---

## Resolution Strategy 1: Rewrite Grammar

### Disambiguated Grammar

**Idea:** Distinguish between matched (has else) and unmatched (no else) statements.

```
Stmt        → MatchedStmt | UnmatchedStmt
MatchedStmt → 'if' '(' Expr ')' MatchedStmt 'else' MatchedStmt
            | 'other'
UnmatchedStmt → 'if' '(' Expr ')' Stmt
              | 'if' '(' Expr ')' MatchedStmt 'else' UnmatchedStmt
```

**Key properties:**
- `MatchedStmt`: Both branches have else (fully matched)
- `UnmatchedStmt`: At least one branch has no else
- Between `if` and `else`, only `MatchedStmt` allowed → forces else to bind to innermost if

**Parse of `if (a) if (b) s1 else s2`:**

```
           Stmt
            |
      UnmatchedStmt
            |
    if (a) Stmt
            |
      MatchedStmt
            |
    if (b) MatchedStmt else MatchedStmt
              |                |
           other(s1)        other(s2)
```

**Only one parse tree possible.** Ambiguity eliminated.

**Tradeoff:** Grammar more complex, but unambiguous.

---

## Resolution Strategy 2: Precedence Rules

### Parser Directive Approach

**Keep simple grammar, add disambiguation rule:**

```
Stmt → 'if' '(' Expr ')' Stmt
     | 'if' '(' Expr ')' Stmt 'else' Stmt
     | 'other'

Disambiguation rule: Else binds to nearest if.
```

**Parser implementation:**
```python
def parse_stmt(self):
    if self.match('if'):
        self.expect('if')
        self.expect('(')
        cond = self.parse_expr()
        self.expect(')')
        then_stmt = self.parse_stmt()
        
        if self.match('else'):
            self.expect('else')
            else_stmt = self.parse_stmt()
            return IfElseStmt(cond, then_stmt, else_stmt)
        else:
            return IfStmt(cond, then_stmt)
    # ... other statements
```

**Effect:** When parsing nested `if`, `else` immediately binds to current `if` (greedy matching).

**Benefit:** Simple grammar, simple implementation, matches programmer intuition.

---

## Classic Example 2: Arithmetic Expressions

### The Problem

**Grammar:**
```
Expr → Expr '+' Expr
     | Expr '-' Expr
     | Expr '*' Expr
     | Expr '/' Expr
     | INT
```

**Input:** `2 + 3 * 4`

**Parse Tree 1:** `(2 + 3) * 4 = 20`
```
       *
      / \
     +   4
    / \
   2   3
```

**Parse Tree 2:** `2 + (3 * 4) = 14`
```
       +
      / \
     2   *
        / \
       3   4
```

**Parse Tree 3:** `((2 + 3) * 4)` — same as Tree 1  
**Parse Tree 4:** `(2 + (3 * 4))` — same as Tree 2

**Multiple parse trees → Ambiguous.**

---

### The Problem: Associativity

**Input:** `5 - 3 - 1`

**Parse Tree 1:** `(5 - 3) - 1 = 1` (left-associative)
```
       -
      / \
     -   1
    / \
   5   3
```

**Parse Tree 2:** `5 - (3 - 1) = 3` (right-associative)
```
       -
      / \
     5   -
        / \
       3   1
```

**Which is correct?** Convention: subtraction is left-associative → Tree 1.

---

## Resolution: Grammar Stratification

**Unambiguous grammar (stratified by precedence):**

```
Expr   → Term (('+' | '-') Term)*
Term   → Factor (('*' | '/') Factor)*
Factor → INT
```

**Properties:**
- Precedence encoded by nesting (Term inside Expr)
- Associativity encoded by iteration (left-to-right)
- Only one parse tree possible for any input

**Parse of `2 + 3 * 4`:**

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

**Simplified AST:**
```
       +
      / \
     2   *
        / \
       3   4
```

**Result:** `2 + (3 * 4) = 14` — unambiguous.

**See:** [[03-parsing/precedence-and-associativity]] for detailed coverage.

---

## Types of Ambiguity

### 1. Structural Ambiguity

**Multiple ways to group symbols.**

**Example:** `a - b - c`
- `(a - b) - c` (left-associative)
- `a - (b - c)` (right-associative)

**Resolution:** Grammar stratification or associativity rules.

---

### 2. Precedence Ambiguity

**Unclear operator binding.**

**Example:** `a + b * c`
- `(a + b) * c` (addition first)
- `a + (b * c)` (multiplication first)

**Resolution:** Precedence levels in grammar.

---

### 3. Syntactic Ambiguity

**Multiple syntactic interpretations.**

**Example (C++):** `A * b;`
- Declaration: "`b` is a pointer to type `A`"
- Expression: "Multiply `A` and `b`, discard result"

**Resolution:** Context-sensitive parsing (symbol table lookup) or grammar constraints.

---

### 4. Lexical Ambiguity

**Multiple ways to tokenize.**

**Example:** `a---b`
- Tokens: `a`, `--`, `-`, `b` → `(a--) - b`
- Tokens: `a`, `-`, `--`, `b` → `a - (--b)`

**Resolution:** Maximal munch (longest token wins).

---

## Detecting Ambiguity

### Method 1: Find Multiple Derivations

**For small grammars:**
1. Pick input string
2. Try to construct two different leftmost (or rightmost) derivations
3. If successful → ambiguous

**Example:**

**Grammar:** `Expr → Expr '+' Expr | INT`

**Input:** `1 + 2 + 3`

**Derivation 1 (left-associative):**
```
Expr
→ Expr '+' Expr
→ (Expr '+' Expr) '+' Expr
→ (INT(1) '+' Expr) '+' Expr
→ (INT(1) '+' INT(2)) '+' Expr
→ (INT(1) '+' INT(2)) '+' INT(3)
```

**Derivation 2 (right-associative):**
```
Expr
→ Expr '+' Expr
→ Expr '+' (Expr '+' Expr)
→ INT(1) '+' (Expr '+' Expr)
→ INT(1) '+' (INT(2) '+' Expr)
→ INT(1) '+' (INT(2) '+' INT(3))
```

**Two different derivations → Ambiguous.**

---

### Method 2: Automated Detection

**Problem:** Undecidable in general (no algorithm can detect all cases).

**Partial solutions:**
- **LR parser generators** (yacc, bison): Report shift/reduce or reduce/reduce conflicts
- **LL parser generators** (ANTLR): Report first/follow set conflicts
- **Manual analysis:** Reason about grammar structure

**Practical approach:** Try to generate parser; if tool reports conflicts, grammar may be ambiguous.

---

## Ambiguity in Parser Generators

### Shift/Reduce Conflicts (LR Parsers)

**Scenario:** Parser can either:
- **Shift:** Read another token
- **Reduce:** Apply a production

**Example (dangling else):**

**State:** Parsed `if (a) if (b) s`, lookahead is `else`

**Choices:**
1. **Shift** `else` → matches inner if
2. **Reduce** `if (b) s` to `Stmt`, then shift `else` → matches outer if

**Conflict!** Parser generator asks: "Which one?"

**Resolution:** Precedence directive (shift wins → else matches nearest if).

---

### Reduce/Reduce Conflicts (LR Parsers)

**Scenario:** Multiple productions apply.

**Example:**

```
A → 'x'
B → 'x'
S → A | B
```

**Input:** `x`

**Choices:**
1. Reduce `x` to `A`, then to `S`
2. Reduce `x` to `B`, then to `S`

**Conflict!** Both reductions possible.

**Resolution:** Grammar is ambiguous; must be rewritten.

---

## When Ambiguity Is Acceptable

### Natural Language Processing

**Natural languages are inherently ambiguous.**

**Example:** "I saw a man with a telescope."
- I used a telescope to see the man
- I saw a man who has a telescope

**Solution:** Generate all parse trees, rank by probability.

---

### Intentional Ambiguity

**Some languages allow multiple interpretations, resolved at runtime.**

**Example (Perl):** Context-sensitive parsing based on symbol table.

**Tradeoff:** Flexibility vs. complexity.

---

## Disambiguation Techniques Summary

| Technique | How It Works | Pros | Cons |
|-----------|--------------|------|------|
| **Grammar rewriting** | Eliminate ambiguity structurally | Unambiguous, clear | Grammar becomes complex |
| **Precedence rules** | Metadata guides parser | Simple grammar | Rules separate from grammar |
| **Associativity rules** | Left/right preference | Intuitive | Not always sufficient |
| **Longest match** | Greedy token matching | Simple, fast | Can cause surprises |
| **Parser directives** | Tool-specific annotations | Pragmatic | Tool-dependent |
| **Context-sensitive** | Use semantic info | Powerful | Complex, slow |

---

## Examples: Ambiguous vs. Unambiguous

### Example 1: Simple Arithmetic

**Ambiguous:**
```
Expr → Expr '+' Expr | INT
```

**Unambiguous:**
```
Expr → Term ('+' Term)*
Term → INT
```

---

### Example 2: If-Else

**Ambiguous:**
```
Stmt → 'if' Expr Stmt
     | 'if' Expr Stmt 'else' Stmt
     | 'other'
```

**Unambiguous:**
```
Stmt → MatchedStmt | OpenStmt
MatchedStmt → 'if' Expr MatchedStmt 'else' MatchedStmt | 'other'
OpenStmt → 'if' Expr Stmt
         | 'if' Expr MatchedStmt 'else' OpenStmt
```

---

### Example 3: Function Calls vs. Multiplication (C++)

**Ambiguous (context-sensitive):**
```
Stmt → Type '*' ID ';'   // Pointer declaration
     | Expr ';'          // Expression statement
Expr → ID '*' ID         // Multiplication
```

**Input:** `A * b;`

**Interpretation depends on:** Is `A` a type or a variable?

**Resolution:** Symbol table lookup during parsing (context-sensitive).

---

## Chess Engine Analogy

**Ambiguity ↔ Multiple best moves**

In chess, sometimes multiple moves appear equally good (ambiguous evaluation).

**Resolution strategies:**
1. **Tie-breaking rules** (like precedence rules): Prefer certain move types
2. **Deeper search** (like lookahead): Analyze further to disambiguate
3. **Heuristics** (like associativity): Left-to-right move ordering

**Compiler parallel:** Grammar ambiguity resolved via precedence, lookahead, or rewriting.

---

## AoC Analogy

**Parsing ambiguous input:**

Some AoC puzzles have intentionally ambiguous specifications:
- "What if there are ties?" (like ambiguous parse)
- Solution: Rules for tie-breaking (precedence/associativity)

**Pattern:** When faced with ambiguity:
1. Identify all possibilities
2. Apply disambiguation rule
3. Proceed deterministically

Same process in parsing.

---

## Practical Implications

### For Language Designers

**Avoid ambiguous grammars when possible:**
- Easier to implement
- Better error messages
- Predictable behavior

**If ambiguity is necessary:**
- Document disambiguation rules clearly
- Provide examples
- Make parser behavior predictable

---

### For Compiler Writers

**Detect ambiguity early:**
- Use parser generator conflict reports
- Test with edge cases
- Manual grammar analysis

**Resolve systematically:**
1. Try grammar rewriting first (cleanest)
2. Use precedence/associativity if rewriting too complex
3. Document any non-obvious choices

---

### For Users

**Understand language disambiguation:**
- Know operator precedence
- Understand associativity
- Use parentheses when in doubt

**Example:** Don't write `a - b - c` if meaning isn't obvious; write `(a - b) - c`.

---

## Testing for Ambiguity

### Systematic Testing

**Like perft testing in chess:**

1. **Generate test cases** covering edge cases:
   - Nested constructs (if inside if)
   - Long chains (a - b - c - d)
   - Mixed operators (a + b * c / d)

2. **Compute expected parse tree** (manually or via reference)

3. **Parse and compare**

4. **Verify determinism:** Same input → same parse tree every time

---

### Edge Cases to Test

**If-else:**
- Single if
- If-else
- If-if-else (dangling else)
- If-else-if-else (chained)

**Expressions:**
- Single operator: `a + b`
- Same precedence: `a + b + c`
- Mixed precedence: `a + b * c`
- Parentheses: `(a + b) * c`
- Deeply nested: `((a + b) * (c - d)) / e`

**Whitespace variations:**
- `a+b` vs. `a + b` (should parse identically)
- `a- -b` vs. `a--b` (lexical ambiguity)

---

## Common Mistakes

### Mistake 1: Ignoring Ambiguity

**Problem:** "It works for my test cases, so it's fine."

**Reality:** Ambiguous grammar may parse some inputs consistently by accident, fail on others unpredictably.

**Fix:** Systematically test edge cases, use parser generator to detect conflicts.

---

### Mistake 2: Conflating Grammar and Language

**Grammar is ambiguous ≠ Language is ambiguous**

A language can have multiple grammars (some ambiguous, some not).

**Example:** Arithmetic expressions
- Ambiguous grammar: `Expr → Expr '+' Expr | INT`
- Unambiguous grammar: `Expr → Term ('+' Term)*`
- Same language, different grammars

**Fix:** Rewrite grammar to eliminate ambiguity; language stays the same.

---

### Mistake 3: Over-Relying on Precedence Tables

**Problem:** Complex precedence rules as band-aid for ambiguous grammar.

**Result:** Grammar is still ambiguous; parser just has hacks to resolve it.

**Fix:** Prefer grammar rewriting. Precedence rules should be **minimal**.

---

## Summary

**Ambiguity:** One input, multiple parse trees.

**Detection:**
- Multiple derivations for same input
- Parser generator conflicts (shift/reduce, reduce/reduce)
- Manual analysis

**Resolution:**
1. **Grammar rewriting** (best: eliminates ambiguity structurally)
2. **Precedence/associativity rules** (pragmatic: simple rules)
3. **Parser directives** (tool-specific)
4. **Context-sensitive parsing** (complex: use semantic info)

**Key principle:** **Determinism** — parser must behave predictably. Ambiguous grammar violates this.

**Best practice:** Design unambiguous grammars from the start. It's easier than fixing later.

---

## Further Reading

- [[03-parsing/precedence-and-associativity]] — Grammar stratification to resolve ambiguity
- [[03-parsing/trees-vs-structure]] — How ambiguity affects AST construction
- [[03-parsing/recursive-descent]] — Implementing unambiguous parsers
- [[Stanford/lecture-25]] — Ambiguity in formal grammars
- [[zettel/Z0023-ambiguity-resolution]] — Quick reference

---

## Reflection Questions

1. **Is the dangling else problem a limitation of the grammar or the language?**
   - Could you design a language syntax that avoids the issue entirely?

2. **Why is `Expr → Expr '+' Expr | INT` ambiguous but `Expr → Term ('+' Term)*` is not?**
   - What structural difference eliminates ambiguity?

3. **Can all ambiguous grammars be rewritten to be unambiguous?**
   - Are there inherently ambiguous languages?

4. **How does maximal munch relate to ambiguity?**
   - Is it a form of disambiguation?

5. **If you were designing a new programming language, how would you avoid common ambiguities?**
   - What syntax decisions matter most?

---

## Historical Note

**The dangling else problem** dates to ALGOL 60 (1960). Early languages struggled with it.

**Solutions evolved:**
- **ALGOL:** Required explicit `begin`/`end` blocks
- **C:** Adopted "else matches nearest if" convention
- **Python:** Eliminated problem via mandatory indentation (no ambiguity possible)
- **Modern languages:** Often require braces or keywords to make structure explicit

**Lesson:** Language design can make parser implementation trivial—or nightmarish. Choose syntax carefully.
