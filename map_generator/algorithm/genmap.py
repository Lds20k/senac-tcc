from PIL import Image
from src.map import Graph
from src.terrain import (assign_terrain_from_image,
                         assign_terrain_types_to_graph)

IMAGE_PATH = "map_generator/algorithm/image.png"

g = Graph(N=250, iterations=2)

image = Image.open(IMAGE_PATH)
assign_terrain_from_image(image, g)
g.assign_corner_elevations()
g.redistribute_elevations()
g.assign_center_elevations()

g.plot_full_map(plot_type='height')
g.plot_full_map()
g.plot_3d_height_map()
