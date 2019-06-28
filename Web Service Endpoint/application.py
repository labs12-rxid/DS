"""
Main application and routing logic
"""
# _____ imports _____________
from flask import Flask, request, render_template, jsonify, url_for
from joblib import load
from flask_cors import CORS
import pandas as pd
import json
import atexit

# ______ Module imports _____
from rxid_util import parse_input
from rds_lib import db_connect, query_sql_data, query_from_rekog
from rekog import post_rekog, post_rekog_with_filter
from nnet import shape_detect


""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)


# ______________ R O U T E S  _____________________
# ________ / HOME __________
@application.route('/')
def index():
    return render_template('base.html', title='Home')


# ________  /rxdata/  route __________
# __ {'imprint' : 'M370',  'color' : 1,  'shape' : 6}
@application.route('/rxdata', methods=['GET', 'POST'])
def rxdata():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
        return jsonify(output_info)

    else:
        return jsonify("GET request to /rxdata :")


# ________  /rekog/  route __________
@application.route('/rekog', methods=['GET', 'POST'])
def rekog():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        print('rekog started - params:', post_params)
        rekog_info = post_rekog(post_params)
        shape_info = shape_detect(post_params)
        print('rekog complete - found:', rekog_info)
        output_info = query_from_rekog(rekog_info)
        return jsonify(output_info)
    else:
        return jsonify("YOU just made a GET request to /rekog")


# ________  /nnet/  route __________
@application.route('/nnet', methods=['GET', 'POST'])
def nnet():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        print('rekog started - params:', post_params)
        rekog_info = post_rekog_with_filter(post_params)
        print('rekog complete - found:', rekog_info)
        output_info = query_from_rekog(rekog_info)
        return jsonify(output_info)
    else:
        return jsonify("YOU just made a GET request to /nnet")


# __________ M A I N ________________________
if __name__ == '__main__':
    application.run(debug=False)

    # --- browser debugging
    # application.run(debug=True)

    #  --- for terminal debugging ------
    # __________________________________________________
    # to launch from terminal :
    #    change line 25 to  application.run(debug=True)
    #    cd to folder (where application.py resides)
    #    run >python application.py
