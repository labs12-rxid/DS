import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd
from itertools import permutations
import json
from dotenv import load_dotenv
import os

load_dotenv()

shape_codes = [
        { "id": 0, "name": 'Round', 'code': 24 },
        { "id": 1, "name": 'Capsule', 'code': 5 },
        { "id": 2, "name": 'Oval',"code": 20 },
        { "id": 3, "name": 'Egg',"code":  9 },
        { "id": 4, "name": 'Barrel',"code": 1 },
        { "id": 5, "name": 'Rectangle',"code": 23 },
        { "id": 6, "name": '3 Sided',"code": 32 },
        { "id": 7, "name": '4 Sided',"code": 14 },
        { "id": 8, "name": '5 Sided',"code": 13 },
        { "id": 9, "name": '6 Sided',"code": 27 },
        { "id": 10, "name": '7 sided',"code": 25 },
        { "id": 11, "name": '8 sided',"code": 10 },
        { "id": 12, "name": 'U Shaped',"code": 33 },
        { "id": 13, "name": 'Figure 8',"code": 12 },
        { "id": 14, "name": 'Heart',"code": 16 },
        { "id": 15, "name": 'Kidney',"code": 18 },
        { "id": 16, "name": 'Gear',"code": 15 },
        { "id": 17, "name": 'Character',"code": 6 },
        { "id": 18, "name": 'Diamand',"code": 7 },
        { "id": 19, "name": 'Square',"code": 28 },
]

