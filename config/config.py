---
upload-to-database:
  import:
    - import:
        dirpath: ./data/raw/
        file_extension: csv 
        prefix_filename: sales
    - import:
        dirpath: ./data/raw/
        file_extension: csv 
        prefix_filename: sensor_stock_levels
    - import:
        dirpath: ./data/raw/
        file_extension: csv 
        prefix_filename: sensor_storage_temperature

cleaned-upload-to-database:
  import:
    - import:
        dirpath: ./data/processed/
        file_extension: csv 
        prefix_filename: sales_processed
    - import:
        dirpath: ./data/processed/
        file_extension: csv 
        prefix_filename: stock_processed
    - import:
        dirpath: ./data/processed/
        file_extension: csv 
        prefix_filename: temp_processed

data_extraction:
  export:
    - export:
        host: s3
        bucket: inventory-agg-data
        filename: inventory_historical_data

inventory_modeling_ml:
  export:
    - export:
        host: gsheet
        spread_sheet_id: 1vhmJcfz7DINZPha-y7TR4gB5pe-h_GwdFy-FfqIrUgk
        worksheet_name: Forecasting-data
