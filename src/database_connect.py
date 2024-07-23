from src.utils import database, dbconnect, table

# load_dotenv(".env")

#Connection to database
db,cr = dbconnect('localhost','root')


#Create Database Inventory
databases = database(cr,'INVENTORY')
print(databases)


#Creating table Customers with name and membership
table(cr,'INVENTORY','customer')


#Insert Values in table Customers