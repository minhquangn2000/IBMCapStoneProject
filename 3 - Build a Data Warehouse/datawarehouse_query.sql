    -- GROUPING SETS Query
    SELECT
        c.country,
        cat.category,
        SUM(f.amount) AS totalsales
    FROM public."FactSales" f
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    LEFT JOIN public."DimCategory" cat ON f.categoryid = cat.categoryid
    GROUP BY GROUPING SETS ((c.country, cat.category), (c.country), (cat.category), ())
    ORDER BY c.country, cat.category;

    -- ROLLUP Query
    SELECT
        d."Year" AS year,
        c.country,
        SUM(f.amount) AS totalsales
    FROM public."FactSales" f
    LEFT JOIN public."DimDate" d ON f.dateid = d.dateid
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    GROUP BY ROLLUP (d."Year", c.country)
    ORDER BY d."Year", c.country;

    -- CUBE Query
    SELECT
        d."Year" AS year,
        c.country,
        AVG(f.amount) AS average_sales
    FROM public."FactSales" f
    LEFT JOIN public."DimDate" d ON f.dateid = d.dateid
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    GROUP BY CUBE (d."Year", c.country)
    ORDER BY d."Year", c.country;

    --  MATERIALIZED VIEW Query
    CREATE MATERIALIZED VIEW total_sales_per_country AS
    SELECT
        c.country,
        SUM(f.amount) AS total_sales
    FROM public."FactSales" f
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    GROUP BY c.country;

    -- Refresh view command
    REFRESH MATERIALIZED VIEW total_sales_per_country;

    -- Query MQT output
    SELECT * FROM total_sales_per_country;