import geopandas as gpd
import pandas as pd
import shapely

from .Layer import Layer
from .Geometry import Geometry

class WFSLayer(Layer):
    def __init__(
        self,
        postgres_url: str,
        wfs_url: str,
        params: dict,
        area: Geometry,
        buffer_distance: int = 0,
        geometry_operand: str = 'within',
        crs: str = 'EPSG:28992'
    ) -> None:
        super().__init__(postgres_url)

        self.wfs_url = wfs_url
        self.crs = crs
        self.params = params
        self.params['bbox'] = area.add_buffer(buffer_distance).bbox_str
        self.features = self.get_features()
        self.gdf = self.filter_features_by_polygon(area.geom_shapely, geometry_operand)
    
    def get_features(self) -> gpd.GeoDataFrame:
        feature_count = self.params['count']
        gdf = pd.DataFrame()
        while feature_count == self.params['count']:
            response = self.get_response(self.wfs_url, self.params)
            response_gdf = self.get_gdf(response.content)
            feature_count = len(response_gdf)
            self.params["startindex"] += self.params['count']
            gdf = pd.concat([gdf, response_gdf])
            print(f"Retrieved {feature_count} features")

        return gpd.GeoDataFrame(gdf, geometry=gdf['geometry'], crs=self.crs)
    
    def filter_features_by_polygon(self, polygon: shapely.geometry.Polygon, geometry_operand: str) -> gpd.GeoDataFrame:
        polygon_gs = gpd.GeoSeries([polygon])

        if geometry_operand == 'within':
            return self.features[self.features.geometry.within(polygon_gs.unary_union)]
        elif geometry_operand == 'intersects':
            return self.features[self.features.geometry.intersects(polygon_gs.unary_union)]
        else:
            raise ValueError(f"Invalid geometry operand: {geometry_operand}. Valid options are 'within' and 'intersects'")