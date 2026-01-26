# Compiler Study Curriculum Roadmap

## Links
- Up: [[00-index/README]]
- Related: [[README]] [[00-index/compiler-map]]

## Purpose

This roadmap provides a **recommended progression** through the compiler study materials.

It is:
- A guide, not a contract
- Designed for ~60 minutes of focused study per day
- Structured to build understanding cumulatively
- Flexible enough to accommodate tangents and deep dives

**You are not locked into this path.** The knowledge graph supports non-linear exploration. This roadmap simply ensures you don't miss foundational concepts that make later topics easier.

---

## Overall Arc (20-24 weeks)

### Phase 1: Foundations (Weeks 1-2)
Build top-down mental models using repository materials

### Phase 2: Stanford Course (Weeks 3-12)
**Priority: Complete before March 25, 2026 (course access expires)**
Comprehensive guided walkthrough of all compiler phases with Cool language

### Phase 3: Hands-On Reinforcement (Weeks 13-18)
Toy implementations for each phase—practice specific techniques in isolation

### Phase 4: Final Integration (Weeks 19-24+)
Build complete compiler (Decaf or Jack), synthesizing Stanford + hands-on practice

---

## Week-by-Week Plan

### **Week 1: Foundations — The Big Picture**
**Theme:** Why compilers exist and what they do

**Topics:**
- [[01-foundations/day-01-what-is-a-compiler]]
- [[01-foundations/day-02-from-text-to-structure]]
- [[01-foundations/day-03-structure-to-meaning]]
- [[01-foundations/day-04-meaning-to-representation]]

**Key Questions:**
- Why do phases exist?
- What ambiguity does each phase resolve?
- Why can't phases be skipped or reordered?

**Deliverables:**
- Complete Days 1-4
- Create/update [[zettel/Z0005-compiler-phases]]
- Sketch a mental model diagram (by hand is fine)

**Success Criteria:**
- Can explain the six phases to someone else
- Understand that compilers trade ambiguity for precision
- Feel oriented, not overwhelmed

---

### **Week 2: Foundations — Invariants and Constraints**
**Theme:** What stays the same, what must hold true

**Topics:**
- [[01-foundations/ambiguity-and-phases]] (review/deepen)
- [[01-foundations/language-as-state]]
- [[zettel/Z0004-invariants]]
- [[00-index/invariants]]

**Key Questions:**
- What invariants does each phase preserve?
- What constraints limit design choices?
- How do representations force tradeoffs?

**Deliverables:**
- Expand [[zettel/Z0004-invariants]]
- Document personal "aha" moments
- Begin a "common misconceptions" list

**Success Criteria:**
- Can identify when an optimization would violate meaning
- Recognize tradeoffs (e.g., speed vs. memory, simplicity vs. generality)
- Ready to start Stanford course with solid mental model

---

## Stanford Course (Weeks 3-12)

**PRIORITY: Complete before March 25, 2026** (course access expires)

See [[Stanford/README]] for detailed lecture breakdown and links to repository concepts.

**Approach:**
- Watch lecture → Take notes → Link to repository concepts
- Format transcripts as you go (aids retention through active processing)
- Complete any Stanford assignments/exercises provided
- Create zettels for new atomic concepts
- Cross-reference to existing repository materials

---

### **Week 3: Stanford Week 1 — Introduction & Cool**
**Stanford Lectures:** 01-01 through 02-03 (6 lectures)

**Core Content:**
- Introduction to compilers vs. interpreters
- Structure of a compiler (five phases)
- Economy of programming languages
- Cool language overview and examples

**Integration with Repository:**
- Reinforces [[01-foundations/day-01-what-is-a-compiler]]
- Concrete examples for [[Z0005-compiler-phases]]
- See Cool as implementation vehicle

**Deliverables:**
- Format all Week 1 Stanford lectures
- Create [[Stanford/lecture-01-introduction]] and subsequent lecture notes
- Update [[00-index/glossary]] with Cool-specific terms
- Cross-link Stanford concepts to repository zettels

**Success Criteria:**
- Understand why Cool was designed for teaching compilers
- Can explain compiler structure in Stanford's terms
- Ready for lexical analysis deep dive

---

### **Week 4: Stanford Week 2 — Lexical Analysis**
**Stanford Lectures:** 03-01 through 04-05 (10 lectures)

**Core Content:**
- Lexical analysis fundamentals
- Regular languages and regular expressions
- Finite automata (NFA, DFA)
- Thompson's construction (Regex → NFA)
- Subset construction (NFA → DFA)
- Implementing lexers

**Integration with Repository:**
- Complements [[02-lexing/README]] with formal theory
- Concrete examples for [[02-lexing/regular-languages]]
- Implementation techniques for [[02-lexing/hand-written-lexer]]

