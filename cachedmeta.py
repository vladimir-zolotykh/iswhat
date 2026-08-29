#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    _instances = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        key = tuple(args)
        if cls not in (cached := type(cls)._instances) or key not in cached[cls]:
            cached[cls][key] = super().__call__(*args, **kwargs)
        return cached[cls][key]


class Cached(metaclass=CachedMeta):
    pass


class Person(Cached):
    _fields = ["name", "age", "salary"]

    def __init__(self, name, age, salary):
        print(f"Initializing {type(self).__name__}({name})")
        for var, val in locals().items():
            setattr(self, var, val)

    def __repr__(self):
        args = ", ".join(str(getattr(self, fld)) for fld in self._fields)
        return f"{type(self).__name__}({args})"


if __name__ == "__main__":
    CachedMeta._instances.clear()
    bob = Person("Bob", 37, 12000)
    print(bob)
    max = Person("Max", 42, 25000)
    print(max)
    bob2 = Person("Bob", 37, 12000)
    assert bob is bob2
