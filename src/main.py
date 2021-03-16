from fileshelper import FilesHelper
import pandas as pd
import os
import sys
import getpass
import cx_Oracle
from sqlalchemy import types, create_engine, exc
from datetime import datetime
import logging
import platform

def initialise_log_file(path = None):

    if (path is None):
        path = os.getcwd()  
        path = path + '\\Log\\'

    if not os.path.exists(path):
        os.mkdir(path)
        
    # Configuration. Log shown in console and in file
    logFilename =path + 'PythonImportFilesIntoDatabase_' + datetime.now().strftime('%Y%m%d%H%M%S%f') [:-3] + '.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:: %(message)s',
        datefmt="%d/%m/%Y %H:%M:%S",
        handlers=[
            logging.FileHandler(filename=logFilename,mode='w', encoding='iso-8859-1'),
            logging.StreamHandler()
        ]
    )
    
    logging.info('_______________________________________________________________________')
    logging.info('Starting app')
    
    logging.info(platform.platform())
    logging.info("Env thinks the user is [%s]" % (os.getlogin()))
    # logging.info("Effective user is [%s]" % (getpass.getuser()))

def main():

    server = '(localdb)\MSSQLLocalDB' 
    database = 'Pruebas' 
    username = 'myusername' 
    password = 'mypassword' 

    try:        
        
        initialise_log_file()

        filesHelper = FilesHelper()

        path = os.getcwd()  
        path = path + '\\ExampleFiles\\'
        logging.info("Searching files in " + path)
        files = filesHelper.get_all_files(path)

        if(len(files)>0):
            logging.info(str(len(files)) + " file(s) found")

            for fileName in files:
                logging.info("Processing file " + fileName)
                df = pd.read_csv(fileName,sep=',',engine='python',encoding='iso-8859-1')
                logging.info('The file contains ' + str(df.shape[0]) + ' rows')
                now = datetime.now()
                # logging.info("now =", str(now))
                # adding new LastUpdated column and renaming index column to Id
                df['LASTUPDATED'] = pd.to_datetime(now)
                df.index.rename('Id', inplace=True)
                print(df)

                table_name="Books"
                conn = create_engine('mssql+pyodbc://(localdb)\MSSQLLocalDB/Pruebas?driver=ODBC Driver 17 for SQL Server?trusted_connection=yes',encoding='iso-8859-1',echo=False)
                logging.info("Saving data in table " + table_name)
                 
                # Very important part related with perfonmance. Replace clob for varchar
                # https://stackoverflow.com/questions/42727990/speed-up-to-sql-when-writing-pandas-dataframe-to-oracle-database-using-sqlalch?noredirect=1&lq=1
                dtyp = {c:types.VARCHAR(df[c].str.len().max())
                for c in df.columns[df.dtypes == 'object'].tolist()}
        
                df.to_sql(table_name, conn, if_exists='replace', index=True,dtype=dtyp) #append

                # TODO: Replace index for Id and create primary key
                logging.info('Data saved for table ' + table_name)
        
                # # move_file_to_backups(fileName)
        
        
        logging.info('Program end')
    except exc.SQLAlchemyError  as sqlex:
        print('Sql error')
        logging.error(sqlex)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(sys.exc_info()[0])
    
if __name__=='__main__':
    main()