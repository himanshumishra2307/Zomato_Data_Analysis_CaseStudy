/*===========================================================*
 * QUERY 1 - Total Restaurants
 *===========================================================*/

SELECT COUNT(*) AS total_restaurants
FROM zomato_clean;


/*===========================================================*
 * QUERY 2 - Total Countries
 *===========================================================*/
SELECT COUNT(DISTINCT "Country") AS total_countries
FROM zomato_clean;

/*===========================================================*
 * QUERY 3 - Restaurants by Country
 *===========================================================*/

SELECT
    "Country",
    COUNT(*) AS total_restaurants
FROM zomato_clean
GROUP BY "Country"
ORDER BY total_restaurants DESC;


/*===========================================================*
 * QUERY 4 - Top 10 Cities by Restaurant Count
 *===========================================================*/

SELECT
    "City",
    COUNT(*) AS total_restaurants
FROM zomato_clean
GROUP BY "City"
ORDER BY total_restaurants DESC
LIMIT 10;


/*===========================================================*
 * QUERY 5 - Average Rating by Country
 *===========================================================*/

SELECT
    "Country",
    ROUND(AVG("Aggregate rating")::numeric,2) AS avg_rating
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "Country"
ORDER BY avg_rating DESC;


/*===========================================================*
 * QUERY 6 - Average Rating and Votes by City
 *===========================================================*/

SELECT
    "City",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric, 2) AS avg_rating,
    ROUND(AVG("Votes")::numeric, 0) AS avg_votes
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "City"
HAVING COUNT(*) >= 20
ORDER BY avg_rating DESC;


/*===========================================================*
 * QUERY 7 - Total Unrated Restaurants
 *===========================================================*/

SELECT
    COUNT(*) AS unrated_restaurants
FROM zomato_clean
WHERE "Aggregate rating" = 0;


/*===========================================================*
 * QUERY 8 - Percentage of Unrated Restaurants Country Wise
 *===========================================================*/

SELECT
    "Country",
    COUNT(*) AS total_restaurants,
    SUM(
        CASE
            WHEN "Aggregate rating" = 0 THEN 1
            ELSE 0
        END
    ) AS unrated_restaurants,
    ROUND(
        SUM(
            CASE
                WHEN "Aggregate rating" = 0 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS unrated_percentage
FROM zomato_clean
GROUP BY "Country"
ORDER BY unrated_percentage DESC;


/*===========================================================*
 * QUERY 9 - Online Delivery vs Average Rating
 *===========================================================*/

SELECT
    "Has Online delivery",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric,2) AS avg_rating
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "Has Online delivery"
ORDER BY avg_rating DESC;


/*===========================================================*
 * QUERY 10 - Table Booking vs Average Rating
 *===========================================================*/

SELECT
    "Has Table booking",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric,2) AS avg_rating
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "Has Table booking"
ORDER BY avg_rating DESC;


/*===========================================================*
 * QUERY 11 - Average Rating by Price Range
 *===========================================================*/

SELECT
    "Price range",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric,2) AS avg_rating
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "Price range"
ORDER BY "Price range";


/*===========================================================*
 * QUERY 12 - Average Votes by Price Range
 *===========================================================*/

SELECT
    "Price range",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Votes")::numeric, 0) AS avg_votes
FROM zomato_clean
GROUP BY "Price range"
ORDER BY "Price range";


/*===========================================================*
 * QUERY 13 - Top 10 Cuisines by Restaurant Count
 *===========================================================*/

SELECT
    "Cuisines",
    COUNT(*) AS total_restaurants
FROM zomato_clean
WHERE "Cuisines" IS NOT NULL
GROUP BY "Cuisines"
ORDER BY total_restaurants DESC
LIMIT 10;


/*===========================================================*
 * QUERY 14 - Top 10 Cuisines by Rating
 *===========================================================*/

SELECT
    "Cuisines",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric, 2) AS avg_rating
FROM zomato_clean
WHERE "Aggregate rating" > 0
GROUP BY "Cuisines"
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 10;

/*===========================================================*
 * QUERY 15 - Top 10 Most Voted Restaurants
 *===========================================================*/

SELECT
    "Restaurant Name",
    "Country",
    "City",
    "Cuisines",
    "Votes",
    "Aggregate rating"
