# Module 3: Build a Data Warehouse

## Module Overview
In this module, the data warehousing layer for the **SoftCart** e-commerce platform was designed, implemented, and queried using **PostgreSQL**. 

The primary objectives were to design a Star Schema Entity-Relationship Diagram (ERD), export and instantiate the DDL schema, populate dimension and fact tables with historical dataset files, and execute advanced OLAP aggregation queries (`GROUPING SETS`, `ROLLUP`, `CUBE`, and Materialized Views / MQTs) for multi-dimensional reporting.

---

## Technical Tasks & Deliverables

* **Star Schema Architecture & ERD Design:** Modeled `softcart` star schema consisting of four dimension tables (`softcartDimDate`, `softcartDimCategory`, `softcartDimItem`, `softcartDimCountry`) and a central fact table (`softcartFactSales`).
* **Database & Schema Initialization:** Created the PostgreSQL database (`Test1`) and executed DDL scripts to set up relational structures and primary key constraints.
* **Data Ingestion:** Loaded CSV raw data feeds into `DimDate`, `DimCategory`, `DimCountry`, and `FactSales` tables using PostgreSQL `\copy` routines.
* **Advanced OLAP Querying:** Authored aggregation queries leveraging `GROUPING SETS`, `ROLLUP`, and `CUBE` clauses to analyze sales volume across dimensions.
* **Materialized Query Table (MQT):** Created a refreshed Materialized View (`total_sales_per_country`) to pre-aggregate country-level metrics for high-speed reporting.

---

## Directory Structure

```text
    module-3-data-warehouse/
    ├── README.md                   # Module documentation & execution steps
    ├── erd_export.sql              # Exported DDL script from ERD design
    ├── CREATE_SCRIPT.sql           # Database setup script for Dim & Fact tables
    ├── data/                       # Dataset files for table ingestion
    │   ├── DimDate.csv
    │   ├── DimCategory.csv
    │   ├── DimCountry.csv
    │   └── FactSales.csv
    ├── img/                        # Screenshot of ERD and sample data
    │   ├── erd.PNG
    │   ├── sample.PNG
    └── sql_queries.sql             # OLAP aggregation queries (GROUPING SETS, ROLLUP, CUBE, MQT)
```

---
## Data Warehousing
### Step 0: Star Schema ERD Design
Here is the sample data that the company sent me:

![SoftCart Data Platform Architecture](img/sample.png)

From the sample data, I'm able to design a Star Schema for the warehouse by identifying the columns for the various dimension and fact tables in the schema. Here are the specifications:

* **softcartDimDate**: Granularity down to a day (`dateid`, `date`, `year`, `quarter`, `month`, `monthname`, `day`, `weekday`).

* **softcartDimCategory**: Category entities (`categoryid`, `category`).

* **softcartDimItem**: Product item entities (`itemid`, `item`).

* **softcartDimCountry**: Geographic entities (`countryid`, `country`).

* **softcartFactSales**: Core transactions (`orderid`, `dateid`, `categoryid`, `itemid`, `countryid`, `price`).

Then I proceed to use the ERD tool in PostgreSQL to make the ERD diagram:

![SoftCart Data Platform Architecture](img/erd.png)

---

### Step 1: Server Connection & Table Creation

Connect to PostgreSQL, create the target analytical database Test1, and instantiate schema tables:

* **Via Command Line / psql:**
  ```sql
  -- Create database
    CREATE DATABASE "Test1";

    -- Connect to Test1 database and execute Create_Script.sql
    \c Test1
    \i Create_Script.sql
  ```
* **Via pgAdmin / GUI:**

1. Open pgAdmin, right-click Databases in the left sidebar, and click Create > Database...

2. Name the database Test1 and click Save.

3. Expand Test1, open the Query Tool (top toolbar icon), open Create_Script.sql, and click Execute (F5).

---

### Step 2: Load Data into tables

Load `DimDate.csv` into the `DimDate` table and display the first 5 records.

* **Via Command Line / psql:**
  ```sql
  \copy public."DimDate" FROM 'DimDate.csv' DELIMITER ',' CSV HEADER;
  SELECT * FROM public."DimDate" LIMIT 5;
  ```
* **Via pgAdmin / GUI:**

1. Right-click `Test1 > Schemas > public > Tables > DimDate` and select `Import/Export Data...`
2. Toggle switch to `Import`, set file path to `DimDate.csv`, and set Format to `csv`.
3. Under the Options tab, set Header to `Yes` and Delimiter to `,` and click `OK`.
4. Run `SELECT * FROM public."DimDate" LIMIT 5;` in the Query Tool to verify.

Load `DimCategory.csv` into the `DimCategory` table and display the first 5 records.
* **Via Command Line / psql:**
  ```sql
  \copy public."DimCategory" FROM 'DimCategory.csv' DELIMITER ',' CSV HEADER;
  SELECT * FROM public."DimCategory" LIMIT 5;
  ```
* **Via pgAdmin / GUI:**

