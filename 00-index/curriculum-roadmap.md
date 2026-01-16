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
**Stanford Content:** (Lecture topics TBD - update when available)

**Expected Core Content:**
- Context-free grammars
- Top-down parsing (recursive descent, LL)
- Bottom-up parsing concepts
- Parse trees vs. abstract syntax trees

**Integration with Repository:**
- Deep dive into [[03-parsing/recursive-descent]]
- Formal grounding for [[03-parsing/ambiguity]]
- Connect to [[03-parsing/precedence-and-associativity]]

**Deliverables:**
- Format Stanford Week 3 lectures
- Document CFG for Cool
- Create examples of ambiguous vs. unambiguous grammars
- Update [[03-parsing/README]] with Stanford insights

**Success Criteria:**
- Can write CFG for simple languages
- Understand parsing algorithm tradeoffs
- Ready for advanced parsing techniques

---

### **Week 6: Stanford Week 4 — Parsing II**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Advanced parsing techniques
- Error recovery
- Parser generators
- Cool parser implementation

**Integration with Repository:**
- Advanced topics for [[03-parsing/README]]
- Practical examples for parser construction

**Deliverables:**
- Format Stanford Week 4 lectures
- Document parser error recovery strategies
- Implementation if Stanford provides assignment

**Success Criteria:**
- Can build parser for Cool (or subset)
- Understand production parser techniques
- Ready for semantic analysis

---

### **Week 7: Stanford Week 5 — Semantic Analysis**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Type systems and type checking
- Symbol tables and scoping
- Semantic rules for Cool
- Type inference (possibly)

**Integration with Repository:**
- Complements [[04-semantics/types-as-constraints]]
- Concrete examples for [[04-semantics/scope]]
- Implementation of [[04-semantics/symbol-tables]]

**Deliverables:**
- Format Stanford Week 5 lectures
- Document Cool's type system
- Build symbol table if assigned
- Connect to [[04-semantics/README]]

**Success Criteria:**
- Can implement type checker
- Understand scoping rules deeply
- Ready for IR generation

---

### **Week 8: Stanford Week 6 — Runtime & IR**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Runtime organization
- Activation records
- IR generation
- Cool runtime model

**Integration with Repository:**
- Bridges [[04-semantics/README]] to [[05-ir/README]]
- Concrete runtime for [[07-codegen/calling-conventions]]
- Stack layout examples

**Deliverables:**
- Format Stanford Week 6 lectures
- Document Cool runtime organization
- Draw stack layouts for Cool functions
- Update [[05-ir/README]] and [[07-codegen/README]]

**Success Criteria:**
- Understand memory layout
- Can generate IR from AST
- Ready for optimization

---

### **Week 9: Stanford Week 7 — Optimization I**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Local optimizations
- Data flow analysis
- Control flow graphs
- Basic optimization techniques

**Integration with Repository:**
- Expands [[06-optimization/constant-folding]]
- Formal treatment of [[06-optimization/data-flow]]
- Examples for [[05-ir/cfg]]

**Deliverables:**
- Format Stanford Week 7 lectures
- Document data flow analysis algorithms
- Implement optimizations if assigned
- Update [[06-optimization/README]]

**Success Criteria:**
- Can perform reaching definitions analysis
- Understand optimization safety
- Ready for advanced optimizations

---

### **Week 10: Stanford Week 8 — Optimization II**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Global optimizations
- SSA form
- Loop optimizations
- Advanced data flow

**Integration with Repository:**
- Deep dive into [[05-ir/ssa-intuition]]
- Advanced topics for [[06-optimization/README]]
- Global vs. local [[06-optimization/local-vs-global]]

**Deliverables:**
- Format Stanford Week 8 lectures
- Document SSA construction
- Understand phi nodes deeply
- Create advanced optimization zettels

**Success Criteria:**
- Can convert to SSA form
- Understand global optimization algorithms
- Ready for code generation

---

### **Week 11: Stanford Week 9 — Code Generation**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Instruction selection
- Register allocation
- Code generation for Cool
- Target architecture specifics

**Integration with Repository:**
- Implementation of [[07-codegen/instruction-selection]]
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

### **Week 12: Stanford Week 10 — Advanced Topics**
**Stanford Content:** (Lecture topics TBD)

**Expected Core Content:**
- Garbage collection (likely)
- Advanced features
- Real-world compiler techniques
- Cool complete compiler

**Integration with Repository:**
- Advanced topics beyond seven phases
- Modern compiler techniques
- Complete picture

**Deliverables:**
- Format Stanford Week 10 lectures
- Complete any final Stanford assignments
- Full Cool compiler if provided
- Comprehensive review of all phases

**Success Criteria:**
- Completed all Stanford content before access expires
- Have working Cool compiler (or substantial portions)
- Deep understanding of all compiler phases
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

**Activities:**
- Fix bugs discovered in testing
- Improve error messages
- Add extensions or optimizations:
  - Additional optimizations from Stanford
  - Better error recovery
  - Features beyond spec
  - Performance tuning
- Compare to Cool compiler
- Document design decisions

**Deliverables:**
- Complete, polished compiler
- Comprehensive test suite
- Documentation comparing Cool → your language
- Retrospective document

**Success Criteria:**
- Compiler is production-quality for pedagogical use
- Knowledge graph is complete
- Can explain every design decision
- Feel confident building another compiler

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
