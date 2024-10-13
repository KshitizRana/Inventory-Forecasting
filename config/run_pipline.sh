#!/bin/bash

# load data from csv files into a database
echo "\n.......Creating raw database......."
python3 src/database_connect.py -cd True -db "Inventory_raw"

# normalize and clean data, and upload to database
echo "\n.......Creating table & uploading data......."
python3 src/database_connect.py -db "Inventory_raw" -id "upload-to-database"

echo "\n.......Running ETL......."
python3 src/etl.py

echo "\n.......Creating processed database......."
python3 src/database_connect.py -cd True -db 'Agg_store'

echo "\n.......Creating table & uploading data......."
python3 src/database_connect.py -db 'Agg_store' -id "cleaned-upload-to-database"


python3 main.py -t data_extraction