import osmnx as ox
import networkx as nx
from geopy.distance import geodesic


# Klasa generująca plik OSM z dodanymi atrybutami
class OSMGenerator:
    def __init__(self, start_loc_name, end_loc_name):
        self.start_loc_name = start_loc_name
        self.end_loc_name = end_loc_name
        self.get_OSM_data()

    def get_OSM_data(self):
        gdf1 = ox.geocode_to_gdf(self.start_loc_name)
        gdf2 = ox.geocode_to_gdf(self.end_loc_name)

        min_x = min(gdf1.geometry.total_bounds[0], gdf2.geometry.total_bounds[0])
        min_y = min(gdf1.geometry.total_bounds[1], gdf2.geometry.total_bounds[1])
        max_x = max(gdf1.geometry.total_bounds[2], gdf2.geometry.total_bounds[2])
        max_y = max(gdf1.geometry.total_bounds[3], gdf2.geometry.total_bounds[3])
        
        bbox = (min_y, max_y, min_x, max_x)
        self.G = ox.graph_from_bbox(bbox=bbox, network_type='all')
        return 0
    
    def save_OSM_data(self, file_path):
        ox.io.save_graph_xml(self.G, filepath=file_path)
        return 0

    def save_OSM_data_png(self, file_path):
        fig, ax = ox.plot_graph(self.G, show=False, close=False)
        fig.savefig(file_path, dpi=500)
        return 0
    
    def edge_add_atrr(self, edge, attr_name, attr_value, key=0):
        self.G.edges[edge[0], edge[1], key][attr_name] = attr_value
        return 0


if __name__ == "__main__":
    print("Test")

    # place1 = 'Skała, Poland'
    # place2 = 'Krzeszowice, Poland'
    place1 = 'Centralna 38, Wielka wieś, Poland'
    place2 = 'Szyce 101, Poland'

    OSMGenerator = OSMGenerator(place1, place2)
    OSMGenerator.save_OSM_data("osm-generator/maps/osm-data.osm")
    OSMGenerator.save_OSM_data_png("osm-generator/maps/data.png")
    G = OSMGenerator.G

    # Wyświetlanie krawędzi z atrybutami
    i = 0
    for edge in G.edges(data=True):
        if i == 5:
            break
        print(edge)
        OSMGenerator.edge_add_atrr(edge, 'test', 'test')
        print(edge)
        i += 1
