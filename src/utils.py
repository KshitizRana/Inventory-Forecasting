import logging
import os
from typing import List, Tuple

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log',format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S",level=logging.INFO)


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
    logger.info('Connected to the server.')
    
    return con, cr


def database(cr:str, dbname:str) -> List[Tuple[str]]: 
    """ Method to create databse using m VALUES(%s,%s) mysql query
    
    Parameters
    ----------
    cr : .
    dbname: the name of the database to create.
    
    Returns
        Returns All databases from the mysql-server.
    """

    #Drop Database 
    cr.execute(f'DROP DATABASE IF EXISTS {dbname};')
    logger.info('Database Dropped')
    
    #Create Database 
    cr.execute(f'CREATE DATABASE {dbname};')
    
    #Show all databases on the mysql-server
    cr.execute('SHOW DATABASES')
    databases = cr.fetchall()
    logger.info(f'Database Created {dbname}, {databases}')
    
    return databases


def table(cr, dbname:str, tbname: str,col_name: str) -> None:
    """ Method to perform table related operation using mysql query

    Parameters
    ----------
    cr :.
    dbname : Name of database to use .
    tbname : Name of the table to be created.
    """
    
    #Use database
    cr.execute(f'USE {dbname}')
    logger.info(f'{dbname} database selected.')
    
    #Drop Table# load_dotenv(".env")
    cr.execute(f'DROP TABLE IF EXISTS {tbname}')
    logger.info("Table Dropped name=%s",tbname)
    
    #Create Table
    cr.execute(f'CREATE Table {tbname} ({col_name});')
    logger.info('Table Created')


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
    """ Method to remove Unnamed: 0 Column.

    Parameters
    ----------
    filepath : Path of the file

    Returns
    -------
    Data Frame removed with Unamed: 0 Column
    
    """
    df = pd.read_csv(filepath)
    logger.info('Data Frame Created')
    
    df.drop(['Unnamed: 0'],axis=1,inplace=True,errors='ignore')
    logger.info('Unnamed: 0 Column Dropped')
    
    return df


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
        elif col_dtypes == 'int64':
            types = types +f"{col_name} INT, "
        
            
    types = types[:-2]
    placeholders = ', '.join(len(df.columns)*['%s'])
    logger.info('Datatypes converted from python to mysql.')
    
    return types, placeholders