import requests
import json


# URL, na który chcesz wysłać zapytanie POST
URL = "https://obserwatoriumbrd.pl/app/api/nodes/post_zdarzenia.php"
TOP_RIGHT_LAT = "55.37983570813803"
TOP_RIGHT_LNG = "26.927490234374996"
BOTTOM_LEFT_LAT = "44.90971245959204"
BOTTOM_LEFT_LNG = "10.975341796875007"

# Dane, które chcesz wysłać w ciele zapytania
data = {
    "type": "DETAILS",
    "rok[]": ["2023"],
    "wybrane_wojewodztwa[]": "12",
    "groupBy": "DEC",
    "obszar_mapy[topRightCorner][lat]": TOP_RIGHT_LAT,
    "obszar_mapy[topRightCorner][lng]": TOP_RIGHT_LNG,
    "obszar_mapy[bottomLeftCorner][lat]": BOTTOM_LEFT_LAT,
    "obszar_mapy[bottomLeftCorner][lng]": BOTTOM_LEFT_LNG,
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
