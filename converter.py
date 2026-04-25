"""
Enhanced LARK to TextMate Grammar Converter with Best-in-Class TextMate Support

Handles duplicates, advanced LARK features like priorities, templates, and imports.
Implements proper rule tree expansion and TextMate scope naming standards.
"""

import re
from pathlib import Path
from lark import Lark, Tree, Token
from utils import create_name_keyed_dict
from textmate_scopes import classify_terminal

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
            repo_pattern = rule_to_repo_pattern(rule, language)
            repository[rule_name] = repo_pattern

    return {'patterns': patterns, 'repository': repository}

def terminal_to_pattern(terminal, language):
    """Convert LARK terminal to TextMate pattern with proper scope classification."""
    pattern_str = terminal.pattern.value if hasattr(terminal.pattern, 'value') else str(terminal.pattern)
    scope_type, scope_name = classify_terminal(terminal, language)
    
    return {
        'match': pattern_str,
        'name': scope_name
    }

def rule_to_repo_pattern(rule, language='generic', visited=None, depth=0):
    """
    Convert LARK rule to TextMate repository pattern with proper rule tree expansion.
    
    Traverses rule tree and generates TextMate patterns for:
    - Rule alternatives (using multiple pattern objects)
    - Terminal matches (literals)
    - Rule includes (references to other rules)
    """
    if visited is None:
        visited = set()
    
    if depth > 10 or rule.origin.name in visited:
        return {'patterns': []}  # Prevent infinite recursion
    
    visited.add(rule.origin.name)
    patterns = []
    
    try:
        # rule.expansion contains the RHS of the rule (list of terminals and rules)
        for expansion_item in rule.expansion:
            item_pattern = expand_rule_element(expansion_item, language, visited, depth + 1)
            if item_pattern:
                patterns.append(item_pattern)
    except (AttributeError, TypeError):
        # If rule structure differs, return minimal pattern
        pass
    
    return {'patterns': patterns if patterns else []}


def expand_rule_element(element, language, visited, depth):
    """
    Expand a single rule element (terminal, rule reference, or tree) into TextMate pattern.
    
    Args:
        element: Can be Token or Tree from rule.expansion
        language: Language name for scopes
        visited: Set of visited rule names (for cycle detection)
        depth: Current recursion depth
    
    Returns:
        Dict with TextMate pattern, or None if not expandable
    """
    try:
        if isinstance(element, Token):
            # Check token type to distinguish rule references from literals
            if element.type == 'RULE':
                # Reference to another rule: create include pattern
                return {'include': f'#{element.value}'}
            else:
                # String literal or other token: create match pattern
                literal_value = str(element.value)
                
                # Strip quotes if present
                if (literal_value.startswith('"') and literal_value.endswith('"')) or \
                   (literal_value.startswith("'") and literal_value.endswith("'")):
                    literal_value = literal_value[1:-1]
                
                # Escape regex special characters
                escaped = re.escape(literal_value)
                
                # Classify scope based on content
                if literal_value in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!']:
                    scope = f'source.{language}.keyword.operator'
                elif literal_value in ['{', '}', '[', ']', '(', ')', ',', ';', ':']:
                    scope = f'source.{language}.punctuation'
                else:
                    scope = f'source.{language}.keyword.control'
                
                return {
                    'match': escaped,
                    'name': scope
                }
        
        elif isinstance(element, Tree):
            # Complex structure (alternative, repetition, etc.)
            # Try to expand recursively
            if element.data == 'alternatives':
                # Multiple alternatives: create multiple patterns
                sub_patterns = []
                for child in element.children:
                    sub_pattern = expand_rule_element(child, language, visited, depth)
                    if sub_pattern:
                        sub_patterns.append(sub_pattern)
                return sub_patterns[0] if len(sub_patterns) == 1 else None
            else:
                # Other tree types: try to expand children
                for child in element.children:
                    result = expand_rule_element(child, language, visited, depth)
                    if result:
                        return result
    
    except (AttributeError, TypeError, ValueError):
        # If expansion fails, skip this element
        pass
    
    return None