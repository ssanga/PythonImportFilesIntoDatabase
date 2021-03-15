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
    logging.info("Effective user is [%s]" % (getpass.getuser()))

def main():
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
                # adding new LastUpdated column
                df['LASTUPDATED'] = pd.to_datetime(now)
                print(df)


        # logging.info('Se va a generar la cadena de conexión')
        # conn = create_engine('oracle+cx_oracle://user:password@sid:port/?service_name=servicename',encoding='iso-8859-1',echo=True)

        # #truncate_table(conn,'organigrama2')
        # logging.info('Se van a guardar los datos en la tabla organigrama2')
        
        # # Esta parte es muy importante para el rendimiento, se sustituyen los campos de tipo clob por varchar
        # # https://stackoverflow.com/questions/42727990/speed-up-to-sql-when-writing-pandas-dataframe-to-oracle-database-using-sqlalch?noredirect=1&lq=1
        # dtyp = {c:types.VARCHAR(df[c].str.len().max())
        #     for c in df.columns[df.dtypes == 'object'].tolist()}
        
        # # df.to_sql('organigrama2', conn, if_exists='replace', index=True,dtype={'NOMBRE': types.VARCHAR(df.NOMBRE.str.len().max())}) #append
        # # df.to_sql('organigrama2', conn, if_exists='replace', index=True,dtype=dtyp) #append
        # df.to_sql('empleados', conn, if_exists='replace', index=True,dtype=dtyp) #append
        
        # # move_file_to_backups(fileName)
        
        # logging.info('Datos salvados correctamente')
        # logging.info('finalizado')
    except exc.SQLAlchemyError  as sqlex:
        print('Sql error')
        logging.error(sqlex)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(sys.exc_info()[0])
    
if __name__=='__main__':
    main()