#!/bin/bash

# load data from csv files into a database
echo "\n.......Creating raw database......."
python3 src/database_connect.py -cd True -db "Inventory_raw"

# normalize and clean data, and upload to database
echo "\n.......Creating table & uploading data......."
python3 src/database_connect.py -db "Inventory_raw" -tb 'sales' -fp 'data/sales.csv'
python3 src/database_connect.py -db "Inventory_raw" -tb 'stock_level' -fp 'data/sensor_stock_levels.csv'
python3 src/database_connect.py -db "Inventory_raw" -tb 'stock_temp' -fp 'data/sensor_storage_temperature.csv'

echo "\n.......Running ETL......."
python3 src/etl.py

echo "\n.......Creating processed database......."
python3 src/database_connect.py -cd True -db 'Agg_store'

echo "\n.......Creating table & uploading data......."
python3 src/database_connect.py -db 'Agg_store' -tb 'sales_agg' -fp 'data/sales_agg.csv'
python3 src/database_connect.py -db 'Agg_store' -tb 'stocklevel_agg' -fp 'data/sensor_stock_level_agg.csv'
python3 src/database_connect.py -db 'Agg_store' -tb 'stocktemp_agg' -fp 'data/sensor_stock_temperature_agg.csv'