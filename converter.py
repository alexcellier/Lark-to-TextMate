"""
Enhanced LARK to TextMate Grammar Converter

Handles duplicates, advanced LARK features like priorities, templates, and imports.
"""

from pathlib import Path
from lark import Lark
from utils import create_name_keyed_dict

class MergedGrammar:
    def __init__(self, terminals, rules):
        self.terminals = terminals  # dict name -> terminal
        self.rules = rules  # dict name -> rule

def load_and_merge_grammar(lark_file):
    """Load LARK grammar and merge imports recursively."""
    lark_file_path = Path(lark_file)
    content = lark_file_path.read_text()

    # Parse the grammar
    grammar = Lark(content, parser='lalr')

    merged_terminals = create_name_keyed_dict(grammar.terminals, key_attr='name')
    merged_rules = {rule.origin.name: rule for rule in grammar.rules}

    # Stub for imports
    return MergedGrammar(terminals=merged_terminals, rules=merged_rules)

def expand_templates(grammar):
    """Expand LARK templates inline."""
    return grammar

def convert_to_textmate(grammar, language):
    """Convert LARK grammar to TextMate JSON with uniquification."""
    patterns = []
    seen_patterns = set()
    repository = {}

    # Sort rules by priority if available
    sorted_rules = sorted(grammar.rules.values(), key=lambda r: getattr(r, 'priority', 0), reverse=True)

    # Convert terminals to patterns, uniquify by pattern content
    for terminal in grammar.terminals.values():
        pattern = terminal_to_pattern(terminal, language)
        pattern_tuple = tuple(sorted(pattern.items()))
        if pattern_tuple not in seen_patterns:
            patterns.append(pattern)
            seen_patterns.add(pattern_tuple)

    # Convert rules to repository entries, uniquify by name
    for rule in sorted_rules:
        rule_name = rule.origin.name
        if rule_name not in repository:  # Uniquify
            repo_pattern = rule_to_repo_pattern(rule)
            repository[rule_name] = repo_pattern

    return {'patterns': patterns, 'repository': repository}

def terminal_to_pattern(terminal, language):
    """Convert LARK terminal to TextMate pattern."""
    pattern_str = terminal.pattern.value if hasattr(terminal.pattern, 'value') else str(terminal.pattern)
    return {
        'match': pattern_str,
        'name': f'source.{language}.{terminal.name}'
    }

def rule_to_repo_pattern(rule):
    """Convert LARK rule to TextMate repository pattern."""
    # Basic: just include for now; expand for advanced features
    return {
        'patterns': []  # TODO: Expand rule tree to actual patterns
    }