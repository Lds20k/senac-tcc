import logging
import random
from enum import Enum

from map_geration.draw_map import convert_map_to_3d_image
from map_geration.graph import *
from map_geration.map import *
from map_geration.terrain import *

class OUTPUT(Enum):
    BOTH = 1
    MAP_2D = 2
    MAP_3D = 3
    MAP_BIOME = 4


def generate(image, points=25, mode = 3, output: OUTPUT = OUTPUT.BOTH, kernel_size=80, border_size = 60):
    logging.info("Gerando diagrama de Voronoi")
    graph = Graph(N=points, iterations=2)

    logging.info("Definindo biomas")
    assign_terrain_from_image(image, graph)

    logging.info("Calculando elevação")
    assign_corner_elevations(graph)
    redistribute_elevations(graph)
    assign_center_elevations(graph)

    if output == OUTPUT.MAP_BIOME:
        logging.info("Gerando biomas")

        loc = {}
        exec(f"number_of_rivers = {math.floor(points/8)} {random.choice(['+', '-'])} {math.floor(points/16)}", globals(), loc)
        number_of_rivers = loc['number_of_rivers']

        logging.info(f"Sera gerado um total de {number_of_rivers} rios")
        create_rivers(graph, 10, 0.6)

        logging.info(f"Calculando umidade")
        assign_moisture(graph)

        logging.info(f"Selecionando biomas")
        assign_biomes(graph)

        logging.info(f"Gerando imagem bioma")
        return convert_map_to_image(
            graph,
            path="output_biomes",
            plot_type='biome',
            debug_height=False, 
            debug_moisture=False, 
            downslope_arrows=False, 
            rivers=True
        )

    if not output == OUTPUT.MAP_2D:
        logging.info("Gerando imagem 3D")
        convert_map_to_3d_image(graph, mode=mode, kernel_size=kernel_size, path="output_3d")

    if not output == OUTPUT.MAP_3D:
        logging.info("Gerando imagem 2D")
        return convert_map_to_image(graph, path="output_2d", border_size=border_size)
