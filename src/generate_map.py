import logging

import cv2
import numpy as np

from map_geration.graph import *
from map_geration.map import convert_map_to_image
from map_geration.terrain import *


def generate(image, points=25):
    logging.info("Gerando diagrama de Voronoi")
    graph = Graph(N=points, iterations=2)

    logging.info("Definindo biomas")
    assign_terrain_from_image(image, graph)

    logging.info("Calculando elevação")
    assign_corner_elevations(graph)
    redistribute_elevations(graph)
    assign_center_elevations(graph)

    logging.info("Gerando imagem")
    fig = convert_map_to_image(graph)
    fig.canvas.draw()
    
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    return img
