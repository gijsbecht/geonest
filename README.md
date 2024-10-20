# GeoNest

GeoNest is a geospatial data management tool for determining the best place to live in The Netherlands. Recommended use in combination with a (local) PostgreSQL database with the POSTGIS extension installed, use QGIS for data visualisation.

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
