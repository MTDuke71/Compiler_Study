## Links
- Up: [[00-index/README]]
- Related: [[00-index/compiler-map]] [[00-index/curriculum-roadmap]]
- Down: 

# Compiler Invariants — Reference Index

This document serves as a comprehensive reference for invariants that must hold throughout the compilation process. Use this as a checklist when implementing or debugging compiler phases.

## What Are Invariants?

**Invariants** are properties that must remain true throughout transformations. They are:
- **Contracts** between compiler phases
- **Assumptions** that downstream code relies on
- **Guarantees** that enable safe optimizations
- **Debugging checkpoints** when things go wrong

## The Master Invariant

### Meaning Preservation (Semantic Equivalence)

**Statement**: The compiled program must have the same observable behavior as the source program.

**Observable behavior includes**:
- Input/output operations
- Return values
- Side effects (memory writes, exceptions)
- Termination vs non-termination

**Not included** (implementation details):
- Execution time (performance)
- Memory layout
- Instruction order (if semantics preserved)
- Register allocation

**Test**: Run the same inputs through source (interpreted) and compiled versions — outputs must match.

---

## Universal Invariants (All Phases)

These must hold after **every** compilation phase:

### 1. Well-Formedness
**Property**: The IR is structurally valid for its representation.

**Per-phase requirements**:
- **Tokens**: Each token has type, value, position
- **AST**: Nodes have correct number/type of children
- **CFG**: Every block has valid successors
- **SSA**: Single assignment, phi nodes at joins

**Violation symptoms**: Crashes, assertion failures, malformed output

---

### 2. Completeness
**Property**: All program elements are represented; nothing is lost.

**Requirements**:
- All source constructs are translated
- No dangling references
- All symbols are defined or imported

**Violation symptoms**: Undefined symbols, linker errors

---

### 3. Determinism
**Property**: The same input always produces the same output.

**Requirements**:
- No random choices without explicit seeding
- No dependence on pointer addresses or hash order
- Reproducible builds

**Violation symptoms**: Flaky tests, unreproducible bugs

---

## Phase-Specific Invariants

### Lexical Analysis (Lexing)

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Coverage** | Every input character consumed | Sum token lengths = input length |
| **No overlap** | Tokens don't overlap | Check token positions |
| **Boundaries** | Token boundaries unambiguous | Lexer is deterministic (DFA) |
| **Position tracking** | Line/column accurate | Check against source map |

**Common violations**:
- Off-by-one in position tracking
- Forgetting to handle EOF
- Incorrectly handling whitespace/comments

---

### Syntactic Analysis (Parsing)

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Grammar conformance** | AST matches language grammar | Grammar validator |
| **Precedence** | Operator precedence correct | Test expressions like `2+3*4` |
| **Associativity** | Operators associate correctly | Test `2-3-4` vs `2-(3-4)` |
| **Complete trees** | No NULL children (unless optional) | Tree traversal checks |

**Common violations**:
- Wrong precedence levels
- Left vs right associativity errors
- Missing syntax error detection

---

### Semantic Analysis

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Name resolution** | All identifiers declared | Symbol table lookup |
| **Type consistency** | Operations have compatible types | Type checker |
| **Scope validity** | Scopes properly nested | Scope stack checks |
| **Initialization** | Variables defined before use | Dataflow analysis |
| **Return coverage** | All paths return (for non-void) | Control flow analysis |

**Common violations**:
- Forgetting to check for undefined variables
- Incorrect scope nesting
- Missing return statements

---

### IR Translation

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Explicit control flow** | All jumps/branches explicit | CFG is complete |
| **Explicit data flow** | All data dependencies visible | Use-def chains valid |
| **Storage allocated** | Variables have locations | Symbol table complete |
| **Jump targets valid** | All labels/blocks exist | CFG validation |
| **Expression order** | Side effects in correct order | Compare with source semantics |

**Common violations**:
- Short-circuit evaluation bugs
- Wrong evaluation order for side effects
- Missing temporary variables

---

### SSA Form (if used)

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Single assignment** | Each variable assigned exactly once | Check definition count |
| **Dominance** | Definitions dominate uses | Dominator tree check |
| **Phi placement** | Phi nodes at join points | Check CFG structure |
| **Minimal phi** | Only necessary phi nodes | Dominance frontier algorithm |

**Common violations**:
- Missing phi nodes
- Phi nodes in wrong blocks
- Breaking SSA during optimization

---