**Deliverables:**
- Format all Week 2 Stanford lectures
- Create detailed notes on finite automata
- Document regex → NFA → DFA transformations
- Expand [[02-lexing/regular-languages]] with Stanford insights

**Implementation (Optional but Recommended):**
- Implement lexer for Cool (if Stanford provides assignment)
- Or: Build simple lexer using techniques from lectures
- Test understanding with concrete code

**Success Criteria:**
- Can convert regex to NFA to DFA
- Understand why lexing uses regular languages
- Know difference between hand-written and generated lexers
- Ready for parsing

---

### **Week 5: Stanford Week 3 — Parsing I**
**Stanford Lectures:** 05-01 through 06-05 (10 lectures)

**Core Content:**
- Introduction to parsing (5-01)
- Context-free grammars (5-02)
- Derivations (5-03)
- Ambiguity in grammars (5-04)
- Error handling in parsers (6-01)
- Abstract syntax trees (6-02)
- Recursive descent parsing (6-03)
- Recursive descent algorithm (6-04)
- Recursive descent limitations (6-04-1)
- Left recursion problem (6-05)

**Integration with Repository:**
- Deep dive into [[03-parsing/recursive-descent]]
- Formal grounding for [[03-parsing/ambiguity]]
- Connect to [[03-parsing/precedence-and-associativity]]
- Practical examples for [[03-parsing/trees-vs-structure]]

**Deliverables:**
- Format all 10 Stanford Week 3 lectures
- Document CFG for Cool
- Create examples of ambiguous vs. unambiguous grammars
- Document left recursion elimination techniques
- Update [[03-parsing/README]] with Stanford insights

**Implementation (if provided):**
- Implement recursive descent parser for Cool subset
- Handle error recovery
- Build AST nodes

**Success Criteria:**
- Can write CFG for simple languages
- Understand derivations (leftmost, rightmost)
- Can identify and resolve grammar ambiguity
- Understand recursive descent algorithm and limitations
- Know how to eliminate left recursion
- Ready for advanced parsing techniques (Week 6)

---

### **Week 6: Stanford Week 4 — Parsing II (Bottom-Up Parsing)**
**Stanford Lectures:** 07-01 through 08-08 (14 lectures)

**Core Content:**
- Predictive parsing and LL(1) theory (7-01)
- First sets computation (7-02)
- Follow sets computation (7-03)
- LL(1) parsing tables (7-04)
- Bottom-up parsing introduction (7-05)
- Shift-reduce parsing (7-06)
- Handles and handle recognition (8-01, 8-02)
- Recognizing viable prefixes (8-03)
- Valid items (8-04)
- SLR parsing algorithm (8-05)
- SLR parsing examples (8-06, 8-08)
- SLR improvements (8-07)

**Integration with Repository:**
- Complements [[03-parsing/recursive-descent]] with bottom-up approach
- Formal theory for parser construction
- Advanced topics for [[03-parsing/README]]
- Comparison of top-down vs. bottom-up strategies

**Deliverables:**
- Format all 14 Stanford Week 4 lectures
- Document First/Follow set computation algorithms
- Create LL(1) parsing table examples
- Document SLR parsing algorithm with examples
- Trace shift-reduce parsing on example inputs
- Update [[03-parsing/README]] with bottom-up insights
- Implementation if Stanford provides assignment

**Success Criteria:**
- Can compute First and Follow sets
- Understand LL(1) parsing table construction
- Can trace shift-reduce parsing
- Understand handle recognition
- Know difference between LL and LR parsing
- Can build parser for Cool (or subset)
- Ready for semantic analysis

---

### **Week 7: Stanford Week 5 — Semantic Analysis**
**Stanford Lectures:** 09-01 through 09-09 (9 lectures)

**Core Content:**
- Introduction to semantic analysis (9-01)
- Scope and scoping rules (9-02)
- Symbol tables and implementation (9-03)
- Type systems fundamentals (9-04)
- Type checking mechanisms (9-05)
- Type environments (9-06)
- Subtyping and inheritance (9-07)
- Typing methods and self-type (9-08)
- Implementing type checking for Cool (9-09)

**Integration with Repository:**
- Complements [[04-semantics/types-as-constraints]]
- Concrete examples for [[04-semantics/scope]]
- Implementation of [[04-semantics/symbol-tables]]
- Practical type checking algorithms

**Deliverables:**
- Format all 9 Stanford Week 5 lectures
- Document Cool's type system and scoping rules
- Implement symbol table with nested scopes
- Implement type checker for Cool subset
- Document subtyping relationships
- Handle SELF_TYPE and method typing
- Update [[04-semantics/README]] with Stanford insights

