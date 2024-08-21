import logging
import os
from typing import List, Tuple

import boto3
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log',format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S",level=logging.INFO)


def aws_auth():
    """ Method to connect to AWS S3.
    
    Parameters
    ----------
    akeys : (str) Acess Keys.
    skeys : (str) Secret Keys.
    rname : (str) Give region name.

    Returns
    -------
        Returns client connected with AWS boto3 client.
    """
    
    s3 = boto3.client('s3',
                        aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))
    
    logger.info("Connected to AWS S3")
    return s3
    
    
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


def upload_to_s3(df: pd.DataFrame, bucket_name: str, file_name: str):
    """_Method to upload files to s3 bucket.

    Parameters
    ----------
    s3 : Connection to bucket.
    file : Filepath for file to be uploaded to bucket.
    bucket_name : Bucket name where file to be uploaded.
    object_name : Key to the file to identify in bucket.
    """
    s3 = aws_auth()
    csv_data = df.to_csv(index = False)
    s3.put_object(Body = csv_data,
                  Bucket = bucket_name,
                  Key = f'{file_name}.csv')
    logger.info(f'Successfully Uploaded data in {bucket_name} as {file_name}')
    

def download_from_s3(bucket,key_name,file_name):
    """Method to download file from AWS S3

    Parameters
    ----------
    s3 : 
    bucket : Name of bucket to download from.
    key_name : The name of the key to download from.
    file_name : The name to the file to download
    """
    s3 = aws_auth()
    response = s3.get_object(bucket,key_name,file_name)
    df = pd.read_csv(response['Body'])
    logger.info(f'Successfully Downloaded data from {bucket} as {file_name}')   
    
    return df
    
    