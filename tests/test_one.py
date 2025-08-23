import pytest


@pytest.mark.parametrize("x, y, result",[
    (3, 2, 5),
    (4, 5, 9)])
def test_add(x, y , result):
    assert(x + y) == result