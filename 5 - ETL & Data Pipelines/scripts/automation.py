# Import libraries required for connecting to mysql
import psycopg2
# Import libraries required for connecting to DB2 or PostgreSql
import mysql.connector
# Connect to MySQL
mysql_conn = mysql.connector.connect(user='root', password='<replace with your Mysql password>',host='<replace with your Mysql hostname>',database='sales')
# Connect to DB2 or PostgreSql
pg_conn = psycopg2.connect(
   database="postgres", 
   user='postgres',
   password='<replace with your postgres hostname>',
   host='<replace with your Mysql hostname>',
   port= "5432"
)
# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    with pg_conn.cursor() as cur:
        query = "SELECT MAX(rowid) FROM sales_data"
        cur.execute(query)
        last_row_id = cur.fetchone()[0]
        return last_row_id


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    with mysql_conn.cursor() as cur:
        query = "SELECT * FROM sales_data WHERE rowid > %s;"
        cur.execute(query,(rowid,))
        new_records = cur.fetchall()
        return new_records

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))
# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
    if not records:
        print("Invalid records")
        return
    with pg_conn.cursor() as cur:
        query = """
                    INSERT INTO sales_data (rowid, product_id, customer_id, quantity) 
                    VALUES (%s, %s, %s, %s);
                """
        cur.executemany(query, records)
        print("Success")
insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
mysql_conn.close()
# disconnect from DB2 or PostgreSql data warehouse 
pg_conn.close()
# End of program