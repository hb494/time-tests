import pytest
from times import time_range
from times import compute_overlap_time
import yaml
from unittest.mock import Mock, patch
import times


def test_time_range():
    with pytest.raises(ValueError):
        time_range("2024-01-12 12:12:12", "2023-01-12 12:12:12")

def test_compute_overlap_time():
    range1 = [("2023-01-12 12:12:12", "2023-02-12 12:12:12")]
    range2 = [("2023-02-12 12:12:12", "2024-01-01 12:12:12")]
    expected = []
    real = compute_overlap_time(range1, range2)

    assert real == expected

@pytest.mark.parametrize(
    "range1, range2, expected",
    [
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"), # Range 1
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60), # range 2
            [("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
             ("2010-01-12 10:38:00", "2010-01-12 10:45:00")], # What we expect the overlap time to be
        ),
        (
            time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"), # Again
            time_range("2010-01-12 12:00:00", "2010-01-12 13:00:00"),
            [],
        ),
    ],
    ids=["generic", "no_overlap"],
)
def test_overlap_time(range1, range2, expected):
    assert compute_overlap_time(range1, range2) == expected

    
with open("fixture.yaml") as f:
    fixture = yaml.safe_load(f)

cases = []
id = []
for param in fixture:
    for name, val in param.items():
        cases.append((val["time_range_1"], val["time_range_2"], val["expected"]))
        id.append(name)

@pytest.mark.parametrize("range1, range2, expected", cases, ids=id)
def test_overlap_time(range1, range2, expected):
    result = compute_overlap_time(time_range(*range1), time_range(*range2))
    assert result == [tuple(e) for e in expected]

# Mocking

def test_iss_passes():
    fake_response = Mock()
    fake_response.json.return_value = {
        "info": {"satid": 25544, "satname": "SPACE STATION", "transactionscount": 1, "passescount": 1},
        "passes": [{"startUTC": 1521368025, "endUTC": 1521368660}],
    }

    with patch.object(times.requests, "get", return_value=fake_response) as mock_get:
        result = times.iss_passes()

    mock_get.assert_called_once()
    assert result == [("2018-03-18 10:13:45", "2018-03-18 10:24:20")]

    
