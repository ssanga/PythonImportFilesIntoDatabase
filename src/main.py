from fileshelper import FilesHelper
import pandas as pd
import os
import sys
from sqlalchemy import types, create_engine, exc
from datetime import datetime
import logging
import platform
import getpass
# import cx_Oracle


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
    logging.info("Effective user is [%s]" % (getpass.getuser()))

def main():

    server = '(localdb)\MSSQLLocalDB' 
    database = 'Pruebas' 
    username = 'myusername' 
    password = 'mypassword' 

    try:        
        
        initialise_log_file()

        filesHelper = FilesHelper()

        searchpath = os.getcwd()  
        searchpath = searchpath + '\\ExampleFiles\\'
        logging.info("Searching files in " + searchpath)
        files = filesHelper.get_all_files(searchpath)

        if(len(files)>0):
            logging.info(str(len(files)) + " file(s) found")

            for fileName in files:
                logging.info("Processing file " + fileName)
                df = pd.read_csv(fileName,sep=',',engine='python',encoding='iso-8859-1')
                logging.info('The file contains ' + str(df.shape[0]) + ' rows')
                now = datetime.now()
                logging.info("now =", str(now))
                # adding new LastUpdated column and renaming index column to Id
                df['LASTUPDATED'] = pd.to_datetime(now)
                df.index.rename('Id', inplace=True)

                table_name = filesHelper.get_file_name_without_extension(fileName)

                conn = create_engine('mssql+pyodbc://(localdb)\MSSQLLocalDB/Pruebas?driver=ODBC Driver 17 for SQL Server?trusted_connection=yes',encoding='iso-8859-1',echo=False)
                logging.info("Saving data in table " + table_name)
                 
                # Very important part related with perfonmance. Replace clob for varchar and set the maxlength of the field
                # https://stackoverflow.com/questions/42727990/speed-up-to-sql-when-writing-pandas-dataframe-to-oracle-database-using-sqlalch?noredirect=1&lq=1
                dtyp = {c:types.VARCHAR(int(df[c].str.len().max()))
                for c in df.columns[df.dtypes == 'object'].tolist()}
        
                df.to_sql(table_name, conn, if_exists='replace', index=False,dtype=dtyp) #append
                # df.to_sql(table_name, conn, if_exists='replace', index=True,dtype=dtyp) #append

                with conn.connect() as con:
                    # con.execute('ALTER TABLE '+ table_name + ' ALTER COLUMN Id bigint NOT NULL')
                    # con.execute('ALTER TABLE '+ table_name + ' ADD CONSTRAINT PK_' +table_name +' PRIMARY KEY(Id)')
                    # con.execute('ALTER TABLE dbo.' + table_name + ' ADD COLUMN Id FIRST')
                    # con.execute('ALTER TABLE dbo.' + table_name + ' ADD Id bigint IDENTITY CONSTRAINT PK_'+ table_name + ' PRIMARY KEY CLUSTERED ')
                    script = 'ALTER TABLE dbo.' + table_name + ' ADD Id bigint IDENTITY CONSTRAINT PK_'+ table_name + ' PRIMARY KEY CLUSTERED '
                    logging.info(script)
                    con.execute(script)
                    # con.execute('ALTER TABLE '+ table_name + ' ALTER COLUMN Id bigint NOT NULL')
                    
                logging.info('Data saved for table ' + table_name)

                logging.info('Moving file from input to backup folder ')
                file_prefix = now.strftime('%Y%m%d%H%M%S%f') [:-3]
                filesHelper.move_file_to_backups(fileName, file_prefix)

        else:
            logging.warning('No file(s) found in ' + searchpath)
        
        logging.info('Program end')
    except exc.SQLAlchemyError  as sqlex:
        print('Sql error')
        logging.error(sqlex)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(sys.exc_info()[0])
    
if __name__=='__main__':
    main()