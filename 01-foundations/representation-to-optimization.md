# From Representation to Optimization

## Links
- Up: [[01-foundations/README]]
- Related: [[01-foundations/day-04-meaning-to-representation]] [[05-ir/README]] [[06-optimization/README]] [[07-codegen/README]]
- See also: [[zettel/Z0005-compiler-phases]]

---

## Completing the Mental Model

You've now covered the foundations:
- **State** - What programs do [[zettel/Z0001-state]]
- **Representation** - How we encode programs [[zettel/Z0003-representation]]
- **Invariants** - What must be preserved [[zettel/Z0004-invariants]]
- **Tradeoffs** - How to make design decisions [[01-foundations/design-tradeoffs]]

Now we complete the picture: **how do we transform representations to produce better code?**

---

## The Complete Six-Phase Pipeline

```
Source Code
    ↓
[1. LEXING]          Character stream → Token stream
    ↓
[2. PARSING]         Token stream → AST
    ↓
[3. SEMANTICS]       AST → Annotated AST + Symbol Table
    ↓
[4. IR GENERATION]   AST → Intermediate Representation
    ↓
[5. OPTIMIZATION]    IR → Better IR (same behavior, faster)
    ↓
[6. CODE GENERATION] IR → Machine Code/Bytecode
    ↓
Executable
```

**Today's focus:** Understanding phases 4-6 and why they exist.

---

## Phase 4: IR Generation — The Working Form

### Why Not Optimize the AST?

**Problem:** ASTs are designed for different tasks:

```c
// Source
x = a + b * c;

// AST (tree structure)
Assignment
  ├── Identifier(x)
  └── BinaryOp(+)
      ├── Identifier(a)
      └── BinaryOp(*)
          ├── Identifier(b)
          └── Identifier(c)

// Good for: Preserving structure, pattern matching
// Bad for: Finding common subexpressions, analyzing control flow
```

**AST challenges:**
- Tree structure makes linear operations awkward
- No explicit control flow (where do jumps go?)
- Expression nesting complicates analysis
- Hard to find opportunities for optimization

### Enter IR: The Optimizer's Friend

**Three-Address Code (TAC):**
```
// Flattened, linear representation
t1 = b * c
t2 = a + t1
x = t2

// Good for: Sequential processing, instruction selection
// Each instruction: result = operand1 op operand2
```

**Key properties:**
- Linear (easy to iterate)
- Atomic operations (easy to analyze)
- Explicit temporaries (data flow visible)
- Platform-independent (not tied to x86 or ARM yet)

**See:** [[05-ir/three-address-code]] [[05-ir/why-ast-is-not-enough]]

---

## Phase 5: Optimization — Making It Faster

### What Is Optimization?

**Definition:** Transformations that preserve semantics but improve some metric.

**Metrics:**
- **Speed** (most common) - faster execution
- **Size** - smaller binary (embedded systems, web)
- **Power** - less energy consumption (mobile)
- **Memory** - smaller working set

**Critical constraint:** Observable behavior must not change (the master invariant!)

### Why IR Enables Optimization

**Before optimization, you need:**
1. **Data flow information** - Where are values computed? Used?
2. **Control flow information** - What paths can execution take?
3. **Alias information** - Do two pointers point to the same memory?

**IR makes these visible:**

```
// Original AST: Nested, implicit
if (x > 0) y = x + 1; else y = x - 1;

// IR (CFG + Basic Blocks): Explicit control flow
BB1:
    t1 = x > 0
    if_false t1 goto BB3
BB2:  // true branch
    t2 = x + 1
    y = t2
    goto BB4
BB3:  // false branch
    t3 = x - 1
    y = t3
BB4:  // merge point
    // Both paths write to y - optimizer can see this!
```

**Now the optimizer can ask:**
- Is variable `y` used after BB4? (dead code elimination)
- Does `x` change between checks? (common subexpression)
- Can we predict the branch? (constant propagation)

### Types of Optimizations

**Local (within a basic block):**
- Constant folding: `2 + 3` → `5`
- Algebraic simplification: `x * 1` → `x`
- Common subexpression elimination (local)

