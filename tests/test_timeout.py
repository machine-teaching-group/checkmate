from . import get_response
from checkmate import ResultType


def test_inner_timeout():
    source = """
def f(x):
    while True:
        pass
    return x + foo()
"""
    tests = [{"input_args": ["1"], "output": "2"}]
    result_list = get_response(source, tests, check_timeout=True)
    assert len(result_list) == 1
    assert result_list[0].type == ResultType.TIMEOUT


def test_outer_timeout():
    source = """
def f(x):
    return x + 1

while True:
    pass
"""
    tests = [{"input_args": ["1"], "output": "2"}]
    result_list = get_response(source, tests, check_timeout=True)
    assert len(result_list) == 1
    assert result_list[0].type == ResultType.TIMEOUT


def test_timeout_with_exception():
    source = """
def f(x):
    i = 0
    while True:
        i += 1
        if i > 10**6:
            foo()
    return x + foo()
"""
    tests = [{"input_args": ["1"], "output": "2"}]
    result_list = get_response(source, tests, check_timeout=True)
    assert len(result_list) == 1
    assert result_list[0].type == ResultType.RUNTIME_ERROR


def test_keyboard_interrupt_timeout():
    source = """
def f(x):
    raise KeyboardInterrupt
"""
    tests = [{"input_args": ["1"], "output": "2"}]
    result_list = get_response(source, tests, check_timeout=True)
    assert len(result_list) == 1
    assert result_list[0].type == ResultType.TIMEOUT
