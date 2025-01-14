#  type: ignore
from time import sleep

import pytest

from tawazi import DAG, ErrorStrategy, ExecNode

T = 0.001
# global comp_str
pytest.comp_str = ""


def a():
    sleep(T)
    pytest.comp_str += "a"


def b(a):
    raise NotImplementedError


def c(b):
    sleep(T)
    pytest.comp_str += "c"


def d(a):
    sleep(T)
    pytest.comp_str += "d"


list_execnodes = [
    ExecNode(a, a, priority=1, is_sequential=False),
    ExecNode(b, b, [a], priority=2, is_sequential=False),
    ExecNode(c, c, [b], priority=2, is_sequential=False),
    ExecNode(d, d, [a], priority=1, is_sequential=False),
]


def test_strict_error_behavior():
    pytest.comp_str = ""
    g = DAG(list_execnodes, 1, behavior=ErrorStrategy.strict)
    try:
        g.execute()
    except NotImplementedError:
        pass


def test_all_children_behavior():
    pytest.comp_str = ""
    g = DAG(list_execnodes, 1, behavior=ErrorStrategy.all_children)
    g.execute()
    assert pytest.comp_str == "ad"


def test_permissive_behavior():
    pytest.comp_str = ""
    g = DAG(list_execnodes, 1, behavior=ErrorStrategy.permissive)
    g.execute()
    assert pytest.comp_str == "acd"


# todo test using argname for ExecNode
