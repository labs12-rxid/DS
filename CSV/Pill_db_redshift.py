import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("DS_DB_NAME")
USER = os.getenv("DS_DB_USER")
PASSWORD = os.getenv("DS_DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = "5439"
SCHEMA = "public" #default is "public"

# ________ Connection to Redshift and Starting Session ___
connection_string = "redshift+psycopg2://%s:%s@%s:%s/%s" % (USER,PASSWORD,HOST,str(PORT),DATABASE)
engine = sa.create_engine(connection_string)
session = sessionmaker()
session.configure(bind=engine)
s = session()

# ________ Creating Table _______________
query1 = '''
CREATE TABLE rxidDS (
id integer,
enabled varchar,
ssp varchar, 
setid varchar,
splsize integer,
pillbox_size integer,
splshape varchar,
splshape_text varchar,
pillbox_shape_text varchar,
splscore integer,
pillbox_score integer,
splimprint varchar,
pillbox_imprint varchar,
splcolor varchar,
splcolor_text varchar,
pillbox_color_text varchar,
spl_strength varchar,
spl_ingredients varchar,
spl_inactive_ing varchar,
source varchar,
rxtty varchar,
rxcui varchar, 
product_code varchar,
part_num varchar,
part_medicine_name varchar,
ndc_labeler_code varchar,
ndc_product_code varchar,
medicine_name varchar,
marketing_act_code varchar,
effective_time varchar,
file_name varchar,
equal_product_code varchar,
dosage_form varchar,
document_type varchar,
dea_schedule_code varchar,
dea_schedule_name varchar,
author_type varchar,
approval_code varchar,
image_source varchar,
splimage varchar,
epc_match varchar,
version_number varchar,
laberer_code varchar,
application_number varchar,
spl_id varchar,
ndc9 integer,
product_code varchar,
equal_product_code varchar,
author varchar,
dea_schedule_code varchar,
rxstring varchar,
image_id varchar,
has_image integer,
from_sis integer,
no_rxcui varchar
);
'''
s.execute(query1)

# Test query for table in same redshift cluster
query2 = '''
SELECT * from flights2003
LIMIT 2
'''
s.execute(query2)
s.commit()

df = pd.read_sql_query(query2, connection_string)
print(df)

# Ending session
s.close()