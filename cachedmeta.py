#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class CachedMeta(type):
    _instances = defaultdict(dict)

    def __new__(mcls, clsname, bases, clsdict):
        fields = clsdict.get("_fields", [])

        def init(self, *args):
            if (n := len(fields)) != len(args):
                raise TypeError(
                    f"{type(self).__name__} gets exactly {n} positional arguments"
                )
            name = args[0]
            print(f"Initializing {type(self).__name__}({name})")
            for k, fld in enumerate(fields):
                setattr(self, fld, args[k])

        def repr(self):
            args = ", ".join(str(getattr(self, fld)) for fld in fields)
            return f"{type(self).__name__}({args})"

        clsdict["__init__"] = init
        clsdict["__repr__"] = repr
        return super().__new__(mcls, clsname, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        key = tuple(args)
        if cls not in (cached := type(cls)._instances) or key not in cached[cls]:
            cached[cls][key] = super().__call__(*args, **kwargs)
        return cached[cls][key]


class Cached(metaclass=CachedMeta):
    pass


class Person(Cached):
    _fields = ["name", "age", "salary"]


def test_person1(capsys):
    CachedMeta._instances.clear()
    bob = Person("Bob", 37, 12000)
    o = capsys.readouterr()
    assert o.out == "Initializing Person(Bob)\n"
    assert str(bob) == "Person(Bob, 37, 12000)"
    max = Person("Max", 42, 25000)
    o = capsys.readouterr()
    assert o.out == "Initializing Person(Max)\n"
    assert str(max) == "Person(Max, 42, 25000)"
    bob2 = Person("Bob", 37, 12000)
    o = capsys.readouterr()
    assert o.out == ""
    assert bob is bob2


if __name__ == "__main__":
    CachedMeta._instances.clear()
    bob = Person("Bob", 37, 12000)
    print(bob)
    max = Person("Max", 42, 25000)
    print(max)
    bob2 = Person("Bob", 37, 12000)
    assert bob is bob2