1. Right-click `Test1 > Schemas > public > Tables > DimCategory` and select `Import/Export Data...`
2. Toggle switch to `Import`, set file path to `DimCategory.csv`, and set Format to `csv`.
3. Under the Options tab, set Header to `Yes` and Delimiter to `,` and click `OK`.
4. Run `SELECT * FROM public."DimCategory" LIMIT 5;` in the Query Tool to verify.

Load `DimCountry.csv` into the `DimCountry` table and display the first 5 records.
* **Via Command Line / psql:**
  ```sql
  \copy public."DimCountry" FROM 'DimCountry.csv' DELIMITER ',' CSV HEADER;
  SELECT * FROM public."DimCountry" LIMIT 5;
  ```
* **Via pgAdmin / GUI:**

1. Right-click `Test1 > Schemas > public > Tables > DimCountry` and select `Import/Export Data...`
2. Toggle switch to `Import`, set file path to `DimCountry.csv`, and set Format to `csv`.
3. Under the Options tab, set Header to `Yes` and Delimiter to `,` and click `OK`.
4. Run `SELECT * FROM public."DimCountry" LIMIT 5;` in the Query Tool to verify.

Load `FactSales.csv` into the `FactSales` table and display the first 5 records.
* **Via Command Line / psql:**
  ```sql
  \copy public."FactSales" FROM 'FactSales.csv' DELIMITER ',' CSV HEADER;
  SELECT * FROM public."FactSales" LIMIT 5;
  ```
* **Via pgAdmin / GUI:**

1. Right-click `Test1 > Schemas > public > Tables > FactSales` and select `Import/Export Data...`
2. Toggle switch to `Import`, set file path to `FactSales.csv`, and set Format to `csv`.
3. Under the Options tab, set Header to `Yes` and Delimiter to `,` and click `OK`.
4. Run `SELECT * FROM public."FactSales" LIMIT 5;` in the Query Tool to verify.

---

### Step 3: Advanced OLAP Queries & Analytics

All of the following queries can be executed in the terminal via psql or in pgAdmin's Query Tool.

* **Grouping Sets Query:**
Calculate total sales across combinations of country and category using `GROUPING SETS`:
```commandline
    SELECT 
        c.country,
        cat.category,
        SUM(f.amount) AS totalsales
    FROM public."FactSales" f
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    LEFT JOIN public."DimCategory" cat ON f.categoryid = cat.categoryid
    GROUP BY GROUPING SETS ((c.country, cat.category), (c.country), (cat.category), ())
    ORDER BY c.country, cat.category;
```

* **Rollup Query:**
Perform a hierarchical aggregation of sales by year, country, and total sales using `ROLLUP`:
```commandline
    SELECT 
        d."Year" AS year,
        c.country,
        SUM(f.amount) AS totalsales
    FROM public."FactSales" f
    LEFT JOIN public."DimDate" d ON f.dateid = d.dateid
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    GROUP BY ROLLUP (d."Year", c.country)
    ORDER BY d."Year", c.country;
```

* **Cube Query:**
Generate all possible aggregation combinations across year and country along with average sales using `CUBE`:
```commandline
    SELECT 
        d."Year" AS year,
        c.country,
        AVG(f.amount) AS average_sales
    FROM public."FactSales" f
    LEFT JOIN public."DimDate" d ON f.dateid = d.dateid
    LEFT JOIN public."DimCountry" c ON f.countryid = c.countryid
    GROUP BY CUBE (d."Year", c.country)
    ORDER BY d."Year", c.country;
```

* **Materialized Query Table (MQT):**
Create a PostgreSQL Materialized View named `total_sales_per_country` to store aggregated total sales per country:

```commandline
    -- Create Materialized Query Table (MQT)
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
```
* **GUI Tip for MQTs in pgAdmin**: After executing the creation script, refresh your browser tree and navigate to Test1 > Schemas > public > Materialized Views > total_sales_per_country. You can right-click it and choose Refresh Materialized View anytime data updates in FactSales.

## Key Takeaways & Engineering Reflections

* **Star Schema Aggregation Efficiency:** Joining normalized dimension tables (`DimCountry`, `DimCategory`, `DimDate`) with fact tables (`FactSales`) via integer primary keys drastically speeds up analytical calculations compared to grouping on raw unindexed text files.
* **OLAP Operators (`GROUPING SETS`, `ROLLUP`, `CUBE`):** These PostgreSQL extensions eliminate the need to run multiple `UNION ALL` subqueries, computing multi-level summary totals in a single database scan.
* **Materialized Views for High-Frequency Queries:** Creating the `total_sales_per_country` MQT pre-computes aggregate metrics on disk, removing query computation overhead during executive dashboard rendering.
* **Schema Implementation Differences:** In the implementation of the PostgreSQL data warehouse, no `DimItem` dataset was provided in the source files, so the `DimItem` table is omitted from the loaded staging database.

[<-- Previous Module](https://github.com/minhquangn2000/IBMCapStoneProject/tree/main/2%20-%20Querying%20Data%20in%20NoSQL%20Databases)  | [Next Module -->](https://github.com/minhquangn2000/IBMCapStoneProject/tree/main/4%20-%20Data%20Analytics)
