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

def create_database(cr,con,query:str):
    cr.execute(query)
    
def create_table(cr,con,query:str):
      
      cr.execute(query)

def insert_into_table(cr,con,query:str,val):
    cr.executemany(query,val)
    db.commit()
    print(cr.rowcount,"was inserted.")
