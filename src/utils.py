import os
from typing import Tuple 
from typing import List
from dotenv import load_dotenv
import mysql.connector
import pandas as pd

load_dotenv(".env")

def dbconnect(
    hostname: str,
    username: str,
    dbname = None)-> Tuple[str,str]: 
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

    cr = con.cursor(buffered=True)
    print(f'Connection Stablished')
    return con, cr


def database(cr, dbname: str) -> List[Tuple[str]] : 
    """ Method to create databse using m VALUES(%s,%s)ysql query
    
    Parameters
    ----------
    cr : .
    dbname: the name of the database to create.
    """

    #Drop Database 
    cr.execute(f'DROP DATABASE IF EXISTS {dbname};')
    
    #Create Database 
    cr.execute(f'CREATE DATABASE {dbname};')
    
    #Show all databases on the mysql-server
    cr.execute(f'SHOW DATABASES;')
    databases = cr.fetchall()
    return databases


def table(cr, dbname:str, tbname: str):
    """ Method to perform table related operation using mysql query

    Parameters
    ----------
    cr :.
    dbname : Name of database to use .
    tbname : Name of the table to be created.
    """
    
    #Use database
    cr.execute(f'USE DATABASE {dbname}')
    
    #Drop Table# load_dotenv(".env")
    cr.execute(f'DROP TABLE IF EXISTS {tbname}')
    
    #Create Table
    
    cr.execute(f'CREATE Table {tbname} (name VARCHAR(50), membership VARCHAR(50));')


def insert_table(cr,con,query,val):
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