**Global (across basic blocks):**
- Dead code elimination
- Loop-invariant code motion
- Global common subexpression elimination

**Interprocedural (across functions):**
- Function inlining
- Devirtualization
- Whole-program optimization

**Complexity increases at each level, but so does impact.**

**See:** [[06-optimization/constant-folding]] [[06-optimization/dead-code]] [[06-optimization/local-vs-global]]

---

## Phase 6: Code Generation — From Abstract to Concrete

### What Does Codegen Do?

**Input:** Platform-independent IR (still abstract)
**Output:** Platform-specific machine code or bytecode

**Three main tasks:**

#### 1. Instruction Selection

**Problem:** Map IR operations to target instructions.

```
// IR
t1 = a + b
t2 = t1 * c

// x86 (two-address instructions)
mov  rax, a
add  rax, b      ; rax = a + b
mov  rbx, rax
imul rbx, c      ; rbx = (a+b) * c

// ARM (three-address instructions)
add  r0, r1, r2  ; r0 = a + b
mul  r3, r0, r4  ; r3 = (a+b) * c
```

**Challenge:** One IR operation might map to multiple machine instructions (or vice versa).

#### 2. Register Allocation

**Problem:** IR has unlimited temporaries, CPU has limited registers.

```
// IR (unlimited temporaries)
t1 = a + b
t2 = c + d
t3 = t1 * t2
t4 = t3 + e

// x86 (limited registers: rax, rbx, rcx, rdx, rsi, rdi, ...)
// Must assign temporaries to registers
// If not enough registers, spill to stack (slow!)

Option 1: All in registers (if we have 4+ available)
    mov rax, a
    add rax, b       ; t1 in rax
    mov rbx, c
    add rbx, d       ; t2 in rbx
    imul rax, rbx    ; t3 in rax
    add rax, e       ; t4 in rax

Option 2: Spilling (if registers scarce)
    mov rax, a
    add rax, b
    mov [rsp-8], rax ; spill t1 to stack
    mov rax, c
    add rax, d       ; t2 in rax
    imul rax, [rsp-8] ; reload t1, multiply
    add rax, e
```

**Tradeoff:** Register allocation directly impacts performance. This is hard!

**See:** [[07-codegen/registers-are-scarce]]

#### 3. Instruction Scheduling

**Problem:** Modern CPUs can execute multiple instructions in parallel (superscalar, out-of-order).

```
// Bad order (data dependency stalls)
mov rax, [x]
add rax, 1       ; must wait for load
mov rbx, [y]
add rbx, 2       ; must wait for load

// Better order (hide load latency)
mov rax, [x]
mov rbx, [y]     ; independent - can start while rax loads
add rax, 1       ; rax ready now
add rbx, 2       ; rbx ready now
```

**Goal:** Arrange instructions to maximize CPU parallelism.

**See:** [[07-codegen/instruction-selection]]

---

## The Relationship: IR → Optimization → Codegen

### Why This Order?

**You might ask:** Why not optimize machine code directly?

**Answer:** Abstraction enables better optimization.

```
// At IR level
t1 = x + 1
t2 = x + 1
// Optimizer sees: "These are the same!" → CSE eliminates t2

// At machine code level (x86)
mov rax, [x]
add rax, 1
mov rbx, [x]
add rbx, 1
// Much harder to see they're equivalent (different registers!)
```

