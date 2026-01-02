# Day 2 (60 minutes): From Text to Structure

## Links

- Up: [[01-foundations/README]]
- Related:
  - [[01-foundations/day-01-what-is-a-compiler]]
  - [[01-foundations/ambiguity-and-phases]]
  - [[02-lexing/tokens-vs-characters]]
  - [[03-parsing/trees-vs-structure]]
  - [[zettel/Z0003-representation]]
- Down: [[01-foundations/day-03-structure-to-meaning]]

## Goal

Build a concrete mental model of the first two phases of every compiler: **lexing** and **parsing**.
By the end, you should be able to describe the inputs, outputs, and failure modes of each phase.

## The boundary between lexing and parsing

- **Lexing** is about *chunks*: it turns characters into **tokens**.
- **Parsing** is about *shape*: it turns tokens into **structure** (a parse tree / AST).

Lexing does not decide meaning. Parsing does not read characters.
They exist as separate phases because each has different rules, tools, and failure modes.

## What each phase consumes and produces

### Lexing

- **Input:** source text (characters)
- **Output:** a token stream (plus source locations)
- **Typical errors:** unknown character, malformed number/string, unterminated string/comment

### Parsing

- **Input:** token stream
- **Output:** a tree (parse tree or AST)
- **Typical errors:** unexpected token, missing delimiter, ambiguous or unsupported syntax

## Worked example (same program, different representations)

Source:

```txt
x = 3 + 4 * 5
```

### Tokens (lexing output)

Each token carries its type, value, and source location (line/column) for error reporting:

```txt
Token { type: IDENT, value: "x",  line: 1, col: 0 }
Token { type: EQUALS, value: "=", line: 1, col: 2 }
Token { type: INT, value: 3,      line: 1, col: 4 }
Token { type: PLUS, value: "+",   line: 1, col: 6 }
Token { type: INT, value: 4,      line: 1, col: 8 }
Token { type: STAR, value: "*",   line: 1, col: 10 }
Token { type: INT, value: 5,      line: 1, col: 12 }
```

Simplified notation (locations omitted):

```txt
IDENT(x)  EQUALS  INT(3)  PLUS  INT(4)  STAR  INT(5)
```

Whitespace mostly disappears; meaning is not assigned yet.

**Why source locations matter:** These locations must be threaded through *every* compiler phase:

- Parser copies them to AST nodes
- Semantic analyzer uses them for error messages ("undefined variable 'x' at line 10, col 5")
- IR translation preserves them for debugger support
- Code generation emits debug metadata linking machine code back to source

Without location tracking, all errors would just say "syntax error" with no context.

### Structure (parsing output)

Parsing makes operator binding explicit:

```txt
Assign(
  name = "x",
  value = Add(Int(3), Mul(Int(4), Int(5)))
)
```

This tree encodes precedence: `*` binds tighter than `+`.

## Key fact: structure is a form of disambiguation

The source text is compact but ambiguous.
The tree is larger but unambiguous.

That is the general pattern of compilers: each phase trades surface simplicity for precision.

## What comes next (preview)

Once structure exists, the compiler can start enforcing meaning:

- resolve names (`x` refers to a declaration)
- enforce constraints (types, arity, lvalues, etc.)
- decide a representation suitable for optimization and code generation

Next note: [[02-lexing/tokens-vs-characters]]