FROM zomato_clean
ORDER BY "Votes" DESC
LIMIT 10;


/*===========================================================*
 * QUERY 16 - Top 3 Cities in Each Country
 *===========================================================*/

WITH city_rating AS
(
    SELECT
        "Country",
        "City",
        COUNT(*) AS total_restaurants,
        ROUND(AVG("Aggregate rating")::numeric, 2) AS avg_rating
    FROM zomato_clean
    WHERE "Aggregate rating" > 0
    GROUP BY "Country", "City"
    HAVING COUNT(*) >= 10
)

SELECT *
FROM
(
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY "Country"
               ORDER BY avg_rating DESC
           ) AS city_rank
    FROM city_rating
) t
WHERE city_rank <= 3;

/*===========================================================*
 * QUERY 17 - Rank Restaurants by Votes
 *===========================================================*/

SELECT
    "Restaurant Name",
    "Country",
    "City",
    "Votes",
    RANK() OVER (ORDER BY "Votes" DESC) AS vote_rank
FROM zomato_clean;


/*===========================================================*
 * QUERY 18 - Dense Rank by Rating
 *===========================================================*/

SELECT
    "Restaurant Name",
    "Country",
    "City",
    "Aggregate rating",
    DENSE_RANK() OVER (
        ORDER BY "Aggregate rating" DESC
    ) AS rating_rank
FROM zomato_clean
WHERE "Aggregate rating" > 0;


/*===========================================================*
 * QUERY 19 - Country Wise Online Delivery %
 *===========================================================*/

SELECT
    "Country",
    COUNT(*) AS total_restaurants,
    SUM(
        CASE
            WHEN "Has Online delivery" = 'Yes' THEN 1
            ELSE 0
        END
    ) AS delivery_restaurants,
    ROUND(
        SUM(
            CASE
                WHEN "Has Online delivery" = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS delivery_percentage
FROM zomato_clean
GROUP BY "Country"
ORDER BY delivery_percentage DESC;


/*===========================================================*
 * QUERY 20 - Country Wise Table Booking %
 *===========================================================*/

SELECT
    "Country",
    COUNT(*) AS total_restaurants,
    SUM(
        CASE
            WHEN "Has Table booking" = 'Yes' THEN 1
            ELSE 0
        END
    ) AS booking_restaurants,
    ROUND(
        SUM(
            CASE
                WHEN "Has Table booking" = 'Yes' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS booking_percentage
FROM zomato_clean
GROUP BY "Country"
ORDER BY booking_percentage DESC;


/*===========================================================*
 * QUERY 21 - Rating Bucket Distribution
 *===========================================================*/

SELECT
    "Rating_Bucket",
    COUNT(*) AS total_restaurants,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM zomato_clean),
        2
    ) AS percentage
FROM zomato_clean
GROUP BY "Rating_Bucket"
ORDER BY total_restaurants DESC;


/*===========================================================*
 * QUERY 22 - India City Performance
 *===========================================================*/
SELECT
    "City",
    COUNT(*) AS total_restaurants,
    ROUND(AVG("Aggregate rating")::numeric, 2) AS avg_rating,
    ROUND(AVG("Votes")::numeric, 0) AS avg_votes
FROM zomato_clean
WHERE "Country" = 'India'
  AND "Aggregate rating" > 0
GROUP BY "City"
HAVING COUNT(*) >= 10
ORDER BY avg_rating DESC;


/*===========================================================*
 * QUERY 23 - Most Expensive Cities
 *===========================================================*/

SELECT
    "City",
    ROUND(AVG("Average Cost for two")::numeric, 0) AS avg_cost
FROM zomato_clean
GROUP BY "City"
ORDER BY avg_cost DESC
LIMIT 10;


/*===========================================================*
 * QUERY 24 - Create Dashboard View
 *===========================================================*/

CREATE OR REPLACE VIEW vw_dashboard_summary AS
SELECT
    "Country",
    "City",
    "Restaurant Name",
    "Cuisines",
    "Average Cost for two",
    "Price range",
    "Aggregate rating",
    "Votes",
    "Has Online delivery",
    "Has Table booking",
    "Rating_Bucket"
FROM zomato_clean;


/*===========================================================*
 * QUERY 25 - Dashboard Data
 *===========================================================*/

SELECT *
FROM vw_dashboard_summary;