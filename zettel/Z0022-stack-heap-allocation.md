# Z0022: Stack and Heap Allocation

## Links
- Up: [[Z0003-representation]]
- Related: [[Z0001-state]] [[Z0004-invariants]] [[Z0005-compiler-phases]]

## Core Concept

**The program doesn't decide how much stack to allocate — the OS and linker do. The program requests heap memory dynamically at runtime.**

This is a fundamental asymmetry in memory management:
- **Stack**: Fixed size, pre-allocated by OS, managed automatically
- **Heap**: Variable size, grows on demand via OS calls, managed explicitly

## Stack Allocation: Decided Before Runtime

### Who Decides Stack Size?

1. **Linker (link time)**: Embeds default stack size in executable header
   - PE header (Windows): typically 1 MB
   - ELF (Linux): typically 8 MB (configurable via `ulimit -s`)

2. **OS (load time)**: Reads executable header and allocates stack region
   - Sets stack pointer register (ESP/RSP on x86-64)
   - Gives program a fixed-size contiguous region

3. **Program (runtime)**: Uses the stack, cannot resize it
   - Stack overflow if limit exceeded
   - No dynamic growth in most systems

### Why Fixed Size?

Stack allocation must be **fast and predictable**:
- Function calls happen constantly
- Allocation is just moving a pointer (sub RSP, imm)
- Deallocation is automatic (add RSP, imm on return)
- No OS involvement per allocation

**Chess Engine Analogy**: Like an opening book — fixed size, pre-loaded, optimized for speed. You don't expand it during the game.

## Heap Allocation: Decided During Runtime

### How Heap Grows

1. **Initial state**: OS may give small initial heap (or none)

2. **Dynamic requests**: Program calls `malloc()`, which:
   - First checks existing free memory (free list management)
   - If insufficient, requests more from OS via:
     - `brk()`/`sbrk()`: Extends data segment (small allocations)
     - `mmap()`: Maps new memory regions (large allocations, >128 KB typically)

3. **Unbounded growth**: Limited only by virtual address space

### Memory Allocator Responsibilities

