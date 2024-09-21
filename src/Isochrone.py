import geopandas as gpd
import geojson
import shapely
import pandas as pd

from .Layer import Layer
from .Geometry import Geometry  

class Isochrone(Layer):
    def __init__(
        self,
        postgres_url: str,
        contours_minutes: list[int],
        api_key: str,
        points: gpd.GeoDataFrame,
        mode: str='driving-traffic'
    ) -> None:
        super().__init__(postgres_url)

        self.url = f'https://api.mapbox.com/isochrone/v1/mapbox/{mode}'
        self.params = {
            'polygons': 'true',
            'denoise': 1,
            'access_token': api_key
        }
        self.contours_minutes = contours_minutes
        self.points = points
        self.get_features()
    
    def _get_isochrones(self, minutes: int) -> gpd.GeoDataFrame:
        for _, feature in self.points.iterrows():
            if isinstance(feature.geometry, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)):
                point = feature.geometry.centroid
            else:
                point = feature.geometry

            coordinates = f'{point.x},{point.y}'
            url = self.url + '/' + coordinates
            response = self.get_response(url, self.params)
            response_gdf = self.get_gdf(response.text)
            response_gdf.crs = 'EPSG:4326'
            joined_gdf = pd.concat(
                [
                    response_gdf.reset_index(drop=True),
                    feature.drop('geometry').to_frame().T.reset_index(drop=True)
                ], 
                axis=1
            )
            self.gdf = pd.concat([self.gdf, joined_gdf])

    def get_features(self):
        for minutes in self.contours_minutes:
            self.params['contours_minutes'] = minutes
            self._get_isochrones(minutes)


        