color_codes = [{'id': 0, 'name': 'Beige', 'code': 14}, {'id': 1, 'name': 'Black', 'code': 73},
        {'id': 2, 'name': 'Blue', 'code': 1}, {'id': 3, 'name': 'Brown', 'code': 2},
        {'id': 4, 'name': 'Clear', 'code': 3}, {'id': 5, 'name': 'Gold', 'code': 4},
        {'id': 6, 'name': 'Gray', 'code': 5}, {'id': 7, 'name': 'Green', 'code': 6},
        {'id': 8, 'name': 'Maroon', 'code': 44}, {'id': 9, 'name': 'Orange', 'code': 7},
        {'id': 10, 'name': 'Peach', 'code': 74}, {'id': 11, 'name': 'Pink', 'code': 8},
        {'id': 12, 'name': 'Purple', 'code': 9}, {'id': 13, 'name': 'Red', 'code': 10},
        {'id': 14, 'name': 'Tan', 'code': 11}, {'id': 15, 'name': 'White', 'code': 12},
        {'id': 16, 'name': 'Yellow', 'code': 13}, {'id': 17, 'name': 'Beige & Red', 'code': 69},
        {'id': 18, 'name': 'Black & Green', 'code': 55}, {'id': 19, 'name': 'Black & Teal', 'code': 70},
        {'id': 20, 'name': 'Black & Yellow', 'code': 48}, {'id': 21, 'name': 'Blue & Brown', 'code': 52},
        {'id': 22, 'name': 'Blue & Grey'}, {'id': 23, 'name': 'Blue & Orange', 'code': 71},
        {'id': 24, 'name': 'Blue & Peach', 'code': 53}, {'id': 25, 'name': 'Blue & Pink', 'code': 34},
        {'id': 26, 'name': 'Blue & White', 'code': 19}, {'id': 27, 'name': 'Blue & White Specks', 'code': 26},
        {'id': 28, 'name': 'Blue & Yellow', 'code': 21}, {'id': 29, 'name': 'Brown & Clear', 'code': 47},
        {'id': 30, 'name': 'Brown & Orange', 'code': 54}, {'id': 31, 'name': 'Brown & Peach', 'code': 28},
        {'id': 32, 'name': 'Brown & Red', 'code': 16}, {'id': 33, 'name': 'Brown & White', 'code': 57},
        {'id': 34, 'name': 'Brown & Yellow', 'code': 27}, {'id': 35, 'name': 'Clear & Green', 'code': 49},
        {'id': 36, 'name': 'Dark & Light Green', 'code': 46}, {'id': 37, 'name': 'Gold & White', 'code': 51},
        {'id': 38, 'name': 'Grey & Peach'}, {'id': 39, 'name': 'Grey & Pink'}, {'id': 40, 'name': 'Grey & Red'},
        {'id': 41, 'name': 'Grey & White'}, {'id': 42, 'name': 'Grey & Yellow'},
        {'id': 43, 'name': 'Green & Orange', 'code': 65}, {'id': 44, 'name': 'Green & Peach', 'code': 63},
        {'id': 45, 'name': 'Green & Pink', 'code': 56}, {'id': 46, 'name': 'Green & Purple', 'code': 43},
        {'id': 47, 'name': 'Green & Turquoise', 'code': 62}, {'id': 48, 'name': 'Green & White', 'code': 30},
        {'id': 49, 'name': 'Green & Yellow', 'code': 22}, {'id': 50, 'name': 'Lavender & White', 'code': 42},
        {'id': 51, 'name': 'Maroon & Pink', 'code': 40}, {'id': 52, 'name': 'Orange & Turquoise', 'code': 50},
        {'id': 53, 'name': 'Orange & White', 'code': 64}, {'id': 54, 'name': 'Orange & Yellow', 'code': 23},
        {'id': 55, 'name': 'Peach & Purple', 'code': 60}, {'id': 56, 'name': 'Peach & Red', 'code': 66},
        {'id': 57, 'name': 'Peach & White', 'code': 18}, {'id': 58, 'name': 'Pink & Purple', 'code': 15},
        {'id': 59, 'name': 'Pink & Red Specks', 'code': 37}, {'id': 60, 'name': 'Pink & Turquoise', 'code': 29},
        {'id': 61, 'name': 'Pink & White', 'code': 25}, {'id': 62, 'name': 'Pink & Yellow', 'code': 72},
        {'id': 63, 'name': 'Red & Turquoise', 'code': 17}, {'id': 64, 'name': 'Red & White', 'code': 35},
        {'id': 65, 'name': 'Red & Yellow', 'code': 20}, {'id': 66, 'name': 'Tan & White', 'code': 33},
        {'id': 67, 'name': 'Turquoise & White', 'code': 59}, {'id': 68, 'name': 'Turquuise & Yellow'},
        {'id': 69, 'name': 'White & Blue Specks', 'code': 32}, {'id': 70, 'name': 'White & Red Specks', 'code': 41},
        {'id': 71, 'name': 'White & Yellow', 'code': 38}, {'id': 72, 'name': 'Yellow & Grey'},
        {'id': 73, 'name': 'Yellow & White', 'code': 36}]

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
       'TURQUOISE;BLUE', 'PINK;ORANGE;YELLOW;RED', 'C48329',
       'YELLOW;PINK;ORANGE;WHITE', 'PURPLE;BLUE;GRAY', 'BROWN;TURQUOISE',
       'PURPLE;RED', 'PURPLE;GREEN', 'BLUE;GREEN;PINK',
       'RED;YELLOW;ORANGE', 'RED;PURPLE;GRAY',
       'BLUE;ORANGE;YELLOW;PURPLE', 'PINK;ORANGE;PURPLE', 
       'PINK;TURQUOISE', 'C48328', 'WHITE;ORANGE;YELLOW;RED',
       'RED;ORANGE;WHITE;YELLOW', 'C48327', 'GRAY;RED;PURPLE', 'RED '],
       "valid_shapes": ['ROUND', 'OVAL', 'CAPSULE', 'DIAMOND', 'TRIANGLE',
       'PENTAGON (5 SIDED)', 'HEXAGON (6 SIDED)', 'RECTANGLE', 'BULLET',
       'FREEFORM', 'SQUARE', 'OCTAGON (8 SIDED)', 'TRAPEZOID',
       'DOUBLE CIRCLE', 'TEAR', 'SEMI-CIRCLE', 'CLOVER'] } 
    return out_put

# __________ M A I N ________________________
if __name__ == '__main__':
    print(query_from_rekog(['126']))