**Success Criteria:**
- Can implement type checker with inheritance
- Understand scoping rules and symbol table management
- Know how to handle subtyping and SELF_TYPE
- Can check method signatures and types
- Ready for runtime organization and IR generation

---

### **Week 8: Stanford Week 6 — Cool Type Checking & Runtime Organization**
**Stanford Lectures:** 10-01 through 11-06 (12 lectures)

**Core Content:**
- Static vs. dynamic typing (10-01)
- SELF_TYPE fundamentals (10-02)
- SELF_TYPE operations and semantics (10-03)
- SELF_TYPE usage patterns (10-04)
- SELF_TYPE checking implementation (10-05)
- Error recovery strategies (10-06)
- Runtime organization overview (11-01)
- Activation records and stack frames (11-02, 11-03)
- Globals and heap management (11-04)
- Memory alignment (11-05)
- Stack machine architecture (11-06)

**Integration with Repository:**
- Bridges [[04-semantics/README]] to [[05-ir/README]]
- Concrete runtime for [[07-codegen/calling-conventions]]
- Stack machine details for [[07-codegen/stack-machines]]
- Memory layout examples

**Deliverables:**
- Format all 12 Stanford Week 6 lectures
- Document SELF_TYPE checking thoroughly
- Document Cool runtime organization and memory model
- Draw activation record layouts
- Understand stack vs. heap allocation
- Document alignment requirements
- Analyze stack machine architecture
- Update [[05-ir/README]] and [[07-codegen/README]]

**Success Criteria:**
- Can implement SELF_TYPE checking correctly
- Understand activation records and calling conventions
- Know memory layout (stack, heap, globals)
- Understand alignment and its importance
- Can design stack machine instruction set
- Ready for code generation and optimization

---

### **Week 9: Stanford Week 7 — Code Generation & Operational Semantics**
**Stanford Lectures:** 12-01 through 13-04 (10 lectures)

**Core Content:**
- Introduction to code generation (12-01)
- Code generation fundamentals (12-02, 12-03)
- Code generation example walkthrough (12-04)
- Temporaries and register management (12-05)
- Object layout in memory (12-06)
- Semantics overview (13-01)
- Operational semantics framework (13-02)
- Cool operational semantics part I (13-03)
- Cool operational semantics part II (13-04)

**Integration with Repository:**
- Implementation of [[07-codegen/instruction-selection]]
- Concrete examples for [[07-codegen/registers-are-scarce]]
- Object layout for [[07-codegen/stack-machines]]
- Operational semantics formalism
- Complete [[07-codegen/README]]

**Deliverables:**
- Format all 10 Stanford Week 7 lectures
- Document code generation algorithms for Cool
- Understand temporary allocation strategies
- Document object layout and memory representation
- Learn operational semantics notation and rules
- Formalize Cool semantics using operational approach
- Implement code generator for Cool subset
- Update [[07-codegen/README]] with Stanford insights

**Success Criteria:**
- Can generate code for Cool expressions and statements
- Understand temporary management and register usage
- Know object memory layout and vtables
- Can read and write operational semantics rules
- Understand formal semantics of Cool
- Ready for optimization techniques

---

### **Week 10: Stanford Week 8 — Local Optimization & Global Optimization**
**Stanford Lectures:** 14-01 through 15-05 (9 lectures)

**Core Content:**
- Intermediate code representation (14-01)
- Optimization overview and framework (14-02)
- Local optimization techniques (14-03)
- Peephole optimization (14-04)
- Dataflow analysis foundations (15-01)
- Constant propagation (15-02)
- Analysis of loops (15-03)
- Orderings and lattices (15-04)
- Liveness analysis (15-05)

**Integration with Repository:**
- Expands [[06-optimization/constant-folding]]
- Formal treatment of [[06-optimization/data-flow]]
- Examples for [[05-ir/cfg]]
- Local vs. global [[06-optimization/local-vs-global]]
- Dead code elimination [[06-optimization/dead-code]]

**Deliverables:**
- Format all 9 Stanford Week 8 lectures
- Document intermediate code forms used by Cool
- Understand local optimization patterns
- Implement peephole optimizer
- Document dataflow analysis framework thoroughly
- Implement constant propagation algorithm
- Analyze loops for optimization opportunities
- Understand lattice theory for dataflow
- Implement liveness analysis
- Update [[06-optimization/README]] with Stanford insights

**Success Criteria:**
- Can perform local optimizations (basic blocks)
- Understand peephole optimization patterns
- Can implement dataflow analysis algorithms
- Understand constant propagation and folding
- Can compute liveness information
- Know difference between forward and backward analysis
- Ready for register allocation and advanced topics

