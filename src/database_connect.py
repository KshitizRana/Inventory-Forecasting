# import os
# from dotenv import load_dotenv
import mysql.connector

#Connection to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password = 'password',
)

#Create a Cursor
cr = db.cursor(buffered=True)

#Create Database Inventory
# cr.execute("DROP DATABASE INVENTORY;")
# cr.execute("CREATE DATABASE INVENTORY;")
cr.execute("SHOW DATABASES;")

#Creating table Customers with name and membership
cr.execute("USE INVENTORY;")
# cr.execute("CREATE TABLE customers (name VARCHAR(255), membership CHAR(50));")
cr.execute("SHOW TABLES;")

#Insert Values in table Customers
val = [
  ('Peter', 'basic'),
  ('Amy', 'premium'),
  ('Hannah', 'bronze'),
  ('Michael', 'non-member'),
  ('Sandy', 'gold'),
  ('Betty', 'silver'),
  ('Richard', 'basic'),
  ('Susan', 'basic'),
  ('Vicky', 'non-member'),
  ('Ben', 'premium'),
  ('William', 'bronze'),
  ('Chuck', 'gold'),
  ('Viola', 'non-member')
]

query = "INSERT INTO customers (name, membership) VALUES (%s, %s);"
cr.executemany(query,val)

db.commit()

print(cr.rowcount,"was inserted.")
