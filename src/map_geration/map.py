from __future__ import absolute_import

import queue
from typing import *

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

from map_geration.graph import *
from map_geration.map_enums import *


def convert_map_to_image(
    graph: Graph,
    plot_type='terrain',
    debug_height=False,
    debug_moisture=False,
    downslope_arrows=False,
    rivers=True,
    path:str=""
):
    """
    Here the next adjustments will be added to create a complete map.
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    polygons = [center_to_polygon(center, plot_type) for center in graph.centers]
    p = PatchCollection(polygons, match_original=True)
    ax.add_collection(p)

    # PLOT HEIGHT LABELS
    if debug_height:
        for corner in graph.corners:
            plt.annotate(
                f"{round(corner.height, 1)}", (corner.x, corner.y), 
                color='white', backgroundcolor='black'
            )
    
    # PLOT MOISTURE LABELS
    if debug_moisture:
        for center in graph.centers:
            plt.annotate(
                f"{round(center.moisture, 1)}", (center.x, center.y), 
                color='white', backgroundcolor='black'
            )

    def drawArrow(A, B, color='darkblue'):
        plt.arrow(
            A[0], A[1], B[0] - A[0], B[1] - A[1],
            head_width=0.015, length_includes_head=True, color=color
        )

    # PLOT DOWNSLOPE ARROWS
    if downslope_arrows:
        for corner in graph.corners:
            if corner.downslope is not None:
                adjacent = corner.adjacent[corner.downslope]
                drawArrow(A=corner.get_cords(), B=adjacent.get_cords())

    # PLOT RIVERS
    if rivers:
        for edge in graph.edges:
            if edge.river > 0:
                beg_x, beg_y = edge.v0.get_cords()
                end_x, end_y = edge.v1.get_cords()
                X = (beg_x, end_x)
                Y = (beg_y, end_y)
                plt.plot(X, Y, linewidth=2+2*np.sqrt(edge.river), color='blue')
                
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.axis('off')
    plt.margins(0,0)

    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    if path != None and path != "":
        plt.savefig(f"{path}.png", bbox_inches = 'tight', pad_inches = 0)

    fig.subplots_adjust(0,0,1,1)
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

def center_to_polygon(center, plot_type):
    """
    Helper function for plotting, which takes the center and returns a polygon which can be plotted.
    """
    if plot_type == 'terrain':
        color = center_to_terrain_color(center)
    elif plot_type == 'moisture':
        color = center_to_moisture_color(center)
    elif plot_type == 'height':
        color = center_to_height_color(center)
    elif plot_type == 'biome':
        color = center_to_biome_color(center)
    else:
        raise AttributeError(f'Unexpected plot type: {plot_type}')
    
    corner_coordinates = np.array([[corner.x, corner.y] for corner in center.corners])
    if is_center_a_map_corner(center):
        corner_coordinates = np.append(corner_coordinates, nearest_map_corner(corner_coordinates))
        corner_coordinates = corner_coordinates.reshape(-1, 2)
    hull = ConvexHull(corner_coordinates)
    vertices = hull.vertices
    vertices = np.append(vertices, vertices[0])
    xs, ys = corner_coordinates[vertices, 0], corner_coordinates[vertices, 1]
    return Polygon(np.c_[xs, ys], facecolor=color)

def center_to_terrain_color(center: Center):
    if center.terrain_type is TerrainType.LAND:
        cmap = matplotlib.cm.get_cmap('Greens')
        color = cmap(1.0 - center.height)
    elif center.terrain_type is TerrainType.OCEAN:
        color = 'deepskyblue'
    elif center.terrain_type is TerrainType.COAST:
        color = 'khaki'
    elif center.terrain_type is TerrainType.LAKE:
        color = 'royalblue'
    else:
        raise AttributeError(f'Unexpected terrain type: {center.terrain_type}')
    return color

def center_to_moisture_color(center: Center):
    if center.terrain_type is TerrainType.LAND or center.terrain_type is TerrainType.COAST:
        cmap = matplotlib.cm.get_cmap('YlGn')
        color = cmap(center.moisture)
    elif center.terrain_type is TerrainType.OCEAN:
        color = 'deepskyblue'
    elif center.terrain_type is TerrainType.LAKE:
        color = 'royalblue'
    else:
        raise AttributeError(f'Unexpected terrain type: {center.terrain_type}')
    return color


def is_center_a_map_corner(center: Center):
    """
    Function returns True only when a center is in a one of 4 corners of the [0, 1]^2.
    """
    corner_coordinates = np.array([[corner.x, corner.y] for corner in center.corners])
    xs, ys = corner_coordinates.T
    return (np.any(xs == 0) or np.any(xs == 1)) and (np.any(ys == 0) or np.any(ys == 1))

def center_to_height_color(center: Center):
    if center.terrain_type is TerrainType.LAND or center.terrain_type is TerrainType.COAST:
        cmap = matplotlib.cm.get_cmap('Greens')
        color = cmap(1.0 - center.height)
    elif center.terrain_type is TerrainType.OCEAN:
        color = 'deepskyblue'
    elif center.terrain_type is TerrainType.LAKE:
        color = 'royalblue'
    else:
        raise AttributeError(f'Unexpected terrain type: {center.terrain_type}')
    return color

def center_to_biome_color(center: Center):
    if center.biome == BiomeType.OCEAN: color = 'deepskyblue'
    elif center.biome == BiomeType.LAKE: color = 'royalblue'
    elif center.biome == BiomeType.COAST: color = 'khaki'
    elif center.biome == BiomeType.SNOW: color = (248/255, 248/255, 248/255)
    elif center.biome == BiomeType.TUNDRA: color = (227/255, 228/255, 224/255)
    elif center.biome == BiomeType.BARE: color = (200/255, 198/255, 195/255)
    elif center.biome == BiomeType.SCORCHED: color = (123/255, 123/255, 123/255)
    elif center.biome == BiomeType.TAIGA: color = (188/255, 214/255, 144/255)
    elif center.biome == BiomeType.SHRUBLAND: color = (211/255, 224/255, 150/255)
    elif center.biome == BiomeType.TEMPERATE_DESERT: color = (208/255, 203/255, 165/255)
    elif center.biome == BiomeType.TEMPERATE_RAIN_FOREST: color = (55/255, 111/255, 44/255)
    elif center.biome == BiomeType.TEMPERATE_DECIDOUS_FOREST: color = (123/255, 164/255, 91/255)
    elif center.biome == BiomeType.GRASSLAND: color = (160/255, 195/255, 121/255)
    elif center.biome == BiomeType.TROPICAL_RAIN_FOREST: color = (32/255, 78/255, 23/255)
    elif center.biome == BiomeType.TROPICAL_SEASONAL_FOREST: color = (91/255, 124/255, 64/255)
    elif center.biome == BiomeType.SUBTROPICAL_DESERT: color = (230/255, 225/255, 168/255)
    elif center.biome == BiomeType.MARSH: color = (148/255, 217/255, 200/255)
    elif center.biome == BiomeType.ICE: color = 'lightcyan'
    elif center.biome == BiomeType.DEEPOCEAN: color = 'dodgerblue'
    else:
        raise AttributeError(f'Unexpected biome type: {center.biome}')
    return color
 
 
def nearest_map_corner(corner_coordinates):
    """
    Assumes that a coordinates belong to the corner being in the corner of the map.
    """
    if np.any(corner_coordinates[:, 0] == 0):
        if np.any(corner_coordinates[:, 1] == 0):
            return [0, 0]
        else:
            return [0, 1]
    else:
        if np.any(corner_coordinates[:, 1] == 0):
            return [1, 0]
        else:
            return [1, 1]
      
def create_rivers(graph: Graph, n, min_height):
    """
    Rivers flow from high elevations down to the coast.
    Having elevations that always increase away from the coast means
    that there’s no local minima that complicate river generation

    This function creates `n` rivers. It draws a random start position for
    each river that is >= min_height.
    Rivers are saved in Edge.

    :param n: number of rivers
    :param min_height: minimum height of the begining of the river
    """

    # reset previous rivers
    for edge in graph.edges:
        edge.river = 0

    def suitable_for_river(c: Corner):
        good_tile = c.terrain_type == TerrainType.LAND or c.terrain_type == TerrainType.COAST
        neighbour_tiles = [nei.terrain_type for nei in c.adjacent]
        good_neighbours = [
            nt == TerrainType.LAND or nt == TerrainType.COAST
            for nt in neighbour_tiles
        ]
        touches_tiles = [center.terrain_type for center in c.touches]
        good_touches = [
            tt == TerrainType.LAND or tt == TerrainType.COAST
            for tt in touches_tiles
        ]

        return good_tile and all(good_neighbours) and all(good_touches)
    
    for corner in graph.corners:
        if corner.terrain_type == TerrainType.LAND or corner.terrain_type == TerrainType.COAST:
            neighbors_heights = [nei.height for nei in corner.adjacent]
            lowest = min(neighbors_heights)
            lowest_id = neighbors_heights.index(lowest)
            corner.downslope = lowest_id

    good_beginnings = [
        c for c in graph.corners
        if ((c.terrain_type == TerrainType.LAND or c.terrain_type == TerrainType.COAST) \
            and c.height >= min_height) \
            or (any([cent.terrain_type == TerrainType.LAKE for cent in c.touches]) \
            and c.terrain_type != TerrainType.LAKE)
    ]

    if len(good_beginnings) < n:
        heighest = max([
            c.height for c in graph.corners 
            if c.terrain_type == TerrainType.LAND or c.terrain_type == TerrainType.COAST
        ])
        print(f'Found only {len(good_beginnings)} river beginnings. Lower min_height.')
        print(f'min_height={min_height} | Heighest mountain has height={heighest}')
        return

    start_corners = np.random.choice(good_beginnings, n, replace=False)
    for corner in start_corners:
        while True:
            if corner.downslope is None or not suitable_for_river(corner):
                break
            
            next_corner = corner.adjacent[corner.downslope]
            if next_corner.terrain_type != TerrainType.LAND and next_corner.terrain_type != TerrainType.COAST:
                break

            mutable_edge = graph.find_edge_using_corners(corner, next_corner)

            # Notice that this line will modify this object in self.edges
            mutable_edge.river += 1
            corner = next_corner
            
    assign_corner_river(graph)

def assign_corner_river(graph: Graph):
    for edge in graph.edges:
        if edge.river > 0:
            edge.v0.river = max(edge.v0.river, edge.river)
            edge.v1.river = max(edge.v0.river, edge.river)

def assign_moisture(graph: Graph, redistribute=True, distance_decay=0.9, river_weight=0.25, lake_value=1.0, ocean_value=1.0):
    assign_corner_moisture(distance_decay, river_weight, lake_value, ocean_value)
    
    for center in graph.centers:
        if center.terrain_type == TerrainType.LAND or center.terrain_type == TerrainType.COAST:
            center.moisture = np.mean(np.array([min(1.0, corner.moisture) for corner in center.corners]))
            
    if redistribute:
        redistribute_moisture(graph)
   

def assign_corner_moisture(graph: Graph, distance_decay, river_weight, lake_value, ocean_value):
    q = queue.Queue()
    for corner in graph.corners:
        if corner.river > 0:
            corner.moisture = max(1.0, min(3.0, river_weight*corner.river))
        if any([center.terrain_type == TerrainType.LAKE for center in corner.touches]):
            corner.moisture = max(lake_value, corner.moisture)
        if corner.moisture > 0:
            q.put(corner)

    while not q.empty():
        corner = q.get()

        new_moisture = distance_decay*corner.moisture
        for nei_corner in corner.adjacent:
            if new_moisture > nei_corner.moisture:
                nei_corner.moisture = new_moisture
                q.put(nei_corner)

    for corner in graph.corners:
        if any([center.terrain_type == TerrainType.OCEAN for center in corner.touches]):
            corner.moisture = max(ocean_value, corner.moisture)

def redistribute_moisture(graph: Graph):
    sorted_centers = sorted(graph.centers, key = lambda c: c.moisture)
    for i, center in enumerate(sorted_centers):
        center.moisture = i / (len(sorted_centers)-1)
     
def assign_biomes(graph: Graph):
        for center in graph.centers:
            if center.terrain_type == TerrainType.COAST:
                center.biome = BiomeType.COAST
            elif center.terrain_type == TerrainType.OCEAN:
                if any([n.terrain_type == TerrainType.COAST for n in center.neighbors]):
                    center.biome = BiomeType.OCEAN
                else:
                    center.biome = BiomeType.DEEPOCEAN
            elif center.terrain_type == TerrainType.LAKE:
                if center.height < 0.2:
                    center.biome = BiomeType.MARSH
                elif center.height > 0.9:
                    center.biome = BiomeType.ICE
                else:
                    center.biome = BiomeType.LAKE
            else:
                if center.height > 0.87:
                    if center.moisture > 0.66:
                        center.biome = BiomeType.SNOW
                    elif center.moisture > 0.44:
                        center.biome = BiomeType.TUNDRA
                    elif center.moisture > 0.22:
                        center.biome = BiomeType.BARE
                    else:
                        center.biome = BiomeType.SCORCHED
                elif center.height > 0.66:
                    if center.moisture > 0.66:
                        center.biome = BiomeType.TAIGA
                    elif center.moisture > 0.33:
                        center.biome = BiomeType.SHRUBLAND
                    else:
                        center.biome = BiomeType.TEMPERATE_DESERT
                elif center.height > 0.4:
                    if center.moisture > 0.8:
                        center.biome = BiomeType.TEMPERATE_RAIN_FOREST
                    elif center.moisture > 0.6:
                        center.biome = BiomeType.TEMPERATE_DECIDOUS_FOREST
                    elif center.moisture > 0.3:
                        center.biome = BiomeType.GRASSLAND
                    else:
                        center.biome = BiomeType.TEMPERATE_DESERT
                else:
                    if center.moisture > 0.66:
                        center.biome = BiomeType.TROPICAL_RAIN_FOREST
                    elif center.moisture > 0.45:
                        center.biome = BiomeType.TROPICAL_SEASONAL_FOREST
                    elif center.moisture > 0.3:
                        center.biome = BiomeType.GRASSLAND
                    else:
                        center.biome = BiomeType.SUBTROPICAL_DESERT
