# Module 2: Querying Data in NoSQL Databases

## Module Overview
In this module, the semi-structured document store layer for the SoftCart e-commerce platform was configured and initialized using **MongoDB**. 

The primary objectives were to ingest product catalog data stored in JSON format, inspect database collections, establish secondary indexes for performance optimization, execute document aggregation queries, and export targeted attributes to CSV format for downstream reporting pipelines.

---

## Technical Tasks & Deliverables

* **MongoDB Instance Setup & Data Ingestion:** Imported semi-structured e-commerce product records (`catalog.json`) into the `catalog` database within the `electronics` collection using `mongoimport`.
* **Database Inspection & Administration:** Executed administrative shell operations to list active databases and inspect collection structures within MongoDB.
* **Query Optimization:** Applied a single-field index on the `type` attribute to optimize document filter queries and aggregation performance.
* **Document Aggregation & Querying:** Authored filtering queries and pipeline aggregations to compute item counts and calculate average screen sizes across product categories.
* **Data Export & Reporting:** Executed `mongoexport` to extract specific fields (`_id`, `type`, `model`) from the document store into a CSV file (`electronics.csv`).

---

## Directory Structure

```text
2 - Querying Data in NoSQL Databases/
├── README.md               # Module documentation & execution steps
├── catalog.json            # Semi-structured raw document dataset
└── exports/
    └── electronics.csv     # Exported CSV dataset containing selected fields
```

## Design & Query the NoSQL Database
### Step 0. Start & Connect to MongoDB

Ensure your MongoDB daemon is active, then connect via terminal or GUI client:

* **Via Command Line:**
  ```bash
  # Start service (if not running automatically)
    sudo service mongodb start

    # Connect to MongoDB Shell
    mongosh
  # Enter your credentials
  ```
* **Via MongoDB Compass / GUI:**
Launch MongoDB Compass, connect to **mongodb://localhost:27017**, and authenticate if credentials are configured.

---

### Step 1: Import Data into MongoDB (`catalog.json`)

After connecting to the MongoDB database, let's import the JSON document dataset into the catalog database under the `electronics` collection.

* **Via Command Line:**
  Run `mongoimport` directly from your terminal:
  ```bash
  mongoimport --db catalog --collection electronics --file catalog.json
  #Verification
  #imported 224 documents successfully
  ```
  
---

### Step 2: List All Databases

Verify database creation by listing all databases present on the MongoDB server.

* **Via Command Line (MongoDB Shell):**
    ```commandline
    show dbs
    ```
* **Output:**
    ```
    admin     0.000GB
    catalog   0.000GB
    config    0.000GB
    local     0.000GB
    ```
  
---

### Step 3: List All Collections in `catalog` Database

Switch context to the `catalog` database and inspect available collections.

* **Via Command Line (MongoDB Shell):**
    ```commandline
    use catalog
    show collections
    ```
* **Output:**
    ```
    electronics
    ```

---

### Step 4: Create an Index on the `type` Field

Build a single-field ascending index on the `type` field in the `electronics` collection to accelerate filtering operations.

* **Via Command Line (MongoDB Shell):**
    ```commandline
    USE catalog;
    db.electronics.createIndex({ type: 1 });
    ```
* **Verification:**
    Confirm index creation by running
    ```
    db.electronics.getIndexes();
    ```

---

### Step 5: Find the Count of Laptops

Execute a document count query to identify total inventory for laptops.
* **Via Command Line (MongoDB Shell):**
    ```commandline
    USE catalog;
    db.electronics.countDocuments({ type: "laptop" });
    ```
* **Expected Output:**
    ```
    389
    ```

---

### Step 6: Count Smartphones with 6-Inch Screen Size

Run a compound field filter query to count smartphones matching specific screen dimensions.

* **Via Command Line (MongoDB Shell):**
    ```commandline
    USE catalog;
    db.electronics.countDocuments({ type: "smart phone", "screen size": 6 });
    ```
* **Expected Output:**
    ```
    8
    ```

---

### Step 7: Find Average Screen Size of Smartphones

Construct a MongoDB aggregation pipeline using $match and $group operators to calculate screen size metrics.

* **Via Command Line (MongoDB Shell):**
    ```commandline
    USE catalog;
    db.electronics.aggregate([
        { $match: { type: "smart phone" } },
        { $group: { _id: "$type", avgScreenSize: { $avg: "$screen size" } } }
    ]);
    ```
* **Expected Output:**
    ```
    { "_id": "smart phone", "avgScreenSize": 6 }
    ```
  
---

### Step 8: Export Selected Fields to CSV File (`electronics.csv`)

Export designated attributes (_id, type, model) from the electronics collection to a structured CSV format.

* **Via Command Line:**
    ```commandline
    mongoexport --db catalog --collection electronics --type=csv --fields _id,type,model --out exports/electronics.csv
    ```
* **Verification:**
    Verify output file creation and sample header records:
    ```
    ls -lh exports/electronics.csv
    head -n 5 exports/electronics.csv
    ```

## Key Takeaways & Engineering Reflections

* **Flexible Schema Advantages:** Storing product catalog records in MongoDB allows distinct item categories (e.g., laptops vs. televisions) to hold unique attribute fields (`ram` and `hard disk` for laptops) within a single collection without storing redundant NULL attributes as required by relational SQL tables.
* **Indexing Execution Strategy:** Creating an index on `{ type: 1 }` prevents full collection scans ($O(N)$) when processing query filters or pipeline stages, ensuring efficient lookup execution time ($O(\log N)$) during product searches.
* **Aggregation Framework Power:** Leveraging native `$match` and `$group` aggregation stages processes metrics directly on the database node, eliminating the bandwidth overhead of transporting bulk documents to downstream application servers.
