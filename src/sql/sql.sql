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
	SELECT * FROM geonest.the_parents_isochrones WHERE contour = 30
)
SELECT
	buurten.buurtnaam,
	buurten.gemeentenaam,
	COALESCE(
		SUM(ROUND((ST_Area(ST_Intersection(parents_isochrone_30.geometry, buurten.geometry))/ST_Area(buurten.geometry))::numeric, 2)),
		0
	) AS overlap_parents_30,
	buurten.geometry
FROM
	geonest.buurten
JOIN geonest.the_parents_isochrones_45_intersection parents_isochrone_45
ON ST_Intersects(buurten.geometry, parents_isochrone_45.geometry)
LEFT JOIN parents_isochrone_30
ON ST_Intersects(buurten.geometry, parents_isochrone_30.geometry)
WHERE buurten."stedelijkheidAdressenPerKm2" > 2
GROUP BY buurten.buurtnaam, buurten.gemeentenaam, buurten.geometry