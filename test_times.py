import pytest
from times import time_range
from times import compute_overlap_time

def test_time_range():
    with pytest.raises(ValueError):
        time_range("2024-01-12 12:12:12", "2023-01-12 12:12:12")


    
