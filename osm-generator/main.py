from omnx import OSMGenerator
from accidents import get_accidents
import json
from add_accidents_volume import main as add_accident_tag
from add_traffic_volume import main as add_traffic_volume_tag

JSON_FILE_PATH = 'osm-generator/maps/accidents.json'
START_LOC_NAME = 'Skała, Poland'
END_LOC_NAME = 'Krzeszowice, Poland'
# START_LOC_NAME = 'Centralna 38, Wielka wieś, Poland'
# END_LOC_NAME = 'Szyce 101, Poland'


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Getting accidents data
get_accidents(START_LOC_NAME, END_LOC_NAME)
accidents_data = load_json_file(JSON_FILE_PATH)

# Creating OSMGenerator object (graph)
OSMGenerator = OSMGenerator(START_LOC_NAME, END_LOC_NAME)

# Adding accidents to nearest edges
for accident in accidents_data:
    nearest_edges = OSMGenerator.nearest_edges(accident["wsp_gps_x"], accident["wsp_gps_y"])
    if type(nearest_edges) is list:
        u, v, k = nearest_edges[0]
    elif type(nearest_edges) is tuple:
        u, v, k = nearest_edges
    else:
        continue

    edge_attrs = OSMGenerator.G.edges[u, v, k]
    print(edge_attrs)
    if 'accidents' in edge_attrs.keys():
        OSMGenerator.G.edges[u, v, k]['accidents'] = str(int(edge_attrs['accidents']) + 1)
    else:
        OSMGenerator.edge_add_atrr((u, v, k), 'accidents', "1")
    print(nearest_edges)
    print(OSMGenerator.G.edges[u, v, k])

# Saving OSM data
OSMGenerator.save_OSM_data("osm-generator/maps/osm-data.osm")
add_accident_tag(OSMGenerator.G)
add_traffic_volume_tag()