**Success Criteria:**
- Can convert to SSA form
- Understand global optimization algorithms
- Ready for code generation

---

### **Week 11: Stanford Week 9 — Register Allocation & Garbage Collection**
**Stanford Lectures:** 16-01 through 17-05 (9 lectures)

**Core Content:**
- Register allocation fundamentals (16-01)
- Graph coloring algorithm (16-02)
- Spilling and register pressure (16-03)
- Managing caches (16-04)
- Automatic memory management overview (17-01)
- Mark and sweep garbage collection (17-02)
- Stop and copy garbage collection (17-03)
- Conservative garbage collection (17-04)
- Reference counting (17-05)

**Integration with Repository:**
- Implementation of [[07-codegen/registers-are-scarce]]
- Graph coloring for register allocation
- Memory management strategies
- Advanced runtime topics

**Deliverables:**
- Format all 9 Stanford Week 9 lectures
- Document register allocation algorithm
- Implement graph coloring for register allocation
- Understand spilling strategies and when to spill
- Document cache management techniques
- Understand garbage collection algorithms (mark-sweep, stop-copy, conservative, reference counting)
- Compare GC strategies (throughput vs. pause time)
- Analyze tradeoffs between different GC approaches
- Update [[07-codegen/README]] with register allocation insights

**Success Criteria:**
- Can implement graph coloring register allocator
- Understand when and how to spill registers
- Know cache management strategies
- Understand all major GC algorithms
- Can compare GC tradeoffs (conservative vs. precise, stop-the-world vs. incremental)
- Can implement basic mark-sweep or reference counting
- Ready for advanced compiler topics and course completion
- Concrete examples for [[07-codegen/registers-are-scarce]]
- Complete [[07-codegen/README]]

**Deliverables:**
- Format Stanford Week 9 lectures
- Document register allocation algorithms
- Implement codegen if assigned
- Update all [[07-codegen/]] notes

**Success Criteria:**
- Can generate assembly/bytecode
- Understand register allocation
- Ready for final integration

---

### **Week 12: Stanford Week 10 — Java**
**Stanford Lectures:** 18-01 through 18-07 (7 lectures)

**Core Content:**
- Java language overview and history (18-01)
- Java arrays and memory model (18-02)
- Java exceptions and exception handling (18-03)
- Java interfaces and abstraction (18-04)
- Java coercions and type conversions (18-05)
- Java threads and concurrency (18-06)
- Other Java topics and advanced features (18-07)

**Integration with Repository:**
- Real-world language design case study
- Comparison with Cool language design
- Advanced type system features
- Concurrency and runtime considerations
- Language feature tradeoffs

**Deliverables:**
- Format all 7 Stanford Week 10 lectures
- Document Java's type system and compare to Cool
- Understand Java's exception handling mechanism
- Analyze interface-based abstraction vs. inheritance
- Document Java's memory model and array representation
- Understand thread model and concurrency primitives
- Compare language design decisions (Java vs. Cool)
- Reflect on compiler implications of Java features
- Complete comprehensive review of all Stanford content

**Success Criteria:**
- Understand Java as a real-world language design case study
- Can compare and contrast Java and Cool design decisions
- Understand exception handling implementation challenges
- Know how interfaces affect type checking and code generation
- Completed all Stanford content before access expires (March 25, 2026)
- Have deep understanding of all compiler phases through Cool
- Can articulate tradeoffs in language design
- Ready to build independent compiler

---

## Hands-On Reinforcement (Weeks 13-18)

**Timeline:** After March 25, 2026 (Stanford access expires)

**Objective:** Build toy implementations to reinforce each phase independently

**Philosophy:** Stanford showed you the complete picture with Cool. Now practice each technique in isolation with simple examples before tackling a full language. This is deliberate practice—focus on specific skills without the complexity of a complete language.

---

### **Week 13: Lexing — From Characters to Tokens**
**Theme:** Chunking input into meaningful units

**Topics:**
- [[02-lexing/tokens-vs-characters]]
- [[02-lexing/regular-languages]]
- [[02-lexing/failure-modes]]

**Key Questions:**
- What makes a good token boundary?
- Why are some patterns "regular" and others not?
- How should a lexer handle errors?

**Deliverables:**
- Implement a hand-written lexer for arithmetic expressions
- Handle: numbers, identifiers, `+`, `-`, `*`, `/`, `(`, `)`
- Test with malformed input (unterminated strings, invalid characters)
- Compare to Cool lexer from Stanford

**Success Criteria:**
- Lexer can tokenize valid input
- Lexer reports meaningful errors for invalid input
- Can explain differences between this simple lexer and Cool's lexer

---

