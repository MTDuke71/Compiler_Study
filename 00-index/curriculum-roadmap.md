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

## Overall Arc (12-16 weeks)

### Phase 1: Mental Models (Weeks 1-2)
Build top-down understanding of what compilers do and why

### Phase 2: Input Processing (Weeks 3-5)
Deep dive into lexing and parsing—turning text into structure

### Phase 3: Meaning and Validation (Weeks 6-7)
Semantic analysis—enforcing rules and assigning types

### Phase 4: Transformation (Weeks 8-10)
IR and optimization—preparing code for execution

### Phase 5: Execution (Weeks 11-12)
Code generation—targeting real machines

### Phase 6: Integration (Weeks 13-16)
Building a complete compiler, revisiting concepts, filling gaps

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

**Implementation Start:**
- Sketch pseudocode for a minimal lexer (no code yet—just design)

**Success Criteria:**
- Can identify when an optimization would violate meaning
- Recognize tradeoffs (e.g., speed vs. memory, simplicity vs. generality)
- Have concrete questions ready for Week 3

---

### **Week 3: Lexing — From Characters to Tokens**
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
- Complete reading of all [[02-lexing/README]] topics
- Create [[zettel/Z0006-tokens]] (or similar)
- Document regex patterns for common tokens

**Implementation:**
- Implement a hand-written lexer for arithmetic expressions
- Handle: numbers, identifiers, `+`, `-`, `*`, `/`, `(`, `)`
- Test with malformed input (unterminated strings, invalid characters)

**Success Criteria:**
- Lexer can tokenize valid input
- Lexer reports meaningful errors for invalid input
- Can explain why lexing ≠ parsing

---

### **Week 4: Lexing — Hand-Written vs. Generated**
**Theme:** Building and understanding lexers deeply

**Topics:**
- [[02-lexing/hand-written-lexer]]
- Explore tools: Flex, Ragel, or similar (reading only)

**Key Questions:**
- When should you hand-write a lexer vs. generate one?
- What patterns are hard to express in regex?
- How do maximal munch and lookahead work?

**Deliverables:**
- Extend lexer to handle strings, comments, whitespace
- Document lexer state machine (draw it)
- Compare hand-written code to generated code (conceptually)

**Implementation:**
- Add keywords (`if`, `while`, `return`)
- Handle line/column tracking for error messages
- Write tests for edge cases

**Success Criteria:**
- Lexer is robust to real-world input
- Error messages include source location
- Can describe how lexer state machines work

---

### **Week 5: Parsing — From Tokens to Trees**
**Theme:** Building structure from flat sequences

**Topics:**
- [[03-parsing/recursive-descent]]
- [[03-parsing/precedence-and-associativity]]
- [[03-parsing/trees-vs-structure]]

**Key Questions:**
- Why does operator precedence need to be encoded in grammar?
- How does recursive descent work?
- What's the difference between parse trees and ASTs?

**Deliverables:**
- Write a recursive descent parser for expressions
- Handle precedence: `*` > `+`, left associativity
- Create AST nodes (not just parse trees)

**Implementation:**
- Parser consumes tokens from Week 3's lexer
- Build: `Expr`, `BinOp`, `Number`, `Ident` AST nodes
- Test: `3 + 4 * 5` → `Add(3, Mul(4, 5))`

**Success Criteria:**
- Parser correctly handles precedence
- AST is simpler than parse tree (no redundant nodes)
- Can explain why `3 + 4 * 5` ≠ `(3 + 4) * 5`

---

### **Week 6: Parsing — Ambiguity and Grammar Design**
**Theme:** Why grammars are hard and how to tame them

**Topics:**
- [[03-parsing/ambiguity]]
- Explore LL vs. LR (reading only—no need to implement)

**Key Questions:**
- What makes a grammar ambiguous?
- How do you refactor grammars to remove ambiguity?
- When do you need a parser generator vs. hand-written code?

**Deliverables:**
- Add statements to grammar: `if`, `while`, `assignment`
- Handle block structure: `{ ... }`
- Document grammar in EBNF or similar notation

**Implementation:**
- Extend parser to handle statements and blocks
- Ensure `if-else` binds correctly (dangling else problem)
- Build full AST for simple programs

**Success Criteria:**
- Parser handles control flow constructs
- Grammar is unambiguous and documented
- Can parse a multi-line program

---

### **Week 7: Semantics — Enforcing Meaning**
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

**Implementation:**
- Walk AST and build symbol table
- Check: variable declared before use
- Check: types match in expressions (e.g., no `int + string`)
- Handle shadowing in nested scopes

**Success Criteria:**
- Semantic errors are caught and reported
- Valid programs pass without errors
- Can explain difference between syntax and semantic errors

---

### **Week 8: Intermediate Representation — The Working Form**
**Theme:** Lowering AST to a form suitable for optimization

**Topics:**
- [[05-ir/why-ast-is-not-enough]]
- [[05-ir/three-address-code]]
- [[05-ir/cfg]]

**Key Questions:**
- Why can't we optimize the AST directly?
- What makes IR easier to transform?
- How do you represent control flow?

**Deliverables:**
- Translate AST to three-address code (TAC)
- Build control-flow graph (CFG) from TAC
- Visualize CFG (draw it)

**Implementation:**
- Lower expressions: `a + b * c` → `t1 = b * c; t2 = a + t1`
- Lower control flow: `if`, `while` → labeled blocks + jumps
- Generate unique temporary names

