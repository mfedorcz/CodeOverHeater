import xml.etree.ElementTree as ET
import json
import re

def extract_street_name(description):
    """
    Extracts the street name from the description.
    Assumes the street name is before the first parenthesis.
    Example: "Poznańska (DK 92)" -> "Poznańska"
    """
    match = re.match(r'([^()]+)', description)
    if match:
        return match.group(1).strip()
    return description.strip()

def build_street_jamfactor_map(json_path):
    """
    Parses the JSON file and builds a mapping from street names to jamFactor.
    
    :param json_path: Path to the JSON file.
    :return: Dictionary mapping street names to jamFactor.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    street_jamfactor = {}
    for result in data.get('results', []):
        location = result.get('location', {})
        description = location.get('description', '')
        street_name = extract_street_name(description)
        
        current_flow = result.get('currentFlow', {})
        jam_factor = current_flow.get('jamFactor', None)
        
        if street_name and jam_factor is not None:
            street_jamfactor[street_name.lower()] = str(jam_factor)  # Convert to string for XML
    return street_jamfactor

def add_traffic_volume_tag(osm_input_path, osm_output_path, street_jamfactor):
    """
    Parses the OSM file, adds traffic_volume tag to ways with matching street names.
    
    :param osm_input_path: Path to the input OSM file.
    :param osm_output_path: Path to save the modified OSM file.
    :param street_jamfactor: Dictionary mapping street names to jamFactor.
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
            jam_factor = street_jamfactor.get(way_name)
            if jam_factor:
                # Check if 'traffic_volume' tag already exists
                existing_traffic_tag = way.find(f'{namespace}tag[@k="traffic_volume"]')
                if existing_traffic_tag is None:
                    # Add the new 'traffic_volume' tag
                    new_tag = ET.Element('tag', k="traffic_volume", v=jam_factor)
                    way.append(new_tag)
                    print(f"Added traffic_volume={jam_factor} to way ID {way.get('id')}, name: {name_tag.get('v')}")
                else:
                    print(f"traffic_volume tag already exists for way ID {way.get('id')}, name: {name_tag.get('v')}")
    
    # Write the modified OSM to the output file
    tree.write(osm_output_path, encoding='utf-8', xml_declaration=True)
    print(f"\nModified OSM file saved to {osm_output_path}")

def main():
    # Define file paths
    input_osm = './osm-files/osm-data.osm'          # Path to your input OSM file
    input_json = 'traffic_data.json'         # Path to your JSON file
    output_osm = './osrm-data/osm-data.osm'        # Path for the modified OSM file
    
    # Step 1: Build the street to jamFactor mapping
    street_jamfactor = build_street_jamfactor_map(input_json)
    # print(street_jamfactor)
    print(f"Built mapping for {len(street_jamfactor)} streets from JSON.")
    
    # Step 2: Modify the OSM file
    add_traffic_volume_tag(input_osm, output_osm, street_jamfactor)

if __name__ == "__main__":
    main()
