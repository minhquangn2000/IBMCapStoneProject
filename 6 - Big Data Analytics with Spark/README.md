# Module 6: ETL and Data Pipelines

## Overview
The team has provided the data set containing search terms on our e-Commerce platform. I need to run analytic queries on it using `pyspark` and `JupyterLab` to provide data for pretrained sales forecasting model to predict the sales for 2023.

## Technical Tasks & Deliverables
* **Data Ingestion & Inspection**: Load and profile raw e-commerce web server search logs (`searchterms.csv`) using PySpark DataFrames with schema inference
* **Distributed Analytics**: Execute aggregated distributed queries to extract search frequency metrics and identify top search trends
* **Feature Engineering**: Vectorize numeric search counts into feature matrices using PySpark ML's `VectorAssembler`
* **Predictive Inference**: Load and deploy a pre-trained **Linear Regression Model** (`sales_prediction.model`) to predict sales volume based on search traffic.

## 📁 Project Directory Structure

```text
.
├── Bigdata and Spark_Spark_MLOps.ipynb     # Main Jupyter notebook with lab solutions
├── README.md                               # Project documentation & guidelines
├── searchterms.csv                         # E-commerce web server search log dataset
├── model.tar.gz                            # Compressed pre-trained regression model archive
└── sales_prediction.model/                 # Extracted PySpark ML model directory
    ├── metadata/                           # Model metadata and JSON parameters
    └── data/                               # Model Parquet data chunks
```
### Executed Workflow

**Step 1.** Environment Initialization & Data Load
   ```python
   import findspark
   findspark.init()

   from pyspark.sql import SparkSession
   from pyspark.ml.feature import VectorAssembler
   from pyspark.ml.regression import LinearRegressionModel

   # Start session
    sc = SparkContext()

    # Creating a spark session
    spark = SparkSession.builder.appName("Analyse search terms on e-commerce web server").getOrCreate()
   ```
Download the data:
```commandline
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/searchterms.csv
```
Load data into DataFrame:
```python
df = spark.read.csv("searchterms.csv",header=True,inferSchema=True)
```
Verify DataFrame:
```python
# Print the number of rows and columns
num_row = df.count()
num_col = len(df.columns)
print("Rows: "+ str(num_row))
print("Columns: "+ str(num_col))

# Print the top 5 rows
df.show(5)

# Find out the datatype of the column searchterm?
datatype = df.schema["searchterm"].dataType
print(datatype)
```
**Step 2.** Run Analytics Query
```python
# How many times was the term `gaming laptop` searched?
count_gaming_laptop = df.filter(df["searchterm"] == "gaming laptop").count()
print(count_gaming_laptop)

# Print the top 5 most frequently used search terms?
search_counts_df = df.groupBy("searchterm").count().orderBy("count", ascending=False)
search_counts_df.show(5)
```
**Step 3.** Load Pretrained Model and Predict Sales
Download the Pretrained Model
```commandline
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/Bigdata%20and%20Spark/model.tar.gz
tar -xzf model.tar.gz
```
Load the sales forecast model.
```python
from pyspark.ml.regression import LinearRegressionModel

lr_model = LinearRegressionModel.load("sales_prediction.model")
```
Using the sales forecast model, predict the sales for the year of 2023.
```python
data_2023 = [[2023]]
df_2023 = spark.createDataFrame(data_2023, ["year"])
assembler = VectorAssembler(inputCols=["year"], outputCol="features")
data = assembler.transform(df_2023)
predictions = lr_model.transform(data)
predictions.select("year", "prediction").show()
```

## Key Takeaways & Engineering Reflections

**Distributed Aggregations:** Utilizing PySpark's `groupBy().count()` offloads heavy log aggregation from single-node memory limits to distributed workers, enabling sub-second execution on large log files.

**ML Persistence & Serialization:** Persisting trained MLlib models (via `LinearRegressionModel.load`) decoupling training pipelines from production inference pipelines, which allows lightweight microservices to serve predictions on demand.

**Feature Vector Requirements:** `PySpark MLlib` transformers require numeric features to be structured as dense or sparse `Vector` objects via `VectorAssembler` rather than primitive types before passing them into downstream estimators.

**Schema Inference vs. Explicit Contracts:** While `inferSchema=True` simplifies rapid prototyping, production big data pipelines should enforce explicit DDL schemas to prevent runtime failure modes caused by schema drift in raw log sources.

[<-- Previous Module](https://github.com/minhquangn2000/IBMCapStoneProject/tree/main/5%20-%20ETL%20%26%20Data%20Pipelines) 
