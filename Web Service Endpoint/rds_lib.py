import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import pandas as pd

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
    rekog_1 = rekog_results[0] + ";" + rekog_results[1]
    rekog_2 = rekog_results[1] + ";" + rekog_results[0]
    qry_r1 = query_sql_data({"pill_name": "", "imprint": rekog_1, "color": 0, "shape": 0})
    qry_r2 = query_sql_data({"pill_name": "", "imprint": rekog_2, "color": 0, "shape": 0})
    if qry_r1 == '[]':
        qry_r = qry_r2
    else:
        qry_r = qry_r1
        if qry_r2 == '[]':
            pass
        else:
            qry_r = (qry_r1 + qry_r2)
    return qry_r

#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    im_print = parameter_list.get('imprint')
    pill_name = parameter_list.get('pill_name')

    sha_pe = parameter_list.get('shape')
    if sha_pe==0 or sha_pe=='None':
        shape_text = None
    else:
        for i in range(len(shape_codes)):
            if shape_codes[i].get("code") == sha_pe:
                dict_index = i
        shape_text = shape_codes[dict_index].get("name").upper()

    col_or = parameter_list.get('color')
    if col_or == 0 or col_or == 'None':
        color_text = None
    else:
        for i in range(len(color_codes)):
            if color_codes[i].get("code") == col_or:
                dict_index = i
        color_text = color_codes[dict_index].get("name").upper()

    db_engine = db_connect('aws.rxidds.pwd')
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 

    query = """SELECT
                    author,
                    splimprint,
                    image_id,
                    spl_strength,
                    splsize,
                    splcolor_text,
                    splshape_text,
                    product_code,
                    DEA_SCHEDULE_CODE,
                    splscore,
                    setid
                    FROM """ + table_string + """ 
                WHERE """
    

    ctr = 0
    if im_print is not None:
        if ctr>0:
            query = query + " AND "
        query = query +" UPPER(splimprint) LIKE '%%" + im_print.upper()+"%%'"
        ctr +=1
    if shape_text is not None or sha_pe > 0:
        if ctr>0:
            query = query + " AND "
        query = query +" splshape_text LIKE " + "'"+shape_text+"'" 
        ctr +=1
    if color_text is not None or col_or > 0 :
        if ctr>0:
            query = query + " AND "
        query = query +" splcolor_text LIKE " + "'"+color_text+"'" 
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
    #print(query)
    results = db_engine.execute(query).fetchall()
    df = pd.DataFrame(results, columns=['author', 'imprint', 'image_id', 'medicine_name', 'size', 'color_text', 'shape_text', 'product_code', 'DEA_schedule', 'score', 'setid' ])
    
    
    
    
    
    
    df.loc[df['image_id'] != None, 'image_id'] += '.jpg'
    results_json = df.to_json(orient='records')
    return results_json


#  ____________  CONNECT TO DATABASE ___________________
def db_connect(pwd_file): 
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = ''
    user = ''
    host = ''
    passw = ''
    file = open(pwd_file, 'r')
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
    print(query_sql_data({"pill_name": ""  ,"imprint": "H;126", "color": 13 , "shape": 20}))



