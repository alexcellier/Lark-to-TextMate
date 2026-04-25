# Syntaxes Generator

A Python tool that automatically generates VS Code extensions for syntax highlighting and TextMate grammars.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python generator.py --lark-file path/to/grammar.lark
```

This will generate a VS Code extension in a subfolder named `{grammar}-syntax`, containing the extension files and TextMate grammar.

## Features

- Generates complete VS Code extensions
- Supports syntax highlighting
- Includes TextMate grammars

## Examples

Sample LARK grammar files are available in the [examples/](examples/) directory, organized by complexity:

- **[Simple](examples/simple/)** - Basic arithmetic expression grammar (learning)
- **[Advanced](examples/advanced/)** - SystemRDL register definition language (production-grade)
- **[Test](examples/test/)** - Invalid syntax for error handling validation

See [examples/README.md](examples/README.md) for detailed documentation on each example and how to use them.