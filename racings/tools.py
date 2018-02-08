from pyrsistent import PSet, PVector


def is_dict(x):
    return hasattr(x, '__getitem__') and hasattr(x, 'keys')


def is_list(x):
    return (isinstance(x, tuple)
            or isinstance(x, list)
            or isinstance(x, PVector))


def is_set(x):
    return isinstance(x, PSet)


def pyrsistent_to_mutable(x):
    if is_dict(x):
        return {k: pyrsistent_to_mutable(x[k]) for k in x}
    if is_set(x):
        return {pyrsistent_to_mutable(y) for y in x}
    if is_list(x):
        return [pyrsistent_to_mutable(y) for y in x]
    return x
