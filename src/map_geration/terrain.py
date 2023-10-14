from __future__ import absolute_import

import logging
import math
import queue

import numpy as np
from map_geration.graph import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
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

    logging.info("Convertendo poligonos")
    polygons = []
    for center in graph.centers:
        points = []
        for corner in center.corners:
            points.append([corner.x, corner.y])
            
        polygons.append(Polygon(points))

    image = image.convert("RGB")

    logging.info("Assinando poligonos como LAND")
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixel = image.getpixel((x, y))
            if(0 in pixel): continue

            x_convert = np.divide(x, image.size[0])
            y_convert = np.divide(image.size[1] - y, image.size[1])
            point = Point(x_convert, y_convert)
            for i in range(len(polygons)):
                if polygons[i].contains(point):
                    break
            
            center: Center = graph.centers[i]
            center.terrain_type = TerrainType.LAND
            for corner in center.corners: corner.terrain_type = TerrainType.LAND

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
  