INSERT OVERWRITE TABLE sales_data
SELECT
    `region`,
    `country`,
    `item_type`,
    `sales_channel`,
    `order_priority`,
    CASE
      WHEN `order_date` RLIKE '([0-9]{2}\-[0-9]{2}\-[0-9]{4})'
        THEN CAST(from_unixtime(unix_timestamp(`order_date` , 'MM-dd-yyyy')) AS DATE)
      WHEN `order_date` RLIKE '([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4})'
        THEN CAST(from_unixtime(unix_timestamp(`order_date` , 'MM/dd/yyyy')) AS DATE)
      ELSE NULL
    END AS `order_date`,
    `order_id`,
    CASE
      WHEN `ship_date` RLIKE '([0-9]{2}\-[0-9]{2}\-[0-9]{4})'
        THEN CAST(from_unixtime(unix_timestamp(`ship_date` , 'MM-dd-yyyy')) AS DATE)
      WHEN `ship_date` RLIKE '([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{4})'
        THEN CAST(from_unixtime(unix_timestamp(`ship_date` , 'MM/dd/yyyy')) AS DATE)
    END AS `ship_date`,
    CAST(`units_sold` AS INTEGER) AS units_sold,
    CAST(`unit_price` AS DECIMAL) AS unit_price,
    CAST(`unit_cost` AS DECIMAL) AS unit_cost,
    CAST(`total_revenue` AS DECIMAL) AS total_revenue,
    CAST(`total_cost` AS DECIMAL) AS total_cost,
    CAST(`total_profit` AS DECIMAL) AS total_profit 
FROM sales_data_raw