# Day 3 (60 minutes): From Structure to Meaning

## Links

- Up: [[01-foundations/README]]
- Related:
  - [[01-foundations/day-02-from-text-to-structure]]
  - [[01-foundations/ambiguity-and-phases]]
  - [[04-semantics/scope]]
  - [[04-semantics/symbol-tables]]
  - [[04-semantics/types-as-constraints]]
  - [[zettel/Z0004-invariants]]
- Down: [[04-semantics/scope]]

## Goal

Understand how **semantic analysis** assigns meaning to syntactically valid structures.
By the end, you should recognize that valid syntax does not imply correct meaning, and know what questions semantic analysis must answer.

## The gap between structure and meaning

After parsing, you have a tree that represents **what was written**, not **what it means**.

Example:

```txt
x = y + 1
```

The parser produces:

```txt
Assign(
  name = "x",
  value = Add(Ident("y"), Int(1))
)
```

But critical questions remain unanswered:

- Does `x` exist? Was it declared?
- What about `y`? Where was it defined?
- Can you add `y` (whatever it is) to `1`?
- Is `x` allowed to be assigned to? (Is it a constant? A function name?)

**Syntax is about shape. Semantics is about validity.**

## What semantic analysis enforces

Semantic analysis answers three classes of questions:

### 1. Name resolution

- Does every identifier refer to something that was declared?
- Is that declaration visible from this location (scope rules)?
- Is the same name declared multiple times in conflicting ways?

### 2. Type checking

- Do operations receive arguments of compatible types?
- Does each expression produce a value of the expected type?
- Are implicit conversions allowed or forbidden?

### 3. Contextual constraints

- Is this identifier being used in the correct position? (lvalue vs rvalue)
- Are control flow constructs used legally? (e.g., `break` only inside loops)
- Do functions have the right number and types of arguments?

## Worked example: finding semantic errors

Consider this snippet:

```txt
const PI = 3.14
x = PI + "hello"
PI = 2.71
```

**Syntax:** Valid. The parser accepts it.

**Semantics:** Invalid. Semantic analysis rejects it because:

1. Line 2: Cannot add a number to a string (type error)
2. Line 3: Cannot reassign a constant (constraint violation)

The tree is well-formed, but the *meaning* violates the language's rules.

## Two fundamental tools

### Symbol tables

A symbol table tracks declarations and their properties:

```txt
name   | type   | kind      | scope
-------|--------|-----------|-------
PI     | float  | constant  | global
x      | ?      | variable  | global
```

During semantic analysis, every identifier is looked up. If it's missing or misused, the compiler reports an error.

### Type environments

A type environment assigns types to expressions by recursive traversal:

```txt
Type(Int(3)) = int
Type(Ident("PI")) = float  (from symbol table)
Type(Add(Int(3), Ident("PI"))) = float  (promotion rule)
```

If the rules cannot produce a valid type, the expression is ill-typed.

## Key insight: meaning is checked, not discovered

The compiler enforces the language's rules. It does not guess what the programmer meant.

If the rules say "you cannot add strings and numbers," the compiler rejects that code—even if a human might understand the intent.

**This is not a bug. This is the feature.**

## Why semantic analysis comes after parsing

Parsing builds structure without understanding context.  
Semantic analysis requires structure to exist first, because:

- Scope depends on nesting (blocks, functions, etc.)
- Type checking depends on expression shape (operators, arguments)
- Name resolution depends on declaration order and visibility

You cannot resolve names while simultaneously building the tree.

## Common semantic errors (preview)

These are the errors you'll see most often:

- **Undefined variable:** `x` was never declared
- **Redeclaration:** `x` declared twice in the same scope
- **Type mismatch:** Expression has type `int`, expected `string`
- **Immutable assignment:** Cannot assign to a constant or function name
- **Arity error:** Function called with wrong number of arguments
- **Break outside loop:** `break` used where it has no meaning

Each of these is *legal syntax* but *illegal semantics*.

## What comes next (preview)

Once the program passes semantic analysis, it is **well-formed**:

- All names are resolved
- All types are known
- All constraints are satisfied

At this point, the compiler can translate the tree into an intermediate representation (IR) suitable for optimization and code generation.

The next phase is no longer about validation—it's about transformation.

Next note: [[04-semantics/scope]]

## Success criteria for Day 3

- You can describe the difference between syntactic and semantic errors.
- You can list three things semantic analysis checks.
- You understand that a valid parse tree is not the same as a valid program.
