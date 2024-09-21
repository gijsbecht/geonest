import shapely
import geopandas as gpd

class Geometry:
    def __init__(self, geom_wkt):
        self.geom_wkt = geom_wkt
        self.geom_shapely = shapely.from_wkt(self.geom_wkt)
        self.set_properties()
    
    def set_properties(self):
        self.bbox = self.geom_shapely.bounds
        self.bbox_str = ",".join(map(str, self.bbox))
        self.bbox_shapely = shapely.geometry.box(*self.bbox)
        self.gdf = gpd.GeoDataFrame(geometry=[self.geom_shapely], crs='EPSG:28992')
    
    def add_buffer(self, buffer_distance: int):
        if buffer_distance == 0:
            return self
        
        self.geom_shapely = shapely.buffer(self.geom_shapely, buffer_distance)
        self.set_properties()
        
        return self