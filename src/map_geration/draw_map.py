from __future__ import absolute_import

import logging
import math
from typing import *

import numpy as np
import cv2
from PIL import Image, ImageDraw

from map_geration.graph import *
from map_geration.map_enums import *
from map_geration.map import is_center_a_map_corner, nearest_map_corner

KERNEL_SIZE = (75, 75)

def pos_processing(image):
    open_cv_image = np.array(image)
    
    _, mask = cv2.threshold(open_cv_image, 1, 255, 0)
    blur_image = cv2.blur(open_cv_image, KERNEL_SIZE)
    open_cv_image = cv2.bitwise_and(blur_image, blur_image, mask=mask)

    return Image.fromarray(open_cv_image)


def convert_map_to_3d_image(
    graph: Graph,
    path:str=""
):
    IMAGE_SIZE = 1000
    image = Image.new('L', (IMAGE_SIZE,) * 2)
    centers = graph.centers

    image_draw = ImageDraw.Draw(image)
    for center in centers:
        if center.terrain_type == TerrainType.OCEAN: continue

        points = np.array([[corner.x, corner.y] for corner in center.corners])
        if is_center_a_map_corner(center):
            points = np.insert(points, -2, nearest_map_corner(points))
            points = points.reshape(-1, 2)
        points = points * IMAGE_SIZE
        points_converted = list(map(tuple, points))
        
        color = math.floor(center.height * 255)
        image_draw.polygon(xy=points_converted, fill=color)
    
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image = pos_processing(image)
    image.save(f"{path}.png")