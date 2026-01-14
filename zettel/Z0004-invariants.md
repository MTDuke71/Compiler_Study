## Links
- Up: [[zettel/README]]
- Related: [[zettel/Z0001-state]] [[zettel/Z0003-representation]] [[zettel/Z0005-compiler-phases]]
- Down: [[zettel/Z0005-compiler-phases]]

## Invariants

**Definition:** An invariant is a property that must remain true throughout a transformation or across all states in a process.

In compilers, invariants are **guarantees** that every phase must preserve. They enable safe transformations because you can rely on these properties without re-verifying them.

## Why Invariants Matter

1. **Safety**: Transformations that violate invariants produce incorrect programs
2. **Modularity**: Each phase can assume invariants from prior phases
3. **Debugging**: When something breaks, check which invariant was violated
4. **Optimization**: Many optimizations rely on specific invariants holding

## The Fundamental Invariant

**Meaning Preservation**: The program's observable behavior must not change.

- Input/output behavior must remain identical
- Program must produce the same results
- Side effects must occur in the same order
- Exceptions: performance, memory layout, timing (unless semantically relevant)

This is the invariant that **all other invariants serve**.

## Critical Compiler Invariants

### 1. **Type Safety** (after semantic analysis)
- Every expression has a consistent type
- Operations receive arguments of correct types
- Type conversions are explicit and valid
- **Violation example**: Optimizing `int x + int y` into a floating-point operation

### 2. **Well-Formedness**
- Each IR is structurally valid for its phase
- AST nodes have proper children
- CFG has valid edges (no dangling jumps)
- SSA form maintains single assignment
- **Violation example**: Creating a CFG node with no exit edges (except return/throw)

### 3. **Scope Validity**
- Variables are defined before use
- Names resolve to the correct declarations
- Shadowing rules are enforced
- **Violation example**: Reordering code that moves a use before its declaration

### 4. **Control Flow Reachability**
- All code is either reachable or explicitly dead
- Every path through function ends in return/throw
- No infinite loops without side effects (unless intended)
- **Violation example**: Creating a block that no jump can reach

### 5. **Data Flow Consistency**
- Every variable use has a corresponding definition
- Definitions dominate uses (in SSA)
- No use of uninitialized variables
- **Violation example**: Removing a definition but keeping its uses

## Phase-Specific Invariants

### Lexing Phase
- Every character is consumed
- Token sequence is deterministic
- Position information is accurate
- No overlapping tokens

### Parsing Phase
- Grammar rules are respected
- AST structure matches language syntax
- Operator precedence is correct
- Parentheses properly nest

### Semantic Analysis Phase
- All identifiers are declared
- Types are consistent
- Scopes are properly nested
- Return types match function signatures

### IR Translation Phase
- Control flow is explicit
- Every variable has storage allocated
- All jumps have valid targets
- Expression evaluation order is preserved

### Optimization Phase
- **Meaning preservation** (most critical)
- Dataflow facts remain valid
- Loop structure is maintained (or improved)
- Exception semantics preserved
- **Cannot optimize away**:
  - I/O operations
  - Infinite loops with side effects
  - Observable exceptions
  - Volatile/synchronized operations

### Code Generation Phase
- Calling conventions followed
- Register allocation is complete
- Stack frame layout is valid
- Alignment requirements met

## Verifying Invariants

### Static Verification
- Type checking (proves type safety)
- Dataflow analysis (proves variables defined before use)
- CFG validation (proves control flow is valid)
- SSA validation (proves single assignment)

