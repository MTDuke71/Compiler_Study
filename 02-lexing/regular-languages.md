## Links
- Up: [[02-lexing/README]]
- Related: [[02-lexing/tokens-vs-characters]] [[02-lexing/hand-written-lexer]] [[02-lexing/failure-modes]]
- Down: [[02-lexing/hand-written-lexer]]

---

# Regular Languages: The Mathematical Foundation of Lexing

## The Core Question

**Why can lexers recognize some patterns but not others?**

The answer lies in **regular languages** - the class of languages recognizable by finite state machines.

## What Is a Regular Language?

A **regular language** is one that can be recognized by a **finite automaton** - a state machine with:
- Finite number of states
- Transitions on input symbols
- No memory beyond current state
- Accepting and non-accepting states

**Three equivalent definitions:**
1. Recognizable by a **Deterministic Finite Automaton (DFA)**
2. Recognizable by a **Nondeterministic Finite Automaton (NFA)**
3. Describable by a **regular expression**

These three formalisms have **exactly the same expressive power** - they define the same set of languages.

---

## The Regular Expression Connection

Every regular expression corresponds to a finite automaton, and vice versa.

**Basic regex operators:**

| Operator | Meaning | Example | Matches |
|----------|---------|---------|---------|
| `a` | Literal character | `a` | "a" |
| `ab` | Concatenation | `ab` | "ab" |
| `a\|b` | Alternation (or) | `a\|b` | "a" or "b" |
| `a*` | Kleene star (0+ times) | `a*` | "", "a", "aa", "aaa", ... |
| `a+` | One or more | `a+` | "a", "aa", "aaa", ... |
| `a?` | Zero or one | `a?` | "" or "a" |

**Note:** `a+` and `a?` are syntactic sugar:
- `a+` = `aa*`
- `a?` = `a|ε` (where ε is the empty string)

**Lexer patterns as regex:**
```
Identifier:  [a-zA-Z_][a-zA-Z0-9_]*
Number:      [0-9]+
HexNumber:   0x[0-9A-Fa-f]+
Operator:    >=|<=|==|!=|>|<|=
```

---

## What Regular Languages CAN Express

Regular languages are perfect for **token recognition**:

### ✅ Keywords
```regex
if|while|for|return|class|def|function
```

Finite set of alternatives → simple alternation.

### ✅ Identifiers
```regex
[a-zA-Z_][a-zA-Z0-9_]*
```

Start with letter/underscore, followed by any number of letters/digits/underscores.

### ✅ Numbers (Various Formats)
```regex
Integer:     [0-9]+
Float:       [0-9]+\.[0-9]+
Hex:         0x[0-9A-Fa-f]+
Octal:       0[0-7]+
Binary:      0b[01]+
Scientific:  [0-9]+(\.[0-9]+)?[eE][+-]?[0-9]+
```

### ✅ Strings (Simple, Non-Nested)
```regex
"[^"]*"              # Simple: any chars except "
"([^"\\]|\\.)*"      # With escapes: non-quote-or-backslash OR escape sequence
```

### ✅ Comments (Single-Line)
```regex
//.*$                # Everything after // to end of line
#.*$                 # Python/Ruby style
```

### ✅ Operators (Fixed Set)
```regex
>=|<=|==|!=|>>|<<|\+=|-=|\*=|/=|>|<|=|\+|-|\*|/
```

Note: Order matters for maximal munch (`>=` before `>`).

---

## What Regular Languages CANNOT Express

The fundamental limitation: **Regular languages cannot count arbitrarily high.**

Since finite automata have finite states, they can only count up to a fixed maximum (the number of states). Patterns requiring unlimited counting are **not regular**.

### ❌ Balanced Parentheses
```
Valid:   ((()))
Invalid: ((()
```

**Why not regular?** Need to count opening `(` and match with closing `)`. Arbitrary nesting depth requires infinite states.

**Formal proof:** Use the Pumping Lemma for regular languages (see below).

### ❌ Nested Block Comments
```c
/* outer /* inner */ still outer */
```

**Why not regular?** Same as balanced parentheses - need to track nesting depth.

