-- sql basics

-- one way to join tables, this is an example of an inner join
-- SELECT 
-- 	tpep_pickup_datetime AS "pick_up", 
-- 	tpep_dropoff_datetime AS "drop_off",
-- 	total_amount,
-- 	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pick_up_location",
-- 	CONCAT(zdo."Borough", '/', zdo."Zone") AS "drop_off_location"
-- 	FROM 
-- 		yellow_taxi_data ytd,
-- 		zones zpu,
-- 		zones zdo
-- 	WHERE 
-- 		ytd."PULocationID" = zpu."LocationID" AND
-- 		ytd."DOLocationID" = zdo."LocationID"
-- 	LIMIT 100


-- SELECT 
-- 	tpep_pickup_datetime AS "pick_up", 
-- 	tpep_dropoff_datetime AS "drop_off",
-- 	total_amount,
-- 	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pick_up_location",
-- 	CONCAT(zdo."Borough", '/', zdo."Zone") AS "drop_off_location"
-- 	FROM 
-- 		yellow_taxi_data ytd 
-- 			JOIN zones zpu 
-- 				ON ytd."PULocationID" = zpu."LocationID" 
-- 			JOIN zones zdo 
-- 				ON ytd."DOLocationID" = zdo."LocationID"
-- 	LIMIT 100

-- -- checking to see if there are any null pick up or drop location
-- -- so pickup location 142 does not exist in zones
-- SELECT 
-- 	tpep_pickup_datetime AS "pick_up", 
-- 	tpep_dropoff_datetime AS "drop_off",
-- 	total_amount,
-- 	"PULocationID",
-- 	"DOLocationID"
-- 	FROM 
-- 		yellow_taxi_data ytd
-- 	WHERE 
-- 		"PULocationID" NOT IN (SELECT "LocationID" FROM zones)
-- 	LIMIT 100

-- --lets delete a zone so we can get the above query to return info 
-- DELETE FROM zones WHERE "LocationID" = 142;

--left joins 
-- SELECT 
-- 	tpep_pickup_datetime AS "pick_up", 
-- 	tpep_dropoff_datetime AS "drop_off",
-- 	total_amount,
-- 	CONCAT(zpu."Borough", '/', zpu."Zone") AS "pick_up_location",
-- 	CONCAT(zdo."Borough", '/', zdo."Zone") AS "drop_off_location"
-- 	FROM 
-- 		yellow_taxi_data ytd 
-- 			LEFT JOIN zones zpu 
-- 				ON ytd."PULocationID" = zpu."LocationID" 
-- 			LEFT JOIN zones zdo 
-- 				ON ytd."DOLocationID" = zdo."LocationID"
-- 	LIMIT 100


-- SELECT 
-- 	--tpep_pickup_datetime AS "pick_up", 
-- 	--tpep_dropoff_datetime AS "drop_off",
-- 	--DATE_TRUNC('DAY', tpep_dropoff_datetime),
-- 	CAST(tpep_dropoff_datetime AS DATE) as "DAY",
-- 	COUNT(1) as "count",
-- 	MAX(total_amount), 
-- 	MAX(passenger_count)
-- 	FROM 
-- 		yellow_taxi_data 
-- 	GROUP BY 
-- 		CAST(tpep_dropoff_datetime AS DATE)
-- 	ORDER BY "count" DESC;
-- 	--LIMIT 100

-- group by multi-fileds
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount), 
	MAX(passenger_count)
	FROM 
		yellow_taxi_data 
	GROUP BY 
		--CAST(tpep_dropoff_datetime AS DATE)
		1,2 --This means the query will create groups for each unique combination of day and DOLocationID.
	ORDER BY "day" ASC;
	--LIMIT 100

-- group by will be the work horse
