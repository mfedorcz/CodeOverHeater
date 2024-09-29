import osmnx as ox
import xml.etree.ElementTree as ET
from omnx import OSMGenerator

def get_street_names_from_graph(graph):
    """
    Extract street names from the OSMnx graph.
    
    :param graph: OSMnx graph object.
    :return: Set of street names.
    """
    street_names = set()
    for u, v, data in graph.edges(data=True):
        if 'name' in data and 'accidents' in data:
            street_names.add(str(data['name']).lower())
    return street_names

def add_accident_tag(osm_input_path, osm_output_path, street_names):
    """
    Parses the OSM file, adds or modifies the 'accident' tag for ways with matching street names.
    
    :param osm_input_path: Path to the input OSM file.
    :param osm_output_path: Path to save the modified OSM file.
    :param street_names: Set of street names from the OSMnx graph.
    """
    tree = ET.parse(osm_input_path)
    root = tree.getroot()
    
    # Handle namespaces if present
    namespace = ''
    if '}' in root.tag:
        namespace = root.tag.split('}')[0] + '}'
    
    for way in root.findall(f'.//{namespace}way'):
        name_tag = way.find(f'{namespace}tag[@k="name"]')
        if name_tag is not None:
            way_name = name_tag.get('v', '').strip().lower()
            if way_name in street_names:
                # Check if 'accident' tag already exists
                accident_tag = way.find(f'{namespace}tag[@k="accidents"]')
                if accident_tag is None:
                    # Add the new 'accident' tag
                    new_tag = ET.Element('tag', k="accidents", v="1")
                    way.append(new_tag)
                    print(f"Added accident=1 to way ID {way.get('id')}, name: {name_tag.get('v')}")
                else:
                    # Modify the existing 'accident' tag
                    accident_tag.set('v', str(int(accident_tag.get('v', '0')) + 1))
                    print(f"Modified accident tag for way ID {way.get('id')}, name: {name_tag.get('v')}, new value: {accident_tag.get('v')}")
    
    # Write the modified OSM to the output file
    tree.write(osm_output_path, encoding='utf-8', xml_declaration=True)
    print(f"\nModified OSM file saved to {osm_output_path}")

def main(G):
    # Step 1: Load the OSMnx graph and extract street names
    # START_LOC_NAME = 'Skała, Poland'
    # END_LOC_NAME = 'Krzeszowice, Poland'
    # OSMGen = OSMGenerator(START_LOC_NAME, END_LOC_NAME)
    graph = G
    street_names = get_street_names_from_graph(graph)
    print(f"Extracted {len(street_names)} street names from the OSMnx graph.")
    
    # Step 2: Modify the OSM file by adding/modifying 'accident' tags
    input_osm = 'osm-generator/maps/osm-data.osm'      # Path to your input OSM file
    output_osm = 'osm-generator/maps/osm-data.osm'  # Path for the modified OSM file
    add_accident_tag(input_osm, output_osm, street_names)

if __name__ == "__main__":
    main()