**Real-world consequence:** C doesn't allow nested block comments. Languages that do (like Pascal, OCaml) must handle them specially in the lexer with a counter, going beyond pure regex.

### ❌ Matching HTML/XML Tags
```html
<div><span>text</span></div>
```

**Why not regular?** Opening tag `<div>` must match closing tag `</div>`. This requires remembering the tag name, which could be arbitrarily long.

**Famous Stack Overflow post:** "You can't parse [X]HTML with regex" - because HTML requires context-free grammar.

### ❌ Palindromes
```
Valid: abccba, racecar, aabbaa
```

**Why not regular?** Need to remember first half to compare with second half. No memory beyond current state.

### ❌ Equal Numbers of Two Symbols
```
Valid: ab, aabb, aaabbb
Pattern: aⁿbⁿ (n a's followed by n b's)
```

**Why not regular?** Need to count a's and ensure equal number of b's. Finite states can't count arbitrarily.

---

## The Pumping Lemma: Proof of Non-Regularity

**The Pumping Lemma** is a formal tool to prove a language is NOT regular.

**Statement:** If L is regular, then there exists a constant p (pumping length) such that any string s in L with |s| ≥ p can be split into three parts s = xyz where:
1. |y| > 0 (y is non-empty)
2. |xy| ≤ p
3. For all i ≥ 0, xyⁱz ∈ L (can "pump" y any number of times)

**Using it to prove non-regularity:**

**Example: L = {aⁿbⁿ | n ≥ 0} is not regular**

Proof by contradiction:
1. Assume L is regular with pumping length p
2. Consider s = aᵖbᵖ (clearly in L)
3. By Pumping Lemma, s = xyz where |xy| ≤ p and |y| > 0
4. Since |xy| ≤ p, both x and y consist only of a's
5. So y = aᵏ for some k > 0
6. Pumping Lemma says xyyz ∈ L
7. But xyyz = aᵖ⁺ᵏbᵖ (more a's than b's)
8. This is NOT in L (not equal counts)
9. Contradiction! Therefore L is not regular.

**Chess Analogy:** Like proving checkmate is forced. Assume opponent has a defense (language is regular), show that every defense (choice of xyz) leads to a position you can win from (contradiction).

---

## Finite Automata: DFA vs. NFA

### Deterministic Finite Automaton (DFA)

**Properties:**
- Exactly **one** transition per (state, input) pair
- No ε-transitions (empty string moves)
- Always in exactly one state
- Fast execution: O(n) guaranteed

**Formal definition:** DFA = (Q, Σ, δ, q₀, F)
- Q: Finite set of states
- Σ: Input alphabet
- δ: Q × Σ → Q (transition function)
- q₀: Initial state
- F ⊆ Q: Set of accepting states

**Example:** DFA for recognizing `>=` or `>`

```
States: {S0, S1, S2, ERROR}
Alphabet: {>, =, other}
Initial: S0
Accepting: {S1, S2}

Transition function δ:
  δ(S0, '>') = S1  (accepting: saw >, could be GT token)
  δ(S1, '=') = S2  (accepting: saw >=, GTE token)
  δ(S1, other) = ERROR
  δ(S2, any) = ERROR
  δ(S0, other) = ERROR
```

**Transition table:**

| State | > | = | other |
|-------|---|---|-------|
| S0 | S1 | ERROR | ERROR |
| S1 | ERROR | S2 | ERROR |
| S2 | ERROR | ERROR | ERROR |

**Execution on `>=`:**
```
Step | Input | State | Accepting?
-----|-------|-------|------------
  0  | start | S0    | No
  1  |  >    | S1    | Yes (GT)
  2  |  =    | S2    | Yes (GTE)
```

**Result:** Accept as GTE token.

**Execution on `>x`:**
```
Step | Input | State | Accepting?
-----|-------|-------|------------
  0  | start | S0    | No
  1  |  >    | S1    | Yes (GT)
  2  |  x    | ERROR | No
```

**Result:** Last accepting state was S1, return GT token, resume from 'x'.

### Nondeterministic Finite Automaton (NFA)

**Properties:**
- **Multiple** transitions possible for (state, input) pair
- **ε-transitions** allowed (move without consuming input)
- Can be in multiple states simultaneously
- Smaller (fewer states than equivalent DFA)
- Execution requires tracking all possible states

