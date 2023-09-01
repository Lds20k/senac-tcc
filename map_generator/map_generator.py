from __future__ import absolute_import

import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from src.map import Graph
from src.terrain import assign_terrain_types_to_graph
from src.voronoi import VoronoiPolygons

voronoi_polygons = VoronoiPolygons(N=25)

new_regions, new_vertices, new_centroids = VoronoiPolygons.find_new_polygons(
    vor=voronoi_polygons.vor
)

neighbors, intersecions =  VoronoiPolygons.generate_neighbours(
    vor=voronoi_polygons.vor,
    regions=new_regions,
    vertices=new_vertices,
)

vorpoints, points, new_vertices, new_regions, neighbors, intersecions \
    = voronoi_polygons.generate_Voronoi(iterations=2)

voronoi_polygons = VoronoiPolygons(N=100)

vorpoints, points, new_vertices, new_regions, neighbors, intersecions \
    = voronoi_polygons.generate_Voronoi(iterations=2)

g = Graph(N=250, iterations=2)


assign_terrain_types_to_graph(graph=g, min_water_ratio=0.25)

g.assign_corner_elevations()
g.redistribute_elevations()
g.assign_center_elevations()

g.plot_full_map(plot_type='height', debug_height=False)
