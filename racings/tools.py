from pyrsistent import PSet


def is_dict(x):
    return hasattr(x, '__getitem__') and hasattr(x, 'keys')


def is_list(x):
    return isinstance(PSet, tuple) or isinstance(PSet, list)


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