### Optimization

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Semantic equivalence** | Behavior unchanged | Differential testing |
| **Dataflow validity** | Use-def chains remain valid | Dataflow analysis |
| **Type preservation** | Types unchanged | Type checker |
| **No new undefined behavior** | Don't introduce UB | Sanitizers, verification |

**Cannot optimize away**:
- I/O operations (observable side effects)
- Infinite loops with side effects
- Volatile/atomic operations
- Exceptions (must preserve throw/catch)

**Common violations**:
- Reordering dependent operations
- Eliminating "dead" I/O code
- Changing floating-point rounding
- Breaking exception semantics

---

### Code Generation

| Invariant | Description | How to Verify |
|-----------|-------------|---------------|
| **Calling convention** | ABI followed correctly | Stack/register inspection |
| **Register allocation** | All values in registers/memory | Liveness analysis |
| **Stack layout** | Frame pointer, locals, temps | Frame analysis |
| **Alignment** | Data aligned per architecture | Alignment checks |
| **Instruction validity** | All instructions encodable | Assembler validation |

**Common violations**:
- Wrong calling convention
- Stack overflow (insufficient space)
- Misaligned memory access
- Invalid instruction encoding

---

## Invariant Verification Strategies

### 1. Assertion-Based Verification
Insert checks in compiler code:
```
void addEdge(Block* from, Block* to) {
    assert(from != nullptr);
    assert(to != nullptr);
    assert(from->cfg == to->cfg);  // same CFG
    from->successors.push_back(to);
}
```

### 2. Phase Verification Passes
Run after each phase:
```
Pipeline:
  Lexing → [Verify tokens] →
  Parsing → [Verify AST] →
  Semantics → [Verify types/scopes] →
  IR → [Verify CFG/SSA] →
  Optimization → [Verify equivalence] →
  Codegen → [Verify instructions]
```

### 3. Property-Based Testing
Generate random valid programs and verify invariants hold.

### 4. Differential Testing
Compare output with other compilers or interpreters.

### 5. Formal Verification
Mathematically prove invariants (research-level, e.g., CompCert).

---

## Recognizing Invariant Violations

### When Reviewing a Transformation, Ask:

1. **Does it preserve types?**
   - Check: Do operand types change?

2. **Does it preserve control flow?**
   - Check: Can execution paths change?

3. **Does it preserve data flow?**
   - Check: Do values reach different places?

4. **Does it preserve side effects?**
   - Check: Are I/O operations reordered/removed?

5. **Does it preserve termination?**
   - Check: Can non-terminating code become terminating (or vice versa)?

6. **Does it preserve exceptions?**
   - Check: Can new exceptions be thrown, or caught exceptions be missed?

---

## Safe Transformation Patterns

### ✅ Safe: Constant Folding
```
Before: x = 2 + 3
After:  x = 5
```
**Why**: No observable change; pure computation.

### ✅ Safe: Dead Code Elimination (Pure Code)
```
Before: x = 5; /* x is never used */
After:  /* removed */
```
**Why**: No side effects, no observable impact.

### ✅ Safe: Algebraic Simplification
```
Before: x = y * 1
After:  x = y
```
**Why**: Mathematically equivalent (for integers).

### ✅ Safe: Common Subexpression Elimination
```
Before: a = x + y; b = x + y;
After:  a = x + y; b = a;
```
**Why**: No side effects in `x + y`, evaluation order preserved.

---

## Unsafe Transformation Patterns

### ❌ Unsafe: Removing I/O
```
Before: x = read(); /* x never used */
After:  /* removed */
```
**Why**: Removes observable side effect!

### ❌ Unsafe: Removing Infinite Loops with Side Effects
```
Before: while(true) { print("x"); }
After:  /* removed as "dead code" */
```
**Why**: Changes termination and removes side effects!

### ❌ Unsafe: Reordering Floating-Point Operations
```
Before: x = (a + b) + c
After:  x = a + (b + c)
```
**Why**: Floating-point addition is not associative due to rounding!

### ❌ Unsafe: Hoisting Exceptions
```
Before: if (cond) { x = arr[i]; }
After:  x = arr[i]; if (cond) { use(x); }
```
**Why**: Can throw exception even when `cond` is false!

---

## Checklist: Implementing a New Optimization

Before adding an optimization, verify:

