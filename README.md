# GeoNest

GeoNest is a geospatial data extraction and processing tool for determining the best place to live in The Netherlands. Recommended use in combination with a (local) PostgreSQL database with the POSTGIS extension installed, use QGIS for data visualisation.

## Installation Guide

Follow these steps to set up GeoNest:

1. **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install PostgreSQL with PostGIS extension:**
    - Visit the [official PostgreSQL website](https://www.postgresql.org/download/) to download the installer for your operating system.
    - Run the installer and follow the on-screen instructions to complete the installation.
    - Create geonest database
      ```sh
      createdb geonest
      ```
    - Enable the PostGIS extension in your PostgreSQL database:
      ```sql
      CREATE EXTENSION postgis;
      ```

6. **Add a `.env` file:**
    Create a `.env` file in the root directory of the project and add the following environment variables:
    ```
    POSTGRES_URL=your_postgres_url  (e.g. postgresql://postgres:postgres@localhost:5432/geonest)
    MAPBOX_API_KEY=your_mapbox_api_key
    ```

You should now have GeoNest up and running!

## How to use

1. **Get data:**
    Use the `get_data.ipynb` notebook to extract all the data required for your analysis. The following options are available:
    - Load local data from `geopackage`.
    - Load data from WFS Layer.
    - Load data from Open Streetmap (OSM).

2. **(Optional) Compute Isochrones:**
    An isochrone map in geography and urban planning is a map that depicts the area accessible from a point within a certain time threshold. A Mapbox API key is required for this step.

3. **Execute geospatial analysis:**
    Run `sql/sql.sql` to compute results.

4. **Visualise results:**
    Use QGIS to display results.
