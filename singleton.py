#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import defaultdict


class Singleton(type):
    _instances = defaultdict(dict)

    def __call__(cls, *args, **kwargs):
        name = args[0]
        if cls not in (instances := Singleton._instances) or name not in instances[cls]:
            instances[cls][name] = super().__call__(*args, **kwargs)
        return instances[cls][name]


class Module(metaclass=Singleton):
    def __init__(self, name: str = "functools"):
        print(f"Initializing module {name}")
        self.name = name


class Package(metaclass=Singleton):
    def __init__(self, name: str = "struct"):
        print(f"Initializing module {name}")
        self.name = name


if __name__ == "__main__":
    m1 = Module("struct")
    m2 = Module("struct")
    m3 = Module("struct")
    assert m1 is m2 is m3


def test_package1(capsys):
    p1 = Package("types")
    o = capsys.readouterr()
    assert o.out == "Initializing module types\n"
    p2 = Package("types")
    o = capsys.readouterr()
    assert o.out == ""
    assert p1 is p2


def test_module1(capsys):
    m1 = Module("struct")
    o = capsys.readouterr()
    assert o.out == "Initializing module struct\n"
    m2 = Module("struct")
    o = capsys.readouterr()
    assert o.out == ""
    assert m1 is m2


def test_mixed(capsys):
    Singleton._instances.clear()
    Module("types")
    o = capsys.readouterr()
    assert o.out == "Initializing module types\n"
    Package("types")
    o = capsys.readouterr()
    assert o.out == "Initializing module types\n"