### **Week 14: Parsing — From Tokens to Trees**
**Theme:** Building structure from flat sequences

**Topics:**
- [[03-parsing/recursive-descent]]
- [[03-parsing/precedence-and-associativity]]
- [[03-parsing/trees-vs-structure]]
- [[03-parsing/ambiguity]]

**Key Questions:**
- Why does operator precedence need to be encoded in grammar?
- How does recursive descent work?
- What's the difference between parse trees and ASTs?

**Deliverables:**
- Write a recursive descent parser for expressions
- Handle precedence: `*` > `+`, left associativity
- Create AST nodes (not just parse trees)
- Add statements: `if`, `while`, `assignment`, blocks `{ ... }`

**Implementation:**
- Parser consumes tokens from Week 13's lexer
- Build: `Expr`, `BinOp`, `Number`, `Ident`, `Stmt` AST nodes
- Test: `3 + 4 * 5` → `Add(3, Mul(4, 5))`
- Ensure `if-else` binds correctly (dangling else problem)

**Success Criteria:**
- Parser correctly handles precedence
- AST is simpler than parse tree
- Can parse multi-line programs
- Can explain how this relates to Cool's parser

---

### **Week 15: Semantics — Enforcing Meaning**
**Theme:** Checking what syntax cannot express

**Topics:**
- [[04-semantics/scope]]
- [[04-semantics/symbol-tables]]
- [[04-semantics/types-as-constraints]]
- [[04-semantics/illegal-states]]

**Key Questions:**
- How do scopes work?
- What goes in a symbol table?
- How do you check types?

**Deliverables:**
- Implement symbol table with nested scopes
- Add semantic checks: undefined variables, type errors
- Report meaningful error messages
- Compare to Cool's type system

**Implementation:**
- Walk AST from Week 14 and build symbol table
- Check: variable declared before use
- Check: types match in expressions (e.g., no `int + string`)
- Handle shadowing in nested scopes

**Success Criteria:**
- Semantic errors are caught and reported
- Valid programs pass without errors
- Can explain difference between syntax and semantic errors
- Understand how this compares to Cool's semantic analysis

---

### **Week 16: Intermediate Representation — The Working Form**
**Theme:** Lowering AST to a form suitable for optimization

**Topics:**
- [[05-ir/why-ast-is-not-enough]]
- [[05-ir/three-address-code]]
- [[05-ir/cfg]]
- [[05-ir/ssa-intuition]]

**Key Questions:**
- Why can't we optimize the AST directly?
- What makes IR easier to transform?
- How do you represent control flow?

**Deliverables:**
- Translate AST to three-address code (TAC)
- Build control-flow graph (CFG) from TAC
- Visualize CFG (draw it)
- Experiment with SSA conversion for simple cases

**Implementation:**
- Lower expressions: `a + b * c` → `t1 = b * c; t2 = a + t1`
- Lower control flow: `if`, `while` → labeled blocks + jumps
- Generate unique temporary names
- Compare to Cool's IR

**Success Criteria:**
- Every expression is atomic (at most three operands)
- Control flow is explicit (gotos, labels)
- CFG shows all execution paths
- Understand why Stanford used their IR design

---

### **Week 17: Optimization — Making Code Better**
**Theme:** Transformations that preserve meaning

**Topics:**
- [[06-optimization/constant-folding]]
- [[06-optimization/dead-code]]
- [[06-optimization/local-vs-global]]
- [[06-optimization/data-flow]]

**Key Questions:**
- What optimizations are always safe?
- How do you prove an optimization is correct?
- What's the difference between local and global optimization?

**Deliverables:**
- Implement constant folding
- Implement dead code elimination
- Measure impact (count IR instructions before/after)
- Apply data flow analysis techniques from Stanford

**Implementation:**
- Fold: `3 + 4` → `7`
- Eliminate: unused temporaries
- Test on real examples
- Compare to Cool's optimizations

**Success Criteria:**
- Optimized IR is smaller and faster
- Semantics are preserved (test with execution)
- Can explain why each optimization is safe
- Understand tradeoffs Stanford made in Cool compiler

---

### **Week 18: Code Generation — Targeting Real Machines**
**Theme:** From IR to executable code

**Topics:**
- [[07-codegen/instruction-selection]]
- [[07-codegen/registers-are-scarce]]
- [[07-codegen/stack-machines]]
- [[07-codegen/calling-conventions]]

**Key Questions:**
- How do IR operations map to machine instructions?
- What happens when you run out of registers?
- Why are stack machines simpler?
- How do function calls work at machine level?

**Deliverables:**
- Generate bytecode for a stack machine
- Document instruction set
- Add function calls with simple calling convention
- Test recursive functions

