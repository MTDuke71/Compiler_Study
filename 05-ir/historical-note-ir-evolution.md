# Historical Note: When Did IR Become Explicit?

## Links
- Up: [[05-ir/README]]
- Related: [[zettel/Z0003-representation]] [[Stanford/lecture-01-introduction]]

---

## The Evolution of IR in Compiler Theory

### FORTRAN I (1957): Implicit IR

FORTRAN I's famous **five phases** didn't include IR as an explicit phase:
1. Lexical Analysis
2. Parsing
3. Semantic Analysis
4. Optimization
5. Code Generation

The internal representation existed but wasn't formalized as a separate concern:
- Semantic analysis produced some internal form
- Optimization operated on that form
- Code generation consumed it directly

The representation was implicit—embedded within the optimization and codegen phases.

---

## Timeline of IR Formalization

### 1960s-1970s: IR Emerges as Distinct Concept

**Why the change?**
- Compilers grew more complex
- Multiple passes required stable intermediate forms
- Optimization theory demanded analyzable representations
- Need for separation between frontend and backend

**Key developments:**
- Recognition that AST alone wasn't sufficient for optimization
- Need for explicit control flow representation
- Multiple target architectures demanded retargetability

### 1970s: Formalization in Textbooks

**Aho & Ullman's "Principles of Compiler Design" (1977)** - the "Dragon Book"
- Explicitly discussed intermediate representations
- Introduced **Three-Address Code (TAC)** as standard pedagogical IR
- Separated IR generation as conceptual phase

**Modern phase structure emerged:**
1. Lexical Analysis
2. Parsing (→ AST)
3. Semantic Analysis
4. **IR Generation** ← Became explicit!
5. Optimization (on IR)
6. Code Generation

### 1980s: Advanced IR Concepts

**Control Flow Graphs (CFG):**
- Formalized as explicit IR structure
- Enabled systematic data flow analysis
- Foundation for modern optimization

**Research focus:**
- IR as subject of study, not just implementation detail
- Multiple IR levels (high, mid, low)
- IR design as tradeoff space

### 1989: SSA Revolution

**Static Single Assignment (SSA)** - Cytron et al.
- Fundamentally changed how we think about IR
- Made data flow explicit in the representation
- Enabled simpler, more powerful optimizations

**Impact:**
- SSA became dominant IR form in production compilers
- Influenced GCC (GIMPLE), LLVM, JVM (eventually)
- Showed IR design directly impacts optimization capability

### 2000s: IR as First-Class Abstraction

**LLVM (started 2000):**
- Made IR a **portable, retargetable** abstraction
- IR became interchange format between tools
- Multiple frontends → one IR → multiple backends
- IR documented, versioned, and stable

**Modern understanding:**
- IR is not just internal detail—it's an **interface**
- Good IR enables optimization
- Poor IR limits what's possible
- IR design is a core compiler design decision

---

## Why the Evolution Happened

### Early Compilers (FORTRAN I era)

**Characteristics:**
- Fewer optimizations (optimization was novel!)
- Simpler languages
- Single target architecture
- Small teams, short timelines

**Implicit IR was sufficient:**
- Not much analysis needed
- Limited optimization passes
- Tightly coupled frontend/backend worked

### Modern Compilers Need Explicit IR

**Multiple optimization passes:**
- Need stable representation between passes
- Passes must not interfere with each other
- Analysis results must be queryable

**Retargetability:**
- Same IR, different backends
- Frontend/backend independence
- Easier to add new targets

**Systematic analysis:**
- CFG enables control flow analysis
- SSA enables data flow analysis
- Explicit structure enables formal reasoning

**Separation of concerns:**
- Frontend knows language semantics
- IR captures computation abstractly
- Backend knows target architecture
- Each can evolve independently

---

## Chess Engine Analogy

**FORTRAN I approach:**
- Like storing a chess position as a FEN string
- Representation exists, but not optimized for analysis
- Have to parse it every time you need information

**Modern IR approach:**
- Like using bitboards for chess positions
- Representation designed for the operations you'll perform
- Piece locations, attacks, moves all efficiently computed
- Multiple representations (bitboards, mailbox, zobrist) for different needs

Just as chess engines discovered better board representations enabled better search, compilers discovered better IR enabled better optimization.

---

## Key Insight

**FORTRAN I proved optimization was valuable.**

**The next 30 years figured out how to do it systematically, which required formalizing IR.**

The evolution from implicit to explicit IR mirrors the maturation of compiler theory from **craft** to **engineering discipline**.

---

## Modern Perspective

Today, IR is understood as:
- **Not optional** - every compiler has IR, even if implicit
- **Design choice** - IR design determines what optimizations are easy/hard
- **Interface boundary** - separates concerns, enables modularity
- **Research area** - ongoing work on better IRs (e.g., MLIR for ML compilers)

**The question isn't "do we need IR?"**

**The question is "which IR best serves our goals?"**

---

## Further Reading

- Aho, Lam, Sethi, Ullman: "Compilers: Principles, Techniques, and Tools" (2007) - Modern Dragon Book
- Cytron et al.: "Efficiently Computing Static Single Assignment Form" (1991) - SSA paper
- LLVM Language Reference - Modern IR documentation
- Cooper & Torczon: "Engineering a Compiler" (2011) - IR design tradeoffs

---

## Connection to Repository

- [[why-ast-is-not-enough]] - Why FORTRAN I's implicit approach had limits
- [[three-address-code]] - The IR that emerged in the 1970s
- [[ssa-intuition]] - The 1989 innovation that changed everything
- [[cfg]] - Explicit control flow representation
- [[zettel/Z0003-representation]] - Representation as a fundamental concept
