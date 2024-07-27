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
types, placeholders = convert_dtypes(df)

total = 0
for _, row in df.iterrows():
    sql = f"INSERT INTO customers VALUES ({placeholders})"
    val = tuple(row)
    cr.execute(sql, val)
    if cr.rowcount == 1:
        total += 1
con.commit() 