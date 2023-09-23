from typing import *

from map_geration.terrain_enum import BiomeType, TerrainType

from map_geration.voronoi import VoronoiPolygons


class Center:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.borders = []
        self.corners = []
        self.terrain_type = TerrainType.OCEAN
        self.biome = BiomeType.OCEAN
        self.height = 0
        self.moisture = 0

class Corner:
    def __init__(self, x, y):
        """
        :param x:
        :param y:
        :param:
        :param:
        :param:
        :param:
        :param:
        :param height: height of the corner
        :param downslope: index of the adjacent corner with the lowest height
        :param:
        :param:
        """
        self.x = x
        self.y = y
        self.touches = []
        self.protrudes = []
        self.adjacent = []
        self.terrain_type = TerrainType.LAND
        self.height = 0
        self.downslope = None
        self.river = 0
        self.moisture = 0

    def get_cords(self) -> Tuple[float, float]:
        return self.x, self.y


class Edge:
    def __init__(self, center1, center2, corner1, corner2):
        self.d0 = center1
        self.d1 = center2
        self.v0 = corner1
        self.v1 = corner2
        self.river = 0

    def is_edge_to_map_end(self):
        """
        Function defining, whether the edge is connected to the end of the map.
        """
        corner_coordinates = [self.v0.x, self.v0.y, self.v1.x, self.v1.y]
        return any([corner_coordinate in [0, 1] for corner_coordinate in corner_coordinates])


class Graph:
    center: Center
    corners: Corner
    edges: Edge
    corners_to_edge: dict

    def __init__(self, N: int = 25, iterations: int = 2):
        voronoi_polygons = VoronoiPolygons(N=N)
        self._points, self._centroids, self._vertices, self._regions, \
            self._neighbors, self._intersecions \
            = voronoi_polygons.generate_Voronoi(iterations=iterations)

        self.centers, self.corners, self.edges, self.corners_to_edge = self.initialize_graph()
        # Notice that corners_to_edge.values() and edges are the same objects

    def initialize_graph(self):
        # creating center object for each point
        centers = []
        for p in self._points:
            center = Center(p[0], p[1])
            centers.append(center)

        # creating corner object for each vertex
        corners = []
        for v in self._vertices:
            corner = Corner(v[0], v[1])
            corners.append(corner)

        corners_inside = [
                (0 <= corner.x <= 1) and
                (0 <= corner.y <= 1) and
                ((0 != corner.x and 1 != corner.x) or
                (0 != corner.y and 1 != corner.y))
            for corner in corners]

        # setting neighbors and corners lists for each center
        for i, c in enumerate(centers):
            c.neighbors = [centers[k] for k in self._neighbors[i]]
            c.corners = [corners[k] for k in self._regions[i] if corners_inside[k]]

        for i, corners_list in enumerate(self._regions):
            for cor in corners_list:
                corners[cor].touches.append(centers[i])

        edges = {}
        for c1, neighbours_list in enumerate(self._neighbors):
            for i, c2 in enumerate(neighbours_list):
                if (c1, c2) in edges or (c2, c1) in edges:
                    continue

                cor1, cor2 = self._intersecions[c1][i]
                edge = Edge(centers[c1], centers[c2], corners[cor1], corners[cor2])
                centers[c1].borders.append(edge)
                centers[c2].borders.append(edge)
                corners[cor1].protrudes.append(edge)
                corners[cor2].protrudes.append(edge)
                corners[cor1].adjacent.append(corners[cor2])
                corners[cor2].adjacent.append(corners[cor1])

                edges[(c1, c2)] = edge

        corners = [corner for i, corner in enumerate(corners) if corners_inside[i]]
        edges_values = list(edges.values())

        return centers, corners, edges_values, edges

    def find_edge_using_corners(self, c1: Corner, c2: Corner) -> Edge:
        """
        Finds Edge object represented by the given corners.
        """
        def same_corner(c1, c2):
            return c1.x == c2.x and c1.y == c2.y

        for edge in self.edges:
            if (same_corner(edge.v0, c1) and same_corner(edge.v1, c2)) \
                or (same_corner(edge.v0, c2) and same_corner(edge.v1, c1)):
                return edge

        raise ValueError('Edge with given corners doesnt exist.')
