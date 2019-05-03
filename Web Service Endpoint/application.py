"""
Main application and routing logic
"""
from flask import Flask, request, render_template, jsonify
from joblib import load
from flask_cors import CORS
import datetime
import pandas as pd
import pytz
from pytz import timezone
import calendar
import psycopg2
from sqlalchemy import create_engine
import boto3
import os

""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)


# ______________ R O U T E S  _____________________
# ________  HOME __________
@application.route('/')
def index():
    return render_template('base.html', title='Home')

# ________  /indentify/  route __________
# __ input  image uri, S3 bucket
@application.route('/identify', methods=['GET', 'POST'])
def indentify():
    if request.method == 'POST':
        return " YOU just made a POST request to /identify"
    else:
        return " YOU just made a GET request to /identify"


# ________  /rxdata/  route __________
@application.route('/rxdata', methods=['GET', 'POST'])
def rxdata():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
        return jsonify(output_info)   # " YOU just made a POST request to /rxdata"
    else:
        return jsonify(" YOU just made a GET request to /rxdata")

# ________  /nnet/  route __________
@application.route('/nnet', methods=['GET', 'POST'])
def nnet():
    if request.method == 'POST':
        return jsonify(" YOU just made a POST request to /nnet")
    else:
        
        return jsonify(" YOU just made a GET request to /nnet")

# ________  /rekog/  route __________
@application.route('/rekog', methods=['GET', 'POST'])
def rekog():
    if request.method == 'POST':
        return jsonify(" YOU just made a POST request to /rekog")
    else:
        return jsonify(" YOU just made a GET request to /rekog")


# ___________________ FUNCTIONS ________________________________

#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    #  echo the output for now  -- needs query code 
    return parameter_list


# ____  download file from AWS S3 Bucket into local tmp dir_______
def download_from_S3(S3_bucketname, S3_filename, local_filename='S3file.jpg'):
    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_bucketname, S3_filename).download_file(f'./{local_filename}')
    return


# _______ GET CURRENT DAY AND HOUR __________
def day_hour():
    # get current time in pacific timezone
    utc = pytz.utc
    utc.zone
    pacific = timezone('US/Pacific')
    
    #  bin the current hour
    time = datetime.datetime.today().astimezone(pacific)    
    hour = (time.hour)
    if hour <= 4:
        hour = 1
    elif 4 > hour <= 8:
        hour = 2
    elif 8 > hour <= 12:
        hour = 3
    elif 12 > hour <= 16:
        hour = 4
    elif 16 > hour <= 20:
        hour = 5
    else:
        hour = 6

    # Day of the week
    weekday = time.isoweekday()
    d = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 
        5: 'FRIDAY', 6: 'SATURDAY', 7: 'SUNDAY'}
    for key, value in d.items():
        if key == weekday:
            weekday = value
    return weekday, hour


# _________ Parse API input string for parameters _________________
#  input->  sample API input string(s)-> /indentify/param1=Red&param2=Pill
#  ouputs -->  
def parse_input(s):

    weekday, hour = day_hour()

    # parse input string for model input values
    weather_str = ''
    weather_loc = s.find("weather=") # returns -1 if not found
    if weather_loc > 0:
        weather_str = s[s.find("weather=")+8:s.find("&",weather_loc)]

    day_str = ''
    day_loc = s.find("day=")
    if day_loc > 0:
        day_str = s[day_loc+4:s.find("&",day_loc)]

    month_num = 1
    month_loc = s.find("month=")
    if month_loc > 0:
        month_str = s[month_loc+7:s.find("&",month_loc)]
        month_str = s.find()
        month_num = 1
        month_dict = dict((v,k) for k,v in enumerate(calendar.month_name))
        for key, value in month_dict.items():
            if key == month_str:
                month_num = value


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


# ________  Verfiy Output From DataBase ______
def verify_output(pgres_engine):
    # ______  verify output-table contents ____
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    query = 'SELECT * FROM ' + table_string + ' LIMIT 10;'
    for row in pgres_engine.execute(query).fetchall():
        print(row)
    return


# __________ M A I N ________________________
if __name__ == '__main__':
    application.run(debug=False)

    # --- browser debugging
    # application.run(debug=True)

    #  --- for terminal debugging ------
    #input_str = 'RED PILL'
    #print(predict(input_str))

# to launch from terminal : 
#    change line 25 to  application.run(debug=True)
#    cd to folder (where application.py resides)
#    run >python application.py 
