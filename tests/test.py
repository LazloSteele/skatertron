from hypothesis import given
from hypothesis.strategies import text
import sys

sys.path.append('../skatertron')

import controller

@given(text())
def test_cli_controller(s):
    pass
