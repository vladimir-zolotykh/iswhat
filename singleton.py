#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        name = args[0]
        if cls in Singleton._instances:
            if name in Singleton._instances[cls]:
                return Singleton._instances[cls][name]
            else:
                obj = super().__call__(*args, **kwargs)
                Singleton._instances[cls][name] = obj
                return obj
        else:
            obj = super().__call__(*args, **kwargs)
            name = args[0]
            Singleton._instances[cls] = {name: obj}
            return obj


class Module(metaclass=Singleton):
    def __init__(self, name: str = "functools"):
        print(f"Initializing module {name}")
        self.name = name


if __name__ == "__main__":
    m1 = Module("struct")
    m2 = Module("struct")
    m3 = Module("struct")
    assert m1 is m2 is m3


def test_module1(capsys):
    m1 = Module("struct")
    o = capsys.readouterr()
    assert o.out == "Initializing module struct\n"
    m2 = Module("struct")
    o = capsys.readouterr()
    assert o.out == ""
    assert m1 is m2