- [ ] Does it preserve program semantics?
- [ ] Does it maintain type safety?
- [ ] Does it preserve control flow validity?
- [ ] Does it update dataflow information correctly?
- [ ] Does it handle side effects correctly?
- [ ] Does it preserve exception semantics?
- [ ] Does it maintain SSA form (if applicable)?
- [ ] Have you added verification checks?
- [ ] Have you added tests for edge cases?
- [ ] Have you tested with sanitizers/validators?

---

## Common Debugging Scenarios

### Symptom: Wrong Output
**Check**: Meaning preservation invariant  
**Likely cause**: Incorrect optimization or transformation

### Symptom: Crash at Runtime
**Check**: Type safety, memory safety invariants  
**Likely cause**: Uninitialized variable, bad pointer

### Symptom: Linker Errors
**Check**: Completeness invariant  
**Likely cause**: Undefined symbols, missing definitions

### Symptom: Nondeterministic Behavior
**Check**: Determinism invariant  
**Likely cause**: Uninitialized memory, hash table iteration order

### Symptom: Type Errors in Later Phases
**Check**: Type safety invariant  
**Likely cause**: Earlier phase didn't enforce types correctly

---

## Advanced Topics

### Aliasing and Invariants
- Pointers complicate invariants (aliasing = same memory, different names)
- Must assume aliased memory can change between accesses
- Alias analysis tries to prove non-aliasing to enable optimizations

### Concurrency and Invariants
- Memory model defines what transformations are valid
- Volatile/atomic operations have ordering constraints
- Cannot reorder operations across synchronization points

### Undefined Behavior
- Languages like C have undefined behavior (UB)
- Compilers can assume UB never happens
- Enables aggressive optimizations but can violate expectations

---

## Summary

**3-5 Critical Invariants** (Success Criteria):

1. **Meaning Preservation**: Observable behavior unchanged
2. **Type Safety**: Types consistent throughout
3. **Well-Formedness**: Each IR is structurally valid
4. **Dataflow Consistency**: Variables defined before use
5. **No Side Effect Reordering**: I/O and exceptions preserved

**How to Verify**:
- Add assertions and verification passes
- Use differential testing
- Run sanitizers and validators

**Recognizing Violations**:
- Optimization changes output → meaning preservation violated
- New type errors → type safety violated
- Compiler crashes → well-formedness violated

**Key Insight**: Invariants are the **contracts** that enable modular, composable compiler construction. Without them, every change risks breaking the entire pipeline.

---

## Related Topics
- [[zettel/Z0004-invariants]] — Detailed zettel note on invariants
- [[zettel/Z0001-state]] — Compilation as state transformation
- [[00-index/compiler-map]] — Overview of compiler architecture
- [[06-optimization/README]] — How optimizations preserve invariants

---

## Advanced Reading (Optional)

**Now free via ACM Open Access! These papers provide research-level understanding of compiler invariants.**

### Essential Papers on Invariants