**Implementation:**
- Define simple bytecode: `PUSH`, `ADD`, `STORE`, `CALL`, `RET`, etc.
- Translate IR → bytecode
- Write interpreter for bytecode
- Generate code for function entry/exit
- Compare to Cool's code generation

**Success Criteria:**
- Programs execute and produce correct results
- Functions can call other functions
- Recursion works correctly
- Can explain stack vs. register machines
- Understand Cool's target architecture choices

---

## Final Integration (Weeks 19-24+)

**Timeline:** After completing hands-on reinforcement

**Objective:** Build complete compiler from scratch, synthesizing Stanford theory + hands-on practice

### **Week 19-20: Design and Foundation**
**Theme:** Choose target language and implement lexer + parser

**Target Language Decision:**

Choose between two well-designed pedagogical languages:

**Option A: Decaf (MIT 6.035)**
- More realistic/complex language (closer to C/Java)
- Better for learning optimization and advanced IR
- Arrays, functions, richer type system
- Requires runtime library or C linkage for I/O
- Specification: [[spec/README]]
- **Best if:** You want deeper optimization experience and don't mind additional complexity

**Option B: Jack (Nand2Tetris)**
- Simpler, faster to complete
- Complete ecosystem (compiler → VM → hardware)
- Stack machine target (no register allocation)
- Built-in OS API (String, Memory, Math, I/O handled)
- Excellent test suite and course materials
- **Best if:** You want end-to-end understanding and a guaranteed win

**Recommendation:** Make this choice based on:
- How comfortable you feel with Stanford + hands-on material
- Whether you value breadth (Jack) or depth (Decaf)
- Time and energy level
- **Key advantage:** You've now seen Cool (Stanford) + built simple compilers (Weeks 13-18)

**Week 19-20 Goals:**
- Choose target language
- Implement complete lexer for chosen language
- Implement complete parser for chosen language
- Build clean AST representation

**Deliverables:**
- Working lexer and parser
- Comprehensive test suite for lexer/parser
- AST design documented

**Success Criteria:**
- Can parse all valid programs in the language
- Error messages are helpful and include location
- AST is clean and suitable for semantic analysis

---

### **Week 21: Semantic Analysis**
**Theme:** Type checking and scope resolution

**Goals:**
- Implement symbol table for chosen language
- Implement type checker following language spec
- Handle all semantic rules (scoping, typing, etc.)
- Meaningful error reporting

**Deliverables:**
- Complete semantic analyzer
- Test programs covering all semantic rules
- Error messages for common mistakes

**Success Criteria:**
- All semantic errors caught before code generation
- Valid programs pass semantic analysis
- Can explain every semantic rule implemented

---

### **Week 22: IR and Optimization**
**Theme:** Lower to IR and apply optimizations

**Goals:**
- Generate IR from semantically-valid AST
- Build control-flow graph
- Implement optimizations from Stanford + hands-on practice
- Measure optimization impact

**Deliverables:**
- IR generator
- CFG construction
- At least 3 optimizations implemented
- Performance measurements

**Success Criteria:**
- IR is suitable for code generation
- Optimizations preserve semantics
- Can explain each optimization's correctness

---

### **Week 23: Code Generation**
**Theme:** Target the machine (or VM)

**Goals:**
- Generate target code (assembly for Decaf, VM code for Jack)
- Implement calling conventions
- Handle all language features
- End-to-end compilation works

**Deliverables:**
- Complete code generator
- Generated code executes correctly
- All spec features implemented

**Success Criteria:**
- Compiler can compile all test programs
- Generated code produces correct output
- Can run non-trivial programs

---

### **Week 24+: Polish and Extension**
**Theme:** Refinement and exploration

**Core Activities:**
- Fix bugs discovered in testing
- Improve error messages
- Add extensions or optimizations:
  - Additional optimizations from Stanford
  - Better error recovery
  - Features beyond spec
  - Performance tuning
- Compare to Cool compiler
- Document design decisions

**Extension: Native Assembly Backend**

After completing the stack machine/VM backend, extend to native assembly:

**Phase 1: x86-64 Backend**
- **Why first:** Native execution on your Windows machine, no emulation needed
- **Target:** x86-64 assembly (System V ABI for Linux, Microsoft x64 for Windows)
- **Toolchain:** GCC/Clang for assembly and linking
- **Register allocation:** Apply graph coloring from Stanford Week 9
- **Calling convention:** Implement stack frames with rbp/rsp
- **Debugging:** Use GDB or LLDB to step through generated assembly
- **Comparison point:** CISC architecture - variable-length instructions, many addressing modes

