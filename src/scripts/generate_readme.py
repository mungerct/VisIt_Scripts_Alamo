#!/usr/bin/env python3
"""
Auto-generate README.md from DEFAULTS dictionary with inline comments.

This script parses your Python source file to extract the DEFAULTS dictionary
along with any inline comments, which are used as descriptions in the README.

Usage:
    python auto_generate_readme.py config.py

Where config.py contains your DEFAULTS dictionary with inline comments like:
    DEFAULTS = {
        "file.width": 1080,  # Image width in pixels
        "file.height": 1080,  # Image height in pixels
    }
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, Tuple


def parse_defaults_from_source(filepath: str) -> Dict[str, Tuple[Any, str]]:
    """
    Parse DEFAULTS dictionary from Python source file, extracting values and comments.
    
    Args:
        filepath: Path to Python file containing DEFAULTS
        
    Returns:
        Dictionary mapping keys to (value, comment) tuples
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find DEFAULTS dictionary - handle multi-line with nested structures
    pattern = r'DEFAULTS\s*=\s*\{(.*?)\n\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError(f"Could not find DEFAULTS dictionary in {filepath}")
    
    dict_content = match.group(1)
    
    # Parse each line
    config = {}
    lines = dict_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
        
        # Match: "key": value,  # comment
        # This handles strings, numbers, tuples, and function calls
        match = re.match(r'"([^"]+)":\s*(.+?),?\s*(?:#\s*(.+))?$', line)
        
        if match:
            key = match.group(1)
            value_str = match.group(2).rstrip(',').strip()
            comment = match.group(3).strip() if match.group(3) else ""
            
            # Parse the value
            value = parse_value(value_str)
            
            config[key] = (value, comment)
    
    return config


def parse_value(value_str: str) -> str:
    """Parse a value string and return formatted version for display."""
    value_str = value_str.strip()
    
    # Handle different value types
    if value_str.startswith('"') and value_str.endswith('"'):
        # String value
        return value_str[1:-1]
    elif value_str.startswith('(') and value_str.endswith(')'):
        # Tuple value
        return value_str
    elif value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
        # Integer
        return value_str
    elif value_str.replace('.', '', 1).replace('e', '', 1).replace('-', '', 1).isdigit():
        # Float (including scientific notation)
        return value_str
    else:
        # Function call or other expression
        return value_str

def print_warning(missing_comments: list) -> None:
    """
    Print red warning message for parameters missing comments.
    
    Args:
        missing_comments: List of parameter keys missing comments
    """
    if not missing_comments:
        return
    
    # ANSI color codes
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    YELLOW = '\033[93m'
    
    print(f"\n{RED}{BOLD}⚠ WARNING: Missing Comments{RESET}")
    print(f"{RED}{'=' * 60}{RESET}")
    print(f"{YELLOW}The following parameters are missing inline comments:{RESET}\n")
    
    for key in sorted(missing_comments):
        print(f"  {RED}✗{RESET} {key}")
    
    print(f"\n{YELLOW}Add comments like this:{RESET}")
    print(f'  "{missing_comments[0]}": value,  # Description here')
    print(f"\n{RED}{'=' * 60}{RESET}\n")

def validate_comments(config: Dict[str, Tuple[Any, str]]) -> list:
    """
    Check for parameters missing comments.
    
    Args:
        config: Dictionary mapping keys to (value, comment) tuples
        
    Returns:
        List of keys that are missing comments
    """
    missing_comments = []
    
    for key, (value, comment) in config.items():
        if not comment or comment.strip() == "":
            missing_comments.append(key)
    
    return missing_comments

def format_value_for_table(value: str) -> str:
    """Format a value for display in markdown table."""
    if isinstance(value, str):
        # Check if it's a function call
        if '(' in value and ')' in value:
            return f'`{value}`'
        # Check if it looks like a tuple
        elif value.startswith('(') and value.endswith(')'):
            return f'`{value}`'
        else:
            return f'`"{value}"`'
    else:
        return f'`{value}`'


def organize_by_category(config: Dict[str, Tuple[Any, str]]) -> Dict[str, Dict]:
    """
    Organize configuration by category based on key prefixes.
    
    Returns nested dictionary structure with categories and subcategories.
    """
    organized = {}
    
    for key, (value, comment) in config.items():
        parts = key.split('.')
        
        # Navigate/create nested structure
        current = organized
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {'_items': {}, '_subcategories': {}}
            if i < len(parts) - 2:
                if '_subcategories' not in current[part]:
                    current[part]['_subcategories'] = {}
                current = current[part]['_subcategories']
            else:
                current = current[part]
        
        # Add the final item
        final_key = parts[-1]
        if '_items' not in current:
            current['_items'] = {}
        current['_items'][final_key] = (value, comment)
    
    return organized


def generate_table_rows(items: Dict[str, Tuple], prefix: str = "") -> str:
    """Generate markdown table rows for a set of items."""
    if not items:
        return ""
    
    rows = []
    for key, (value, comment) in sorted(items.items()):
        param_name = f"{prefix}.{key}" if prefix else key
        formatted_value = format_value_for_table(value)
        description = comment if comment else "Configuration parameter"
        rows.append(f"| `{param_name}` | {formatted_value} | {description} |")
    
    return "\n".join(rows)


