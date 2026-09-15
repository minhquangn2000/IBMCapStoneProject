# Module 1: Data Platform Architecture & OLTP Database

## Module Overview
In this module, the relational transactional database (OLTP) layer for the SoftCart e-commerce platform was configured and initialized using **MySQL**. 

The primary objectives were to set up the sales transactional schema, import historic sales data, establish database indexes to optimize read/query performance, and perform database administration tasks such as creating backups and automated dumps.

---

## Technical Tasks & Deliverables

* **MySQL Instance Setup & Database Creation:** Created the core transactional database (`sales`) to capture e-commerce order logs, inventory changes, and customer transactions.
* **Schema Design & Table Creation:** Configured the `sales_data` relational table with appropriate data types, primary keys, and constraints.
* **Data Ingestion:** Imported raw transactional data (`sales.csv`) into the MySQL server.
* **Query Optimization:** Applied MySQL indexing strategies on frequently queried fields (e.g., `timestamp`, `product_id`) to optimize performance for downstream ETL processes.
* **Database Backup & Maintenance:** Executed `mysqldump` to create a binary/SQL backup of the transactional database for disaster recovery and staging pipelines.

---

## Directory Structure

```text
1 - Data Platform Architecture And OLTP Database/
├── README.md               # Module documentation & execution steps
├── datadump.sh             # Bash script to export data
├── oltp_setup.sql          # SQL DDL script to create database, schema & tables
├── sales_data.csv          # Sample raw transactional data file
├── create_index.sql        # SQL script to create query indexes
└── backup/
    └── sales_backup.sql    # Database backup generated using mysqldump
```
---

## Design the OLTP Database
### Step 0. Start & Connect to MySQL

Make sure your MySQL server is running, then connect via terminal or GUI:

* **Via Command Line:**
  ```bash
  # Start service (if not running automatically)
  sudo service mysql start

  # Connect to MySQL server
  mysql -u root -p
  # Enter your credentials
  ```
* **Via MySQL Workbench / GUI:**
Launch MySQL Workbench, connect to **localhost:3306** and enter your root credentials.

---



### Step 1: Initialize Database & Tables (`oltp_setup.sql`)

After connecting to MySQL, the next step is to create the database schema and relational table structure.


Create the `sales` database and the `sales_data` transactional table using the `oltp_setup.sql` DDL script.
* **Via Command Line:**
  Run the script directly from your terminal:
  ```bash
  mysql -u root -p < oltp_setup.sql
  ```
* **Via MySQL Workbench / GUI:**
1. Go to File > Open SQL Script... and select oltp_setup.sql.
2. Click the Execute (Lightning Bolt) icon to create the database and tables.
3. Verify the schema creation by querying MySQL:
  ```sql
  USE sales;
  DESCRIBE sales_data;
  ```

---

### Step 2: Load Transactional Data (sales_data.csv)
Import the historic sales records into the newly created sales_data table.
* **Via Command Line:**
  Run mysqlimport from your terminal (ensure sales_data.csv is in your current directory):
  ```bash
  mysqlimport --ignore-lines=1 --fields-terminated-by=',' --local -u root -p sales sales_data.csv
  ```
* **Via MySQL Workbench / GUI:**
1. In the Schemas tab on the left, expand sales > Tables.
2. Right-click on sales_data and select Table Data Import Wizard.
3. Browse to select sales_data.csv, click Next, and complete the mapping wizard.
4. Verify the records import by querying MySQL:
  ```sql
  USE sales;
  SELECT COUNT(*) FROM sales_data;
  ```

---

### Step 3: Query Optimization & Indexing (create_index.sql)
Create indexes on frequently queried columns (such as `timestamp` or `product_id`) to optimize read efficiency for downstream ETL jobs.
* **Via Command Line:**
  Execute the indexing script:
  ```bash
  mysql -u root -p sales < create_index.sql
  ```
* **Via MySQL Workbench / GUI:**
1. Open create_index.sql in MySQL Workbench.
2. Click the Execute (Lightning Bolt) icon.
3. Verify created indexes by checking output or running SQL commands:
  ```sql
  USE sales;
  SHOW INDEX FROM sales_data;
  ```

---

### Step 4: Automated Data Export Script (datadump.sh)
Create and execute a bash script named datadump.sh to automatically export all rows from the sales_data table into a file named sales_data.sql.

Script Content (datadump.sh):
```
#!/bin/bash
# Exports all rows from the sales_data table into sales_data.sql

mysqldump -u root -p sales sales_data > sales_data.sql
```
* **Via Command Line:**
```bash
#Grant write and execute permission
chmod +wx datadump.sh
#Run script
./datadump.sh
```
* **Verification:**
```bash
ls -lh sales_data.sql
head -n 20 sales_data.sql
```

---

## Key Takeaways & Engineering Reflections

* **Why Indexing Matters for ETL:** Creating an index on `timestamp` drastically reduces full table scans when downstream Apache Airflow pipelines extract incremental sales batches, moving query complexity from $O(N)$ to $O(\log N)$.
* **OLTP vs. OLAP Tradeoffs:** While MySQL excels at rapid write operations for incoming e-commerce orders, running complex aggregation queries on live transactional tables can cause lock contention. This reinforced why offloading transactional data to a dedicated PostgreSQL/Hadoop staging warehouse in later modules is critical.
* **Storage Precision:** Using `DECIMAL(10,2)` instead of floating-point numbers (`FLOAT`/`DOUBLE`) for financial data prevents cumulative rounding errors during currency calculations and business reporting.

 [Next Module -->](https://github.com/minhquangn2000/IBMCapStoneProject/tree/main/2%20-%20Querying%20Data%20in%20NoSQL%20Databases)
