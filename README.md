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