def generate_section(name: str, data: Dict, level: int = 3, prefix: str = "") -> str:
    """Recursively generate markdown sections with proper nesting."""
    h_tag = f"h{level}"
    section = f"<details>\n<summary><{h_tag}>{name}</{h_tag}></summary>\n\n"
    
    # Add table for direct items
    items = data.get('_items', {})
    if items:
        section += "| Parameter | Default | Description |\n"
        section += "|-----------|---------|-------------|\n"
        section += generate_table_rows(items, prefix) + "\n\n"
    
    # Add subcategories
    subcats = data.get('_subcategories', {})
    for subcat_key, subcat_data in sorted(subcats.items()):
        subcat_name = subcat_key.replace('_', ' ').title()
        new_prefix = f"{prefix}.{subcat_key}" if prefix else subcat_key
        section += generate_section(subcat_name, subcat_data, level + 1, new_prefix)
    
    section += "</details>\n\n"
    return section


def generate_colormaps_section(colormaps: set) -> str:
    """Generate the available colormaps section."""
    section = "<details>\n<summary><h2>Available Colormaps</h2></summary>\n\n"
    section += "The following colormaps are supported for visualization:\n\n"
    
    # Categorize colormaps
    categories = {
        "Sequential Colormaps": ['viridis', 'plasma', 'magma', 'inferno', 'cividis', 'turbo', 'hot'],
        "Grayscale": ['gray'],
        "Single Hue Sequential": ['blues', 'Blues', 'Greens', 'Oranges', 'Purples', 'Reds'],
        "Multi-Hue Sequential": ['BuGn', 'GnBu', 'PuBu', 'PuBuGn', 'OrRd', 'PuRd', 'RdPu', 
                                  'YlGn', 'YlgGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'],
        "Diverging Colormaps": ['PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral'],
        "Qualitative Colormaps": ['rainbow', 'Dark2', 'Paired', 'Set1']
    }
    
    for title, maps in categories.items():
        section += f"### {title}\n"
        for cmap in maps:
            if cmap in colormaps:
                section += f"- `{cmap}`\n"
        section += "\n"
    
    section += "</details>\n\n"
    return section


def generate_readme(config: Dict[str, Tuple], colormaps: set, 
                   category_titles: Dict[str, str], custom_header: str = None) -> str:
    """Generate the complete README.md content."""
    
    # Organize configuration
    organized = organize_by_category(config)
    
    # Start README with custom header or default
    if custom_header:
        readme = custom_header
        # Ensure there's spacing before the configuration section
        if not readme.endswith('\n\n'):
            readme += '\n\n' if readme.endswith('\n') else '\n\n'
    else:
        readme = "# Configuration Defaults\n\n"
        readme += "This document describes the default configuration values for the visualization tool.\n\n"
    
    readme += "<details>\n<summary><h2>Configuration Details</h2></summary>\n\n"
    
    # Generate sections for each top-level category
    for category_key, category_data in sorted(organized.items()):
        title = category_titles.get(category_key, category_key.replace('_', ' ').title())
        readme += generate_section(title, category_data, level=3, prefix=category_key)
    
    readme += "</details>\n\n"
    
    # Add colormaps if provided
    if colormaps:
        readme += generate_colormaps_section(colormaps)
    
    # Add notes
    readme += "## Notes\n\n"
    readme += "- Boolean parameters use `0` for off/disabled and `1` for on/enabled\n"
    readme += "- Color values are specified as RGBA tuples with values 0-255\n"
    readme += "- Use `-1` for `step.end` to process all available timesteps\n"
    
    return readme


def extract_colormaps_from_source(filepath: str) -> set:
    """Extract ALLOWED_COLORMAPS set from source file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find ALLOWED_COLORMAPS set
    pattern = r'ALLOWED_COLORMAPS\s*=\s*\{([^}]+)\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return set()
    
    # Extract colormap names
    colormaps_str = match.group(1)
    colormaps = set()
    
    for line in colormaps_str.split('\n'):
        line = line.strip().strip(',').strip('"').strip("'")
        if line and not line.startswith('#'):
            colormaps.add(line)
    
    return colormaps


def read_custom_header(header_file: str) -> str:
    """Read custom header content from a file."""
    if not Path(header_file).exists():
        return None
    
    with open(header_file, 'r') as f:
        return f.read()



def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python auto_generate_readme.py <source_file.py> [header_file.md]")
        print("\nArguments:")
        print("  source_file.py   - Python file containing DEFAULTS dictionary")
        print("  header_file.md   - (Optional) Markdown file with custom header content")
        print("\nExample:")
        print("  python auto_generate_readme.py config.py")
        print("  python auto_generate_readme.py config.py custom_header.md")
        sys.exit(1)
    
    source_file = sys.argv[1]
    header_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(source_file).exists():
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    
    print(f"Parsing configuration from {source_file}...")
    
    # Parse configuration
    try:
        config = parse_defaults_from_source(source_file)
        colormaps = extract_colormaps_from_source(source_file)
        custom_header = read_custom_header(header_file) if header_file else None
        
        print(f"  Found {len(config)} configuration parameters")
        if colormaps:
            print(f"  Found {len(colormaps)} colormaps")
        if custom_header:
            print(f"  Using custom header from {header_file}")
        
        # Validate comments
        missing_comments = validate_comments(config)
        if missing_comments:
            print_warning(missing_comments)
            # Continue anyway, but user is warned

        # Define category titles
        category_titles = {
            'file': 'Database Settings',
            'step': 'Step Control',
            'plotting': 'Plotting Configuration (Variables, legend, location, etc.)',
            'sim': 'Data Transfer, not for input use'
        }
        
        # Generate README
        readme_content = generate_readme(config, colormaps, category_titles, custom_header)
        
        # Write to file
        output_path = Path("README.md")
        with open(output_path, 'w') as f:
            f.write(readme_content)
        
        print(f"✓ README.md generated successfully!")
        print(f"  Output: {output_path.absolute()}")

        if missing_comments:
            print(f"\n⚠ Note: {len(missing_comments)} parameter(s) missing comments (see warning above)")
        
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()