**IR optimization is:**
- Platform-independent (write once, works for x86, ARM, RISC-V)
- Higher-level (easier to see semantic equivalences)
- More aggressive (can make assumptions machine code can't)

**Machine code optimization is:**
- Platform-specific (x86 tricks don't work on ARM)
- Lower-level (instruction latencies, cache effects)
- Final polish (can't change semantics much)

**Best practice:** Most optimization at IR level, final tuning at machine code level.

---

## Complete Mental Model

### The Flow of Information

```
SOURCE CODE
    ↓ [Characters]
LEXER
    ↓ [Tokens]
PARSER
    ↓ [AST - preserves structure]
SEMANTIC ANALYSIS
    ↓ [Annotated AST + Types + Symbols]
IR GENERATION
    ↓ [IR - enables analysis]
    ├─ Three-Address Code (linear)
    ├─ Control Flow Graph (explicit paths)
    └─ SSA Form (explicit data flow)
OPTIMIZATION
    ↓ [Optimized IR - same semantics, better performance]
CODE GENERATION
    ├─ Instruction Selection (IR → machine ops)
    ├─ Register Allocation (temporaries → registers)
    └─ Instruction Scheduling (parallel execution)
    ↓ [Machine Code / Bytecode]
EXECUTABLE
```

### What Each Phase Assumes

| Phase | Assumes (Invariants from Previous) | Provides |
|-------|-----------------------------------|----------|
| Lexer | Input is valid text | Well-formed tokens |
| Parser | Tokens are well-formed | Syntactically valid AST |
| Semantics | AST is syntactically valid | Type-checked AST, symbol table |
| IR Gen | Semantics are correct | Platform-independent IR |
| Optimization | IR is well-formed, types correct | Faster IR (same semantics) |
| Codegen | IR is optimized, semantically valid | Executable machine code |

Each phase **trusts** the previous phases (via invariants) and **prepares** for the next.

---

## Why This Matters for Implementation

### Starting Week 3: Lexer Implementation

You now understand:
- **Where lexing fits** (Phase 1 of 6)
- **What it must guarantee** (well-formed tokens)
- **What it enables** (parsing assumes valid tokens)
- **Why it exists** (separate concerns: characters vs. structure)

When you implement your lexer, you're not just "making tokens"—you're:
- **Establishing the first invariant** (token well-formedness)
- **Setting up the pipeline** (parser depends on your output)
- **Making a tradeoff** (hand-written vs. generated, speed vs. flexibility)

### The Big Picture

Every phase you implement will:
1. **Rely on invariants** from previous phases
2. **Transform representation** to enable the next phase
3. **Maintain semantics** (preserve program meaning)
4. **Make tradeoffs** (complexity vs. performance vs. simplicity)

Understanding the complete pipeline means you know **why** you're doing what you're doing, not just **what** to do.

---

## Optimization Deep Dive Preview

### What Makes Optimization Hard?

**The challenges:**

1. **Correctness is paramount**
   - Wrong code fast is still wrong
   - Optimizations must preserve all invariants
   - Edge cases are everywhere

2. **Interactions between optimizations**
   - Constant propagation enables dead code elimination
   - Dead code elimination enables more constant propagation
   - Need multiple passes or fixed-point iteration

3. **Tradeoff: compile time vs. benefit**
   - Some optimizations take forever and help little
   - Some are cheap and help a lot
   - Must choose which to implement

4. **Alias analysis is undecidable**
   ```c
   *p = 5;
   *q = 10;
   x = *p;  // Is x = 5 or 10? Depends if p == q!
   
   // Compiler must be conservative
   // Assume p and q might alias (overlap)
   // This blocks many optimizations
   ```

5. **Loops are critical but complex**
   - Most time is spent in loops
   - Most opportunity for speedup in loops
   - But loops have complex invariants and dependencies

### Common Optimizations (Preview)

**You'll implement:**

1. **Constant folding** (Week 9)
   - `2 + 3` → `5`
   - Easy, high impact, good first optimization

2. **Dead code elimination** (Week 10)
   - Remove unused computations
   - Requires data flow analysis

3. **Common subexpression elimination** (Week 10)
   - `x = a+b; y = a+b;` → `temp = a+b; x = temp; y = temp;`
   - Local vs. global versions

4. **Loop optimizations** (Week 11, if time)
   - Move invariant code out of loops
   - Unroll small loops
   - High impact but complex

**See:** [[06-optimization/README]] for the full list.

---

## Code Generation Deep Dive Preview

### What Makes Codegen Hard?

**The challenges:**

1. **Instruction selection is a matching problem**
   - One IR operation might match multiple instruction sequences
   - Some sequences are better (fewer instructions, faster)
   - Finding optimal match is NP-complete

2. **Register allocation is graph coloring**
   - NP-complete problem
   - But fast heuristics work well (linear scan, graph coloring)
   - Critical for performance

3. **Architecture-specific details**
   - x86: complex instructions, few registers (historical)
   - ARM: simple instructions, many registers
   - Each needs different strategies

4. **Calling conventions**
   - How to pass arguments? (registers, stack, both?)
   - Who saves registers? (caller, callee?)
   - Where's the return address? (register, stack?)
   - Different on every platform

### Your Codegen Target

**Week 11-12, you'll choose:**

**Option A: Stack machine (Jack/Nand2Tetris)**
- Simple: no register allocation needed
- Push/pop architecture
- Easy to implement, understand
- Good for learning fundamentals

**Option B: Register machine (Decaf → x86/bytecode)**
- Realistic: like real CPUs
- Must do register allocation
- More complex but more powerful
- Good for depth

**See:** [[07-codegen/stack-machines]] [[07-codegen/calling-conventions]]

---

## The Chess Engine Parallel (Again!)

You've built intuition from chess engines. Here's the compiler parallel:

| Chess Engine Phase | Compiler Phase | What It Does |
|-------------------|----------------|--------------|
| **Board Representation** | **IR** | Internal form optimized for analysis |
| **Move Generation** | **IR Generation** | Convert position to analyzable form |
| **Evaluation Function** | **Optimization** | Analyze and improve quality |
| **Move Selection** | **Codegen** | Convert decision to concrete action |

**In chess:**
- Board rep enables fast move generation
- Evaluation guides search
- Search depth vs. eval complexity tradeoff

**In compilers:**
- IR enables optimization
- Optimization improves code quality
- Compile time vs. code quality tradeoff

**Both:** Right representation enables the transformations you need.

---

## Preparation for Week 3

### You're Ready When You Can Answer:

1. **Why do we need IR?**
   - AST optimized for structure, IR optimized for transformation
   - Explicit control flow and data flow enable analysis
   - Platform-independent until codegen

2. **What does optimization do?**
   - Transforms IR to faster/smaller IR
   - Preserves semantics (invariants!)
   - Requires data flow and control flow information

3. **What does codegen produce?**
   - Machine code or bytecode
   - Maps abstract IR to concrete instructions
   - Handles registers, calling conventions, scheduling

4. **What's the complete pipeline?**
   - Lex → Parse → Analyze → IR → Optimize → Codegen
   - Each phase relies on invariants from previous
   - Each phase prepares for next

5. **Why start with lexing?**
   - Foundation: everything else needs tokens
   - Simple: good place to learn compiler basics
   - Well-defined: clear input (chars) and output (tokens)

### Ready for Implementation

**Week 3 starts:** Lexer implementation

**You'll build:**
- Hand-written lexer (design tradeoff!)
- Token data structure
- Error handling
- Test suite

**You understand:**
- Why you're doing it (Phase 1 of pipeline)
- What it guarantees (token invariants)
- How it fits (enables parsing)
- What tradeoffs you're making (hand-written vs. generated)

---

## Key Takeaways

1. **IR exists to enable optimization**
   - ASTs preserve structure
   - IR exposes data and control flow
   - Platform-independent optimization

2. **Optimization transforms while preserving semantics**
   - Must maintain all invariants
   - Tradeoff: compile time vs. code quality
   - Measure, don't guess (Advent of Code lesson!)

3. **Codegen makes it concrete**
   - Instruction selection (IR → machine ops)
   - Register allocation (temporaries → registers)
   - Architecture-specific details

4. **The pipeline is a series of representations**
   - Each optimized for different tasks
   - Each with its own invariants
   - Transformations between them

5. **You now have the complete mental model**
   - Six phases
   - Why each exists
   - How they connect
   - Ready to implement

---

## Related Reading

- [[05-ir/why-ast-is-not-enough]] - Why we can't optimize AST
- [[06-optimization/README]] - Optimization overview
- [[07-codegen/README]] - Code generation overview
- [[01-foundations/day-04-meaning-to-representation]] - State and representation
- [[zettel/Z0005-compiler-phases]] - Phase interactions

---

## Next Week Preview

**Week 3: Lexing**
- Implement hand-written lexer
- Handle numbers, identifiers, operators, keywords
- Build test suite
- Learn about regular languages and finite automata

You're moving from **understanding** to **building**. Everything you've learned in Week 1-2 will guide your implementation decisions.

**See you in the code!** 🚀