**Phase 2: ARM Backend (RISC comparison)**
- **Why:** Cleaner RISC architecture, better for understanding compiler design
- **Target:** ARMv8/AArch64 (64-bit ARM)
- **Emulation:** QEMU user-mode (`qemu-aarch64`) - runs ARM binaries on x86
  ```bash
  # Compile for ARM
  aarch64-linux-gnu-as -o program.o program.s
  aarch64-linux-gnu-ld -o program program.o
  
  # Run with QEMU
  qemu-aarch64 ./program
  ```
- **Toolchain:** `aarch64-linux-gnu-gcc` cross-compiler (available on Windows/Linux)
- **Architecture benefits:**
  - Fixed-length instructions (4 bytes each)
  - Regular encoding (easier instruction selection)
  - More registers (31 general-purpose vs x86's 16)
  - Load/store architecture (operations only on registers)
  - Cleaner than 6502 but same RISC philosophy
- **Comparison:** Document how register allocation differs with 31 registers vs 16

**Implementation Strategy:**
1. **Instruction selection:** Create pattern matching for IR → assembly
2. **Register allocation:** Use graph coloring with actual register constraints
3. **Code emission:** Generate `.s` assembly files
4. **Linking:** Use system linker to create executables
5. **Testing:** Compare output with VM version for correctness

**Connection to 6502 Experience:**
- ARM is 6502's spiritual successor (both RISC, load/store architectures)
- x86 is the opposite (CISC, complex addressing modes)
- Understanding both gives you the full spectrum of code generation

**Deliverables:**
- Complete, polished compiler with stack machine backend
- x86-64 assembly backend (native execution)
- ARM backend (QEMU emulation)
- Comprehensive test suite for all three targets
- Documentation comparing:
  - Stack machine vs register machine code generation
  - CISC (x86) vs RISC (ARM) instruction selection
  - Register allocation strategies for different register counts
  - Cool (Stanford) → your language → native assembly journey
- Retrospective document on entire learning journey

**Success Criteria:**
- Compiler can target three backends: stack machine, x86-64, ARM
- Generated native assembly runs correctly and efficiently
- Can explain register allocation and instruction selection for both architectures
- Knowledge graph documents CISC vs RISC tradeoffs
- Compiler is production-quality for pedagogical use
- Can explain every design decision
- Feel confident building another compiler
- **Have come full circle:** From disassembling 6502 to generating ARM assembly

---

## Critical Timeline

**January 16 - March 25, 2026:** 10 weeks (70 days)
- **Weeks 1-2:** Foundations (current)
- **Weeks 3-12:** Stanford content (must complete before access expires)

**After March 25, 2026:** Flexible timeline
- **Weeks 13-18:** Hands-on reinforcement (6 weeks, but can adjust)
- **Weeks 19-24+:** Final compiler project (6+ weeks minimum)

**Total estimated time:** 24+ weeks (6 months)

**Key Milestone:** March 25, 2026 - Stanford access expires (only hard deadline)

**Pacing:**
- Stanford: ~60-90 min/day, 6-7 days/week (time-critical)
- Hands-on: ~60-90 min/day, 5-6 days/week (flexible)
- Final project: ~90-120 min/day, 5-6 days/week (flexible)

---

## Flexibility and Adaptation

**Critical Priority: Stanford Course (Weeks 3-12)**
- You have **10 weeks** to complete 10 weeks of Stanford content (Jan 16 - Mar 25)
- Stay on schedule with Stanford lectures—they expire March 25, 2026
- Repository materials are permanent—can always revisit
- Format lecture notes as you go (aids retention), but don't let it block progress
- If falling behind, **watch lectures first**, format notes later

**Hands-On Reinforcement (Weeks 13-18): Flexible**
- No deadline pressure after Stanford completes
- Take time to internalize each phase
- Can spend more time on challenging topics (e.g., optimization, codegen)
- Can spend less time on easier topics (e.g., if lexing clicked during Stanford)
- Skip or condense weeks if you feel confident from Stanford alone

**Final Project (Weeks 19-24+): Very Flexible**
- This is the synthesis—take as long as needed
- Quality matters more than speed
- Can pause for deep dives into specific topics
- Can extend indefinitely with additional features

**Note on Structure:**
- **Weeks 1-2**: Foundation using repository materials (flexible, in progress)
- **Weeks 3-12**: Stanford course (time-bound, must complete before access expires)
- **Weeks 13-18**: Toy implementations for reinforcement (flexible, no deadline)
- **Weeks 19-24+**: Complete compiler project (flexible, no deadline)

This roadmap assumes:
- ~60-90 minutes per day during Stanford weeks (required for staying on track)
- ~60-90 minutes per day during hands-on weeks (recommended)
- ~90-120 minutes per day during final project (recommended)
- Zettels created as insights emerge, not on schedule
- **Finishing Stanford is priority #1 through Week 12**

**Adjust the pace based on:**
- How quickly Stanford concepts click
- How much time you have available
- Whether you're doing Stanford assignments (recommended if provided)
- Your energy level and absorption rate
- How much hands-on practice you need after Stanford

**If falling behind Stanford schedule:**
1. Watch lectures first (don't skip)
2. Take minimal notes during viewing
3. Format/expand notes after access expires
4. Prioritize understanding over perfect documentation

**The goal is understanding, not completion, but Stanford content is time-limited.**

---

## Success Metrics

**By end of Week 12 (Stanford completion - March 25, 2026):**

1. **Completed** all Stanford lectures before access expires
2. **Understand** Cool language and why it's designed as it is
3. **Can explain** compiler phases using Stanford's examples
4. **Have notes** linking Stanford content to repository concepts
5. **Completed** any Stanford assignments provided
6. **Feel ready** to implement independent compiler

**By end of Week 18 (Hands-on reinforcement):**

1. **Built** toy implementations for each major phase
2. **Internalized** core techniques through practice
3. **Can explain** each phase independently with concrete examples
4. **Have working** lexer, parser, semantic analyzer, IR generator, optimizer, codegen (simple versions)
5. **Understand** how techniques from Stanford apply to different contexts

**By end of Week 24+ (Final compiler project):**

1. **Explain** every compiler phase without notes
2. **Built** a complete compiler from scratch for Decaf or Jack
3. **Debug** compiler bugs by knowing which phase is responsible
4. **Read** compiler papers and understand their claims
5. **Design** optimizations and prove them correct
6. **Navigate** this knowledge graph fluently
7. **Compare** implementation choices across Cool (Stanford), simple compilers (Weeks 13-18), and final project
8. **Articulate** tradeoffs in different compiler designs

If you can do these things, the roadmap served its purpose.

If you can't yet, extend the timeline—**after March 25, there's no deadline.**

This roadmap assumes:
- ~60-90 minutes per day, 6-7 days per week during Stanford weeks
- Stanford lectures vary: 8-23 minutes each
- Week 2 has 10 lectures (~2.5 hours of video)—spread across 7 days = ~20 min/day
- Some days will go faster, some slower
- Zettels created as insights emerge, not on schedule
- **Finishing Stanford is priority #1 through Week 12**

**Adjust the pace based on:**
- How quickly Stanford concepts click
- How much time you have available
- Whether you're doing Stanford assignments (recommended if provided)
- Your energy level and absorption rate

**If falling behind Stanford schedule:**
1. Watch lectures first (don't skip)
2. Take minimal notes during viewing
3. Format/expand notes after access expires
4. Prioritize understanding over perfect documentation

**The goal is understanding, not completion, but Stanford content is time-limited.**

---

## Success Metrics

**By end of Week 12 (Stanford completion - March 25, 2026):**

1. **Completed** all Stanford lectures before access expires
2. **Understand** Cool language and why it's designed as it is
3. **Can explain** compiler phases using Stanford's examples
4. **Have notes** linking Stanford content to repository concepts
5. **Completed** any Stanford assignments provided
6. **Feel ready** to build compilers independently

**By end of Week 18 (Hands-on reinforcement):**

1. **Built** toy implementations for each major phase
2. **Internalized** core techniques through practice
3. **Can explain** each phase independently with concrete examples
4. **Have working** lexer, parser, semantic analyzer, IR generator, optimizer, codegen (simple versions)
5. **Understand** how techniques from Stanford apply to different contexts

**By end of Week 24+ (Final compiler project):**

1. **Explain** every compiler phase without notes
2. **Built** a complete compiler from scratch for Decaf or Jack
3. **Debug** compiler bugs by knowing which phase is responsible
4. **Read** compiler papers and understand their claims
5. **Design** optimizations and prove them correct
6. **Navigate** this knowledge graph fluently
7. **Compare** implementation choices across Cool (Stanford), simple compilers (Weeks 13-18), and final project
8. **Articulate** tradeoffs in different compiler designs

If you can do these things, the roadmap served its purpose.

If you can't yet, extend the timeline—**after March 25, there's no deadline.**

---

## Next Steps

- [ ] Review this roadmap
- [ ] Adjust based on your goals and constraints
- [ ] Complete Week 1-2 foundations
- [ ] Begin Stanford Week 1 (target: Week 3)
- [ ] Create weekly notes as you go
- [ ] Update this roadmap when you discover better paths

This is a living document. Improve it as you learn.
- [ ] Create weekly notes as you go
- [ ] Update this roadmap when you discover better paths

This is a living document. Improve it as you learn.
