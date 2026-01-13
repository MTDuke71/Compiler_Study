# Language as State

## Links
- Up: [[01-foundations/README]]
- Related: 
  - [[01-foundations/day-01-what-is-a-compiler]]
  - [[01-foundations/ambiguity-and-phases]]
  - [[zettel/Z0001-state]]
  - [[zettel/Z0002-control-flow]]
  - [[zettel/Z0004-invariants]]
  - [[zettel/Z0005-compiler-phases]]
- Down: [[01-foundations/README]]

## Core Principle

**Compilation is a series of deterministic state transformations.**

Each compiler phase takes one representation of the program (a state) and transforms it into another representation. The entire compilation process is a state machine where:
- Source code is the **initial state**
- Machine code is the **final state**  
- Each compiler phase is a **transition function**
- The pipeline is **deterministic** (same input → same output)

## The State Transformation Pipeline

### Overview

```
Characters → Tokens → AST → Typed AST → IR → Optimized IR → Machine Code
```

Each arrow represents a **state transition** that:
1. Makes implicit information explicit
2. Removes a specific kind of ambiguity
3. Preserves program meaning
4. Produces a valid representation for the next phase

### Example: `x = 3 + 4 * 5` Through All States

**State₀: Character Stream**
```
"x = 3 + 4 * 5"
```
- Type: Unstructured bytes
- Ambiguity: Where do symbols begin and end?
- Invariants: Valid character encoding

**State₁: Token Stream** (after Lexing)
```
[IDENT(x), EQUALS, INT(3), PLUS, INT(4), STAR, INT(5)]
```
- Type: Sequence of classified symbols with boundaries
- Ambiguity: How do operators bind?
- Invariants: Each token has type, value, position

**State₂: Abstract Syntax Tree** (after Parsing)
```
Assign(
  target: Ident("x"),
  value: Add(
    left: Int(3),
    right: Mul(
      left: Int(4),
      right: Int(5)
    )
  )
)
```
- Type: Tree representing syntactic structure
- Ambiguity: What is `x`? What types are involved?
- Invariants: Valid syntax, proper nesting, precedence resolved

**State₃: Typed AST** (after Semantic Analysis)
```
Assign(
  target: Ident("x", type=int, addr=rbp-4),
  value: Add(
    left: Int(3, type=int),
    right: Mul(
      left: Int(4, type=int),
      right: Int(5, type=int)
    ),
    type: int
  )
)
```
- Type: Tree with types and resolved names
- Ambiguity: Execution order not explicit
- Invariants: All names resolved, types checked, scope valid

**State₄: Intermediate Representation** (after IR Translation)
```
t1 = 4 * 5      # Mul
t2 = 3 + t1     # Add
x = t2          # Assign
```
- Type: Three-address code with explicit control flow
- Ambiguity: Contains redundant computation
- Invariants: Control flow explicit, each operation simple

**State₅: Optimized IR** (after Optimization)
```
x = 23          # Constant folded
```
- Type: Improved IR with redundancy removed
- Ambiguity: Not mapped to machine instructions
- Invariants: Semantically equivalent to State₄

**State₆: Machine Code** (after Code Generation)
```
mov dword ptr [rbp-4], 23
```
- Type: Binary instructions for target architecture
- Ambiguity: None—fully explicit
- Invariants: Valid encoding, calling convention followed

## What "State" Means at Each Phase

### Character-Level State
- **Representation:** Raw bytes/text
- **Structure:** None—just a sequence
- **Information Available:** Character values only
- **Ambiguities:** Everything

### Token-Level State
- **Representation:** Classified symbols
- **Structure:** Flat sequence with boundaries
- **Information Available:** Symbol types, values, positions
- **Ambiguities:** Structure, meaning, execution

### AST-Level State
- **Representation:** Syntax tree
- **Structure:** Hierarchical, reflects grammar
- **Information Available:** Syntactic relationships, operator precedence
- **Ambiguities:** Meaning, types, execution order

### Typed AST-Level State
- **Representation:** Annotated syntax tree
- **Structure:** Same as AST, with metadata
- **Information Available:** Types, scopes, symbol bindings
- **Ambiguities:** Control flow, data flow, efficiency

