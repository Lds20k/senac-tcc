from enum import Enum

class TerrainType(Enum):
    OCEAN = 1
    LAND = 2
    LAKE = 3
    COAST = 4

class BiomeType(Enum):
    OCEAN = 1
    LAKE = 2
    COAST = 3
    SNOW = 4
    TUNDRA = 5
    BARE = 6
    SCORCHED = 7
    TAIGA = 8
    SHRUBLAND = 9
    TEMPERATE_DESERT = 10
    TEMPERATE_RAIN_FOREST = 11
    TEMPERATE_DECIDOUS_FOREST = 12
    GRASSLAND = 13
    TROPICAL_RAIN_FOREST = 14
    TROPICAL_SEASONAL_FOREST = 15
    SUBTROPICAL_DESERT = 16
    MARSH = 17
    ICE = 18
    DEEPOCEAN = 19

def height_color(height, color):
    return (height * 10) + color

terrainColors = {
    TerrainType.OCEAN: lambda height: [255, 191, 0],
    TerrainType.LAND: lambda height: height_color(height, [50, 205, 50]),
    TerrainType.LAKE: lambda height: [225, 105, 65],
    TerrainType.COAST: lambda height: [145, 176, 195]
}

biomeColors = {
    BiomeType.OCEAN: [255, 191, 0],
    BiomeType.LAKE: [225, 105, 65],
    BiomeType.COAST: [199, 232, 252],
    BiomeType.SNOW: [248, 248, 248],
    BiomeType.TUNDRA: [224, 228, 227],
    BiomeType.BARE: [195, 198, 200],
    BiomeType.SCORCHED: [123, 123, 123],
    BiomeType.TAIGA: [144, 214, 188],
    BiomeType.SHRUBLAND: [150, 224, 211],
    BiomeType.TEMPERATE_DESERT: [165, 203, 208],
    BiomeType.TEMPERATE_RAIN_FOREST: [44, 111, 55],
    BiomeType.TEMPERATE_DECIDOUS_FOREST: [91, 164, 123],
    BiomeType.GRASSLAND: [121, 195, 160],
    BiomeType.TROPICAL_RAIN_FOREST: [23, 78, 32],
    BiomeType.TROPICAL_SEASONAL_FOREST: [64, 124, 91],
    BiomeType.SUBTROPICAL_DESERT: [168, 225, 230],
    BiomeType.MARSH: [200, 217, 148],
    BiomeType.ICE: [255, 255, 224],
    BiomeType.DEEPOCEAN: [255, 144, 30]
}