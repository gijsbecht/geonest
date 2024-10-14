-- create geometry indexes
CREATE INDEX IF NOT EXISTS buurten_geom_idx
  ON geonest.buurten
  USING GIST (geometry);

CREATE INDEX IF NOT EXISTS osm_climbing_isochrone_geom_idx
  ON geonest.osm_climbing_isochrone
  USING GIST (geometry);

-- create geometry that is an intersection of the two parents isochrones
CREATE MATERIALIZED VIEW geonest.the_parents_isochrones_45_intersection AS
WITH intersections AS (
  	SELECT 
    	ST_Intersection(a.geometry, b.geometry) AS geom
  	FROM 
    	geonest.the_parents_isochrones a,
    	geonest.the_parents_isochrones b
  	WHERE 
    	ST_Intersects(a.geometry, b.geometry)
  	AND
		a.contour = 45 AND a.wie = 'Gijs'
	AND
		b.contour = 45 AND b.wie = 'Femke'
)
SELECT 	
	ST_Union(geom) AS geometry
FROM 
	intersections;

-- ANALYSIS
DROP TABLE IF EXISTS geonest.buurten_result;

CREATE TABLE IF NOT EXISTS geonest.buurten_result AS
WITH parents_isochrone_30 AS (
	SELECT
		buurten.buurtcode,
		SUM(ROUND((ST_Area(ST_Intersection(the_parents_isochrones.geometry, buurten.geometry))/ST_Area(buurten.geometry))::numeric, 2)) AS overlap_parents_30
	FROM 
		geonest.buurten
	JOIN geonest.the_parents_isochrones
	ON ST_Intersects(the_parents_isochrones.geometry, buurten.geometry)
	WHERE contour = 30
	GROUP BY buurten.buurtcode
),
climbing_isochrone_15 AS (
	SELECT
		buurten.buurtcode,
		SUM(ROUND((ST_Area(ST_Intersection(osm_climbing_isochrone.geometry, buurten.geometry))/ST_Area(buurten.geometry))::numeric, 2)) AS overlap_climbing_15
	FROM 
		geonest.buurten
	JOIN geonest.osm_climbing_isochrone
	ON ST_Intersects(osm_climbing_isochrone.geometry, buurten.geometry)
	WHERE contour = 15
	GROUP BY buurten.buurtcode
)
SELECT DISTINCT
	buurten.buurtnaam,
	buurten.gemeentenaam,
	COALESCE(parents_isochrone_30.overlap_parents_30, 0) overlap_parents_30,
	COALESCE(climbing_isochrone_15.overlap_climbing_15, 0) overlap_climbing_15,
	COALESCE(parents_isochrone_30.overlap_parents_30, 0)*10+LEAST(COALESCE(climbing_isochrone_15.overlap_climbing_15, 0),2)*5 AS score,
	buurten.geometry
FROM
	geonest.buurten
JOIN geonest.the_parents_isochrones_45_intersection parents_isochrone_45
ON ST_Intersects(buurten.geometry, parents_isochrone_45.geometry)
JOIN geonest.osm_climbing_isochrone
ON ST_Intersects(buurten.geometry, osm_climbing_isochrone.geometry)
LEFT JOIN parents_isochrone_30
ON parents_isochrone_30.buurtcode = buurten.buurtcode
LEFT JOIN climbing_isochrone_15
ON climbing_isochrone_15.buurtcode = buurten.buurtcode
WHERE osm_climbing_isochrone.contour = 30
AND buurten."stedelijkheidAdressenPerKm2" > 2