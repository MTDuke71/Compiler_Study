# Lox Language Specification

## Links
- Up: [[lox-rs/STUDY-PLAN]]
- Source: *Crafting Interpreters* by Robert Nystrom (Ch 3, 4, 7-13, Appendix I)
- Related: [[00-index/invariants]]

## Purpose

A numbered specification extracted from *Crafting Interpreters* for **traceability** between spec items and the lox-rs implementation. Each item has a unique ID that maps to source code and tests.

---

## Traceability Key

| Column | Meaning |
|--------|---------|
| **ID** | Unique spec identifier |
| **Rule** | What the language must do |
| **Source** | Crafting Interpreters chapter/section |
| **Impl** | Source file and line(s) in lox-rs |
| **Test** | Test function(s) covering this rule |

Impl and Test columns are filled in as implementation proceeds. Mark with:
- (done) — implemented and tested
- (stub) — AST/parser done, interpreter TODO
- (todo) — not yet started

---

## LOX-LEX: Lexical Rules

*Source: CI Chapter 4 (Scanning), Appendix I (Lexical Grammar)*

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-LEX-001 | Single-character tokens: `(` `)` `{` `}` `,` `.` `-` `+` `;` `*` | | |
| LOX-LEX-002 | One-or-two-character tokens: `!` `!=` `=` `==` `<` `<=` `>` `>=` | | |
| LOX-LEX-003 | Slash `/` is a token; `//` begins a comment to end of line | | |
| LOX-LEX-004 | Whitespace (space, `\r`, `\t`) is ignored; newlines increment line counter | | |
| LOX-LEX-005 | String literals are delimited by double quotes `"..."` | | |
| LOX-LEX-006 | Strings may span multiple lines; newlines inside strings increment line counter | | |
| LOX-LEX-007 | No escape sequences are processed in strings | | |
| LOX-LEX-008 | Unterminated string is a scan error | | |
| LOX-LEX-009 | Number literals: one or more digits, optional `.` followed by one or more digits | | |
| LOX-LEX-010 | Leading dot (`.5`) and trailing dot (`5.`) are not valid number literals | | |
| LOX-LEX-011 | Numbers are stored as double-precision floating point | | |
| LOX-LEX-012 | Identifiers start with a letter or `_`, followed by letters, digits, or `_` | | |
| LOX-LEX-013 | Reserved keywords: `and`, `class`, `else`, `false`, `for`, `fun`, `if`, `nil`, `or`, `print`, `return`, `super`, `this`, `true`, `var`, `while` | | |
| LOX-LEX-014 | Keywords are recognized by lookup after scanning an identifier | | |
| LOX-LEX-015 | Maximal munch: the longest matching lexeme wins | | |
| LOX-LEX-016 | Unexpected characters produce an error but scanning continues | | |
| LOX-LEX-017 | Scanner errors set a `had_error` flag; multiple errors may be reported | | |

---

## LOX-SYN: Syntax Rules

*Source: CI Chapters 5-6, 8, Appendix I (Syntax Grammar)*

### Declarations

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SYN-001 | A program is a sequence of declarations followed by EOF | | |
| LOX-SYN-002 | A declaration is a class declaration, function declaration, variable declaration, or statement | | |
| LOX-SYN-003 | Variable declaration: `var` IDENTIFIER (`=` expression)? `;` | | |
| LOX-SYN-004 | Function declaration: `fun` IDENTIFIER `(` parameters? `)` `{` body `}` | | |
| LOX-SYN-005 | Class declaration: `class` IDENTIFIER (`<` IDENTIFIER)? `{` methods `}` | | |
| LOX-SYN-006 | Methods are function declarations without the `fun` keyword | | |

### Statements

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SYN-010 | Expression statement: expression `;` | | |
| LOX-SYN-011 | Print statement: `print` expression `;` | | |
| LOX-SYN-012 | Block: `{` declarations* `}` | | |
| LOX-SYN-013 | If statement: `if` `(` expression `)` statement (`else` statement)? | | |
| LOX-SYN-014 | While statement: `while` `(` expression `)` statement | | |
| LOX-SYN-015 | For statement: `for` `(` (varDecl \| exprStmt \| `;`) expression? `;` expression? `)` statement | | |
| LOX-SYN-016 | Return statement: `return` expression? `;` | | |

