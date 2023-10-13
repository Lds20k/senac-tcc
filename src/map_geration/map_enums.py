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