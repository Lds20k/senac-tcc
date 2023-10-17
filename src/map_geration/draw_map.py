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
BORDER_SIZE = 150

def pos_processing(image):
    img = np.array(image)
    img= cv2.copyMakeBorder(img,BORDER_SIZE,BORDER_SIZE,BORDER_SIZE,BORDER_SIZE,cv2.BORDER_CONSTANT,value=(0,0,0))
    img = cv2.resize(img, (1000, 1000))
    img = cv2.blur(img, KERNEL_SIZE)

    img.astype('int8').tofile("unity/3d_map/Assets/output_3d.raw")

    return Image.fromarray(img)


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