### Expressions (by precedence, lowest to highest)

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SYN-020 | Assignment: IDENTIFIER `=` assignment (right-associative) | | |
| LOX-SYN-021 | Logical or: `or` (left-associative) | | |
| LOX-SYN-022 | Logical and: `and` (left-associative) | | |
| LOX-SYN-023 | Equality: `==` `!=` (left-associative) | | |
| LOX-SYN-024 | Comparison: `<` `<=` `>` `>=` (left-associative) | | |
| LOX-SYN-025 | Addition/subtraction: `+` `-` (left-associative) | | |
| LOX-SYN-026 | Multiplication/division: `*` `/` (left-associative) | | |
| LOX-SYN-027 | Unary: `!` `-` (right-associative, prefix) | | |
| LOX-SYN-028 | Call: expression `(` arguments? `)` — may chain | | |
| LOX-SYN-029 | Property access: expression `.` IDENTIFIER | | |
| LOX-SYN-030 | Property set: expression `.` IDENTIFIER `=` expression | | |
| LOX-SYN-031 | `super` `.` IDENTIFIER | | |
| LOX-SYN-032 | `this` | | |
| LOX-SYN-033 | Primary: NUMBER, STRING, `true`, `false`, `nil`, IDENTIFIER, `(` expression `)` | | |
| LOX-SYN-034 | Maximum 255 arguments in a call expression | | |
| LOX-SYN-035 | Maximum 255 parameters in a function declaration | | |

### Error Recovery

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SYN-040 | On parse error, synchronize by discarding tokens to the next statement boundary | | |
| LOX-SYN-041 | Statement boundaries: `;` or keywords `class`, `fun`, `var`, `for`, `if`, `while`, `print`, `return` | | |
| LOX-SYN-042 | Dangling else: `else` binds to the nearest preceding `if` | | |
| LOX-SYN-043 | For loop desugars to a while loop (not a distinct AST node) | | |

---

## LOX-SEM: Semantic Rules

*Source: CI Chapters 7-13*

### Types and Values

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-001 | Lox has four value types: numbers, strings, booleans, nil | | |
| LOX-SEM-002 | Numbers are double-precision IEEE 754 floating point | | |
| LOX-SEM-003 | Strings are sequences of characters (no escape processing) | | |
| LOX-SEM-004 | Booleans are `true` or `false` | | |
| LOX-SEM-005 | `nil` represents the absence of a value | | |

### Truthiness

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-010 | `false` is falsy | | |
| LOX-SEM-011 | `nil` is falsy | | |
| LOX-SEM-012 | All other values are truthy (numbers including 0, non-empty and empty strings) | | |

### Equality

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-015 | `nil == nil` is `true` | | |
| LOX-SEM-016 | `nil == (anything else)` is `false` | | |
| LOX-SEM-017 | Values of different types are never equal (e.g. `1 == "1"` is `false`) | | |
| LOX-SEM-018 | Values of the same type use value equality (numbers by value, strings by contents) | | |
| LOX-SEM-019 | `!=` is the logical negation of `==` | | |
| LOX-SEM-020 | Equality never produces a runtime error regardless of operand types | | |

### Arithmetic Operators

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-025 | Binary `-`, `*`, `/`: both operands must be numbers; result is a number | | |
| LOX-SEM-026 | Binary `+` with two numbers: numeric addition, result is a number | | |
| LOX-SEM-027 | Binary `+` with two strings: concatenation, result is a string | | |
| LOX-SEM-028 | Binary `+` with any other type combination: runtime error | | |
| LOX-SEM-029 | Unary `-`: operand must be a number; result is its negation | | |
| LOX-SEM-030 | Unary `!`: operand may be any type; result is `!isTruthy(operand)` (always a boolean) | | |
| LOX-SEM-031 | Binary operands are evaluated left-to-right | | |

### Comparison Operators

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-035 | `<`, `<=`, `>`, `>=`: both operands must be numbers | | |
| LOX-SEM-036 | Comparison result is a boolean | | |

### Logical Operators

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-040 | `and` evaluates left operand; if falsy, returns it without evaluating right | | |
| LOX-SEM-041 | `and` evaluates right operand if left is truthy; returns right operand's value | | |
| LOX-SEM-042 | `or` evaluates left operand; if truthy, returns it without evaluating right | | |
| LOX-SEM-043 | `or` evaluates right operand if left is falsy; returns right operand's value | | |
| LOX-SEM-044 | Logical operators return the *actual operand value*, not a boolean coercion | | |

### Variables

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-050 | `var` with initializer: evaluates initializer, binds result to name in current scope | | |
| LOX-SEM-051 | `var` without initializer: binds name to `nil` in current scope | | |
| LOX-SEM-052 | Variable access looks up the name in the current environment, then enclosing, recursively | | |
| LOX-SEM-053 | Accessing an undefined variable is a runtime error | | |
| LOX-SEM-054 | Assignment evaluates the value, stores it in the variable's environment; returns the value | | |
| LOX-SEM-055 | Assigning to an undefined variable is a runtime error (assignment does not create variables) | | |
| LOX-SEM-056 | A variable may be redeclared at the same scope level (new binding replaces old) at global scope | | |