### IR-Level State
- **Representation:** Control flow graph (CFG)
- **Structure:** Nodes = basic blocks, edges = control flow
- **Information Available:** Explicit control/data flow, def-use chains
- **Ambiguities:** Performance characteristics

### Optimized IR-Level State
- **Representation:** Transformed CFG
- **Structure:** Same as IR, reorganized
- **Information Available:** Same as IR, redundancies removed
- **Ambiguities:** Machine-specific details

### Machine Code-Level State
- **Representation:** Binary instructions
- **Structure:** Linear sequence for CPU
- **Information Available:** Everything—fully explicit
- **Ambiguities:** None

## Control Flow and Data Flow as State

Program state at any point during execution is:

```
State = (Control Location, Variable Values)
```

### Control Flow: "Where Are We?"

Control flow defines the **possible execution paths** through the program.

**Questions it answers:**
- Which statement executes next?
- What are all the possible paths from here?
- Can this code ever be reached?

**Representation:**
- **Implicit** in source code: `if`, `while`, `for` statements
- **Explicit** in IR: Control Flow Graph (CFG) with basic blocks and edges

**Example:**
```python
if x > 0:      # Control flow decision
    y = 1      # One path
else:
    y = -1     # Another path
print(y)       # Paths merge here
```

**CFG:**
```
[Entry] → [Test: x > 0] → [True: y = 1] ↘
                       ↘ [False: y = -1] → [Print y] → [Exit]
```

### Data Flow: "What Values Exist?"

Data flow tracks how **values propagate** through the program.

**Questions it answers:**
- Where is variable `x` defined?
- Where is `x` used?
- What value does `x` have here?
- Does this variable need to exist in a register?

**Representation:**
- **Implicit** in source: Variable names and assignments
- **Explicit** in IR: SSA (Static Single Assignment), def-use chains

**Example:**
```python
x = 3          # Define x (version 1)
y = x + 1      # Use x (version 1)
x = 5          # Define x (version 2)
z = x * 2      # Use x (version 2)
```

**SSA Form (makes versions explicit):**
```
x₁ = 3
y = x₁ + 1
x₂ = 5
z = x₂ * 2
```

### Combined: Program State Space

The **state space** of a program is the set of all possible `(location, values)` pairs:

```
StateSpace = {(pc, {var₁: val₁, var₂: val₂, ...}) | reachable}
```

**Why This Matters:**
- Compiler correctness means preserving the state space
- Optimizations must produce the same states at **observable points**
- Observable points: I/O, function returns, program termination

**Optimization Example:**
```python
# Original
x = 3
y = x + 1
z = y * 2

# Optimized (constant folding + propagation)
z = 8
```

Both have the same observable state: `z = 8` at the end.  
Intermediate states (`x = 3`, `y = 4`) are not observable, so they can be eliminated.

## State Invariants

**Invariants** are properties that must hold throughout compilation.  
They define the **contract** of each phase.

### Cross-Phase Invariants (Always True)

1. **Meaning Preservation**
   - Observable behavior never changes
   - Same inputs → same outputs
   - Violated = compiler bug

2. **Well-Formedness**
   - Each representation is valid for its phase
   - No malformed trees, invalid IR, or broken instructions
   - Violated = compiler crash or wrong code

3. **Traceability**
   - Can map machine code back to source lines
   - Essential for debugging
   - Preserved via metadata/debug info

4. **Determinism**
   - Same source + same options → same output
   - Required for reproducible builds
   - (Some randomness allowed if seeded consistently)

### Phase-Specific Invariants

**After Lexing:**
- Every token has a source location
- Token boundaries are non-overlapping
- Token stream covers entire source (no gaps)

**After Parsing:**
- AST is well-formed (valid tree)
- All syntax rules satisfied
- Every node has a source location
- Operator precedence correctly represented

**After Semantic Analysis:**
- All names are resolved to declarations
- All types are checked and valid
- Scope rules are enforced
- No type errors, no undefined variables
- Constants have known values

**After IR Translation:**
- All control flow is explicit (CFG)
- All data flow is traceable
- Every variable is defined before use
- CFG has single entry and exit points
- Basic blocks contain only straight-line code

**After Optimization:**
- Observable behavior unchanged (state space preserved)
- Semantic equivalence to unoptimized IR
- IR remains well-formed
- Dead code may be removed (unreachable states eliminated)

