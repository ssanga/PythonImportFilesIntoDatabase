#https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
#https://stackoverflow.com/questions/47540837/how-to-write-pandas-dataframe-to-oracle-database-using-to-sql
#https://stackoverflow.com/questions/36778688/pandas-to-oracle-via-sql-alchemy-unicodeencodeerror-ascii-codec-cant-encode
#https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
#https://stackoverflow.com/questions/39504351/save-pandas-string-object-column-as-varchar-in-oracle-db-instead-of-clob-defa/39514888
#pip install --proxy cecada\user:password@proxy:port cx_Oracle


def truncate_table(engine, tableName):
    import sqlalchemy
    
    connection = engine.connect()
    truncate_query = sqlalchemy.text("TRUNCATE TABLE " + tableName)
    connection.execution_options(autocommit=True).execute(truncate_query)
    

    
def main():
    
    try:
        import pandas as pd
        import os
        import sys
        import getpass
        # Es necesario establecer el lenguaje de Oracle a español para guardar tildes
        os.environ["NLS_LANG"] = "SPANISH_SPAIN.WE8ISO8859P1"

        import cx_Oracle
        from sqlalchemy import types, create_engine, exc
        from datetime import datetime
        import logging
        import platform
        
        path = os.getcwd()  
        path = path + '\\Log\\'

        if not os.path.exists(path):
            os.mkdir(path)
            
        input_files_path = os.getcwd()  
        input_files_path = input_files_path + '\\Input\\'

        if not os.path.exists(input_files_path):
            os.mkdir(input_files_path)
      
        # Configuración del fichero de log para que muestre la info por fichero y por consola
        logFilename =path + 'SalvarTablaEmpleados_' + datetime.now().strftime('%Y%m%d%H%M%S%f') [:-3] + '.log'
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
        logging.info('Iniciando aplicación')
        
        logging.info(platform.platform())
        logging.info("Env thinks the user is [%s]" % (os.getlogin()))
        logging.info("Effective user is [%s]" % (getpass.getuser()))
        
        logging.info('Se va a procesar el último fichero encontrado en la carpeta ' + input_files_path)
        fileName = get_newest_file(input_files_path)
        
        # dir_path = os.path.dirname(os.path.realpath("__file__"))
        # fileName = dir_path + "/BPM2000EM23062020.txt" 
        
        logging.info('Se va a leer el fichero ' + fileName)
        
        # El fichero termina en ; lo que genera una columna más
        # Es necesario reemplazar ;\n por \n antes de leer el fichero con pandas. Si no se hace así, crea una columna de más y no casan los datos con la cabecera
        # Read in the file
        with open(fileName, 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(';\n', '\n')

        # Write the file out again
        with open(fileName, 'w') as file:
            file.write(filedata)

        # df = pd.read_csv(fileName,sep=';',engine='python',encoding='iso-8859-1',header=None, names=['CODIGO_USUAR','NOMBRE','APELLID1','APELLID2','COD_CENTRO','TXT_CENTRO'])
        # df = pd.read_csv(fileName,sep=';',engine='python',encoding='iso-8859-1',header=None)
        df = pd.read_csv(fileName,sep=';',engine='python',encoding='iso-8859-1')
        
        # El indice por defecto se llama index y es una palabra reservada de Oracle, de esta forma cambiamos el nombre por Id
        df.index.rename('Id', inplace=True)

        # Si se pone rara la cosa con la cabecera se puede usar esta forma para poner nombre a las columnas. También se puede usar la colección names en la lectura del dataframe
        #df.rename(columns={0:'CODIGO_USUAR'}, inplace=True)
        
        print (df)
        # logging.info(df.shape)
        # logging.info(df.info())
        # df.info()
        
        # logging.info(df)
        
        logging.info('El fichero contiene ' + str(df.shape[0]) + ' filas')
        
        now = datetime.now()
        logging.info("now =", str(now))

        # Se incluye una nueva columna para ver en qué fecha se cargó la tabla por última vez
        df['LASTUPDATED']=pd.to_datetime(now)

        logging.info('Se va a generar la cadena de conexión')
        conn = create_engine('oracle+cx_oracle://user:password@sid:port/?service_name=servicename',encoding='iso-8859-1',echo=True)

        #truncate_table(conn,'organigrama2')
        logging.info('Se van a guardar los datos en la tabla organigrama2')
        
        # Esta parte es muy importante para el rendimiento, se sustituyen los campos de tipo clob por varchar
        # https://stackoverflow.com/questions/42727990/speed-up-to-sql-when-writing-pandas-dataframe-to-oracle-database-using-sqlalch?noredirect=1&lq=1
        dtyp = {c:types.VARCHAR(df[c].str.len().max())
            for c in df.columns[df.dtypes == 'object'].tolist()}
        
        # df.to_sql('organigrama2', conn, if_exists='replace', index=True,dtype={'NOMBRE': types.VARCHAR(df.NOMBRE.str.len().max())}) #append
        # df.to_sql('organigrama2', conn, if_exists='replace', index=True,dtype=dtyp) #append
        df.to_sql('empleados', conn, if_exists='replace', index=True,dtype=dtyp) #append
        
        # move_file_to_backups(fileName)
        
        logging.info('Datos salvados correctamente')
        logging.info('finalizado')
    except exc.SQLAlchemyError  as sqlex:
        print('Sql error')
        logging.error(sqlex)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        logging.error(sys.exc_info()[0])
    

if __name__=='__main__':
    print('inicio de la app 12')
    main()