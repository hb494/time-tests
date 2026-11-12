import datetime
import dotenv
import os
import requests
from unittest.mock import Mock, patch


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") # Start time string parsed into a datetime object
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") # End time string passed into a datetime object

    if end_time_s < start_time_s:
        raise ValueError('End time is before the Start time')
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1) # Effective size of each interval (s)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)] # List comprehension building intervals
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range] # converts each datetime back to a string and returns list of (start_string, end_string) tuples


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if low < high:
                overlap_time.append((low, high))
    return overlap_time # Returns all overlap times between two intervals

if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))

dotenv.load_dotenv()
API_KEY = os.getenv("N2YO_API_KEY")

def iss_passes():
    response = requests.get(
        url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50&apiKey={API_KEY}",
    )
    data = response.json()
    passes = []
    for p in data["passes"]:
        start = datetime.datetime.fromtimestamp(p["startUTC"], tz=datetime.timezone.utc)
        end = datetime.datetime.fromtimestamp(p["endUTC"], tz=datetime.timezone.utc)
        passes.append((start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")))
    return passes

# Mocking

def test_iss_passes():
    with patch.object(requests, 'get') as mock_get:
        s