import pytest
import gpxpy
import polyline
import json
from main import generate_gpx


@pytest.fixture
def osrm_graph():
    with open("tests/osrm_graph.json", "r") as f:
        content = json.load(f)
    return content


def test_conversion(osrm_graph):
    gpx = generate_gpx(osrm_graph)

    print(gpx)