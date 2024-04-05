DROP TABLE sales_data_raw;
CREATE EXTERNAL TABLE sales_data_raw (
    `region` STRING,
    `country` STRING,
    `item_type` STRING,
    `sales_channel` STRING,
    `order_priority` STRING,
    `order_date` STRING,
    `order_id` STRING,
    `ship_date` STRING,
    `units_sold` STRING,
    `unit_price` STRING,
    `unit_cost` STRING,
    `total_revenue` STRING,
    `total_cost` STRING,
    `total_profit` STRING
)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
  's3://emr-pipeline-c2be3our7i/emr_pipeline/data/sales_data_raw/'
TBLPROPERTIES (
    "skip.header.line.count"="1"
);

CREATE EXTERNAL TABLE sales_data (
    `region` STRING,
    `country` STRING,
    `item_type` STRING,
    `sales_channel` STRING,
    `order_priority` STRING,
    `order_date` date,
    `order_id` STRING,
    `ship_date` date,
    `units_sold` INTEGER,
    `unit_price` DECIMAL(10,2),
    `unit_cost` DECIMAL(10,2),
    `total_revenue` DECIMAL(12,2),
    `total_cost` DECIMAL(12,2),
    `total_profit` DECIMAL(12,2)
)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://emr-pipeline-c2be3our7i/emr_pipeline/data/sales_data/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY'
);