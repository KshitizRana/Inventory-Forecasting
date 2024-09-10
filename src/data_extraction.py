from pathlib import Path

import mysql.connector as mysql
import pandas as pd

from src.utils import connector


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
    cnx, cur = dbconnect('localhost','root', dbname='processed_inventory_data')
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
    sql_script = Path('src/forecast_extraction.sql')
    df = execute_sql_from_file(sql_script)
    return df
  
