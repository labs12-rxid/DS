"""
Main application and routing logic
"""
# _____ imports _____________
from flask import Flask, request, render_template, jsonify
from joblib import load
from flask_cors import CORS
import pandas as pd
import json
import atexit

# ______ Module imports _____
from drugscom import drugscom
from rxid_util import parse_input
from rds_lib import db_connect, query_sql_data, query_from_rekog
from rekog import post_rekog


""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)

drugs_com = drugscom()

def close_drugs_com():
    print('started closing')
    if drugs_com != None:
        print('closing drugs_com')
        drugs_com.close()

atexit.register(close_drugs_com)

# ______________ R O U T E S  _____________________
# ________ / HOME __________
@application.route('/')
def index():
    return render_template('base.html', title='Home')

# ________  /identify/  route __________
# __ input  {'imprint' : 'M370',  'color' : 1,  'shape' : 6}    
@application.route('/identify', methods=['GET', 'POST'])
def identify():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        results = get_drugscom(post_params)
        return results
    else:
        return jsonify("GET request to /identify :")


# ________  /rxdata/  route __________
# __ {'imprint' : 'M370',  'color' : 1,  'shape' : 6}    
@application.route('/rxdata', methods=['GET', 'POST'])
def rxdata():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
        return output_info

    else:
        return jsonify("GET request to /rxdata :")


# ________  /rekog/  route __________
@application.route('/rekog', methods=['GET', 'POST'])
def rekog():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        # https://s3.amazonaws.com/labs12-rxidstore/reference/00002-3228-30_391E1C80.jpg
        rekog_info = post_rekog(post_params)
        output_info = query_from_rekog(rekog_info)
        return output_info
    else:
        return jsonify("YOU just made a GET request to /rekog")

# ________  /nnet/  route __________
@application.route('/nnet', methods=['GET', 'POST'])
def nnet():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        return jsonify(post_params)
    else:
        return jsonify("YOU just made a GET request to /nnet")

# ___________________ FUNCTIONS ________________________________
def get_drugscom(query_string):
    out_put = ''
    try:
        out_put = drugs_com.get_data(query_string)
    except Exception as e:
        out_put = f'error: {e}'
    finally:
        if drugs_com is not None: 
            drugs_com.reset()
    return out_put


# __________ M A I N ________________________
if __name__ == '__main__':
    application.run(debug=False)


    # --- browser debugging
    # application.run(debug=True)

    #  --- for terminal debugging ------
    # results = get_drugscom()
    # print(results)
# __________________________________________________
# to launch from terminal : 
#    change line 25 to  application.run(debug=True)
#    cd to folder (where application.py resides)
#    run >python application.py 
