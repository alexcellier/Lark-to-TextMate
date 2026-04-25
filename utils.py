"""
Shared utility functions for LARK-to-TextMate syntax conversion.
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


# Global Jinja2 environment
_ENV = None


def get_jinja_env():
    """Get or create the Jinja2 environment for templates."""
    global _ENV
    if _ENV is None:
        template_dir = Path(__file__).parent / 'templates'
        _ENV = Environment(loader=FileSystemLoader(template_dir))
    return _ENV


def render_and_write_template(template_name, context, output_path):
    """
    Render a Jinja2 template and write the result to a file.
    
    Args:
        template_name: Name of the template file (e.g., 'package.json.j2')
        context: Dictionary of variables to pass to the template
        output_path: Path object or string for the output file
    """
    env = get_jinja_env()
    template = env.get_template(template_name)
    content = template.render(**context)
    Path(output_path).write_text(content)


def create_name_keyed_dict(items, key_attr='name'):
    """
    Create a dictionary from a collection of objects, keyed by a specified attribute.
    
    Args:
        items: Iterable of objects
        key_attr: Attribute name to use as dictionary key (default: 'name')
    
    Returns:
        Dictionary with {obj.attr: obj} for each item in items
    """
    return {getattr(item, key_attr): item for item in items}


def ensure_directory(path, create_parents=True):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Path object or string to the directory
        create_parents: If True, create parent directories as needed (default: True)
    
    Returns:
        Path object of the directory
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=create_parents, exist_ok=True)
    return path_obj


def extract_language_metadata(lark_file_path):
    """
    Extract language metadata from a LARK file path.
    
    Args:
        lark_file_path: Path to the LARK grammar file
    
    Returns:
        Tuple of (language, name, scope) where:
            - language: Lowercase stem of filename (e.g., 'arithmetic-expression')
            - name: Language name formatted for package.json (e.g., 'arithmetic-expression-syntax')
            - scope: TextMate scope (e.g., 'source.arithmetic-expression')
    """
    language = Path(lark_file_path).stem.lower()
    name = f"{language}-syntax"
    scope = f"source.{language}"
    return language, name, scope


def deduplicate_patterns(patterns_list, seen_patterns_set):
    """
    Remove duplicate patterns from a list, tracking seen patterns.
    
    Args:
        patterns_list: List of pattern dictionaries to deduplicate
        seen_patterns_set: Set to track seen pattern tuples (modified in place)
    
    Returns:
        List of unique patterns
    """
    unique_patterns = []
    for pattern in patterns_list:
        pattern_tuple = tuple(sorted(pattern.items()))
        if pattern_tuple not in seen_patterns_set:
            unique_patterns.append(pattern)
            seen_patterns_set.add(pattern_tuple)
    return unique_patterns
