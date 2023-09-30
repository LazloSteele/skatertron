from hypothesis import given
from hypothesis.strategies import text
import sys

sys.path.append('../skatertron')

import cli

@given(text())
def test_cli_text_input(s):
    pass
    