**Formal definition:** NFA = (Q, Σ, δ, q₀, F)
- Q: Finite set of states
- Σ: Input alphabet
- δ: Q × (Σ ∪ {ε}) → 2^Q (transition relation - returns SET of states)
- q₀: Initial state
- F ⊆ Q: Set of accepting states

**Example:** NFA for `a*b` (zero or more a's, then b)

```
States: {S0, S1, S2}
Initial: S0
Accepting: {S2}

Transitions:
  δ(S0, 'a') = {S1}
  δ(S0, ε) = {S1}      # Can skip directly to S1
  δ(S1, 'a') = {S1}    # Self-loop on a
  δ(S1, 'b') = {S2}    # Accept on b
```

**Visual representation:**
```
       ε-transition
      ┌───────────┐
      │           v
[S0] ──'a'──> [S1] ──'b'──> [S2] (accepting)
               ^│
               └─── 'a' (self-loop)
```

**Execution on `aab`:**
```
Step | Input | Active States (ε-closure)
-----|-------|---------------------------
  0  | start | {S0, S1}  (S0 + ε-transition to S1)
  1  |  a    | {S1}      (from S0 on 'a', or S1 self-loop)
  2  |  a    | {S1}      (S1 self-loop)
  3  |  b    | {S2}      (accepting!)
```

**Result:** Accept.

**Key difference:** NFA must track **all possible states** at once. Acceptance means **at least one** path reaches accepting state.

---

## DFA vs. NFA: Tradeoffs

| Aspect | DFA | NFA |
|--------|-----|-----|
| **States** | More (potentially exponentially more) | Fewer |
| **Transitions** | Exactly one per (state, input) | Multiple possible |
| **ε-transitions** | Not allowed | Allowed |
| **Execution speed** | O(n) - one state at a time | O(n × \|Q\|) - track multiple states |
| **Space during execution** | O(1) - single state | O(\|Q\|) - set of states |
| **Table size** | Larger | Smaller |
| **Construction from regex** | Harder | Easier (Thompson's construction) |
| **Implementation** | Simple loop | Need set tracking |

**The fundamental theorem:** Every NFA has an equivalent DFA (recognizes same language).

**Conversion cost:** NFA with n states → DFA with up to **2ⁿ states** (worst case).

**In practice:** Lexer patterns rarely hit worst case. Most convert to reasonable-sized DFAs.

---

## Thompson's Construction: Regex → NFA

**Thompson's Construction** converts any regular expression to an NFA.

**Algorithm:** Build NFA fragments for each regex operator, compose them.

### Base Cases

**1. Empty string ε:**
```
[S0] ──ε──> [S1]
(S1 accepting)
```

**2. Single character 'a':**
```
[S0] ──'a'──> [S1]
(S1 accepting)
```

### Inductive Cases

**3. Concatenation: r₁r₂**

Build NFA for r₁ (N₁) and r₂ (N₂), connect them:
```
[Start] ──N₁──> [End₁] ──ε──> [Start₂] ──N₂──> [End₂]
                (remove                      (accepting)
                 accepting
                 from End₁)
```

**4. Alternation: r₁|r₂**

Build NFAs for r₁ and r₂, add new start/end with ε-transitions:
```
              ┌──ε──> [N₁] ──ε──┐
[New Start] ──┤                 ├──> [New End] (accepting)
              └──ε──> [N₂] ──ε──┘
```

**5. Kleene Star: r***

Build NFA for r, add loop and bypass:
```
    ┌─────────ε─────────┐
    │                   v
[S] ──ε──> [Nr] ──ε──> [E] (accepting)
    │       ^│          ^
    │       └─ε─┘       │
    └────────ε──────────┘
(can loop back or skip entirely)
```

**Example: (a|b)*c**

Step 1: Build `a` and `b`:
```
[S1] ─'a'─> [E1]
[S2] ─'b'─> [E2]
```

Step 2: Combine with `|`:
```
       ┌─ε─> [S1] ─'a'─> [E1] ─ε─┐
[S0] ──┤                          ├──> [E0]
       └─ε─> [S2] ─'b'─> [E2] ─ε─┘
```

Step 3: Apply `*`:
```
     ┌────────────ε─────────────┐
     │                          v
[S] ─┴─ε─> (a|b machine) ─ε─> [E]
     └────────────ε─────────────┘
```

Step 4: Concatenate with `c`:
```
[Full NFA] = ((a|b)* machine) ─ε─> [Sc] ─'c'─> [Accepting]
```

**Result:** NFA with ~10-15 states recognizing `(a|b)*c`.

---

## Subset Construction: NFA → DFA

**Subset Construction** (also called **powerset construction**) converts NFA to equivalent DFA.

**Key insight:** Each DFA state represents a **set of NFA states** the NFA could be in.

**Algorithm:**

```
1. Start with ε-closure of NFA start state (all states reachable via ε)
2. For each DFA state D and input symbol a:
   a. Compute T = set of NFA states reachable from any state in D on input a
   b. Compute ε-closure(T) = all states reachable from T via ε-transitions
   c. If this set is new, add it as a new DFA state
   d. Add transition: δ_DFA(D, a) = ε-closure(T)
3. DFA accepting states = sets containing at least one NFA accepting state
```

**ε-closure:** Given set S of NFA states, ε-closure(S) = all states reachable from S via zero or more ε-transitions.

**Example: Convert NFA for `a*b` to DFA**

**NFA:**
```
[S0] ─ε─> [S1] ─'a'─> [S1] (self-loop)
           │
           └─'b'─> [S2] (accepting)
```

**Step 1:** ε-closure({S0}) = {S0, S1} = DFA state A (start)

**Step 2:** From A on 'a':
- From S0: can go to S1
- From S1: can go to S1
- Result: {S1}
- ε-closure({S1}) = {S1} = DFA state B
- Transition: δ(A, 'a') = B

**Step 3:** From A on 'b':
- From S0: no transition
- From S1: can go to S2
- Result: {S2}
- ε-closure({S2}) = {S2} = DFA state C (accepting)
- Transition: δ(A, 'b') = C

**Step 4:** From B on 'a':
- From S1: go to S1
- ε-closure({S1}) = {S1} = B (already exists)
- Transition: δ(B, 'a') = B

**Step 5:** From B on 'b':
- From S1: go to S2
- ε-closure({S2}) = {S2} = C
- Transition: δ(B, 'b') = C

**Step 6:** From C: no outgoing transitions (accepting state, done)

**Resulting DFA:**

| State | 'a' | 'b' | Accepting? |
|-------|-----|-----|------------|
| A {S0,S1} | B | C | No |
| B {S1} | B | C | No |
| C {S2} | ERROR | ERROR | **Yes** |

**Graphically:**
```
[A] ─'a'─> [B] ─'a'─> [B] (loop)
 │          │
 'b'        'b'
 │          │
 v          v
[C]        [C] (accepting)
```

**Complexity:** NFA with n states → DFA with up to **2ⁿ states** (every subset of NFA states is potential DFA state).

**In practice:** Most patterns generate far fewer than 2ⁿ states. The exponential blowup is rare for typical lexer patterns.

---

## DFA Minimization

After subset construction, DFA may have **redundant states** - states that behave identically.

**DFA Minimization** finds the equivalent DFA with fewest states.

**Hopcroft's Algorithm:**

```
1. Partition states into accepting and non-accepting
2. Repeat until no changes:
   a. For each partition P and symbol a:
      - Split P into subgroups where states go to same partition on 'a'
   b. If P was split, create new partitions
3. Merge states in same partition
```

**Example:**

**Original DFA (6 states):**
```
States: {A, B, C, D, E, F}
Accepting: {E, F}
```

Suppose B and C always transition to the same states on all inputs, and both are non-accepting.

**After minimization:** Merge B and C into single state BC.

**Result:** 5 states instead of 6.

**Benefits:**
- Smaller transition table
- Less memory
- Better cache performance
- Faster (fewer states to check)

**AoC Analogy:** Like optimizing a solution after it works. First make it correct (subset construction), then make it efficient (minimization).

---

## Why DFA Is O(n) Guaranteed

**The critical property:** No backtracking, no choices, no ambiguity.

**DFA execution (pseudocode):**
```c
int lex(char *input) {
    int state = START_STATE;
    int last_accept_state = -1;
    int last_accept_pos = -1;
    
    for (int i = 0; input[i] != '\0'; i++) {
        state = transition_table[state][input[i]];  // O(1) array lookup
        
        if (state == ERROR_STATE) {
            if (last_accept_state >= 0) {
                return make_token(last_accept_state, last_accept_pos);
            }
            return ERROR;
        }
        
        if (is_accepting[state]) {
            last_accept_state = state;
            last_accept_pos = i;
        }
    }
    
    return last_accept_state >= 0 ? make_token(...) : ERROR;
}
```

**Analysis:**
- Loop runs n times (n = input length)
- Each iteration: O(1) array lookup + O(1) checks
- Total: O(n)

**No backtracking:** Unlike backtracking regex engines (PCRE, Python re), DFA never revisits input.

**Compare to backtracking regex:**
- Pattern: `(a+)+b`
- Input: `aaaaaaaaaa` (no 'b')
- Backtracking engine tries: aa-aaa, aaa-aa, a-aaaa, etc.
- Complexity: **O(2ⁿ) worst case**

**DFA always wins on worst-case complexity.**

---

## Practical Implications for Lexers

### Why Lexers Use DFAs

1. **O(n) guaranteed** - No exponential blowup on pathological inputs
2. **Simple implementation** - Just array lookups in a loop
3. **Predictable performance** - No surprising slowdowns
4. **Cache-friendly** - Sequential array access

### Why Lexers Are Fast

```c
// The inner loop of a DFA lexer:
while (*input) {
    state = table[state][*input++];  // ~3-4 CPU cycles
    if (state < 0) break;
}
```

**This is essentially optimal** for sequential character processing.

### Limitations: What Lexers Can't Do

Because lexers use DFAs (recognize regular languages):

**Cannot handle:**
- Nested structures (requires stack → context-free grammar → parser)
- Context-sensitive tokens (requires symbol table → semantic analysis)
- Balanced delimiters (requires counting → not regular)

**Solution:** Pass to next compiler phase:
- Lexer: Recognize individual tokens
- Parser: Handle nesting and structure
- Semantic analyzer: Handle context

---

## Summary: The Regular Language Hierarchy

**Regular languages** are the simplest in the Chomsky Hierarchy:

```
Regular Languages (Type 3)
  ↓ (properly contained in)
Context-Free Languages (Type 2)
  ↓
Context-Sensitive Languages (Type 1)
  ↓
Recursively Enumerable Languages (Type 0)
```

**Lexing operates at Type 3 (regular)**:
- Recognized by finite automata
- Described by regular expressions
- O(n) recognition guaranteed

**Parsing operates at Type 2 (context-free)**:
- Recognized by pushdown automata (FSM + stack)
- Described by context-free grammars
- O(n) to O(n³) recognition depending on algorithm

**This separation is fundamental** - it's not just convention, it's rooted in formal language theory.

---

## Key Takeaways

1. **Regular languages = finite automata = regular expressions** - Three equivalent formalisms
2. **The limitation is counting** - Can't count arbitrarily with finite states
3. **DFAs are deterministic, NFAs allow choices** - Same power, different tradeoffs
4. **Thompson's construction: regex → NFA** - Compositional, easy to implement
5. **Subset construction: NFA → DFA** - Can be exponential, rarely is in practice
6. **DFA execution is O(n)** - No backtracking, just table lookups
7. **Minimization reduces states** - Optimization after correctness
8. **Lexers use DFAs for speed** - Predictable, fast, simple

---

## Cross-References

- [[02-lexing/tokens-vs-characters]] - Why lexing is separate from parsing
- [[02-lexing/hand-written-lexer]] - Implementing these concepts in code
- [[zettel/Z0006-tokens]] - Tokens as DFA output
- [[zettel/Z0005-compiler-phases]] - Lexing as Type 3 recognition
- [[00-index/invariants]] - O(n) lexing as invariant

---

**Next:** [[02-lexing/hand-written-lexer]] - Putting theory into practice with actual code.