### Scoping

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-060 | Entering a block (`{`) creates a new scope (new environment) chained to the enclosing one | | |
| LOX-SEM-061 | Exiting a block (`}`) discards the block's scope | | |
| LOX-SEM-062 | A local variable shadows an outer variable with the same name | | |
| LOX-SEM-063 | The shadowed outer variable is restored when the inner scope exits | | |

### Print

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-065 | `print` evaluates its expression, converts the result to a string, and outputs to stdout | | |
| LOX-SEM-066 | Numbers print without trailing `.0` for integers (CI convention) or as-is for floats | | |
| LOX-SEM-067 | `nil` prints as `"nil"` | | |
| LOX-SEM-068 | Booleans print as `"true"` or `"false"` | | |

### Control Flow

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-070 | `if`: condition is evaluated; if truthy, then-branch executes; otherwise else-branch (if present) | | |
| LOX-SEM-071 | `while`: condition is evaluated before each iteration; body executes while truthy | | |
| LOX-SEM-072 | `for` initializer executes once; condition tested before each iteration; increment runs after each body | | |
| LOX-SEM-073 | `for` with omitted condition loops forever (condition defaults to `true`) | | |
| LOX-SEM-074 | `for` variable declaration is scoped to the loop | | |

### Functions

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-080 | A function declaration creates a function object and binds it to the name in the current scope | | |
| LOX-SEM-081 | Functions are first-class values: can be stored in variables, passed as arguments, returned | | |
| LOX-SEM-082 | Calling a function: evaluate arguments left-to-right, create new environment with params bound to args | | |
| LOX-SEM-083 | Wrong number of arguments is a runtime error: "Expected N arguments but got M." | | |
| LOX-SEM-084 | Calling a non-callable value is a runtime error: "Can only call functions and classes." | | |
| LOX-SEM-085 | `return` with a value: exits the function immediately, returning that value | | |
| LOX-SEM-086 | `return` without a value: returns `nil` | | |
| LOX-SEM-087 | Reaching the end of a function body without `return`: implicitly returns `nil` | | |
| LOX-SEM-088 | A function captures the environment at declaration time (closure) | | |
| LOX-SEM-089 | When called, the closure environment is the parent of the function's local environment | | |
| LOX-SEM-090 | Multiple closures over the same variable share state (mutations visible to each other) | | |
| LOX-SEM-091 | Native function `clock()` takes 0 arguments and returns seconds since epoch as a number | | |

### Classes

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-100 | A class declaration creates a LoxClass and binds it to the name in the current scope | | |
| LOX-SEM-101 | Calling a class (e.g. `Foo()`) creates a new instance of that class and returns it | | |
| LOX-SEM-102 | Properties can be freely added to any instance via set expressions (`obj.field = value`) | | |
| LOX-SEM-103 | Getting a property: check instance fields first, then class methods | | |
| LOX-SEM-104 | Getting an undefined property (not a field and not a method) is a runtime error | | |
| LOX-SEM-105 | Methods are stored on the class, not on individual instances | | |
| LOX-SEM-106 | Accessing a method on an instance returns a bound method with `this` set to that instance | | |
| LOX-SEM-107 | `this` inside a method refers to the instance the method was accessed on | | |
| LOX-SEM-108 | `this` is only valid inside a method body; using it elsewhere is a compile-time error | | |
| LOX-SEM-109 | If a class defines `init()`, it is called automatically on instantiation with forwarded arguments | | |
| LOX-SEM-110 | `init()` always returns `this`, even with an explicit `return` | | |
| LOX-SEM-111 | Returning a non-nil value from `init()` is a compile-time error; bare `return` is allowed | | |
| LOX-SEM-112 | A class prints as its name (e.g. `"Foo"`) | | |
| LOX-SEM-113 | An instance prints as `"ClassName instance"` | | |

### Inheritance

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-120 | A class may inherit from one superclass via `class Sub < Super {}` | | |
| LOX-SEM-121 | The superclass expression must evaluate to a class at runtime; otherwise runtime error | | |
| LOX-SEM-122 | A class cannot inherit from itself (compile-time error) | | |
| LOX-SEM-123 | A subclass inherits all methods from its superclass | | |
| LOX-SEM-124 | Method resolution: check subclass first, then walk up the superclass chain | | |
| LOX-SEM-125 | A subclass method with the same name as a superclass method overrides it | | |
| LOX-SEM-126 | `super.method()` looks up the method starting from the superclass of the *class containing the super expression* | | |
| LOX-SEM-127 | `super` binds `this` to the current instance (same object, different method resolution start) | | |
| LOX-SEM-128 | `super` is only valid inside a method of a class that has a superclass | | |
| LOX-SEM-129 | Using `super` in a class with no superclass is a compile-time error | | |