The runtime allocator (libc's malloc) must:
- Track free blocks (free lists, bins, arenas)
- Coalesce adjacent free blocks (reduce fragmentation)
- Request more memory from OS when needed
- Return memory to OS when possible (but often doesn't)

**Chess Engine Analogy**: Like a transposition table — you allocate what you need at startup, can grow it dynamically, and manage it yourself.

## The Classic Mental Model

Traditionally taught as "stack grows down, heap grows up":

```
High addresses (0xFFFFFFFF on 32-bit)
┌─────────────────┐
│  Kernel Space   │
├─────────────────┤
│     Stack       │ ← starts high, grows DOWN
│        ↓         │
│                 │
│   (unmapped)    │
│                 │
│        ↑         │
│      Heap       │ ← starts low, grows UP
├─────────────────┤
│   BSS (uninit)  │
├─────────────────┤
│   Data (init)   │
├─────────────────┤
│   Text (code)   │
└─────────────────┘
Low addresses (0x08048000)
```

**This model is pedagogically useful** because it explains:
- Why unlimited recursion crashes (stack hits limit)
- Why stack allocation is fast (just pointer arithmetic)
- Why heap can fragment (grows from opposite direction)
- Why memory exhaustion happens (they "meet in the middle")

## The Modern Reality

### 1. Address Space is Massive (64-bit)

User space: `0x0000_0000_0000_0000` to `0x0000_7FFF_FFFF_FFFF` ≈ **128 TB**

Stack and heap are **nowhere near each other**:
- Stack: ~`0x7FFF_FFFF_F000` (near top)
- Heap: ~`0x0000_5555_5800_0000` (after text/data)
- Gap: **~120 TB** of unmapped space

They will **never collide** on modern systems.

### 2. ASLR Randomizes Layout

Address Space Layout Randomization means starting addresses **change every run**:

```
$ ./program
Stack: 0x7ffd_a2b3_c000

$ ./program
Stack: 0x7ffe_1f8a_b000  # Different address!
```

**Why?** Security — makes buffer overflow exploits harder.

### 3. Modern Heap is Complex

Not a simple "grows upward" region anymore:
- **Small allocations**: `brk()` extends data segment (contiguous)
- **Large allocations**: `mmap()` creates **separate regions** anywhere
- **Thread arenas**: Multiple heaps for multi-threaded programs
- **Memory-mapped files**: Can appear anywhere in address space

Real process memory map (Linux x86-64):
```
0x5555_5555_4000  text (executable code)
0x5555_5555_6000  data (initialized globals)
0x5555_5555_7000  heap (via brk, grows up)
...
0x7f8a_b000_0000  mmap'd region (large malloc)
0x7f8a_c000_0000  shared library (.so file)
0x7f8a_d000_0000  another mmap'd region
...
0x7ffd_a2b3_c000  stack (grows down)
```

### 4. Platform Differences

**Linux/Unix** (traditional model):
```
0x7FFF_FFFF_FFFF  ← Stack (high)
      ...
0x0000_5555_5000  ← Heap (low)
```

**Windows** (inverted!):
```
0x7FFF_FFFF_FFFF  ← Text/Data (high!)
      ...
0x0001_D000_0000  ← Heap (middle)
      ...
0x0000_B000_0000  ← Stack (low!)
```

Empirical evidence from `memory-layout.c` on Windows:
```
Text (code):   0x00007FF6_6B52_1000  ← Highest
Data (global): 0x00007FF6_6B54_1000
Heap:          0x00001D15_BFFC_8EE0  ← Middle
Stack:         0x0000B31E_55F9_10    ← Lowest
```

## Code Example

```c
#include <stdio.h>
#include <stdlib.h>

int global = 42;  // Data section (fixed by linker)

void recurse(int n) {
    int local[1000];  // Stack allocation (automatic)
    if (n > 0) recurse(n - 1);
}  // Stack automatically freed on return

int main() {
    // Stack allocation - size known at compile time
    int stack_var;
    // Compiler generates: sub rsp, 4

    // Heap allocation - size determined at runtime
    int* heap_var = malloc(sizeof(int) * 1000);
    // malloc() may call brk() to request more memory from OS

    free(heap_var);  // Must manually free
    // Stack_var automatically freed when main() returns

    return 0;
}
```

## Compiler's Role

### At Compile Time

1. **Stack frame layout**: Compiler computes size of local variables
   - Knows exact stack space needed per function
   - Generates prologue/epilogue (adjust stack pointer)

2. **Stack usage**: Can estimate total stack depth (static analysis)
   - Warns about large stack frames
   - Can detect some infinite recursion cases

3. **Heap calls**: Generates calls to `malloc()`/`free()`
   - Does NOT manage heap itself (that's the runtime library)

### At Link Time

1. **Linker embeds stack size** in executable header
   - Default or user-specified (`-Wl,--stack,<size>`)

2. **Reserves address space** for data/BSS sections
   - Heap starts after BSS

### At Runtime

1. **OS loader**:
   - Allocates stack based on executable header
   - Sets up initial heap region (or defers to first malloc)
   - Applies ASLR (randomizes base addresses)

2. **Runtime library** (`libc`):
   - Implements `malloc()`/`free()`
   - Manages heap growth via system calls
   - Handles thread-local arenas

## Why the Asymmetry?

| Aspect | Stack | Heap | Reason |
|--------|-------|------|--------|
| **Size** | Fixed | Dynamic | Stack must be fast; heap must be flexible |
| **Allocation** | Automatic | Explicit | Functions need local storage without code |
| **Speed** | O(1) pointer bump | O(log n) or worse | Stack is just arithmetic; heap searches free lists |
| **Lifetime** | Scope-bound | Manual | Stack frames = function calls; heap persists |
| **Fragmentation** | None | Common | Stack grows/shrinks contiguously; heap has mixed lifetimes |
| **Overflow** | Immediate crash | Graceful failure | Stack is fixed; heap can request more |

## Stack Overflow vs Out of Memory

**Stack overflow**:
```c
void infinite() {
    int big[1000000];  // Huge stack frame
    infinite();        // Infinite recursion
}  // Crashes when stack limit exceeded
```

**Heap exhaustion**:
```c
while (1) {
    malloc(1000000);  // Eventually malloc returns NULL
}  // Doesn't crash immediately - malloc just fails
```

**Key difference**: Stack overflow is a **hard limit** (process killed). Heap exhaustion is a **soft failure** (allocation returns NULL, program can handle it).

## Invariants

1. **Stack allocation is compiler-controlled**: Size computed at compile time
2. **Heap allocation is runtime-controlled**: Size requested at runtime
3. **Stack cannot grow**: Fixed by OS at program start
4. **Heap can grow**: Requests more from OS via syscalls
5. **Stack is automatic**: No manual memory management
6. **Heap is manual**: Must explicitly free (in C/C++)

## Connection to Compiler Phases

- **Parsing/Semantics**: Tracks local variable declarations
- **IR Generation**: Computes stack frame size, emits malloc calls
- **Optimization**: Can promote heap allocations to stack (escape analysis)
- **Code Generation**: Emits stack pointer adjustments, calling conventions

## Practical Implications

### For Language Design

**Stack-based languages** (C, Rust):
- Fast function calls
- But: risk of stack overflow, no closures over locals (without escape analysis)

**Heap-based languages** (Python, JavaScript):
- All objects on heap
- Slower allocation, but GC handles lifetime

**Hybrid** (Go, modern C++):
- Compiler decides stack vs heap via escape analysis
- Best of both worlds (when analysis succeeds)

### For Optimization

**Escape analysis**: Promotes heap → stack
```c
// Original: heap allocation
int* f() {
    int* p = malloc(sizeof(int));
    *p = 42;
    return p;  // Escapes! Must be heap
}

// Optimizable: doesn't escape
void g() {
    int* p = malloc(sizeof(int));
    *p = 42;
    use(*p);
    free(p);  // Compiler can move to stack!
}

// After optimization:
void g() {
    int p = 42;  // Stack allocation!
    use(p);
}
```

### For Debugging

**Stack traces** work because:
- Stack frames are contiguous
- Return addresses stored on stack
- Unwinding is just following frame pointers

**Heap debugging** (valgrind, asan) must:
- Track every allocation/free
- Detect use-after-free, double-free
- Much more complex than stack checking

## Measuring It Yourself

```c
// Compile and run to see actual addresses:
#include <stdio.h>
#include <stdlib.h>

int global = 42;

int main() {
    int stack_var;
    int* heap_var = malloc(sizeof(int));

    printf("Text:  %p\n", (void*)main);
    printf("Data:  %p\n", (void*)&global);
    printf("Heap:  %p\n", (void*)heap_var);
    printf("Stack: %p\n", (void*)&stack_var);

    free(heap_var);
    return 0;
}
```

Run it multiple times — you'll see ASLR randomize heap/stack!

## Summary

**The classic model** ("stack grows down, heap grows up") is:
- ✅ Pedagogically useful
- ✅ Explains why stack is fast
- ✅ Explains why heap fragments
- ❌ Not literally true on modern 64-bit systems
- ❌ Oversimplifies ASLR, mmap, thread arenas
- ❌ Platform-specific (Windows inverts it!)

**The key insight**: Stack allocation is a **compile-time decision** (fixed size); heap allocation is a **runtime decision** (dynamic growth). This asymmetry drives everything about how they're managed.

## Further Reading

- [[Z0001-state]] — Why state must live somewhere (stack or heap)
- [[Z0003-representation]] — Memory as a representation choice
- [[Z0004-invariants]] — Stack frame invariants
- [[Z0005-compiler-phases]] — Where stack/heap decisions happen

---

**Created**: 2026-02-14
**Source**: Discussion of memory layout, empirical testing with `memory-layout.c`, ASLR demonstration
