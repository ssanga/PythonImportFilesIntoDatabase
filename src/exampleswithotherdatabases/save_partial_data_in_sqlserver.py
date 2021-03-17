# https://docs.microsoft.com/es-es/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15

import pyodbc 
import pandas as pd
import sqlalchemy
from sqlalchemy import types, create_engine, exc
import sys
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = '(localdb)\MSSQLLocalDB' 
database = 'Pruebas2' 
username = 'myusername' 
password = 'mypassword' 
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+ ';Trusted_Connection=yes;')
# cursor = cnxn.cursor()

# cursor.execute("SELECT @@version;") 
# row = cursor.fetchone() 
# while row: 
#     print(row[0])
#     row = cursor.fetchone()

try:

    # https://stackoverflow.com/questions/46045834/pyodbc-data-source-name-not-found-and-no-default-driver-specified
    conn = create_engine('mssql+pyodbc://(localdb)\MSSQLLocalDB/Pruebas2?driver=ODBC Driver 17 for SQL Server?trusted_connection=yes')
    # df =  pd.read_sql_table('Employees', conn)
    # print(df)

    # df = df.append({'Id':0, 'Name':'Santi', 'Department':'HR', 'Salary':1}, ignore_index=True)

    # df=df.drop(columns=['Id'])

    # df.to_sql('Employees', conn, if_exists='append', index=False) #append #replace
    # df =  pd.read_sql_table('Employees', conn)

    data = {'Name': 'Santi2', 'Department': 'New', 'Salary':50000}
    df2 = pd.DataFrame([data])
    print(df2)
    df2.to_sql('Employees', conn, if_exists='append', index=False) #append #replace
    df =  pd.read_sql_table('Employees', conn)

    print(df)
except exc.SQLAlchemyError  as sqlex:
    print('Sql error')
    # logging.error(sqlex)
except:
    print("Unexpected error:", sys.exc_info()[0])
    # logging.error(sys.exc_info()[0])