#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
import pytest


class TupleMeta(type):
    def __init__(cls, clsname, bases, ns):
        super().__init__(clsname, bases, ns)
        fields = ns.get("_fields", [])
        for n, fname in enumerate(fields):
            setattr(cls, fname, property(itemgetter(n)))


class Tuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args, **kwargs):
        if (n := len(cls._fields)) != len(args):
            raise TypeError(f"{cls} gets exactly {n} arguments")
        return super().__new__(cls, args)


class Person(Tuple):
    _fields = ["name", "age", "salary"]


if __name__ == "__main__":
    bob = Person("Bob", 37, 12000)
    print(bob)


@pytest.fixture
def bob():
    return Person("Bob", 37, 12000)


@pytest.mark.parametrize(
    "attr, expected",
    [
        ("name", "Bob"),
        ("age", 37),
        ("salary", 12000),
    ],
)
def test_person_fields(bob, attr, expected):
    assert getattr(bob, attr) == expected


def test_person():
    bob = Person("Bob", 37, 12000)
    assert str(bob) == "('Bob', 37, 12000)"
    for attr, expected in zip(Person._fields, ("Bob", 37, 12000)):
        assert getattr(bob, attr) == expected
    with pytest.raises(TypeError, match=""):
        Person("Max", 38)
    with pytest.raises(TypeError, match=""):
        Person("Max", 38, 12000, "Software engineer")
