import mysql.connector


def dbconnect(
    hostname: str,
    username: str,
    dbname:str):
    """
    Method to connect database and python Script
    
    Parameters
    ----------
    hostname : (str) host name of mysql-server 
    username : (str) username of mysql-server
    dbname : (str) name of database to be accessed 
    
    Returns
        Returns Tuple(con,cr) connection and cursor
    """
    
    con = mysql.connector.connect(host=hostname,
                                  user=username,
                                  password = 'password',
                                  database = dbname)

    cr = con.cursor()
    return con, cr


def database(cr,query:str):
    """ Method to create databse using mysql query
    
    Parameters
    ----------
    cr : 
    query : query related to database creation,show , drop etc
    """
    cr.execute(query)


    
def table(cr,query:str):
    """Method to perform table related operation using mysql query

    Parameters
    ----------
    cr :
    query : query related to table creation, drop and use etc 
    """
    cr.execute(query)

def insert_table(cr,con,query:str,val):
    """_summary_

    Parameters
    ----------
    cr : cursor
    con : databse connection to fetch and commit to mysql-server
    query : query related to insertion of values in table 
    val : data to be inserted in the table 
    """
    cr.executemany(query,val)
    con.commit()
    
    print(cr.rowcount,"was inserted.")
