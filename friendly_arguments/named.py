import sys
from typing import Dict, Any, Optional


def get_args(defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Parse command line arguments in a simple and flexible way.
    
    Supports multiple syntaxes:
    - --arg=value or -a=value
    - --arg value or -a value
    - --flag (returns True for boolean flags)
    
    Example usage:
        # python script.py --name João --age 25 --verbose
        args = get_args()
        print(args['--name'])    # 'João'
        print(args['--age'])     # '25'
        print(args['--verbose']) # True
    
    Example with defaults:
        args = get_args(defaults={'--name': 'Anonymous', '--age': '18'})
        print(args['--name'])  # 'Anonymous' if not provided
    
    Args:
        defaults: Optional dictionary with default values
    
    Returns:
        Dictionary with parsed arguments
    """
    args = defaults.copy() if defaults else {}
    i = 1
    
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        # Handle --arg=value or -a=value
        if '=' in arg:
            key, value = arg.split('=', 1)
            args[key] = value
        
        # Handle --arg or -a
        elif arg.startswith('-'):
            # Check if next item exists and is not another argument
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                args[arg] = sys.argv[i + 1]
                i += 1
            else:
                # Boolean flag
                args[arg] = True
        
        i += 1
    
    return args


def get_arg(args: dict, *keys, default=None):
    """
    Get an argument value by searching multiple possible key names.
    Useful for supporting both long and short argument names.
    
    Example:
        args = get_args()
        # Search for --name or -n, return 'Anonymous' if not found
        name = get_arg(args, '--name', '-n', default='Anonymous')
        
        # Search for --verbose or -v, return False if not found
        verbose = get_arg(args, '--verbose', '-v', default=False)
    
    Args:
        args: Dictionary returned by get_args()
        *keys: Variable number of key names to search for
        default: Default value if none of the keys are found
    
    Returns:
        The value of the first matching key, or default if not found
    """
    for key in keys:
        if key in args:
            return args[key]
    return default


# Backward compatibility: keep the old function name
def get_params_sys_args(keys: list, silent: bool = True) -> Dict[str, str]:
    """
    Legacy function for backward compatibility.
    
    Parse named command line arguments (old API).
    Consider using get_args() for a more flexible approach.
    
    Example:
        # python script.py --text=hello --name=world
        args = get_params_sys_args(['--text=', '--name='])
        print(args['--text='])  # 'hello'
    
    Args:
        keys: List of expected keys with '=' suffix (e.g., ['--text=', '--name='])
        silent: If True, doesn't print values (default: True)
    
    Returns:
        Dictionary with found arguments
    """
    args_dict = {}
    
    for i in range(1, len(sys.argv)):
        for key in keys:
            if sys.argv[i].startswith(key):
                value = sys.argv[i][len(key):]
                args_dict[key] = value
                
                if not silent:
                    print(f"The {key} value is: {value}")
                break
    
    return args_dict