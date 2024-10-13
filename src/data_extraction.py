from pathlib import Path

import mysql.connector as mysql
import pandas as pd

from utils import dbconnect, download_from_s3, upload_to_s3


def execute_sql_from_file(file_path: str) -> pd.DataFrame:
    """
    Executes SQL queries from a file on the given MySQL connection and cursor.

    Args:
        file_path (str): The path to the SQL file.

    Returns:
        pd.DataFrame: A DataFrame containing the query results.

    Raises:
        mysql.Error: If there is an error executing the SQL queries.
    """
    cnx, cur = dbconnect('localhost','root', dbname='Agg_store')
    with open(file_path, 'r') as sql_file:
        sql = sql_file.read()
    try:
        cur.execute(sql)
        cur.fetchall()
        df = pd.read_sql(sql, cnx)
        cur.close()
        cnx.close()
        return df
    except mysql.Error as err:
        raise mysql.Error(f"Error executing SQL query: {err}")
    

def process():
    """
    Execute SQL script to join tables, load data into a Pandas DataFrame, 
    and upload the resulting DataFrame to an S3 bucket.
    """
    sql_script = Path('src/forecasting_data.sql')
    df = execute_sql_from_file(sql_script)
    df['is_forecast'] = False
    upload_to_s3(df = df, bucket_name = 'inventory-agg-data', file_name = 'Inventory_historical_data')
    return df