"""Test Module"""


def __virtual__(hub):
    return False, "no reason"


A: int = 1


def __init__(hub):
    hub.tree.test.B = 2


class C:
    """Class doc"""

    def __init__(self):
        """init doc"""

    def method(self):
        """method doc"""

    var: int = 1


def func(hub):
    """func doc"""
