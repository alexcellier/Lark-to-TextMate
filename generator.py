#!/usr/bin/env python3
"""
Syntaxes Generator

Generates VS Code extensions for syntax highlighting and TextMate grammars.
"""

import os
import json
from pathlib import Path
import click
from jinja2 import Environment, FileSystemLoader
from lark import Lark
from converter import load_and_merge_grammar, expand_templates, convert_to_textmate

# Set up Jinja2 environment
template_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

@click.command()
@click.option('--lark-file', required=True, help='Path to the LARK grammar file')
@click.option('--output', default='.', help='Output directory for the extension')
def generate(lark_file, output):
    """Generate a VS Code extension for syntax highlighting from LARK grammar."""
    
    # Extract language name from filename
    language = Path(lark_file).stem.lower()
    name = f"{language}-syntax"
    scope = f"source.{language}"
    output_path = Path(output) / name
    
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
    output_path.mkdir(parents=True, exist_ok=True)
    package_template = env.get_template('package.json.j2')
    package_content = package_template.render(
        name=name,
        language=language,
        scope=scope
    )
    (output_path / 'package.json').write_text(package_content)

    # Create syntaxes directory
    syntaxes_dir = output_path / 'syntaxes'
    syntaxes_dir.mkdir(exist_ok=True)

    # Generate grammar file
    grammar_template = env.get_template('grammar.json.j2')
    grammar_content = grammar_template.render(
        language=language,
        scope=scope,
        patterns=patterns,
        repository=repository
    )
    (syntaxes_dir / f'{language}.tmLanguage.json').write_text(grammar_content)

    click.echo(f'VS Code extension generated in {output_path}')

if __name__ == '__main__':
    generate()