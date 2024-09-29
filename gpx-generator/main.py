import requests
import gpxpy
import polyline
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

URL = "http://osrm:3000/route/v1/driving"

app = FastAPI()

allowed_profiles = {"bike", "safebike", "strictbike", "bike50"}


class RouteRequest(BaseModel):
    start_latitude: float = Field(..., description="Starting point latitude")
    start_longitude: float = Field(..., description="Starting point longitude")
    end_latitude: float = Field(..., description="Ending point latitude")
    end_longitude: float = Field(..., description="Ending point longitude")
    profile: str = Field(..., description="Profile to use")

    # Validate the profile field
    @classmethod
    def validate_profile(cls, profile):
        if profile not in allowed_profiles:
            raise HTTPException(
                status_code=400,
                detail="Invalid profile. Allowed profiles: bike, safebike, strictbike, bike50",
            )
        return profile


class Waypoint:
    def __init__(self, lat: float, lut: float) -> None:
        self.lat = lat
        self.lut = lut


def fetch_osrm_route(start: Waypoint, end: Waypoint):
    url = f"{URL}/{start.lat},{start.lut};{end.lat},{end.lut}"

    params = {"overview": "false", "steps": "true"}

    response = requests.get(url, params=params)

    return response


def generate_gpx(osrm_graph):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for step in osrm_graph["routes"][0]["legs"][0]["steps"]:
        geometry = step["geometry"]
        decoded_coords = polyline.decode(geometry)

        for coord in decoded_coords:
            latitude, longitude = coord
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude, longitude))

    return gpx.to_xml()


@app.post("/route")
def get_route(data: RouteRequest):
    # Validate the profile
    RouteRequest.validate_profile(data.profile)

    # Normally, you'd process the route here
    return {
        "start": [data.start_latitude, data.start_longitude],
        "end": [data.end_latitude, data.end_longitude],
        "profile": data.profile,
        "message": "Route calculated successfully!",
    }
