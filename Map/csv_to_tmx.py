import csv
import xml.etree.ElementTree as ET

MAP_WIDTH = 120
MAP_HEIGHT = 23
TILE_SIZE = 16

LAYERS = [
    ("Solid", "level1_solid.csv"),
    ("OneWay", "level1_oneway.csv"),
    ("DecorFront", "level1_decorfront.csv"),
    ("DecorBack", "level1_decorback.csv"),
]


def read_csv(path):
    with open(path, newline="") as file:
        return [[int(cell.strip()) for cell in row] for row in csv.reader(file)]


def csv_to_tmx_data(grid):
    output = []

    for row in grid:
        for tile_id in row:
            # CSV của bạn: -1 là ô trống, 0 là tile đầu tiên.
            # TMX: 0 là ô trống, 1 là tile đầu tiên.
            tmx_gid = 0 if tile_id == -1 else tile_id + 1
            output.append(str(tmx_gid))

    return ",".join(output)


map_element = ET.Element(
    "map",
    version="1.10",
    tiledversion="1.12.2",
    orientation="orthogonal",
    renderorder="right-down",
    width=str(MAP_WIDTH),
    height=str(MAP_HEIGHT),
    tilewidth=str(TILE_SIZE),
    tileheight=str(TILE_SIZE),
    infinite="0",
    nextlayerid=str(len(LAYERS) + 1),
    nextobjectid="1",
)

tileset = ET.SubElement(
    map_element,
    "tileset",
    firstgid="1",
    name="Snow platform tileset",
    tilewidth="16",
    tileheight="16",
    tilecount="121",
    columns="11",
)

ET.SubElement(
    tileset,
    "image",
    source="Snow platform tileset.png",
    width="176",
    height="176",
)

for layer_id, (layer_name, csv_name) in enumerate(LAYERS, start=1):
    grid = read_csv(csv_name)

    layer = ET.SubElement(
        map_element,
        "layer",
        id=str(layer_id),
        name=layer_name,
        width=str(MAP_WIDTH),
        height=str(MAP_HEIGHT),
    )

    data = ET.SubElement(layer, "data", encoding="csv")
    data.text = "\n" + csv_to_tmx_data(grid) + "\n"

tree = ET.ElementTree(map_element)
ET.indent(tree, space="  ")
tree.write(
    "level1_recovered.tmx",
    encoding="UTF-8",
    xml_declaration=True,
)

print("Created: level1_recovered.tmx")
