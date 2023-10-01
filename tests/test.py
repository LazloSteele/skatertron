from hypothesis import given
from hypothesis.strategies import text
import sys

sys.path.append('../skatertron')

import sqlalchemy_backend
    
@given(db = text())
def test_connections():
    pass

if __name__ == "__main__":
    test_postgres_connections()
