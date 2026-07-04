-- ============================================================
-- Australian Car Sales Analysis — SQL Queries
-- Author: Dhwani Shah | Victoria University MBA Analytics
-- ============================================================

-- 1. Brand market share by units and revenue
SELECT
    brand,
    COUNT(*)                                    AS total_units,
    ROUND(AVG(sale_price), 0)                  AS avg_price_aud,
    ROUND(SUM(sale_price), 0)                  AS total_revenue_aud,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS market_share_pct
FROM car_sales
GROUP BY brand
ORDER BY total_units DESC;

-- 2. EV adoption by year
SELECT
    year,
    fuel_type,
    COUNT(*)                                    AS units,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY year), 1) AS pct_of_year
FROM car_sales
GROUP BY year, fuel_type
ORDER BY year, units DESC;

-- 3. State-level performance
SELECT
    state,
    COUNT(*)                                    AS total_units,
    ROUND(AVG(sale_price), 0)                  AS avg_price,
    ROUND(SUM(sale_price) / 1000000.0, 2)      AS revenue_millions_aud
FROM car_sales
GROUP BY state
ORDER BY total_units DESC;

-- 4. Seasonal Q4 vs Q1 comparison
SELECT
    quarter,
    COUNT(*)                                    AS units,
    ROUND(AVG(sale_price), 0)                  AS avg_price,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS share_pct
FROM car_sales
GROUP BY quarter
ORDER BY quarter;

-- 5. Top 10 brand-state combos by revenue
SELECT
    brand,
    state,
    fuel_type,
    COUNT(*)                                    AS total_sales,
    ROUND(AVG(sale_price), 2)                  AS avg_price,
    ROUND(SUM(sale_price), 0)                  AS total_revenue
FROM car_sales
WHERE year BETWEEN 2022 AND 2024
GROUP BY brand, state, fuel_type
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. EV growth rate (2021 to 2024)
SELECT
    ROUND(
        (SUM(CASE WHEN year = 2024 AND fuel_type = 'Electric' THEN 1 ELSE 0 END) -
         SUM(CASE WHEN year = 2021 AND fuel_type = 'Electric' THEN 1 ELSE 0 END)) * 100.0 /
        NULLIF(SUM(CASE WHEN year = 2021 AND fuel_type = 'Electric' THEN 1 ELSE 0 END), 0),
    1
    ) AS ev_growth_pct_2021_to_2024
FROM car_sales;
