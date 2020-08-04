import pytest
from .converter import vh

def test_vh():
   # test base case
   assert pytest.approx(vh(0.0, 0.0), 0.0)
   assert pytest.approx(vh(-0.0, 0.0), 0.0)
   # and unit vectors...
   assert pytest.approx(vh(1.0, 0.0), 1.0)
   assert pytest.approx(vh(0.0, 1.0), 1.0)
   # negative u/v values handled
   assert pytest.approx(vh(-1.0, 0.0), 1.0)
   assert pytest.approx(vh(0.0, -1.0), 1.0)
