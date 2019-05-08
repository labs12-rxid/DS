#  ________ CONVERT Pill CSV data to SQL _____________
import pandas as pd
import sqlite3
import psycopg2
from sqlalchemy import create_engine
from sqlite3 import dbapi2 as sqlite


def verify_output(pgres_engine, table_name):
    # ______  verify output-table contents ____
    query = 'SELECT * FROM ' +  table_name + ' LIMIT 10;'
    for row in pgres_engine.execute(query).fetchall():
        print(row)
    return


def run_conversion(engine):
    # ___ load the CSV into a df ____
    csv_url = "Pills.Final.csv"
    df = pd.read_csv(csv_url)
    
    # ___ process tables ____
    # - WARNING!  schema must already exist in AWS-RDS
    schema_name = 'rxid'
    tables = ['rxid_meds_data']
    for table_name in tables:
        print('converting........ ', table_name)
        #  BUG ALERT! drop the dataframe index column
        #             before executing .to_sql()
        # ___ Convert to postgres DB____
        df.to_sql(table_name,
                  if_exists='replace',
                  con=engine,
                  schema=schema_name,
                  chunksize=1000,
                  index=False,
                  method='multi')

        #_____  VERIFY _______________
        verify_output(engine, (schema_name + "." + table_name))
    return

def main():
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = ''
    user = ''
    host = ''
    password = ''
    file = open('aws.rxidds.pwd', 'r')
    ctr = 1
    for line in file:
        line = line.replace('\n', '')
        if ctr == 1: dbname = line
        if ctr == 2: user = line
        if ctr == 3: host = line
        if ctr == 4: passw = line
        ctr = ctr + 1
    pgres_str = 'postgresql+psycopg2://'+user+':'+passw+'@'+host+'/'+dbname
    pgres_engine = create_engine(pgres_str)

    # ____ Port CSV to AWS_RDS(postgres) ___
    run_conversion(pgres_engine)

    # ___ end main ___________
    print('Conversion successful.....')
    return

#  Launched from the command line
if __name__ == '__main__':
    main()