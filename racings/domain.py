import importlib
import functools

MODULES = ['racings.base_model']

DOMAIN = functools.reduce(lambda x, y: x + y,
                          map(lambda x: importlib.import_module(x).DOMAIN,
                              MODULES))
