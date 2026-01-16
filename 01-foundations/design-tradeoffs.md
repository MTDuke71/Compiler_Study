# Design Tradeoffs in Compilers

## Links
- Up: [[01-foundations/README]]
- Related: [[01-foundations/language-as-state]] [[05-ir/why-ast-is-not-enough]]
- See also: [[zettel/Z0003-representation]]

---

## The Central Truth

**There is no perfect compiler design.**

Every choice is a tradeoff. Every representation optimizes for something and pays a cost elsewhere. Understanding these tradeoffs is what separates copying patterns from making informed engineering decisions.

### A Familiar Analogy: Chess Engines

If you've worked with chess engines, you already understand compiler tradeoffs intuitively:

**Chess Engine Requirements:**
- **Must follow all the rules** (legal moves only)
- **Want it to be fast** (evaluate positions quickly)
- **Want it to be smart** (complex evaluation for better play)
- **But:** More complex evaluation = slower per position = less depth searched

**The Tradeoff:**
You can't use every evaluation technique known to man AND search to depth 20 in reasonable time. You must choose:
- Simple evaluation + deep search?
- Complex evaluation + shallow search?
- Somewhere in between?

**Compiler Parallel:**
- **Must follow all the rules** (preserve program semantics/invariants)
- **Want fast compilation** (quick developer feedback)
- **Want fast execution** (optimized output code)
- **But:** More optimization = slower compilation = longer feedback loop

**The Same Tradeoff:**
You can't apply every optimization known to man AND compile instantly. You must choose:
- Minimal optimization + fast builds? (debug mode: `-O0`)
- Aggressive optimization + slow builds? (release mode: `-O3`)
- Somewhere in between? (default: `-O1` or `-O2`)

**Just like chess engines have different "personalities" (Stockfish vs. LC0), compilers have different philosophies:**
- **LLVM:** Deep analysis, excellent optimization (like Stockfish: deep search, refined evaluation)
- **TinyCC:** Minimal optimization, instant compilation (like a simple engine: fast, shallow)
- **V8 JIT:** Adaptive tiers (like an opening book + search: fast at first, optimize hot code later)

All correct. All successful. All making different tradeoffs for different goals.

---

## The Fundamental Tradeoffs

### 1. Compile Time vs. Runtime Performance

**The Tension:**
- More analysis = better optimization = faster executable
- More analysis = slower compilation = longer developer feedback loop

**Examples:**

| Approach | Compile Time | Runtime | Use Case |
|----------|--------------|---------|----------|
| No optimization | Very fast | Slow | Development builds, debugging |
| `-O1` basic opts | Fast | Good | Default production |
| `-O2` aggressive | Slow | Better | Release builds |
| `-O3` + inlining | Very slow | Best | Performance-critical code |

**Real Impact:**
```
// Constant folding (cheap at compile time, helpful at runtime)
x = 2 + 3;  →  x = 5;  // Trivial cost, small benefit

// Whole-program analysis (expensive, high payoff)
// Requires analyzing entire codebase
// Can inline across files, devirtualize calls, remove dead code
// Cost: Minutes to hours
// Benefit: 10-30% faster executable
```

