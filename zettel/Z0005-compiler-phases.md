## Links
- Up: [[zettel/README]]
- Related: [[01-foundations/day-01-what-is-a-compiler]] [[zettel/Z0001-state]]
- Down: [[zettel/Z0001-state]]

# Z0005: Compiler phases exist to remove ambiguity

A compiler transforms text into behavior while preserving meaning.
Each phase exists because the next phase needs a more precise input.

- Lexing defines tokens.
- Parsing defines structure.
- Semantics defines meaning and legality.
- IR defines a stable form for analysis.
- Optimization improves performance without changing meaning.
- Codegen targets the machine.

The pipeline is not optional; it is the minimum sequence that makes execution possible.
