'''
  Aggregate and label pill images for shape detection training
'''
import os
import cv2
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


def create_training_data(parameter_list):
    def db_connect():
        # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
        dbname = os.getenv("DS_DB_NAME")
        usr = os.getenv("DS_DB_USER")
        host = os.getenv("DS_DB_HOST")
        pw = os.getenv("DS_DB_PASSWORD")
        connect_str = 'postgresql+psycopg2://'+usr+':'+pw+'@'+host+'/'+dbname
        return create_engine(connect_str)

    def process_results():
        df = pd.DataFrame(results, columns=['author',
                                            'imprint',
                                            'image_id',
                                            'medicine_name',
                                            'color_text',
                                            'shape_text'])
        # drop rows with no image_id
        df.dropna(subset=['image_id'], inplace=True)

        # drop rows with blank image holder
        df = df[df.image_id != 'no_product_image']
        
        # Add suffix to image file name
        df.loc[df['image_id'] != None, 'image_id'] += '.jpg'

        # Label & Copy selected images to separate folder
        print(f'\n\nCreating folder with {len(df)} {sha_pe} pill shape images')
        bksl = '\.'
        bksl = bksl[:-1] 
        print(f'FROM: {source_dir}')
        print(f'  TO: {source_dir[:-1] + sha_pe + bksl}')
        for source_name in df['image_id']:
            source = source_dir[:-1] + source_name
            destination = source_dir[:-1]+sha_pe+bksl+abbrev+'.'+source_name
            print(f'\r{source_name:<60}', end='')
            cv2.imwrite(destination, cv2.imread(source))
        print(f'\r{sha_pe}: {len(df):<70}')
        return

    # ___ assign input parameters ___
    source_dir = parameter_list.get('source_dir')
    sha_pe = parameter_list.get('shape')
    abbrev = parameter_list.get('abbrev')
    if sha_pe == '':
        print('ERROR: No shape specified. Search canceled...')
        return
    # ___ connect & query the DB ___
    db_engine = db_connect()
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name
    query = """SELECT
                    author,
                    splimprint,
                    image_id,
                    spl_ingredients,
                    splcolor_text,
                    splshape_text
                    FROM """ + table_string + """
                WHERE """
    query = query + "splshape_text ILIKE " + "'"+sha_pe+"'"
    """ _______  Search Guide  _______________________
     WHERE splimprint  ILIKE ''       im_print
     AND splshape_text ILIKE 'OVAL'   shape_text
     AND splcolor_text ILIKE 'YELLOW'  color_text
     ----use double %% for wildcards!!!!!----
     AND medicine_name ILIKE '%%PANTO%%'  pill_name
    ________________________________________________"""

    # ___ Send query results to dataframe __
    results = db_engine.execute(query).fetchall()
    if len(results) > 0:
        process_results()
    else:
        print(f'NO IMAGES FOUND for {sha_pe}.')
    
    # __buh bye ___
    return

# __________ M A I N ________________________
if __name__ == '__main__':
    # pill_shapes = {"ROUND": "rnd",
    #                "OVAL": "ovl",
    #                "CAPSULE": "cap",
    #                "DIAMOND": "dia",
    #                "TRIANGLE": "tri",
    #                "PENTAGON (5 SIDED)": "pen",
    #                "HEXAGON (6 SIDED)": "hex",
    #                "RECTANGLE": "rec",
    #                "BULLET": "bul",
    #                "FREEFORM": "ffm",
    #                "SQUARE": "sqr",
    #                "OCTAGON (8 SIDED)": "oct",
    #                "TRAPEZOID": "tra",
    #                "DOUBLE CIRCLE": "dbc",
    #                "TEAR": "tea",
    #                "SEMI-CIRCLE": "sem",
    #                "CLOVER": "clo"}

    os.system('cls' if os.name == 'nt' else 'clear')
    print(" _____ Create Folders with labeled Pill Images by Pill Shape ___\n")
    source_dir = "d:\GITHUB\pillbox_production_images_full_201805\ "
    pill_shapes = {"BULLET": "bul"}
    for pill_shape, abbrev in pill_shapes.items():
        create_training_data({"source_dir": source_dir,
                              "shape": pill_shape,
                              "abbrev": abbrev
                              })
