#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Callable
from functools import update_wrapper


class parmdispatch:
    def __init__(self, func):
        self.else_func = func
        self.dispatch: dict[int, Callable] = {}
        update_wrapper(self, func)

    def register(self, *values):
        def decorate(func):
            self.dispatch.update(dict.fromkeys(values, func))
            return func

        return decorate

    def __call__(self, num):
        try:
            return self.dispatch[num](num)
        except KeyError:
            return self.else_func(num)


@parmdispatch
def iswhat(num):
    return f"{num} is something else"


@iswhat.register(2, 4, 6)
def _(num):
    return f"{num} is even"


@iswhat.register(1, 5)
def _(num):
    return f"{num} is odd"


if __name__ == "__main__":
    print(iswhat(1))
    print(iswhat(4))
    print(iswhat(100))
