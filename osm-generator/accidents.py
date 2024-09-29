import requests
import json
import osmnx as ox


# URL, na który chcesz wysłać zapytanie POST
URL = "https://obserwatoriumbrd.pl/app/api/nodes/post_zdarzenia.php"
TOP_RIGHT_LAT = "55.37983570813803"
TOP_RIGHT_LNG = "26.927490234374996"
BOTTOM_LEFT_LAT = "44.90971245959204"
BOTTOM_LEFT_LNG = "10.975341796875007"

# def get_accidents(top_right_lat, top_right_lng, bottom_left_lat, bottom_left_lng):
def get_accidents(start_loc_name, end_loc_name):

    gdf1 = ox.geocode_to_gdf(start_loc_name)
    gdf2 = ox.geocode_to_gdf(end_loc_name)

    min_x = min(gdf1.geometry.total_bounds[0], gdf2.geometry.total_bounds[0])
    min_y = min(gdf1.geometry.total_bounds[1], gdf2.geometry.total_bounds[1])
    max_x = max(gdf1.geometry.total_bounds[2], gdf2.geometry.total_bounds[2])
    max_y = max(gdf1.geometry.total_bounds[3], gdf2.geometry.total_bounds[3])

    top_right_lat = max_y
    top_right_lng = max_x
    bottom_left_lat = min_y
    bottom_left_lng = min_x

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

    # Wysyłanie zapytania POST
    response = requests.post(URL, data=data)

    # Sprawdzanie odpowiedzi serwera
    if response.status_code == 200:
        print('Zapytanie zostało pomyślnie wysłane!')
        response_data = response.json()
        # print('Odpowiedź serwera:', response.json())
        accidents_per_wojewodztwo = response.json()["mapa"]["wojewodztwa"]

        accidents = []
        for wojewodztwo in accidents_per_wojewodztwo:
            for powiat in wojewodztwo["powiaty"]:
                for gmina in powiat["gminy"]:
                    accidents.extend(gmina["zdarzenia_detale"])

        # Zapisanie odpowiedzi do pliku JSON
        with open('osm-generator/maps/accidents.json', 'w') as json_file:
            json.dump(accidents, json_file, indent=4)
        
        print('Dane zostały zapisane do pliku response_data.json')
    else:
        print(f'Błąd: {response.status_code}')
        print('Treść odpowiedzi:', response.text)
