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

# Set up Jinja2 environment
template_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(template_dir))

def convert_lark_to_textmate(parser):
    """Convert LARK grammar to TextMate patterns and repository."""
    patterns = []
    repository = {}
    
    # Add terminals as match patterns
    for term in parser.terminals:
        if hasattr(term, 'pattern') and term.pattern:
            pattern_str = term.pattern.value
            patterns.append({
                "name": f"constant.{term.name}",
                "match": pattern_str
            })
    
    # Add rules as includes
    for rule in parser.rules:
        rule_name = rule.origin.name
        patterns.append({
            "include": f"#{rule_name}"
        })
        # Repository entry (basic)
        repository[rule_name] = {
            "patterns": []  # TODO: expand rule tree
        }
    
    return patterns, repository

@click.command()
@click.option('--lark-file', required=True, help='Path to the LARK grammar file')
@click.option('--output', default='.', help='Output directory for the extension')
def generate(lark_file, output):
    """Generate a VS Code extension for syntax highlighting from LARK grammar."""
    
    try:
        # Load LARK grammar
        with open(lark_file) as f:
            grammar_text = f.read()
        
        # Parse grammar
        parser = Lark(grammar_text, parser='lalr')
    except Exception as e:
        click.echo(f"Error parsing LARK file: {e}", err=True)
        return
    
    # Extract language name from filename
    language = Path(lark_file).stem.lower()
    name = f"{language}-syntax"
    scope = f"source.{language}"
    
    # Generate patterns from LARK grammar
    patterns, repository = convert_lark_to_textmate(parser)
    
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
        scope=scope,
        patterns=patterns,
        repository=repository
    )
    (syntaxes_dir / f'{language}.tmLanguage.json').write_text(grammar_content)

    click.echo(f'VS Code extension generated in {output_path}')

if __name__ == '__main__':
    generate()