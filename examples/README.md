# LARK Examples

This directory contains sample LARK grammar files organized by complexity level. Each grammar can be used with the Lark-to-TextMate generator to create VS Code extensions with syntax highlighting.

## Directory Structure

```
examples/
├── simple/                          # Learning examples
│   └── arithmetic-expression.lark   # Basic arithmetic expressions
├── advanced/                        # Production-grade grammars
│   └── systemrdl-register-definition.lark  # Hardware register definitions
└── test/                            # Test and validation examples
    └── invalid-syntax-test.lark     # Invalid syntax for error handling
```

## Examples

### Simple Examples

#### arithmetic-expression.lark
Basic arithmetic expression grammar with support for:
- **Operators**: Addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`)
- **Grouping**: Parentheses for expression grouping
- **Numbers**: Integer literals via `common.NUMBER` import

**Use cases**:
- Learning LARK syntax fundamentals
- Testing basic operator precedence
- Creating a simple expression calculator extension

**Generate extension**:
```bash
python generator.py --lark-file examples/simple/arithmetic-expression.lark
```

Output: `arithmetic-expression-syntax/` extension directory

### Advanced Examples

#### systemrdl-register-definition.lark
Comprehensive SystemRDL (System Register Description Language) grammar for hardware register bank definitions. Supports:
- **Components**: Address maps, registers, fields, signals
- **Definitions**: Enums, structs, constraints, properties
- **Expressions**: Complex conditional and arithmetic expressions
- **Operators**: Comparison, bitwise, logical operations

**Use cases**:
- Hardware design automation tools
- Register specification languages
- Complex grammar syntax highlighting

**Generate extension**:
```bash
python generator.py --lark-file examples/advanced/systemrdl-register-definition.lark
```

Output: `systemrdl-syntax/` extension directory

### Test Examples

#### invalid-syntax-test.lark
Intentionally invalid LARK syntax used for testing error handling and validation.

**Use cases**:
- Testing error messages
- Verifying error handling in the generator
- Validation workflow testing

**Expected behavior**:
```bash
python generator.py --lark-file examples/test/invalid-syntax-test.lark
# Output: Error parsing LARK file: Rule 'syntax' used but not defined (in rule start)
```

## Running Examples

### Prerequisites
```bash
pip install -r ../requirements.txt
```

### Generate Extensions

For each example, the generator creates a VS Code extension directory:

```bash
# Simple example
python ../generator.py --lark-file examples/simple/arithmetic-expression.lark
# Creates: arithmetic-expression-syntax/

# Advanced example
python ../generator.py --lark-file examples/advanced/systemrdl-register-definition.lark
# Creates: systemrdl-syntax/

# Test example (demonstrates error handling)
python ../generator.py --lark-file examples/test/invalid-syntax-test.lark
# Shows error message instead of generating extension
```

## Generated Files

Each successfully generated extension contains:
- `package.json` - VS Code extension manifest with language configuration
- `syntaxes/{language}.tmLanguage.json` - TextMate grammar with patterns extracted from LARK

## Adding New Examples

To add a new example:

1. Create a `.lark` file in the appropriate subdirectory
2. Add documentation to this README
3. Test with: `python ../generator.py --lark-file examples/{category}/{filename}.lark`
4. Commit the grammar file

## Tips

- **Simple grammars** are easier to understand and generate better syntax highlighting initially
- **Complex grammars** require more manual refinement of the generated TextMate patterns
- **Test grammars** help verify error handling and edge cases
