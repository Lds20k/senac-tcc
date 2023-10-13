from __future__ import absolute_import

import logging
import math
from typing import *

import numpy as np
from PIL import Image
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from map_geration.graph import *
from map_geration.terrain_enum import *


def set_color():
    pass

def convert_map_to_3d_image(
    graph: Graph,
    path:str=""
):
    image = Image.new('RGB', (1000, 1000))
    pixel_map = image.load()
    centers = graph.centers

    polygons = []
    for center in graph.centers:
        points = []
        for corner in center.corners:
            points.append([corner.x, corner.y])
        
        polygons.append(Polygon(points))
        

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            x_convert = np.divide(x, image.size[0])
            y_convert = np.divide(y, image.size[1])
            point = Point(x_convert, y_convert)

            for i in range(len(polygons)):
                if polygons[i].contains(point):
                    break
            
            if centers[i].terrain_type in (TerrainType.OCEAN, TerrainType.LAKE):
                continue
            
            color = math.floor(centers[i].height * 255)
            pixel_map[x, y] = (color, color, color)

    image.save(f"{path}.png")