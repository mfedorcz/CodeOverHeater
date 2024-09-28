import osmnx as ox
import networkx as nx
from geopy.distance import geodesic


# Pobranie siatki dróg pomiędzy dwoma miejscowosciami
def get_OSM_data(start_loc_name, end_loc_name):
    # geokodowanie miejscowosci
    gdf1 = ox.geocode_to_gdf(start_loc_name)
    gdf2 = ox.geocode_to_gdf(end_loc_name)

    min_x = min(gdf1.geometry.total_bounds[0], gdf2.geometry.total_bounds[0])
    min_y = min(gdf1.geometry.total_bounds[1], gdf2.geometry.total_bounds[1])
    max_x = max(gdf1.geometry.total_bounds[2], gdf2.geometry.total_bounds[2])
    max_y = max(gdf1.geometry.total_bounds[3], gdf2.geometry.total_bounds[3])
    
    bbox = (min_y, max_y, min_x, max_x)
    G = ox.graph_from_bbox(bbox=bbox, network_type='all')
    ox.io.save_graph_xml(G, filepath="./osm-generator/maps/osm-data.osm")

    # Saving the graph to a .png file
    # fig, ax = ox.plot_graph(G, show=False, close=False)
    # fig.savefig(f"./osm-generator/maps/osm-data.png", dpi=500)

    return 0

# Funkcja do obliczania odległości między dwoma punktami
def calculate_distance(point1, point2):
    return geodesic(point1, point2).meters

# Funkcja obliczajaca dlugosc drogi w metrach
def calculate_shortest_path_length(graph, route):
    route_length = 0

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]
        key = 0
        length = graph[u][v][key].get('length', 0)
        # print(f"Krawedz {u} -> {v} ma dlugosc {length} m")
        route_length += length

    return route_length


if __name__ == "__main__":
    print("Test")

    place1 = 'Skała, Poland'
    place2 = 'Krzeszowice, Poland'

    get_OSM_data(place1, place2)
