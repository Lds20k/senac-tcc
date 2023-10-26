import logging
from enum import Enum

from map_geration.graph import *
from map_geration.map import convert_map_to_image
from map_geration.draw_map import  convert_map_to_3d_image
from map_geration.terrain import *

class OUTPUT(Enum):
    BOTH = 1
    MAP_2D = 2
    MAP_3D = 3


def generate(image, points=25, mode = 3, output: OUTPUT = OUTPUT.BOTH, kernel_size=None, border_size = 0):
    logging.info("Gerando diagrama de Voronoi")
    graph = Graph(N=points, iterations=2)

    logging.info("Definindo biomas")
    assign_terrain_from_image(image, graph)

    logging.info("Calculando elevação")
    assign_corner_elevations(graph)
    redistribute_elevations(graph)
    assign_center_elevations(graph)

    if not output == OUTPUT.MAP_2D:
        logging.info("Gerando imagem 3D")
        convert_map_to_3d_image(graph, mode=mode, kernel_size=kernel_size, path="output_3d")

    if not output == OUTPUT.MAP_3D:
        logging.info("Gerando imagem 2D")
        return convert_map_to_image(graph, path="output_2d", border_size=border_size)
