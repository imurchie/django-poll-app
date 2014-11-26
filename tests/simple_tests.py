import pytest


def add(a, b):
    return a + b

def test_add():
    assert add(4, 5) == 9



def divide_by_zero(a):
    a / 0

def test_exception():
    with pytest.raises(ZeroDivisionError) as excinfo:
        divide_by_zero(3)

    assert 'exceptions.ZeroDivisionError' in str(excinfo.type)
    assert 'by zero' in str(excinfo.value)
