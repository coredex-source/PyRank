import ast

def convert_value(value):
    # Try converting to an integer
    try:
        if value.isdigit():  # Check if the string is a number
            return int(value)
    except ValueError:
        pass
    
    # Try converting to a float
    try:
        return float(value)
    except ValueError:
        pass

    # Try converting to a list
    try:
        if value.startswith('[') and value.endswith(']'):
            return ast.literal_eval(value)  # Safe evaluation of lists
    except (ValueError, SyntaxError):
        pass

    # Try converting to a tuple
    try:
        if value.startswith('(') and value.endswith(')'):
            return ast.literal_eval(value)  # Safe evaluation of tuples
    except (ValueError, SyntaxError):
        pass

    # Try converting to a dictionary
    try:
        if value.startswith('{') and value.endswith('}'):
            return ast.literal_eval(value)  # Safe evaluation of dicts
    except (ValueError, SyntaxError):
        pass

    # If it's a boolean
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'  # Convert to True/False

    # Return the value as a string if no conversion is applicable
    return value
    