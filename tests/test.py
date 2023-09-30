from hypothesis import given
from hypothesis.strategies import text

from skatertron import controller

@given(text())
def test_cli_controller(s):
    pass
