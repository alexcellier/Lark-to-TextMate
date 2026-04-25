"""
TextMate Scope Classification Engine

Maps LARK constructs to standard TextMate scope names following conventions:
- source.language (root)
- source.language.comment.line
- source.language.comment.block
- source.language.string.quoted.double
- source.language.keyword.control
- source.language.keyword.operator
- source.language.constant.numeric
- source.language.entity.name
- source.language.punctuation
"""


def classify_terminal(terminal, language='generic'):
    """
    Classify a LARK terminal and return a standard TextMate scope.
    
    Args:
        terminal: LARK Terminal object (has .name and .pattern)
        language: Language name for context-specific classification
    
    Returns:
        Tuple of (scope_type, scope_name) where:
        - scope_type: one of 'comment.line', 'comment.block', 'string', 'number', 'operator', 'keyword', 'punctuation'
        - scope_name: full TextMate scope like 'source.language.constant.numeric'
    """
    name = terminal.name.upper()
    pattern_str = str(terminal.pattern.value if hasattr(terminal.pattern, 'value') else terminal.pattern)
    
    # Comment patterns
    if any(x in name for x in ['COMMENT', 'IGNORE']):
        if 'BLOCK' in name or '/*' in pattern_str or '*/' in pattern_str:
            return ('comment.block', f'source.{language}.comment.block')
        else:
            return ('comment.line', f'source.{language}.comment.line')
    
    # String patterns
    if any(x in name for x in ['STRING', 'CNAME', 'WORD']):
        return ('string.quoted.double', f'source.{language}.string.quoted.double')
    
    # Number patterns
    if any(x in name for x in ['NUMBER', 'INT', 'FLOAT', 'HEX', 'HEXNUMBER', 'VERILOG_NUMBER']):
        return ('constant.numeric', f'source.{language}.constant.numeric')
    
    # Operator patterns
    if any(x in name for x in ['PLUS', 'MINUS', 'MUL', 'DIV', 'MOD', 'EQ', 'NEQ', 'LT', 'GT', 'AND', 'OR', 'NOT']):
        return ('keyword.operator', f'source.{language}.keyword.operator')
    
    # Punctuation (single/small symbols)
    if len(pattern_str) <= 3 and not pattern_str.replace('\\', '').isalnum():
        return ('punctuation', f'source.{language}.punctuation')
    
    # Default: entity/identifier
    return ('entity.name', f'source.{language}.entity.name')


def get_comment_config_from_grammar(grammar):
    """
    Detect comment syntax from LARK grammar.
    
    Args:
        grammar: LARK grammar object
    
    Returns:
        Dict with 'lineComment' and 'blockComment' keys
    """
    config = {}
    
    for terminal in grammar.terminals:
        pattern_str = str(terminal.pattern.value if hasattr(terminal.pattern, 'value') else terminal.pattern)
        name_upper = terminal.name.upper()
        
        if name_upper.startswith('__IGNORE') or 'COMMENT' in name_upper:
            if '//' in pattern_str or '#' in pattern_str:
                config['lineComment'] = '//'
            if '/*' in pattern_str or '*/' in pattern_str:
                config['blockComment'] = ['/*', '*/']
    
    # Default fallback
    if not config:
        config = {
            'lineComment': '//',
            'blockComment': ['/*', '*/']
        }
    else:
        # Ensure both are set
        if 'lineComment' not in config:
            config['lineComment'] = '//'
        if 'blockComment' not in config:
            config['blockComment'] = ['/*', '*/']
    
    return config


def get_brackets_from_grammar(grammar):
    """
    Detect bracket pairs from LARK grammar.
    
    Args:
        grammar: LARK grammar object
    
    Returns:
        List of [open, close] pairs
    """
    # Standard brackets for most languages
    return [
        ['(', ')'],
        ['[', ']'],
        ['{', '}']
    ]


def generate_language_config(grammar):
    """
    Generate a complete language configuration object from grammar.
    
    Args:
        grammar: LARK grammar object
    
    Returns:
        Dict with language configuration
    """
    comments = get_comment_config_from_grammar(grammar)
    brackets = get_brackets_from_grammar(grammar)
    
    return {
        'comments': {
            'lineComment': comments.get('lineComment', '//'),
            'blockComment': comments.get('blockComment', ['/*', '*/'])
        },
        'brackets': brackets,
        'autoClosingPairs': [
            *brackets,
            ['"', '"'],
            ["'", "'"]
        ],
        'surroundingPairs': [
            *brackets,
            ['"', '"'],
            ["'", "'"]
        ],
        'indentationRules': {
            'increaseIndentPattern': '^.*\\{[^}]*$',
            'decreaseIndentPattern': '^\\s*\\}'
        },
        'folding': {
            'offSide': True,
            'markers': {
                'start': '^.*\\{\\s*$',
                'end': '^\\s*\\}',
                'nested': True
            }
        }
    }