**Success Criteria:**
- Every expression is atomic (at most three operands)
- Control flow is explicit (gotos, labels)
- CFG shows all execution paths

---

### **Week 9: Intermediate Representation — SSA and Data Flow**
**Theme:** Making data dependencies explicit

**Topics:**
- [[05-ir/ssa-intuition]]
- [[06-optimization/data-flow]]

**Key Questions:**
- Why SSA (Static Single Assignment)?
- What are phi nodes and when do you need them?
- How does SSA enable optimization?

**Deliverables:**
- Convert TAC to SSA form
- Understand where phi nodes appear
- Document data flow patterns

**Implementation:**
- Transform TAC → SSA (simple cases)
- Handle variable merging at control flow join points
- Read about SSA construction algorithms (don't implement yet)

**Success Criteria:**
- Can identify where phi nodes are needed
- Understand why SSA makes dead code obvious
- Recognize data flow in CFG

---

### **Week 10: Optimization — Making Code Better**
**Theme:** Transformations that preserve meaning

**Topics:**
- [[06-optimization/constant-folding]]
- [[06-optimization/dead-code]]
- [[06-optimization/local-vs-global]]

**Key Questions:**
- What optimizations are always safe?
- How do you prove an optimization is correct?
- What's the difference between local and global optimization?

**Deliverables:**
- Implement constant folding
- Implement dead code elimination
- Measure impact (count IR instructions before/after)

**Implementation:**
- Fold: `3 + 4` → `7`
- Eliminate: unused temporaries
- Test on real examples

**Success Criteria:**
- Optimized IR is smaller and faster
- Semantics are preserved (test with execution)
- Can explain why each optimization is safe

---

### **Week 11: Code Generation — Targeting Real Machines**
**Theme:** From IR to executable code

**Topics:**
- [[07-codegen/instruction-selection]]
- [[07-codegen/registers-are-scarce]]
- [[07-codegen/stack-machines]]

**Key Questions:**
- How do IR operations map to machine instructions?
- What happens when you run out of registers?
- Why are stack machines simpler?

**Deliverables:**
- Generate bytecode for a stack machine
- Document instruction set
- Run programs on a VM

**Implementation:**
- Define simple bytecode: `PUSH`, `ADD`, `STORE`, etc.
- Translate IR → bytecode
- Write interpreter for bytecode

**Success Criteria:**
- Programs execute and produce correct results
- Can explain stack vs. register machines
- Bytecode is readable and compact

---

### **Week 12: Code Generation — Calling Conventions**
**Theme:** How functions work at the machine level

**Topics:**
- [[07-codegen/calling-conventions]]
- Function prologues and epilogues
- Stack frames

**Key Questions:**
- How are arguments passed?
- Where does the return address go?
- How do stack frames work?

**Deliverables:**
- Add function calls to IR and codegen
- Implement simple calling convention
- Test recursive functions

**Implementation:**
- Generate code for function entry/exit
- Handle arguments and return values
- Ensure stack is balanced

**Success Criteria:**
- Functions can call other functions
- Recursion works correctly
- Can draw stack layout for nested calls

---

### **Week 13-14: Integration — Building a Complete Compiler**
**Theme:** Connect all phases end-to-end

**Goals:**
- Combine lexer, parser, semantics, IR, optimization, codegen
- Compile source programs to bytecode and execute
- Handle errors gracefully at every stage

**Deliverables:**
- A working compiler for a small language
- Test suite covering all features
- Documentation of design choices

**Success Criteria:**
- End-to-end: source → bytecode → execution
- Errors are caught and reported meaningfully
- You can explain every phase's role

---

### **Week 15-16: Reflection and Extension**
**Theme:** Consolidate understanding and explore advanced topics

**Activities:**
- Revisit zettels and strengthen connections
- Implement missing features (arrays, structs, etc.)
- Explore advanced topics:
  - Garbage collection
  - Type inference
  - Register allocation algorithms
  - JIT compilation

**Deliverables:**
- Complete zettel network
- Personal compiler design philosophy document
- Identify areas for future deep dives

**Success Criteria:**
- Compiler knowledge graph is navigable and coherent
- Can design a compiler for a new language from scratch
- Have specific questions for further study

---

## Flexibility and Adaptation

This roadmap assumes:
- ~60 minutes of focused study per day, 5-6 days per week
- Some days will go faster, some slower
- Implementation is encouraged but not required every week
- You'll create zettels as insights emerge, not on schedule

**Adjust the pace based on:**
- How quickly concepts click
- How deep you want to go on implementation
- What questions arise that demand tangents

**The goal is understanding, not completion.**

---

## Success Metrics

By the end of 16 weeks, you should be able to:

1. **Explain** every compiler phase without notes
2. **Build** a simple compiler from scratch
3. **Debug** compiler bugs by knowing which phase is responsible
4. **Read** compiler papers and understand their claims
5. **Design** optimizations and prove them correct
6. **Navigate** this knowledge graph fluently

If you can do these things, the roadmap served its purpose.

If you can't yet, extend the timeline—there's no deadline.

---

## Next Steps

- [ ] Review this roadmap
- [ ] Adjust based on your goals and constraints
- [ ] Start Week 1
- [ ] Create weekly notes as you go
- [ ] Update this roadmap when you discover better paths

This is a living document. Improve it as you learn.
