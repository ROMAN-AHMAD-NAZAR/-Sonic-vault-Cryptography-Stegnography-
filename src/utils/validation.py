"""Input validation helpers."""

def is_nonempty_str(s) -> bool:
    return isinstance(s, str) and bool(s.strip())


def validate_nonempty(value: str, field_name: str):
    """
    Validate that a string is not empty.
    
    Args:
        value (str): Value to validate
        field_name (str): Name of the field for error message
        
    Raises:
        ValueError: If value is empty
    """
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
