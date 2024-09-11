import pandas as pd

from utils import data

# Convert timestamp to hourly level
def convert_timestamp_to_hourly(df: pd.DataFrame = None, column: str = None) -> pd.DataFrame:
    """
    Convert timestamp to hourly level

    Args:
        df (pd.DataFrame, optional): Input dataframe. Defaults to None.
        column (str, optional): Column related to datetime data. Defaults to None.

    Returns:
        DataFrame: resultant dataframe with hourly timestamps.
    """
    dummy = df.copy()
    dummy[column] = pd.to_datetime(dummy[column], format='%Y-%m-%d %H:%M:%S')  # String to datetime datatype conversion
    dummy[column] = dummy[column].dt.floor('h')  # Truncate timestamps to beginning of hour
    return dummy
    

# Aggregate data
sales_df = convert_timestamp_to_hourly(data('data/sales.csv'),'timestamp')
salesagg_df = sales_df.groupby(by=['timestamp','product_id']).agg({'quantity' : 'sum'}).reset_index()
salesagg_df.to_csv('data/sales_agg.csv',index=False)

stocklevel_df = convert_timestamp_to_hourly(pd.read_csv('data/sensor_stock_levels.csv'),'timestamp')
stocklevel_df = stocklevel_df.groupby(by=['timestamp','product_id']).agg({'estimated_stock_pct' : 'mean'}).reset_index()
# extract additional columns from sales data
product_categories = df1[['product_id', 'category']].drop_duplicates()
product_price = df1[['product_id', 'unit_price']].drop_duplicates()

# combine with stock data
merged_df = stocklevel_df.merge(product_categories, on="product_id", how="left")
stocklevel_df = merged_df.merge(product_price, on="product_id", how="left")
stocklevel_df.to_csv('data/sensor_stock_level_agg.csv')

stocktemp_df = convert_timestamp_to_hourly(pd.read_csv('data/sensor_storage_temperature.csv'),'timestamp')
stocktemp_df = stocktemp_df.groupby(by=['timestamp']).agg({'temperature' : 'mean'}).reset_index()
stocktemp_df.to_csv('data/sensor_stock_temperature_agg.csv',index=False)
