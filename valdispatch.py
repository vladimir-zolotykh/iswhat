#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from functools import update_wrapper

DispatchType = Callable[[int, str], str]
RegisterResultType = Callable[[DispatchType], DispatchType]


class valdispatch:
    def __init__(self, func: DispatchType):
        self.default = func
        self.dispatch: dict[int, DispatchType] = {}
        update_wrapper(self, func)

    def register(self, *values: int) -> RegisterResultType:
        def decorate(func: DispatchType) -> DispatchType:
            self.dispatch.update(dict.fromkeys(values, func))
            return func

        return decorate

    def __call__(self, num: int, *args: str) -> str:
        try:
            return self.dispatch[num](num, *args)
        except KeyError:
            return self.default(num, *args)


@valdispatch
def classify(num: int, msg: str = "something else") -> str:
    return f"{num} is {msg}"


@classify.register(1, 3, 5)
def _(num: int, msg: str = "odd") -> str:
    return f"{num} is {msg}"


@classify.register(2, 4, 6)
def _(num: int, msg: str = "even") -> str:
    return f"{num} is {msg}"


if __name__ == "__main__":
    print(classify(3))
    print(classify(4))
    print(classify(100))
