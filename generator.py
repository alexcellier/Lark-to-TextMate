#!/usr/bin/env python3
"""
Syntaxes Generator

Generates VS Code extensions for syntax highlighting and TextMate grammars.
"""

from pathlib import Path
import click
from converter import load_and_merge_grammar, expand_templates, convert_to_textmate
from utils import (
    render_and_write_template,
    ensure_directory,
    extract_language_metadata
)

@click.command()
@click.option('--lark-file', required=True, help='Path to the LARK grammar file')
@click.option('--output', default='.', help='Output directory for the extension')
def generate(lark_file, output):
    """Generate a VS Code extension for syntax highlighting from LARK grammar."""
    
    # Extract language metadata from filename
    language, name, scope = extract_language_metadata(lark_file)
    output_path = ensure_directory(Path(output) / name)
    
    try:
        # Load and process LARK grammar with advanced features
        merged_grammar = load_and_merge_grammar(lark_file)
        expanded_grammar = expand_templates(merged_grammar)
        tm_grammar = convert_to_textmate(expanded_grammar, language)
        patterns = tm_grammar['patterns']
        repository = tm_grammar['repository']
    except Exception as e:
        click.echo(f"Error processing LARK file: {e}", err=True)
        return

    # Generate package.json
    render_and_write_template(
        'package.json.j2',
        {'name': name, 'language': language, 'scope': scope},
        output_path / 'package.json'
    )

    # Create syntaxes directory and generate grammar file
    syntaxes_dir = ensure_directory(output_path / 'syntaxes', create_parents=False)
    render_and_write_template(
        'grammar.json.j2',
        {
            'language': language,
            'scope': scope,
            'patterns': patterns,
            'repository': repository
        },
        syntaxes_dir / f'{language}.tmLanguage.json'
    )

    click.echo(f'VS Code extension generated in {output_path}')

if __name__ == '__main__':
    generate()