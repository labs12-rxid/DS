import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


#  ____________  CONNECT TO DATABASE ___________________
def db_connect(): 
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = os.getenv("DS_DB_NAME")
    user = os.getenv("DS_DB_USER")
    host = os.getenv("DS_DB_HOST")
    passw = os.getenv("DS_DB_PASSWORD")
    pgres_str = 'postgresql+psycopg2://'+user+':'+passw+'@'+host+'/'+dbname
    pgres_engine = create_engine(pgres_str)
    return pgres_engine
#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    im_print = parameter_list.get('imprint')
    pill_name = parameter_list.get('pill_name')
    sha_pe = parameter_list.get('shape')
    col_or = parameter_list.get('color')

    db_engine = db_connect()
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    query = """SELECT
                    author,
                    splimprint,
                    image_id,
                    spl_strength,
                    spl_ingredients,
                    splsize,
                    splcolor_text,
                    splshape_text,
                    product_code,
                    DEA_SCHEDULE_CODE,
                    setid,
                    spl_inactive_ing
                    FROM """ + table_string + """ 
                WHERE """

    """
        WHERE splimprint  ILIKE ''       im_print
        AND splshape_text ILIKE 'OVAL'   shape_text
        AND splcolor_text ILIKE 'YELLOW'  color_text
        
        ----use double %% for wildcards!!!!!----
        AND medicine_name ILIKE '%%PANTO%%'  pill_name
    """
    results = db_engine.execute(query).fetchall()
    df = pd.DataFrame(results, columns=['author', 
                                        'imprint',
                                        'image_id',
                                        'spl_strength',
                                        'medicine_name',
                                        'size',
                                        'color_text',
                                        'shape_text',
                                        'product_code',
                                        'DEA_schedule',
                                        'setid',
                                        'spl_inactive_ing' ])
    df.loc[df['image_id'] != None, 'image_id'] += '.jpg'
    results_json = df.to_json(orient='records')
    return results_json[1:-1]

# __________ M A I N ________________________
if __name__ == '__main__':
    print('Hello')
