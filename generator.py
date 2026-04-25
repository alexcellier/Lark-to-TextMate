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

# Set up Jinja2 environment
template_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

@click.command()
@click.option('--name', prompt='Extension name', help='Name of the VS Code extension')
@click.option('--language', prompt='Language name', help='Name of the language for syntax highlighting')
@click.option('--scope', prompt='Language scope', help='TextMate scope name, e.g., source.language')
@click.option('--output', default='.', help='Output directory for the extension')
def generate(name, language, scope, output):
    """Generate a VS Code extension for syntax highlighting."""
    output_path = Path(output) / name
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate package.json
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
        scope=scope
    )
    (syntaxes_dir / f'{language}.tmLanguage.json').write_text(grammar_content)

    click.echo(f'VS Code extension generated in {output_path}')

if __name__ == '__main__':
    generate()