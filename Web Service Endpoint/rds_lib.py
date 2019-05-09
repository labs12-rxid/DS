import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine


#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    imprint = parameter_list.get('imprint')
    db_context = db_connect() # 'aws.rxidds.pwd'
    
    schema = 'rxid'
    table = 'rxid_meds_data'
    schema_table = schema + '.' + table 
    
    query = 'SELECT * FROM ' + schema_table + ' LIMIT 10;'
    
    results = db_context.execute(query).fetchall()

    return results


#  ____________  CONNECT TO DATABASE ___________________
def db_connect(): # pwd_file
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = 'rxidDS'
    user = 'rxidDS'
    host = 'rxidds.cqqygklpjkea.us-east-2.rds.amazonaws.com'
    passw = 'rxid_lambda'
    # file = open(pwd_file, 'r')
    # ctr = 1
    # for line in file:
    #     line = line.replace('\n', '')
    #     if ctr == 1: dbname = line
    #     if ctr == 2: user = line
    #     if ctr == 3: host = line
    #     if ctr == 4: passw = line
    #     ctr = ctr + 1
    pgres_str = 'postgresql+psycopg2://'+user+':'+passw+'@'+host+'/'+dbname
    pgres_engine = create_engine(pgres_str)
    return pgres_engine


# ________  SQL Queries ______
def verify_output(pgres_engine):
    # ______  verify output-table contents ____
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    
    # Query in JSON format for each row in SQL:
    # https://stackoverflow.com/questions/25564654/select-query-in-row-to-json-function
    # Name of relevant columns based on pillbox results (col_name = pillbox_label):
        # splimprint = imprint, medicine_name = name, setid = drug label,
        # spl_ingredients = ingredients, author = label author, splsize = size, 
        # splscore = score, spl_inactive_ing = inactive ingredients, product_code = product code
    
    query = """
            SELECT row_to_json(t) 
            FROM (
                SELECT splimprint, 
                medicine_name, 
                setid, 
                spl_ingredients, 
                author, 
                splsize, 
                splscore, 
                spl_inactive_ing, 
                product_code 
                FROM """ + table_string + """) t 
            LIMIT 5;"""

    results = pgres_engine.execute(query).fetchall()
    print(results)
    
    return

# __________ M A I N ________________________
if __name__ == '__main__':
    engine = db_connect() # 'aws.rxidds.pwd'
    verify_output(engine)