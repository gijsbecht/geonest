import osmnx as ox
import geopandas as gpd
from .Layer import Layer
from .Geometry import Geometry  

class OSMLayer(Layer):
    def __init__(self, postgres_url: str, tags: dict, area: Geometry) -> None:
        super().__init__(postgres_url)

        self.tags = tags
        self.area = area
        self.get_geometries()

    def get_geometries(self):
        try:
            self.gdf = ox.features_from_polygon(self.area.reproject().geom_shapely, tags=self.tags)
        except:
            self.gdf  = gpd.GeoDataFrame()