**1. [Translation Validation for an Optimizing Compiler](https://dl.acm.org/doi/10.1145/349299.349314)** — PLDI 2000  
*Pnueli, Siegel, Singerman*
- **What it covers**: How to verify optimizations preserve semantics without proving the compiler correct
- **Key insight**: Check each compilation's output, not the compiler implementation
- **Why it matters**: Practical approach to ensuring invariants hold
- **Read when**: After Week 10 (optimization implementation)

**2. [Formal verification of a realistic compiler](https://dl.acm.org/doi/10.1145/1538788.1538814)** — CACM 2009  
*Xavier Leroy* (CompCert)
- **What it covers**: Mechanically verified C compiler using Coq proof assistant
- **Key insight**: Proves meaning preservation invariant for entire compilation pipeline
- **Why it matters**: Shows it's actually possible to guarantee compiler correctness
- **Read when**: Week 15+ (advanced topics), or when you want inspiration
- **Also see**: [CompCert website](http://compcert.inria.fr/) for full documentation and source code

**3. [Efficiently Computing Static Single Assignment Form](https://dl.acm.org/doi/10.1145/115372.115320)** — POPL 1991  
*Cytron, Ferrante, Rosen, Wegman, Zadeck*
- **What it covers**: **The** foundational SSA paper
- **Key insight**: SSA's invariants (single assignment, dominance) enable powerful optimizations
- **Why it matters**: Understanding SSA is crucial for modern compilers
- **Read when**: After Week 9 (SSA implementation)
- **Companion resource**: [SSA Book (free PDF)](https://pfalcon.github.io/ssabook/latest/book-v1.pdf)

### Type Safety Invariants

**4. [Proof-Carrying Code](https://dl.acm.org/doi/10.1145/263699.263712)** — POPL 1997  
*Necula, Lee*
- **What it covers**: Embedding invariant proofs in compiled code
- **Key insight**: Consumer verifies invariants, not producer
- **Why it matters**: Security and mobile code safety
- **Read when**: Week 7+ (after type checking), or interested in security

**5. [Types and Programming Languages](https://dl.acm.org/doi/book/10.5555/509043)** — Book (available through many libraries)  
*Pierce*
- **What it covers**: Formal treatment of type safety
- **Key sections**: Progress and preservation theorems (type safety invariants)
- **Why it matters**: Foundation for understanding type system guarantees
- **Alternative**: Search ACM for "type soundness" papers

### Optimization and Correctness

**6. [Alive: Automatic LLVM InstCombine Verifier](https://dl.acm.org/doi/10.1145/2737924.2737965)** — PLDI 2015  
*Lopes, Menendez, Nagarakatte, Regehr*
- **What it covers**: Automated verification of LLVM optimizations
- **Key insight**: Many "obviously correct" optimizations are actually buggy
- **Why it matters**: Shows real-world invariant violations in production compiler
- **Read when**: After Week 10 (optimization), to see how hard it is
- **Try online**: [Alive2 tool](https://alive2.llvm.org/ce/)

**7. [Finding and Understanding Bugs in C Compilers](https://dl.acm.org/doi/10.1145/1993498.1993532)** — PLDI 2011  
*Yang et al.* (Csmith paper)
- **What it covers**: Random testing found hundreds of bugs in GCC/LLVM
- **Key insight**: Most bugs are invariant violations in optimizations
- **Why it matters**: Even mature compilers get invariants wrong
- **Read when**: Week 10+ or when implementing optimizations

### Dataflow Analysis and Verification

**8. [A Unified Approach to Global Program Optimization](https://dl.acm.org/doi/10.1145/512927.512945)** — POPL 1973  
*Kildall*
- **What it covers**: Framework for dataflow analysis
- **Key insight**: Lattice theory ensures invariants converge
- **Why it matters**: Foundation for verifying dataflow invariants
- **Read when**: Week 9+ (dataflow), more theoretical but foundational

### Search Strategies

**To find more papers on ACM:**
- Search: "compiler correctness", "translation validation", "program verification"
- Browse: PLDI, POPL, OOPSLA, CGO conference proceedings
- Filter by: "Most cited" or "Highly influential"
- Look for: Papers citing the above foundational works

### Free Resources (No ACM needed)

**Documentation:**
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html#well-formedness) — IR well-formedness rules
- [LLVM Verifier documentation](https://llvm.org/docs/ProgrammersManual.html#the-verifier-module) — What gets checked
- [GCC Internals Manual](https://gcc.gnu.org/onlinedocs/gccint/RTL.html) — RTL invariants

**Source Code (Best Learning Resource):**
- [LLVM IR Verifier](https://github.com/llvm/llvm-project/blob/main/llvm/lib/IR/Verifier.cpp) — 5000+ lines of invariant checks
- [GCC Tree Verification](https://github.com/gcc-mirror/gcc/blob/master/gcc/tree.cc) — AST/GIMPLE invariants
- Study these to see how real compilers maintain invariants!

**Books (Free/Open Access):**
- [SSA Book](https://pfalcon.github.io/ssabook/latest/book-v1.pdf) — Complete SSA treatment
- [Crafting Interpreters](https://craftinginterpreters.com/) — Practical invariant maintenance

### Reading Strategy

**Progressive Approach:**

1. **Week 2 (Now)**: Skim abstracts, understand landscape
2. **During Implementation (Weeks 3-12)**: Read relevant papers *after* hitting the problems yourself
3. **Week 15-16**: Deep dive on formal methods and verification
4. **Ongoing**: Use papers to understand "why" after you understand "what"

**Don't read papers before implementation!** You won't understand the problems they solve. Implement first, struggle, *then* read how experts solved it.

**Best use of papers**: When you've implemented something and wonder "is there a better way?" or "how do I prove this is correct?"

---

## Your Learning Path

✅ **You've completed**: Understanding what invariants are and why they matter  
📖 **Optional next**: Skim SSA paper abstract to preview Week 9  
🔨 **Focus now**: Move to Week 3 (lexing implementation)  
🎓 **Return to papers**: After implementing each phase
