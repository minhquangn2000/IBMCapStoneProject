-- Create an index named ts on the timestamp field.
CREATE INDEX ts ON sales_data (timestamp);
-- List indexes
SHOW INDEX FROM sales_data;