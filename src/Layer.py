import geopandas as gpd
import pandas as pd
import geojson
from sqlalchemy import create_engine
import requests


class Layer:
    def __init__(self, postgres_url: str, gdf: gpd.GeoDataFrame=gpd.GeoDataFrame()) -> None:
        self.engine = create_engine(postgres_url)
        self.gdf = gdf

    def to_postgres(self, table_name: str, schema_name: str) -> None:
        self.gdf.to_postgis(table_name, self.engine, if_exists='replace', schema=schema_name)
    
    def get_response(self, url: str, params: dict) -> requests.Response:
        response = requests.get(url, params=params) 
        if response.status_code == 200:
            return response
        else:
            raise requests.HTTPError(
                f"Failed to retrieve data. Status code: {response.status_code}. Response: {response.text}"
            )
    
    def get_gdf(self, response) -> gpd.GeoDataFrame: 
        return gpd.GeoDataFrame.from_features(geojson.loads(response))