### Dynamic Verification
- Assertions in compiler code
- IR verification passes (like LLVM's verifier)
- Test suites with known-good programs
- Differential testing (compare output with other compilers)

### Common Verification Techniques
1. **Assertion checks**: Insert runtime checks in compiler
2. **Verification passes**: Run after each phase to check invariants
3. **Property-based testing**: Generate random programs and verify
4. **Formal verification**: Prove invariants mathematically (research-level)

## When Invariants Are Violated

### Symptoms
- Crashes at runtime
- Wrong results
- Type errors in later phases
- Undefined behavior

### Debugging Strategy
1. Identify the failing phase
2. Check which invariant is violated
3. Find the transformation that broke it
4. Add verification to catch it earlier

### Example: Dead Code Elimination Gone Wrong
```
Original:
  if (condition) {
    x = 1;
  }
  print(x);  // x might be uninitialized!

Optimization removes dead assignment:
  if (condition) {
    // x = 1;  [removed as "dead code"]
  }
  print(x);  // BUG: x is now definitely uninitialized!
```
**Violated invariant**: "Variables must be defined before use"  
**Root cause**: Dead code analysis didn't account for conditional execution

## Recognizing Unsafe Transformations

An optimization violates an invariant if it:
- Changes program output
- Changes exception behavior  
- Changes termination (finite → infinite or vice versa)
- Changes side effect order (I/O, memory writes)
- Makes defined behavior undefined
- Violates language semantics (type rules, evaluation order, etc.)

### Safe vs Unsafe Examples

**Safe:**
- `x = 2 + 3` → `x = 5` (constant folding)
- `x = x * 1` → (remove multiplication) (algebraic simplification)
- Reorder independent statements

**Unsafe:**
- `x = read()` → (remove if x is unused) — removes I/O side effect!
- `while(true);` → (remove as dead code) — changes termination!
- `x = (y + z)` → `x = (z + y)` for floating point — changes results due to rounding!

## Invariants Enable Composability

Because each phase maintains invariants:
- You can **add optimizations** without breaking later phases
- You can **change one phase** without rewriting others
- You can **verify correctness** incrementally
- You can **reuse infrastructure** (e.g., SSA framework)

**Without invariants**, every change requires checking the entire pipeline.

## Key Takeaways

1. Invariants are **contracts** between compiler phases
2. **Meaning preservation** is the ultimate invariant
3. Each phase has **specific invariants** to maintain
4. **Verification** catches violations early
5. Understanding invariants helps you recognize **safe transformations**
6. **Violated invariants = bugs**, not warnings

## Questions for Deeper Understanding

- What invariants does SSA form maintain, and why is it powerful?
- How do aliasing and pointers complicate invariant maintenance?
- Why can't you eliminate infinite loops with I/O?
- What happens when optimizations are applied in the wrong order?
- How do modern compilers verify IR invariants (e.g., LLVM verifier)?

## Advanced Reading (Optional)

**For deeper understanding, explore these foundational papers (free via ACM Open Access):**

### On Compiler Correctness and Verification

**[Translation Validation for an Optimizing Compiler](https://dl.acm.org/doi/10.1145/349299.349314)** (PLDI 2000)  
*Pnueli, Siegel, Singerman*
- How to prove optimizations preserve semantics
- Translation validation approach (verify output, not compiler)
- **Read after**: Understanding optimization basics (Week 10+)

**[Formal verification of a realistic compiler](https://dl.acm.org/doi/10.1145/1538788.1538814)** (CACM 2009)  
*Xavier Leroy* (CompCert compiler)
- Mechanically proved compiler correctness using Coq proof assistant
- Shows which invariants must hold at each phase and proves they're maintained
- **Read for**: Gold standard of verified compilation
- **Also see**: [CompCert website](http://compcert.inria.fr/) for full documentation

### On Type Safety and Soundness

**[Type Safety for Java](https://dl.acm.org/doi/10.1145/263699.263751)** (OOPSLA 1998)  
*Drossopoulou, Eisenbach*
- Formalizing type safety invariants
- Proof techniques for type soundness
- **Read after**: Implementing type checking (Week 7+)

### On SSA and Dataflow Invariants

**[Efficiently Computing Static Single Assignment Form](https://dl.acm.org/doi/10.1145/115372.115320)** (POPL 1991)  
*Cytron et al.* — **The foundational SSA paper**
- Defines SSA invariants rigorously
- Dominance properties and phi placement
- **Read after**: Understanding SSA intuition (Week 9+)
- **Also available**: [SSA Book (free PDF)](https://pfalcon.github.io/ssabook/latest/book-v1.pdf) — comprehensive modern treatment

### On Optimization Correctness

**[Automatic Discovery of Optimization Opportunities](https://dl.acm.org/doi/10.1145/1273442.1250754)** (PLDI 2006)  
*Tate et al.*
- How to verify optimizations preserve semantics
- Program equivalence checking
- **Read for**: Understanding why optimizations are hard to get right

**[Alive: Automatic LLVM InstCombine Verifier](https://dl.acm.org/doi/10.1145/2737924.2737965)** (PLDI 2015)  
*Lopes et al.*
- Tool for verifying LLVM optimizations
- Shows real bugs found by checking invariants
- **Read after**: Implementing your own optimizations (Week 10+)

### Free Alternative Resources

**Books (no ACM required):**
- [LLVM Language Reference](https://llvm.org/docs/LangRef.html) — Well-formedness rules
- [GCC Internals Manual](https://gcc.gnu.org/onlinedocs/gccint/) — RTL invariants

**Source Code (learn from production):**
- [LLVM Verifier](https://github.com/llvm/llvm-project/blob/main/llvm/lib/IR/Verifier.cpp) — Real invariant checking
- [GCC Tree Checking](https://github.com/gcc-mirror/gcc/blob/master/gcc/tree.cc) — AST invariants

**When to Read These:**
- Week 2 (now): Skim abstracts, understand that verification is important
- Week 9+: Read SSA paper after implementing basic SSA
- Week 10+: Read optimization papers after implementing optimizations
- Week 15+: Deep dive on formal verification and CompCert
