import shapely
import geopandas as gpd
import shapely.ops
import pyproj

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
    
    def reproject(self, from_crs: str='EPSG:28992', to_crs: str='EPSG:4326'):
        if not isinstance(self.geom_shapely, shapely.geometry.Polygon):
            raise TypeError("Geometry must be a Polygon to reproject.")
        
        transformer = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True)
        transformed_coords = [transformer.transform(x, y) for x, y in self.geom_shapely.exterior.coords]
        self.geom_shapely = shapely.geometry.Polygon(transformed_coords)
        self.set_properties()
        
        return self