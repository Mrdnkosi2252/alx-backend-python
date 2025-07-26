import requests

def access_nested_map(nested_map, path):
    """Access a nested value in a dictionary using a tuple of keys."""
    value = nested_map
    for key in path:
        if isinstance(value, dict):
            value = value[key]
        else:
            raise KeyError(key)
    return value




def get_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def memoize(method):
    """Cache the result of a method."""
    attr_name = f"_{method.__name__}_cache"
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self, *args, **kwargs))
        return getattr(self, attr_name)
    return wrapper
