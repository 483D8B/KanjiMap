import xml.etree.ElementTree as ET

# Define the namespaces
namespaces = {
    '': 'http://www.w3.org/2000/svg',
    'amcharts': 'http://amcharts.com/ammap'
}

# Register the namespaces with ElementTree
for prefix, uri in namespaces.items():
    ET.register_namespace(prefix, uri)

def merge_svg_maps(source_file, target_file, output_file):
    # Parse the source SVG (with continent data)
    source_tree = ET.parse(source_file)
    source_root = source_tree.getroot()

    # Parse the target SVG (more complete map)
    target_tree = ET.parse(target_file)
    target_root = target_tree.getroot()

    # Create a dictionary to store continent data from the source file
    continent_data = {}
    for path in source_root.findall(".//*[@id]", namespaces):
        continent = path.get('data-continent')
        if continent:
            continent_data[path.get('id')] = continent

    # Update the target SVG with continent data
    for path in target_root.findall(".//*[@id]", namespaces):
        path_id = path.get('id')
        if path_id in continent_data:
            path.set('data-continent', continent_data[path_id])

    # Save the updated target SVG
    target_tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Usage
source_file = 'worldWithContinent.svg'
target_file = 'worldWithAntarcticaHigh.svg'
output_file = 'mergedWorld.svg'

merge_svg_maps(source_file, target_file, output_file)
print(f"Merged SVG saved as {output_file}")