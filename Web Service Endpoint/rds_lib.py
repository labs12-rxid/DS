import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd
from itertools import permutations
import json
from dotenv import load_dotenv
import os

load_dotenv()

# ______query_from rekog __________
def query_from_rekog(rekog_results):
    if len(rekog_results) > 1:
        results = [x for x in list(map(";".join, permutations(rekog_results)))]
    else:
        results = rekog_results

    total_results= []
    for result in results:
        qry_r = query_sql_data({"pill_name": "", "imprint": result, "color": "", "shape": ""})
        if qry_r == '':
            continue
        else:
            total_results.append(qry_r)
    return total_results

#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    im_print = parameter_list.get('imprint')
    pill_name = parameter_list.get('pill_name')
    sha_pe = parameter_list.get('shape')
    col_or = parameter_list.get('color')

    # if sha_pe==0 or sha_pe=='None':
    #     shape_text = None
    # else:
    #     for i in range(len(shape_codes)):
    #         if shape_codes[i].get("code") == sha_pe:
    #             dict_index = i
    #     shape_text = shape_codes[dict_index].get("name").upper()

    # if col_or == 0 or col_or == 'None':
    #     color_text = None
    # else:
    #     for i in range(len(color_codes)):
    #         if color_codes[i].get("code") == col_or:
    #             dict_index = i
    #     color_text = color_codes[dict_index].get("name").upper()

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
    

    ctr = 0
    if im_print is not None:
        if ctr>0:
            query = query + " AND "
        query = query +" UPPER(splimprint) LIKE '%%" + im_print.upper()+"%%'"
        ctr +=1
    if sha_pe == "" or sha_pe == "None" :
        pass
    else:        
        if ctr>0:
            query = query + " AND "
        query = query +" splshape_text LIKE " + "'"+sha_pe+"'" 
        ctr +=1
    if col_or == "" or col_or == "None":
        pass
    else:
        if ctr>0:
            query = query + " AND "
        query = query +" splcolor_text LIKE " + "'"+col_or+"'" 
        ctr +=1

    if pill_name == '' or pill_name == 'None':
        pass
    else:
        if ctr>0:
            query = query + " AND "
        query = query +" medicine_name LIKE '%%"+pill_name.upper()+"%%'"
        ctr +=1

    query = query + " LIMIT 25;"       
    """
        WHERE splimprint  LIKE ''       im_print
        AND splshape_text LIKE 'OVAL'   shape_text
        AND splcolor_text LIKE 'YELLOW'  color_text
        
        ----use double %% for wildcards!!!!!----
        AND medicine_name LIKE '%%PANTO%%'  pill_name
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

# ______  return colors, shapes list in reponse to GET request from /rxdata
def get_colors_shapes():
    out_put = { "valid_colors": ['GREEN', 'WHITE', 'BLUE;BLUE', 'ORANGE', 'YELLOW', 'PURPLE',
       'BROWN', 'RED', 'PINK', 'ORANGE;GREEN', 'BLUE', 'RED;WHITE;YELLOW',
       'GRAY;YELLOW', 'GRAY', 'PINK;WHITE', 'PINK;BROWN', 'GRAY;GRAY',
       'RED;BLUE;PURPLE', 'YELLOW;WHITE', 'WHITE;BLUE', 'PINK;GREEN',
       'WHITE;WHITE', 'PURPLE;YELLOW', 'GREEN;WHITE', 'BLACK',
       'BLUE;GRAY;BLUE', 'RED;WHITE', 'ORANGE;WHITE', 'BLUE;PINK',
       'WHITE;GREEN', 'WHITE;BROWN', 'YELLOW;BLUE', 'BLUE ', 'WHITE;PINK',
       'YELLOW;GREEN;RED;ORANGE', 'PINK;ORANGE;YELLOW', 'WHITE;ORANGE',
       'GREEN;ORANGE;PINK;YELLOW', 'GRAY;PINK', 'BLUE;GRAY',
       'GRAY;ORANGE', 'YELLOW;ORANGE;WHITE;RED', 'ORANGE;RED',
       'YELLOW;PINK', 'RED;GREEN;ORANGE;YELLOW', 'BLUE;GREEN',
       'BLUE;WHITE', 'GREEN;BLUE', 'WHITE;RED', 'ORANGE;ORANGE',
       'PINK;YELLOW', 'BROWN;BROWN', 'GREEN;YELLOW', 'RED;GREEN',
       'PURPLE;TURQUOISE', 'YELLOW;YELLOW', 'BROWN;WHITE', 'BLUE;ORANGE',
       'YELLOW;GRAY', 'ORANGE;RED;PURPLE', 'PURPLE;WHITE', 'ORANGE;GRAY',
       'ORANGE;PINK;YELLOW', 'TURQUOISE;WHITE', 'RED;BROWN',
       'WHITE;YELLOW', 'YELLOW;BROWN', 'BLUE;YELLOW', 'PINK;PINK',
       'PINK;BLACK', 'YELLOW;PINK;ORANGE', 'ORANGE;BLUE', 'TURQUOISE',
       'GREEN;GREEN', 'WHITE;PURPLE', 'GREEN;ORANGE', 'RED;RED',
       'YELLOW;BLACK', 'RED;ORANGE', 'BLUE;BROWN', 'GRAY;GREEN',
       'BLUE;BLACK', 'PURPLE;PINK', 'GREEN;BLUE;WHITE', 'PINK;BLUE',
       'BROWN;YELLOW', 'PINK;BLUE;PINK', 'YELLOW;PURPLE', 'YELLOW;RED',
       'GRAY;BROWN', 'GREEN;BROWN', 'PINK;BLUE;PURPLE', 'PURPLE;PURPLE',
       'PINK;WHITE;RED', 'BROWN;ORANGE', 'WHITE;TURQUOISE', 'BROWN;PINK',
       'WHITE;RED;ORANGE;YELLOW', 'BLUE;PURPLE', 'RED;BLUE;GRAY',
       'RED;GREEN;YELLOW;ORANGE', 'ORANGE;YELLOW', 'GRAY;WHITE',
       'PINK;RED', 'GRAY;RED', 'YELLOW;GREEN', 'YELLOW;ORANGE',
       'RED;PINK', 'RED;YELLOW;GREEN;ORANGE', 'BLACK;GREEN',
       'YELLOW;ORANGE;RED;PURPLE', 'GRAY;RED;PURPLE;ORANGE', 'WHITE ',
       'YELLOW;ORANGE;PINK;GREEN', 'ORANGE;YELLOW;GREEN;PINK',
       'GRAY;PURPLE', 'RED;BLUE', 'ORANGE;BROWN',
       'PINK;ORANGE;YELLOW;GREEN', 'WHITE;GRAY', 'GREEN;PINK',
       'RED;YELLOW', 'ORANGE;PINK;PURPLE', 'GRAY;BLUE',
       'YELLOW;PINK;GREEN', 'BLACK;YELLOW', 'ORANGE;PURPLE',
       'GREEN;PURPLE', 'PINK;PINK;PURPLE', 'PINK;ORANGE;YELLOW;WHITE',
       'BROWN;GRAY', 'BLUE;TURQUOISE', 'RED;GRAY', 'PURPLE;ORANGE',
       'WHITE;BLACK', 'GREEN;RED', 'BLACK;PURPLE', 'RED;PINK;PURPLE',
       'BROWN;GREEN', 'PURPLE;BLUE', 'BLUE;RED', 'BROWN;RED',
       'RED;PURPLE', 'BROWN;PURPLE', 'GREEN;TURQUOISE;WHITE',
       'PURPLE;GRAY', 'ORANGE;PINK', 'ORANGE;YELLOW;PINK', 'C48325',
       'GREEN;GRAY', 'PINK;YELLOW;ORANGE', 'GREEN;WHITE;YELLOW',
       'RED;GRAY;BLUE', 'BLACK;WHITE', 'PINK;ORANGE',
       'RED;ORANGE;YELLOW;GREEN', 'ORANGE ', 'YELLOW;GREEN;ORANGE;RED',
       'GRAY ;BROWN ', 'GRAY;BLACK', 'GRAY;RED;ORANGE', 'PINK;GRAY',
       'GREEN;BLACK', 'WHITE;GREEN;BLUE', 'BLUE;PURPLE;WHITE',
       'ORANGE ;ORANGE ', 'TURQUOISE;PINK', 'PINK;YELLOW;ORANGE;PINK',
       'PINK;RED;BLUE', 'TURQUOISE;TURQUOISE', 'BLACK;PINK',
       'RED;YELLOW;ORANGE;GREEN', 'YELLOW;ORANGE;PINK',
       'ORANGE;YELLOW;RED', 'BLUE;PINK;PURPLE', 'WHITE;RED;GREEN',
       'YELLOW ', 'BROWN ', 'YELLOW;RED;ORANGE;WHITE', 'BROWN;BLUE',
       'ORANGE;RED;YELLOW;PURPLE', 'YELLOW;ORANGE;RED;GREEN',
       'PINK;WHITE;BLUE', 'YELLOW;RED;ORANGE', 'RED;PURPLE;YELLOW;ORANGE',
       'TURQUOISE;BLUE', 'PINK;ORANGE;YELLOW;RED', 
       'YELLOW;PINK;ORANGE;WHITE', 'PURPLE;BLUE;GRAY', 'BROWN;TURQUOISE',
       'PURPLE;RED', 'PURPLE;GREEN', 'BLUE;GREEN;PINK',
       'RED;YELLOW;ORANGE', 'RED;PURPLE;GRAY',
       'BLUE;ORANGE;YELLOW;PURPLE', 'PINK;ORANGE;PURPLE', 
       'PINK;TURQUOISE', 'WHITE;ORANGE;YELLOW;RED', 'RED;ORANGE;WHITE;YELLOW',
       'GRAY;RED;PURPLE', 'RED '],
       "valid_shapes": ['ROUND', 'OVAL', 'CAPSULE', 'DIAMOND', 'TRIANGLE',
       'PENTAGON (5 SIDED)', 'HEXAGON (6 SIDED)', 'RECTANGLE', 'BULLET',
       'FREEFORM', 'SQUARE', 'OCTAGON (8 SIDED)', 'TRAPEZOID',
       'DOUBLE CIRCLE', 'TEAR', 'SEMI-CIRCLE', 'CLOVER'] } 
    return out_put

# __________ M A I N ________________________
if __name__ == '__main__':
    print(query_from_rekog(['126']))