import pandas as pd
from utils import  dbconnect, upload_to_s3

def sqlquery(sql_query: str) -> pd.DataFrame:
    """ Method to left join tables 

    Parameters
    ----------
    sql_query : Query to left join stock_level, sales and stock_temperature 

    Returns
    -------
    Dataframe of joined table
    """
    conn, cur = dbconnect('localhost','root')

    with open(sql_query,'r') as q:
        query = q.read()

    cur.execute(query)
    cur.fetchall()
    df = pd.read_sql(query,conn)
    return df


def process():
    """
    Function for process the code sequentially.
    Returns
    -------
    
    """
    
    sql_query = "src/data_extraction.sql"
    df = sqlquery(sql_query = sql_query)
    
    return upload_to_s3(df = df, bucket_name = 'inventory_data', file_name = 'Inventory_historical_data')