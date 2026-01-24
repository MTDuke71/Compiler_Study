# Z0007: Chomsky Hierarchy — Formal Languages by Expressive Power

## Links
- Up: [[zettel/README]]
- Related: [[Stanford/lecture-18-parsing-intro]] [[Stanford/lecture-19-context-free-grammars]] [[02-lexing/README]] [[03-parsing/README]] [[04-semantics/README]]
- Down: [[02-lexing/regular-languages]] [[03-parsing/recursive-descent]]

---

## Core Principle

The **Chomsky hierarchy** is a classification of formal grammars ordered by **expressive power**. Each level can express strictly more language patterns than the level below, but requires more computational complexity to parse.

**Why it matters for compilers:** Each compiler phase needs exactly the right level of formalism—no more, no less.

---

## The Four Levels

### Type 0: Unrestricted (Recursively Enumerable)

**Recognition:** Turing machine

**Constraint:** No restrictions on production rules

**Example language:**
- Halting problem encoded in language membership
- Any language recognized by any computable algorithm

**Why compilers don't use it:**
- Parsing is undecidable
- Can't tell if string is in language (might loop forever)
- Completely impractical

**Analogy:** Chess rules that allow any physical modification of the board at any time.

---

### Type 1: Context-Sensitive

**Recognition:** Linear-bounded automaton (Turing machine with bounded tape)

**Constraint:** 
$$\alpha A \beta \to \alpha \gamma \beta$$
where $|\gamma| \geq |A|$

Production applies only in specific context ($\alpha$ and $\beta$ surround $A$).

**Example language:**
$$L = \{a^n b^n c^n : n \geq 1\}$$
("Equal counts of a, b, c")

**Why compilers rarely use it explicitly:**
- Parsing is exponential/polynomial time
- Dependency on context makes analysis hard
- Most programs don't need it

**Where it appears:**
- Type checking (context affects validity)
- Semantic constraints on syntax

**Analogy:** Chess rules where "you can move a knight this way, but NOT if your king is in check."

---

### Type 2: Context-Free

**Recognition:** Pushdown automaton (finite automaton + one stack)

**Constraint:**
$$A \to \beta$$

Left side is **always a single non-terminal** (no context needed).

**Example languages:**
- Balanced parentheses: $S \to (S) \mid \epsilon$
- Arithmetic expressions: $E \to E + E \mid E * E \mid \text{id}$
- Most programming language syntax

**Why compilers use it:**
- **Polynomial-time parsing** (typically linear for restricted subclasses)
- **Recursive structure** naturally expresses nesting
- **Well-understood algorithms** (LL, LR, recursive descent)

**Key property:** Can handle arbitrary nesting depth with finite memory (via stack).

**Analogy:** Chess rules that apply uniformly regardless of board position.

---

### Type 3: Regular

**Recognition:** Finite automaton (no memory, only states)

**Constraint:**
$$A \to aB \mid a \mid \epsilon$$

Productions generate at most one terminal and one non-terminal (or just terminals).

**Example languages:**
- Identifiers: `[a-zA-Z_][a-zA-Z0-9_]*`
- Integers: `[0-9]+`
- Floating point: `[0-9]+\.[0-9]*`
- Email: `[a-z]+@[a-z]+\.[a-z]+`

**Why compilers use it for lexing:**
- **Linear-time parsing** (DFA scan)
- **Perfect for flat structures** (tokens have no nesting)
- **Simple and fast** (compiled to efficient tables)

**Key limitation:** Cannot count arbitrarily (only modulo k for fixed k states).

**Why it fails for expressions:**
- Cannot recognize balanced parentheses (needs arbitrary counting)
- Cannot recognize nested structures

**Analogy:** Chess position validation that only checks if piece is on board.

---

## Practical Compiler Structure

```
Programming Language Syntax
        ↓
   Chomsky Type 2 (Context-Free)
     ↓
   Parsing Algorithms (LL, LR, recursive descent)
     ↓
   Parse Tree
     ↓
   Type 1 (Context-Sensitive) Constraints
     ↓
   Semantic Analysis (types, scope, meaning)
     ↓
   Abstract Syntax Tree
     ↓
   IR Generation
     ↓
   ... (optimization, codegen)
```

**Division of labor:**

| Phase | Formal Level | Job | Tool |
|-------|--------------|-----|------|
| **Lexing** | Type 3 (Regular) | Tokenize (flat) | Regex, DFA |
| **Parsing** | Type 2 (CFG) | Recursive structure | LL, LR, recursive descent |
| **Semantics** | Type 1 (Context-sensitive) | Meaning, constraints | Symbol tables, type checking |

---

## Why This Hierarchy Matters

### 1. **Computational Trade-off**

| Level | Parse Time | Expressiveness | Complexity |
|-------|-----------|-----------------|-----------|
| Type 3 (Regular) | Linear | Flat structures | Very simple |
| Type 2 (CFG) | Linear-polynomial | Nested structures | Moderate |
| Type 1 (Context-sensitive) | Polynomial-exponential | Context-dependent | Complex |
| Type 0 (Unrestricted) | Undecidable | Arbitrary | Impossible |

**Each level up:** More expressive but more expensive to parse.

### 2. **The Pigeonhole Principle**

