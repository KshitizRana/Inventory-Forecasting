import argparse
import yaml
from pathlib import Path
import os

from utils import (convert_dtypes, get_data, database, dbconnect, download_from_s3,
                   table, upload_to_s3)

parser = argparse.ArgumentParser(
    description = 'Database script to connect to mysql server, create database, table and insert data to the table.'
    )
parser.add_argument('-cd', '--create_db', type = bool, help = 'Do you wanna create new database or work on existing database ?')
parser.add_argument('-db', '--database_name',type = str, required = True, help = 'Provide a name for the database.')
parser.add_argument('-id', '--task_id', type=str, help='The tasks defined in the config files.')
args = parser.parse_args()

# load tasks from config --------------------------------------------------------------
with open("./config/config.yml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

#Connection to database
db,cr = dbconnect('localhost','root')

#Create Database 
if args.create_db:
    databases = database(cr=cr,dbname=args.database_name)
else:
    # define variables
    config_import = config[args.task_id]["import"]
    for i in range(len(config_import)):
        data = Path(config_import[i]["import"]["dirpath"],
                    config_import[i]["import"]["prefix_filename"] + '.' +
                    config_import[i]["import"]["file_extension"])
        table_name = os.path.basename(data).split('.')[0]
        #Insert Values in table Customers
        file_df = get_data(filepath = data)
        types, placeholders = convert_dtypes(file_df)
        
        #Creating table  
        table(cr = cr, dbname = args.database_name, tbname = table_name, col_name = types)
        total = 0
        for _, row in file_df.iterrows():
            sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            # val = tuple(row)
            # print(val)
            cr.execute(sql, tuple(row))
            db.commit() 
            if cr.rowcount == 1:
                total += 1
db.close()
cr.close()
