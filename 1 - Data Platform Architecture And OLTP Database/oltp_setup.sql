-- 1. Create database if it does not already exist
CREATE DATABASE IF NOT EXISTS sales;

-- 2. Switch to the 'sales' database context
USE sales;

-- 3. Drop existing table to ensure clean execution
DROP TABLE IF EXISTS sales_data;

-- 4. Create the 'sales_data' transactional table schema
CREATE TABLE sales_data (
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    timestamp DATETIME NOT NULL,
);

-- 5. Optional verification statement
USE sales;
DESCRIBE sales_data;
