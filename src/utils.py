import os
from typing import List, Tuple

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")

def dbconnect(hostname: str,
              username: str,
              dbname:str = None)-> Tuple[str,str]: 
    """
    Method to connect database and python Script
    
    Parameters
    ----------
    hostname : (str) host name of mysql-server.
    username : (str) username of mysql-server.
    dbname : (str) name of database to be accessed.
    
    Returns
        Returns Tuple(con,cr) connection and cursor
    """
    
    con = mysql.connector.connect(host=hostname,
                                  user=username,
                                  password = os.getenv("PASSWORD"),
                                  database = dbname)

    cr = con.cursor()
    print('Connection Stablished')
    return con, cr


def database(cr:str, dbname:str) -> List[Tuple[str]]: 
    """ Method to create databse using m VALUES(%s,%s)ysql query
    
    Parameters
    ----------
    cr : .
    dbname: the name of the database to create.
    
    Returns
        Returns All databases from the mysql-server
    """

    #Drop Database 
    cr.execute(f'DROP DATABASE IF EXISTS {dbname};')
    
    #Create Database 
    cr.execute(f'CREATE DATABASE {dbname};')
    
    #Show all databases on the mysql-server
    cr.execute('SHOW DATABASES')
    databases = cr.fetchall()
    return databases


def table(cr, dbname:str, tbname: str) -> None:
    """ Method to perform table related operation using mysql query

    Parameters
    ----------
    cr :.
    dbname : Name of database to use .
    tbname : Name of the table to be created.
    """
    
    #Use database
    cr.execute(f'USE {dbname}')
    
    #Drop Table# load_dotenv(".env")
    cr.execute(f'DROP TABLE IF EXISTS {tbname}')
    
    #Create Table
    cr.execute(f'CREATE Table {tbname} (name VARCHAR(50), membership VARCHAR(50));')


def insert_table(cr,con,query,val) :
    """ Method to insert into table 

    Parameters
    ----------
    cr : cursor.
    con : databse connection to fetch and commit to mysql-server.
    query : query related to insertion of values in table .
    val : data to be inserted in the table .
    """
    
    # Insert Values
    cr.executemany(query,val)
    con.commit()
    print(cr.rowcount,"was inserted.")


def data(filepath):
    df = pd.read_csv(filepath)
    df.drop(['Unnamed: 0'],axis=1,inplace=True,errors='ignore')
    return df

ds=data('./data/sales.csv')
ds.to_csv('./data/test.csv',index=True)
ds2=data('./data/test.csv')

def convert_dtypes(df):
    """Method to convert datatypes of the columns from python dtypes to sql dtypes

    Parameters
    ----------
    df : dataframe 

    Returns
    -------
        types: String with coverted datatypes of different columns from python to sql datatypes
        placeholders : no. of place holders for no. of columns to insert values 
    """
    types = ""
    for i, col_dtypes in enumerate(df.dtypes):
        
        col_name = df.columns[i]
        col_name = col_name.replace('.','_')
        
        if col_dtypes == 'object':
            types = types + f"{col_name} VARCHAR(255), "
        elif col_dtypes == 'float64':
            types = types +f"{col_name} FLOAT, "
    
    print(types)
    
    placeholders = ', '.join(len(df.columns)*['%s'])
    print(placeholders)
    return types, placeholders

types, placeholders = convert_dtypes(df)

total = 0
for _, row in df.iterrows():
    sql = f"INSERT INTO customers VALUES ({placeholders})"
    val = tuple(row)
    # print(val)
    cr.execute(sql, val)
    if cr.rowcount == 1:
        total += 1
con.commit() 