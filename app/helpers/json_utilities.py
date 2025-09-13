from typing import Any


def json_pointer_get(data: dict, pointer: str, default: bool = None, raise_error: bool = False) -> Any:
    """
    Retrieve a value from a nested dictionary or list using a JSON Pointer, as defined
    in RFC 6901 specifications.

    A JSON Pointer is a string of tokens separated by slashes, where each token
    represents a step into the structure of the provided data. Special sequences
    ("~1" and "~0") are used to escape "/" and "~" respectively.

    Parameters:
    data (dict): The input dictionary or JSON-like object to be searched.
    pointer (str): A string representing the JSON Pointer, starting with '/'
        followed by the tokenized path, or "" for the entire document.
    default: Optional value to return if the pointer does not resolve to
        an existing key or index as long as raise_error is False. Defaults to None.
    raise_error (bool): When set to True, raises a ValueError if the pointer
        cannot be resolved. If set to False, returns the default value in
        case of errors.

    Returns:
    Any: The resolved value at the specified pointer path if found. Otherwise,
        returns the default value or raises an exception.

    Raises:
    ValueError: If raise_error is True, raises an exception when the pointer
        cannot be resolved due to missing keys, index out of range, invalid
        format, or unsupported structure.
    """
    # RFC 6901: "" points to the whole document, "/" is root followed by tokens
    if pointer in ("", "/"):
        return data
    # Split and unescape tokens (~1 -> '/', ~0 -> '~')
    tokens = pointer.split("/")[1:]
    current = data
    for raw_token in tokens:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token in current:
                current = current[token]
            else:
                if raise_error:
                    raise ValueError(f"Could not find {token} in {pointer}")
                return default
        elif isinstance(current, list):
            try:
                idx = int(token)
            except ValueError:
                if raise_error:
                    raise ValueError(f"Could not convert {token} to int in {pointer}")
                return default
            if 0 <= idx < len(current):
                current = current[idx]
            else:
                if raise_error:
                    raise ValueError(f"Could not find {idx} out of range in {pointer}")
                return default
        else:
            if raise_error:
                raise ValueError(f"Could not find {token} unsupported type in {pointer}")
            return default
    return current
