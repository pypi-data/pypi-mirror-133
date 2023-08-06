from typing import TypeVar, Callable

T = TypeVar('T')


def get_value(dictionary: dict, key: list, default_supplier: Callable[[], T] = lambda: None) -> T:
    value = dictionary.get(key) if dictionary else None
    return value if value else default_supplier()


def get_value_from_path(dictionary: dict, path: list, default_supplier: Callable[[], T] = lambda: None) -> T:
    if not path:
        return default_supplier()
    elif len(path) == 1:
        return get_value(dictionary, path[0], default_supplier)

    value = get_value(dictionary, path[0])
    return get_value_from_path(value, path[1:], default_supplier) if type(value) is dict else default_supplier()
