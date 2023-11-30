from __future__ import absolute_import

import logging
import math
import queue

import numpy as np
import cv2

from map_geration.graph import *
from map_geration.map import is_center_a_map_corner, nearest_map_corner
from map_geration.map_enums import *

def assign_terrain_from_image(image, graph: Graph):

    def set_cost(center: Center, neighbor: Center):
        center.terrain_type = TerrainType.COAST

        for corner_n in neighbor.corners:
            for corner_c in center.corners:
                if corner_n == corner_c:
                    corner_c.terrain_type = TerrainType.COAST

    def generate_coast(center: Center, visited: list=[]):
        if center in visited: return
        visited.append(center)
        
        for neighbor in center.neighbors:
            if neighbor.terrain_type == TerrainType.OCEAN:
                set_cost(center, neighbor)
                continue
            
            generate_coast(neighbor)

    logging.info("Assinando poligonos como LAND")
    image_size = image.shape[1]

    flag = True
    index = 0
    for center in graph.centers:
        image_aux = np.zeros((image_size, image_size, 3), dtype=np.uint8)

        points = np.array([[corner.x, corner.y] for corner in center.corners])
        if is_center_a_map_corner(center):
            points = np.insert(points, -2, nearest_map_corner(points))
            points = points.reshape(-1, 2)
        points = points * image_size
        points = points.astype(np.int32)
        points = points.reshape((-1, 1, 2))

        cv2.fillPoly(image_aux, [points], [1, 1, 1])
        mask = cv2.inRange(image_aux, (1, 1, 1), (1, 1, 1))
        result = cv2.bitwise_and(image, image, mask=mask)

        if(np.sum(result) > 0):
            center.terrain_type = TerrainType.LAND
            if flag:
                cv2.imwrite(f"src/output/mask/mask_{index}.png", mask)
                cv2.imwrite(f"src/output/result/result_{index}.png", result)
                index += 1

    logging.info("Procurando o primeiro poligono LAND")
    a_land_center = graph.centers[0]
    for center in graph.centers:
        if center.terrain_type == TerrainType.LAND:
            a_land_center = center
            break
    
    logging.info("Marcando poligonos como COAST")
    generate_coast(a_land_center)

def assign_corner_elevations(graph: Graph, borders=None):
    '''
    Runs BFS from every border corner to calculate height of every corner. 
    '''
    for corner in graph.corners:
        corner.height = float('inf')
    border_corners = [
        corner for corner in graph.corners 
        if corner.x == 0 or corner.x == 1 or corner.y == 0 or corner.y == 1
    ]
    for border in border_corners:
        q = queue.Queue()
        border.height = 0
        q.put(border)
        while not q.empty():
            current_corner = q.get()
            for adjacent_corner in current_corner.adjacent:
                new_elevation = current_corner.height + 0.01
                if (current_corner.terrain_type != TerrainType.OCEAN and
                    current_corner.terrain_type != TerrainType.LAKE and
                    adjacent_corner.terrain_type != TerrainType.OCEAN and
                    adjacent_corner.terrain_type != TerrainType.LAKE):
                    new_elevation += 1
                if adjacent_corner.height > new_elevation:
                    adjacent_corner.height= new_elevation
                    q.put(adjacent_corner)
    for corner in graph.corners:
        if corner.terrain_type == TerrainType.LAKE:
            corner.height -= 1
            
def assign_center_elevations(graph: Graph):
    '''
    Calculates height for every center by taking the mean height of corners that surround it.
    '''
    for center in graph.centers:
        corners_heights = [corner.height for corner in center.corners]
        if center.terrain_type == TerrainType.LAKE:
            center.height = min(corners_heights)
        else:
            center.height = sum(corners_heights) / len(corners_heights)
        
def redistribute_elevations(graph: Graph, scale_factor = 1.1):
    sorted_corners = sorted(graph.corners, key = lambda c: c.height)
    for i, corner in enumerate(sorted_corners):
        y = i / len(sorted_corners)
        x = math.sqrt(scale_factor) - math.sqrt(scale_factor * (1 - y))
        corner.height = x
  