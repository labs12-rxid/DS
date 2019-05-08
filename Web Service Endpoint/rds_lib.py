import psycopg2
from sqlalchemy import create_engine


#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    engin = db_connect()
    verify_output(engin)
    #  echo the output for now  -- needs query code 
    return parameter_list


#  ____________  CONNECT TO DATABASE ___________________
def db_connect():
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
    return pgres_engine


# ________  SQL Queries ______
def verify_output(pgres_engine):
    # ______  verify output-table contents ____
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    query = 'SELECT * FROM ' + table_string + ' LIMIT 10;'
    for row in pgres_engine.execute(query).fetchall():
        print(row)
    return