**The Decision:**
- Debug builds: Optimize for compile time
- Release builds: Optimize for runtime
- JIT compilers: Balance both (can't take forever to start)

---

### 2. Memory Usage vs. Speed

**The Tension:**
- Cache more data = fewer recomputations = faster
- Cache more data = more memory = worse cache locality

**Examples:**

**Hash Tables vs. Linear Search:**
```
// Symbol table implementation choice

// Option 1: Hash table
- Lookup: O(1) expected
- Memory: ~2x entries (for load factor)
- Cache: Poor (scattered memory)

// Option 2: Sorted array
- Lookup: O(log n) with binary search
- Memory: Exact size needed
- Cache: Excellent (sequential memory)

Decision: Hash table for large codebases (100+ symbols)
          Array for small scopes (function-local variables)
```

**Memoization:**
```
// Type checking expensive expressions

// Without memoization
checkType(expr):
    if expr is BinaryOp:
        leftType = checkType(expr.left)   // Might recompute
        rightType = checkType(expr.right) // Might recompute
        return combine(leftType, rightType)

// With memoization (cache results)
typeCache = {}
checkType(expr):
    if expr in typeCache:
        return typeCache[expr]
    
    // ... compute type ...
    typeCache[expr] = result
    return result

Tradeoff: Memory for speed
Cost: One entry per unique expression
Benefit: Shared subexpressions checked once
```

---

### 3. Simplicity vs. Generality

**The Tension:**
- Simple implementations are easier to understand and maintain
- General implementations handle more cases but add complexity

**Examples:**

**Register Allocation:**

**Simple (Linear Scan):**
```
- Single pass through code
- Assign registers in order
- Spill when out of registers
- Implementation: ~200 lines
- Quality: 80% as good as optimal
- Speed: Very fast
```

**General (Graph Coloring):**
```
- Build interference graph
- Use heuristics to color graph
- Handle spilling, coalescing, rematerialization
- Implementation: ~2000 lines
- Quality: Near optimal
- Speed: Can be slow for large functions
```

**The Decision:**
- JIT compilers: Use linear scan (compile time matters)
- Optimizing compilers: Use graph coloring (quality matters)
- Your learning compiler: Start simple, add complexity only when needed

---

**Parsing Approaches:**

**Hand-Written Recursive Descent:**
```
Pros:
- Easy to understand and debug
- Full control over error messages
- Can handle context-sensitive cases
- ~500 lines for basic language

Cons:
- Tedious to write for large grammars
- Hard to maintain if grammar changes
- Can't handle all grammar classes
```

**Parser Generator (Bison/ANTLR):**
```
Pros:
- Grammar is declarative and clear
- Handles more grammar classes
- Changes are localized

Cons:
- Generated code is hard to debug
- Error messages are generic
- Adds tool dependency
- Learning curve for tool syntax
```

**The Decision:**
- Educational: Hand-written (you learn more)
- Production (stable grammar): Hand-written (better errors)
- Production (evolving grammar): Generator (easier to change)

---

### 4. Early Detection vs. Flexibility

**The Tension:**
- Catching errors early helps developers
- Strict checking limits what programs can express

**Examples:**

**Type Checking Strictness:**

```
// Strict (Rust, Haskell)
let x = 5;
let y = "hello";
let z = x + y;  // ERROR: Type mismatch

Pros:
- Catches bugs at compile time
- Optimizer has more information
- No runtime type checks needed

Cons:
- More verbose code
- Harder to prototype quickly
- Learning curve
```

```
// Permissive (JavaScript, Python)
let x = 5;
let y = "hello";
let z = x + y;  // OK: "5hello"

Pros:
- Faster to write
- Flexible conversions
- Easy to learn

Cons:
- Bugs slip to runtime
- Harder to optimize
- Unexpected behaviors
```

**The Decision:** Language philosophy, not a clear winner.

---

**Initialization Checks:**

```
// Strict: Must initialize before use
int x;
print(x);  // ERROR: x might be uninitialized

// Permissive: Allow uninitialized reads
int x;
print(x);  // OK: Prints garbage or zero
```

**Tradeoff:**
- Strict: More work for compiler, safer programs
- Permissive: Less work for compiler, more runtime bugs

---

### 5. Representation: Trees vs. Linear vs. Graphs

**The Tension:** Different representations excel at different tasks.

**AST (Tree):**
```
Good for:
- Preserving source structure
- Pattern matching
- Recursive algorithms
- Local transformations

Bad for:
- Analyzing control flow
- Identifying common subexpressions
- Representing jumps/loops
- Global optimization

Example:
if (x > 0) {
    y = x + 1;
} else {
    y = x - 1;
}

Tree clearly shows nesting, but hides the fact that both branches assign to y.
```

**Three-Address Code (Linear):**
```
Good for:
- Instruction selection
- Simple to generate
- Easy to read/debug
- Register allocation input

Bad for:
- Control flow representation
- Representing expression structure
- Finding basic blocks requires analysis

Example:
    t1 = x > 0
    if_false t1 goto L2
    t2 = x + 1
    y = t2
    goto L3
L2: t3 = x - 1
    y = t3
L3: ...

Linear but control flow is implicit in labels.
```

**CFG (Graph):**
```
Good for:
- Control flow analysis
- Data flow analysis
- Loop detection
- Global optimization

Bad for:
- Initial code generation
- Memory overhead
- Complexity of manipulation

Example:
[Entry]
   |
[if x > 0]
   /    \
[y=x+1] [y=x-1]
   \    /
  [Exit]

Control flow is explicit, but expression structure is flattened.
```

**SSA Form (Graph with constraints):**
```
Good for:
- Data flow analysis
- Dead code detection
- Constant propagation
- Many optimizations

Bad for:
- Initial construction (needs dominance)
- Destruction for codegen (phi functions aren't real)
- Memory overhead (more variables)

Example:
    if (x₁ > 0)
        y₁ = x₁ + 1
    else
        y₂ = x₁ - 1
    y₃ = φ(y₁, y₂)  // phi function selects based on path

Makes data flow explicit: y₃ depends on which path was taken.
```

**The Decision:**
- Use multiple representations!
- AST → TAC → CFG → SSA → Assembly
- Each phase uses the best representation for its task

---

## Common Design Constraints

### 1. Language Semantics (Non-Negotiable)

Some tradeoffs aren't actually tradeoffs—they're requirements:

```
// C language: Evaluation order is mostly undefined
x = f() + g();  // Can call f or g first

Constraint: Compiler MUST preserve observable behavior
- Side effects must happen
- Order can change only if semantically equivalent

This allows optimization but constrains reordering.
```

### 2. Target Architecture

```
// x86-64: Two-address instructions
add rax, rbx  // rax = rax + rbx (destroys rax)

Constraint: IR with three-address form must be lowered
    t1 = t2 + t3
    ↓
    mov rax, t2
    add rax, t3
    mov t1, rax

Different architectures force different tradeoffs in codegen.
```

### 3. Development Time

```
Perfect optimization suite: 5 years
Good enough optimizer: 6 months

Constraint: Time to market matters
Decision: Implement high-impact optimizations first
- Constant folding: Easy, high impact
- Alias analysis: Hard, medium impact

80/20 rule applies to compilers too.
```

### 4. Debuggability

```
// Heavy optimization breaks debugging

Original:
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }

Optimized (vectorized):
    for (int i = 0; i < n; i += 4) {
        sum += arr[i] + arr[i+1] + arr[i+2] + arr[i+3];
    }

Problem: Can't step through original loop body
Constraint: Debug builds must preserve source structure
```

---

## Case Study: The SSA Tradeoff

**SSA Form: A Tradeoff Analysis**

**Benefits:**
- ✓ Simpler data flow (def-use is explicit)
- ✓ Constant propagation is trivial
- ✓ Dead code is obvious (unused defs)
- ✓ Many optimizations become easier

**Costs:**
- ✗ Construction requires dominance analysis
- ✗ More variables (memory overhead)
- ✗ Phi functions must be eliminated for codegen
- ✗ More complex to understand initially

**When is it worth it?**

```
Small scripts (< 100 lines):
- Cost: Dominance analysis overhead
- Benefit: Minimal (few optimizations matter)
- Decision: Skip SSA, use simpler IR

Medium programs (1000-10000 lines):
- Cost: Worth it if compiling once
- Benefit: Meaningful speedups from optimization
- Decision: Use SSA for release builds

Large programs (100000+ lines):
- Cost: Amortized over many optimizations
- Benefit: Essential for good performance
- Decision: Always use SSA in optimizer
```

---

## Misconceptions About Tradeoffs

### Misconception #1: "More optimization is always better"

**Reality:** Diminishing returns and new bugs.

```
Optimization levels in GCC:
-O0:  0% benefit,  0% compile time (baseline)
-O1: 40% benefit, 50% compile time increase
-O2: 60% benefit, 200% compile time increase
-O3: 70% benefit, 400% compile time increase

Each level adds less benefit but more cost.
Plus: Aggressive optimization can introduce bugs.
```

**Real-world lesson from Advent of Code optimization:**
- Complex optimization that looks promising: 2% speedup (or makes it worse!)
- Simple optimization (better data structure, eliminate allocation): 50% speedup

**The principle:** Measure, don't guess. Profile before optimizing. The "obvious" big optimization often disappoints, while the simple one surprises.

### Misconception #2: "Simple is always worse"

**Reality:** Simple is often better.

```
// Linear scan register allocation
// Simpler than graph coloring
// 95% as good in practice
// 10x faster to compile
// Used in V8, HotSpot, LuaJIT (production systems!)
```

**Real-world examples:**
- Advent of Code: Simple algorithm with good data structure often beats complex algorithm
- Compilers: Simple constant folding (easy) gives more benefit than complex alias analysis (hard)
- Chess engines: Simple evaluation + deeper search can beat complex evaluation + shallow search

**The pattern:** Complexity has a cost. Sometimes the simple solution wins on overall effectiveness.

### Misconception #3: "There's one right way"

**Reality:** Context determines the right approach.

```
Same language, different compilers:

JavaScript:
- V8 (Chrome): JIT, optimize hot code aggressively
- Node.js: Same engine, but different tradeoff (startup time matters)
- Hermes (React Native): AOT, optimize for size and startup

All correct, all different tradeoffs.
```

### Misconception #4: "Design tradeoffs are one-time decisions"

**Reality:** Tradeoffs shift as project evolves.

```
Phase 1: Getting it working
- Decision: Simple linear IR, no optimization
- Rationale: Prove correctness first

Phase 2: Basic performance
- Decision: Add constant folding, DCE
- Rationale: High impact, low complexity

Phase 3: Real-world use
- Decision: Convert to SSA, add more opts
- Rationale: Now worth the complexity

The "right" answer changed as goals changed.
```

---

## Practical Exercise: Identifying Tradeoffs

For each decision, identify the tradeoff:

### 1. String Representation in Compiler

**Option A:** Store strings as raw bytes
- Pro: Minimal memory
- Con: Every comparison is O(n)

**Option B:** Intern strings (store once, compare pointers)
- Pro: O(1) comparison
- Con: Upfront cost, hash table overhead

**Tradeoff:** Memory + setup time vs. comparison speed

**When to use each:**
- A: Few comparisons, many unique strings
- B: Many comparisons, many duplicate strings (typical in compilers)

---

### 2. Error Recovery in Parser

**Option A:** Stop at first error
- Pro: Simple to implement
- Pro: No cascade errors
- Con: Developer sees one error at a time

**Option B:** Try to continue parsing
- Pro: Report multiple errors
- Con: Later errors might be wrong (cascading)
- Con: Complex implementation

**Tradeoff:** Developer experience vs. implementation complexity

**When to use each:**
- A: Small files, fast compilation (see error, fix, recompile)
- B: Large files, slow compilation (fix multiple errors at once)

---

### 3. Type Representation

**Option A:** Store full type information everywhere
```
{
    kind: "function",
    params: [{name: "x", type: "int"}, {name: "y", type: "int"}],
    return: "int"
}
```
- Pro: All information available
- Con: Lots of memory

**Option B:** Use type IDs, store types in table
```
TypeID: 47  // Look up in type table
```
- Pro: Compact (just an integer)
- Con: Indirection to get type info

**Tradeoff:** Convenience vs. memory

**When to use each:**
- A: Small programs, prototyping
- B: Large programs, production compilers

---

## Your Turn: Start a "Tradeoffs I've Seen" List

As you progress, document tradeoffs you encounter:

```
| Decision | Option A | Option B | Chose | Why |
|----------|----------|----------|-------|-----|
| Lexer | Hand-written | Regex | Hand | Learning |
| Symbol table | Array | Hash | Hash | Performance |
| ... | ... | ... | ... | ... |
```

The goal: Build intuition for when to choose what.

---

## Key Takeaways

1. **Every design choice has costs and benefits**
   - There is no universally best option
   - Context determines the right choice

2. **Common tradeoff dimensions:**
   - Time (compile vs. runtime)
   - Space (memory vs. other resources)
   - Complexity (simple vs. powerful)
   - Strictness (safe vs. flexible)

3. **Multiple representations are normal:**
   - AST for structure
   - TAC for simplicity


   - CFG for control flow
   - SSA for optimization

4. **Tradeoffs change over time:**
   - Start simple
   - Add complexity when it's justified
   - Measure before optimizing

5. **Learn from real compilers:**
   - LLVM: Chose power over simplicity
   - TinyCC: Chose speed over optimization
   - V8: Chose runtime perf over compile time
   - All successful, all different

6. **Lessons from optimization work (compilers, Advent of Code, chess engines):**
   - **Measure, don't guess** - Your intuition about what's expensive is often wrong
   - **Simple can beat complex** - The elegant solution often outperforms the clever one
   - **Context matters** - The "best" approach depends on your constraints
   - **Big changes ≠ big improvements** - Sometimes small tweaks have huge impact
   - **Profile first** - Know where the time actually goes before optimizing

---

## Related Reading

- [[01-foundations/language-as-state]] - Why state representation matters
- [[05-ir/why-ast-is-not-enough]] - Why we need multiple IRs
- [[zettel/Z0003-representation]] - Representation tradeoffs
- [[00-index/invariants]] - What must be preserved despite tradeoffs

---

## Questions to Keep Thinking About

1. When is it worth adding a new IR to your compiler?
2. How do you measure whether a tradeoff was worth it?
3. What tradeoffs are forced by your target language?
4. What tradeoffs are forced by your target architecture?
5. When should you choose simplicity over performance?

Remember: **The best compiler isn't the one with the most features. It's the one that makes the right tradeoffs for its goals.**
