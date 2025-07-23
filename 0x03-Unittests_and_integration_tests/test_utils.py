#!/usr/bin/env python3


import requests
from functools import wraps
from typing import Any, Tuple, Union


def access_nested_map(nested_map: dict, path: Tuple[str]) -> Union[Any, None]:
    """
 
    """
    if not isinstance(nested_map, dict) or not isinstance(path, tuple):
        raise TypeError("nested_map must be a dictionary and path must be a tuple")
    if not path:
        return nested_map

    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url: str) -> Union[dict, list, None]:
    """
   
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException:
        return None


def memoize(method):
    """
   
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to handle caching."""
        cache_key = f"_{method.__name__}_cache"
        if not hasattr(self, cache_key):
            setattr(self, cache_key, method(self, *args, **kwargs))
        return getattr(self, cache_key)
    return wrapper


if __name__ == "__main__":
    
    nested = {"a": {"b": 42}}
    print(access_nested_map(nested, ("a", "b"))) 
    print(get_json("https://api.github.com"))  
