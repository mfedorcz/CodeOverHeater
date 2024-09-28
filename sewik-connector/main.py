import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

URL = "https://obserwatoriumbrd.pl/app/api/nodes/post_zdarzenia.php"


def fetch_accidents(
    top_right_lat: float,
    top_right_lng: float,
    bottom_left_lat: float,
    bottom_left_lng: float,
):
    data = {
        "type": "DETAILS",
        "rok[]": ["2023"],
        "wybrane_wojewodztwa[]": "12",
        "groupBy": "DEC",
        "obszar_mapy[topRightCorner][lat]": top_right_lat,
        "obszar_mapy[topRightCorner][lng]": top_right_lng,
        "obszar_mapy[bottomLeftCorner][lat]": bottom_left_lat,
        "obszar_mapy[bottomLeftCorner][lng]": bottom_left_lng,
    }
    response = requests.post(URL, data=data)

    if requests.status_codes != 200:
        raise HTTPException(status_code=500, detail="Could not fetch accidents")

    accidents_per_wojewodztwo = response.json()["mapa"]["wojewodztwa"]

    accidents = []
    for wojewodztwo in accidents_per_wojewodztwo:
        for powiat in wojewodztwo["powiaty"]:
            for gmina in powiat["gminy"]:
                accidents.extend(gmina["zdarzenia_detale"])

    return accidents


app = FastAPI()


class Coordinates(BaseModel):
    lat: float
    lng: float


class MapData(BaseModel):
    topRightCorner: Coordinates
    bottomLeftCorner: Coordinates


class RequestData(BaseModel):
    obszar_mapy: MapData


@app.post("get_accidents")
async def submit_data(request_data: RequestData):
    top_right_lat = request_data.obszar_mapy.topRightCorner.lat
    top_right_lng = request_data.obszar_mapy.topRightCorner.lng
    bottom_left_lat = request_data.obszar_mapy.bottomLeftCorner.lat
    bottom_left_lng = request_data.obszar_mapy.bottomLeftCorner.lng

    accidents_data = fetch_accidents(
        top_right_lat, top_right_lng, bottom_left_lat, bottom_left_lng
    )

    return accidents_data