### Variable Resolution (Static Analysis)

| ID | Rule | Impl | Test |
|----|------|------|------|
| LOX-SEM-140 | A resolver pass runs between parsing and interpretation | | |
| LOX-SEM-141 | Local variables are resolved to a depth (number of enclosing scopes) | | |
| LOX-SEM-142 | Global variables are not resolved; they are looked up dynamically at runtime | | |
| LOX-SEM-143 | Reading a local variable in its own initializer is a compile-time error | | |
| LOX-SEM-144 | Declaring two variables with the same name in the same local scope is a compile-time error | | |
| LOX-SEM-145 | `return` at the top level (outside any function) is a compile-time error | | |

---

## LOX-ERR: Error Conditions Summary

*Cross-references to rules above. Organized by phase.*

### Scan-Time Errors

| ID | Rule | Triggers |
|----|------|----------|
| LOX-ERR-001 | Unterminated string literal | LOX-LEX-008 |
| LOX-ERR-002 | Unexpected character | LOX-LEX-016 |

### Parse-Time Errors

| ID | Rule | Triggers |
|----|------|----------|
| LOX-ERR-010 | Missing `;` after statement | LOX-SYN-010, LOX-SYN-011, LOX-SYN-003 |
| LOX-ERR-011 | Missing `)` after expression or arguments | LOX-SYN-033, LOX-SYN-028 |
| LOX-ERR-012 | Missing `}` after block | LOX-SYN-012 |
| LOX-ERR-013 | Expect expression (unexpected token in primary position) | LOX-SYN-033 |
| LOX-ERR-014 | Invalid assignment target (e.g. `a + b = c`) | LOX-SYN-020 |
| LOX-ERR-015 | More than 255 parameters | LOX-SYN-035 |
| LOX-ERR-016 | More than 255 arguments | LOX-SYN-034 |

### Compile-Time Errors (Resolver)

| ID | Rule | Triggers |
|----|------|----------|
| LOX-ERR-020 | Variable read in its own initializer | LOX-SEM-143 |
| LOX-ERR-021 | Duplicate variable in same local scope | LOX-SEM-144 |
| LOX-ERR-022 | `return` at top level | LOX-SEM-145 |
| LOX-ERR-023 | `this` outside of a class method | LOX-SEM-108 |
| LOX-ERR-024 | Return value from `init()` | LOX-SEM-111 |
| LOX-ERR-025 | `super` outside of a class | LOX-SEM-128 |
| LOX-ERR-026 | `super` in a class with no superclass | LOX-SEM-129 |
| LOX-ERR-027 | A class inheriting from itself | LOX-SEM-122 |

### Runtime Errors

| ID | Rule | Triggers |
|----|------|----------|
| LOX-ERR-030 | Operand must be a number (unary `-`) | LOX-SEM-029 |
| LOX-ERR-031 | Operands must be numbers (binary `-`, `*`, `/`) | LOX-SEM-025 |
| LOX-ERR-032 | Operands must be two numbers or two strings (`+`) | LOX-SEM-028 |
| LOX-ERR-033 | Operands must be numbers (comparison) | LOX-SEM-035 |
| LOX-ERR-034 | Undefined variable | LOX-SEM-053 |
| LOX-ERR-035 | Undefined variable on assignment | LOX-SEM-055 |
| LOX-ERR-036 | Can only call functions and classes | LOX-SEM-084 |
| LOX-ERR-037 | Wrong number of arguments | LOX-SEM-083 |
| LOX-ERR-038 | Undefined property on get | LOX-SEM-104 |
| LOX-ERR-039 | Only instances have properties (get on non-instance) | LOX-SEM-104 |
| LOX-ERR-040 | Only instances have fields (set on non-instance) | LOX-SEM-102 |
| LOX-ERR-041 | Superclass must be a class | LOX-SEM-121 |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 64 | Incorrect usage (wrong number of CLI arguments) |
| 65 | Scan or parse error (data error) |
| 70 | Runtime error |

---

## Counts

| Category | Count |
|----------|-------|
| LOX-LEX (Lexical) | 17 |
| LOX-SYN (Syntax) | 24 |
| LOX-SEM (Semantic) | 52 |
| LOX-ERR (Errors) | 26 |
| **Total** | **119** |

---

## How to Use This Spec

1. **During implementation:** Before coding a feature, find the spec items it must satisfy
2. **Writing tests:** Each LOX-ERR item needs at least one test; each LOX-SEM item needs at least one
3. **Filling the trace:** Update the Impl and Test columns as you go
4. **Reviewing:** If a test fails, trace back to the spec item to understand the expected behavior
5. **Completeness check:** When all Impl/Test columns are filled, lox-rs is complete

This is a living document. Update it as edge cases are discovered.
