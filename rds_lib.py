import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd


#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    im_print = "'"+parameter_list.get('imprint')+"'"
    print (im_print)
    im_print = "'WATSON;151;4;mg'"
    db_engine = db_connect()
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    query = """
            SELECT
                    author,
                    splimprint,
                    image_id,
                    medicine_name,
                    splsize,
                    splcolor_text,
                    splshape_text,
                    product_code,
                    DEA_SCHEDULE_CODE,
                    splscore,
                    setid
                    FROM """ + table_string + """ WHERE splimprint LIKE """ + im_print + """
            LIMIT 25;"""

    results = db_engine.execute(query).fetchall()
    # Passing SQL query into a Pandas DF
    df = pd.DataFrame(results, columns=['author', 'imprint', 'image_id', 'medicine_name', 'size', 'color_text', 'shape_text', 'product_code', 'DEA_schedule', 'score', 'setid' ])
    # Adding '.jpg' to image_id's
    df.loc[df['image_id'] != None, 'image_id'] += '.jpg'
    # Passing DF to JSON
    results_json = df.to_json(orient='records')
    
    return results_json


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
        # spl_strength = ingredients, author = label author, splsize = size, 
        # splscore = score, spl_inactive_ing = inactive ingredients, product_code = product code
    im_print = "'WATSON;151;4;mg'"

    query = """
            SELECT
                    author,
                    splimprint,
                    image_id,
                    medicine_name,
                    splsize,
                    splcolor_text,
                    splshape_text,
                    product_code,
                    DEA_SCHEDULE_CODE,
                    splscore,
                    setid
                    FROM """ + table_string + """ WHERE splimprint LIKE """ + im_print + """
            LIMIT 25;"""

    results = pgres_engine.execute(query).fetchall()
    print(results)
    return 

# __________ M A I N ________________________
if __name__ == '__main__':
    #engine = db_connect('aws.rxidds.pwd')
    #verify_output(engine)

    print(query_sql_data({"imprint":"WATSON;151;4;mg", "color": 12 , "shape": 5 }))

