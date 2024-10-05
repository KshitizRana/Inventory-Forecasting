import pandas as pd

from utils import convert_timestamp_to_hourly, data

# Aggregate data
sales_df = convert_timestamp_to_hourly(data('data/sales.csv'),'timestamp')
salesagg_df = sales_df.groupby(by=['timestamp','product_id']).agg({'quantity' : 'sum'}).reset_index()
product_category = sales_df[['product_id','category','unit_price']].drop_duplicates()
sales_agg_merged = salesagg_df.merge(product_category, on= 'product_id',how='left')
sales_agg_merged.to_csv('data/sales_agg.csv',index=False)


stocklevel_df = convert_timestamp_to_hourly(data('data/sensor_stock_levels.csv'),'timestamp')
stocklevel_df = stocklevel_df.groupby(by=['timestamp','product_id']).agg({'estimated_stock_pct' : 'mean'}).reset_index()
# extract additional columns from sales data
product_categories = sales_df[['product_id', 'category']].drop_duplicates()
product_price = sales_df[['product_id', 'unit_price']].drop_duplicates()

# combine with stock data
merged_df = stocklevel_df.merge(product_categories, on="product_id", how="left")
stocklevel_df = merged_df.merge(product_price, on="product_id", how="left")
stocklevel_df.to_csv('data/sensor_stock_level_agg.csv')

stocktemp_df = convert_timestamp_to_hourly(data('data/sensor_storage_temperature.csv'),'timestamp')
stocktemp_df = stocktemp_df.groupby(by=['timestamp']).agg({'temperature' : 'mean'}).reset_index()
stocktemp_df.to_csv('data/sensor_stock_temperature_agg.csv',index=False)