**After Code Generation:**
- Valid machine instructions for target
- Calling convention followed
- Register allocation is valid (no conflicts)
- Stack frame properly maintained
- Alignment requirements satisfied

## State Transformation Properties

### Determinism

Each phase is a **deterministic function**:

```
phase: State_in → State_out
```

Given the same input state, always produces the same output state.

**Why it matters:**
- Reproducible builds
- Debugging consistency
- Testing reliability

### Irreversibility (Usually)

Most transformations are **not reversible**:

```
Lexing:  "x=3" → [IDENT(x), EQUALS, INT(3)]
         Cannot reverse: whitespace lost
         
Optimization: x = 3 + 4 → x = 7
              Cannot reverse: structure lost
```

**Exception:** Debug info can provide partial reverse mapping.

### Monotonic Information Growth

Each phase **adds information** (makes implicit things explicit):

```
Characters: No structure
  ↓ +boundaries
Tokens: No grouping
  ↓ +precedence
AST: No types
  ↓ +type info
Typed AST: No control flow
  ↓ +CFG
IR: No optimization
  ↓ +efficiency
Optimized IR: No machine mapping
  ↓ +registers
Machine Code: Fully explicit
```

Information never flows backward in the pipeline.

### Preservation of Meaning

The most critical property:

```
∀ observables: behavior(State₀) = behavior(State₆)
```

All transformations preserve the **observable semantics** of the program:
- Same inputs produce same outputs
- I/O happens in the same order
- Same termination behavior (terminates/loops/errors)

Internal states can differ—only observables must match.

## Why This View Matters

### 1. Clarifies Compiler Correctness

A compiler is correct if:
```
∀ programs P: observables(execute(compile(P))) = observables(execute(P))
```

State transformation view makes this formal and testable.

### 2. Explains Why Phases Cannot Be Skipped

Each phase produces state that the next phase **requires**:
- Can't parse without tokens (need boundaries)
- Can't check types without AST (need structure)
- Can't optimize without IR (need explicit control flow)
- Can't generate code without optimization (would be inefficient)

### 3. Enables Formal Reasoning

State machines can be:
- **Verified** (prove invariants hold)
- **Tested** (check state transitions)
- **Debugged** (inspect intermediate states)

### 4. Guides Optimization Design

An optimization is valid iff:
```
StateSpace(original) ∩ Observables = StateSpace(optimized) ∩ Observables
```

Non-observable states can change freely.

### 5. Unifies Different Compiler Architectures

Whether single-pass or multi-pass, JIT or AOT, all compilers:
1. Transform state
2. Preserve meaning
3. Make information explicit
4. Follow a deterministic pipeline

## Common Patterns

### State Validation

Each phase should **validate its input** and **guarantee its output**:

```python
def parse(tokens: TokenStream) -> AST:
    assert is_valid_token_stream(tokens)  # Input contract
    ast = build_ast(tokens)
    assert is_valid_ast(ast)              # Output contract
    return ast
```

### State Debugging

Compilers often provide flags to **dump intermediate states**:

```bash
gcc -fdump-tree-all        # Dump all AST states
clang -emit-llvm           # Dump LLVM IR state
rustc --emit=mir           # Dump MIR state
```

This lets you inspect the state transformation pipeline.

### State Caching (Incremental Compilation)

Modern compilers cache intermediate states:

```
Source change → Invalidate affected states → Re-run phases → Cache new states
```

Only recompute states that depend on changed inputs.

## Connections to Other Concepts

- **[[ambiguity-and-phases]]**: Each phase removes ambiguity = makes state more explicit
- **[[zettel/Z0001-state]]**: Deep dive into state representation
- **[[zettel/Z0002-control-flow]]**: Control flow as state transitions
- **[[zettel/Z0004-invariants]]**: Properties that must hold across state transformations
- **[[zettel/Z0005-compiler-phases]]**: The six canonical state transformations

## Key Takeaways

1. **Compilation = State Transformation**: Each phase converts one program representation to another
2. **State = Structure + Information**: More explicit states have more information
3. **Control + Data = Complete State**: Program state requires both location and values
4. **Invariants = Compiler Correctness**: Violated invariants mean bugs
5. **Meaning Preservation is Central**: All transformations must preserve observable behavior
6. **Irreversible but Traceable**: Can't reverse transformations, but can map back via debug info

