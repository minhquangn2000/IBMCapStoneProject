#!/bin/bash
# Exports all rows from the sales_data table into sales_data.sql

mysqldump -u root -p sales sales_data > sales_data.sql