**Type 3 limitation (finite automata):**

A DFA with $k$ states can distinguish $k$ different configurations. This means it can count only modulo $k$.

**Example:**
```
DFA with 2 states recognizes odd/even parity of 1's
- Can tell "odd" vs. "even"
- Cannot tell "5 ones" vs. "7 ones" (both look the same: odd)
```

For balanced parentheses, you need to count arbitrarily high → need unbounded memory → need Type 2 (stack) or higher.

**This is mathematical, not algorithmic** — no clever DFA can recognize balanced parentheses.

### 3. **Natural Hierarchy Alignment**

Compiler phases naturally align with hierarchy levels:

- **Lexer:** Works at Type 3 level (fast, simple)
- **Parser:** Works at Type 2 level (recursive, polynomial)
- **Semantic analyzer:** Works at Type 1 level (context-dependent constraints)

**Why?** Each phase solves exactly the problem that needs solving, using the minimal formalism.

---

## Historical Context

**Introduced:** Noam Chomsky, 1956

**Original purpose:** Understand natural language grammars

**Why it's perfect for compilers:** The hierarchy was designed to classify *expressive power*, which is exactly what compiler phases need to understand.

**Production compilers discovered:** Each phase uses exactly the right level of the hierarchy. Not by accident—because the hierarchy describes fundamental computational limits.

---

## The Undecidability at Each Level

### Can we automatically convert?

| Conversion | Decidable? | Example |
|-----------|-----------|---------|
| Type 3 → Type 2 | ✓ Yes | Add a stack to accept balanced parens |
| Type 2 → Type 3 | ✗ No | Cannot remove stack without losing power |
| Type 2 → Type 1 | ✓ Yes | Add context constraints |
| Type 1 → Type 2 | ✗ No | Cannot work in context-free world |
| Ambiguous CFG → Unambiguous CFG | ✗ No | No algorithm exists (Lecture 21) |

**Implication:** We must choose the right level from the start. Can't upgrade later (or can't downgrade without losing power).

---

## Practical Example: Why Parsing Needs Type 2

**Can't use Type 3 (regular) for expressions:**

```
Pattern: (balanced parens around operations)
Examples:  (), (()), ((())) ...

Type 3 Attempt:
- Need states for each nesting depth
- Each new depth requires new states
- Unbounded nesting needs infinite states
- **Impossible with finite automaton**

Type 2 Solution:
- Non-terminal S with production S → (S)
- Stack stores open parens
- Finite rules, unbounded nesting
- **Works perfectly**
```

**Why languages use Type 2:** The problem domain (nested structures) fundamentally requires Type 2 expressive power.

---

## Connection to Compiler Invariants

[[zettel/Z0004-invariants]]: Each phase maintains invariants about its input/output.

**Chomsky hierarchy validates these invariants:**

| Phase | Input Property | Output Property |
|-------|----------------|-----------------|
| **Lexer** | Characters (unstructured) | Tokens (Type 3 language) |
| **Parser** | Tokens (flat stream) | Parse tree (Type 2 structure) |
| **Semantics** | Parse tree (syntax only) | Annotated tree (meaning + context) |

The hierarchy guarantees each phase works with the right formalism.

---

## Misconceptions Cleared

### "Can't I write a CFG to recognize balanced parens in Type 3?"

**No.** This is mathematical, not a limitation of your grammar-writing skill. The pigeonhole principle forbids it. No infinite amount of cleverness can create a finite automaton that counts arbitrarily.

### "Can't I simulate a stack with multiple states?"

**No.** Simulating a stack requires unbounded memory. Multiple states are *fixed*—you still have only $k$ states total. A stack is fundamentally different.

### "Doesn't PEG (Parsing Expression Grammars) change this?"

**No.** PEG is Type 2 (context-free), just with different semantics (ordered choice instead of ambiguity). It doesn't escape the hierarchy.

### "Why can't we just use Type 0 for everything?"

**Because undecidability.** Parsing becomes unsolvable—the algorithm can't tell if a string is in the language. Useless for compilation.

---

## Key Insights

1. **The hierarchy is fundamental, not arbitrary** — It describes mathematical limits on what different formalisms can express.

2. **Each compiler phase uses the minimum necessary level** — Not because it's "optimal" in some abstract sense, but because that's what the problem requires.

3. **The pigeonhole principle is absolute** — Finite automata cannot count arbitrarily. This isn't a limitation of implementation; it's a mathematical fact.

4. **Upward conversions are easy; downward are impossible** — Can always use more powerful formalism; can never reduce power without losing expressiveness.

5. **Most programming languages are Type 2** — Because they have recursive nesting (expressions, statements, declarations). Type 1 is needed only for semantic constraints that syntax alone can't express.

---

## Related Zettel

- [[zettel/Z0005-compiler-phases]]: How phases align with hierarchy
- [[zettel/Z0001-state]]: Why state machines hit Type 3 limits
- [[zettel/Z0006-tokens]]: Why tokenization is naturally Type 3

---

## References

- Chomsky, N. (1956). "Three Models for the Description of Language"
- Hopcroft & Ullman. Introduction to Automata Theory, Languages, and Computation
- Stanford Lectures 18-21 on parsing
