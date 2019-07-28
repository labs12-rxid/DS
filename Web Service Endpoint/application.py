"""
Main application and routing logic
"""
# _____ imports _____________
from flask import Flask, request, render_template, jsonify, url_for
from joblib import load
from flask_cors import CORS
import pandas as pd
import json

# ______ Module imports _____
from rxid_util import parse_input
from rds_lib import db_connect, query_sql_data, query_from_rekog
from rekog import post_rekog, post_rekog_with_filter
from nnet import shape_detect
from ocr_site import allowed_image, add_to_s3, file_upload


""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)

# ___________ Pill Display Layout ___________
# posts = [
#     {
#         'author': 'Carlos Gutierrez',
#         'title': '1st Post',
#         'content': 'This is the first post in here.',
#         'date_posted': 'June 14, 2019'
#     },
#     {
#         'author': 'Carlos Gutierrez',
#         'title': '2nd Post',
#         'content': 'This is the second post in here.',
#         'date_posted': 'June 17, 2019'
#     }
# ]



# ______________ R O U T E S  _____________________
# _________ / HOME  _________________
@application.route("/")
def index():
    return render_template("upload.html")


# __________ /upload  __________________
@application.route("/upload", methods=["GET", "POST"])
def upload():
    # Check if request is POST and the request has files (not empty)
    if request.method == "POST" and request.files:
        # file_upload returns dict with list of S3 images
        data = file_upload()

        print('rekog started - params:', data)
        rekog_info = post_rekog(data)
        # shape_info = shape_detect(data)
        print('rekog complete - found:', rekog_info)
        output_json = query_from_rekog(rekog_info)
        if output_json == []:
            output_dict = []
        else:
            # Replacing nulls for Nones to avoid errors with 'eval' method
            output_json = output_json[0].replace('null', 'None')
            # 'eval' built-in method will return the pass in expression as Python
            output_dict = list(eval(output_json))
    else:
        return 'You did not select an image file from your device for us to process.\n Please go back choose an image.'
    return render_template("results.html", results=output_dict)


# ___________  /about  __________________
@application.route("/about")
def about():
    return render_template("about.html", title="About")


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
    application.run(debug=True)

    # --- browser debugging
    # application.run(debug=True)

    #  --- for terminal debugging ------
    # __________________________________________________
    # to launch from terminal :
    #    change line 25 to  application.run(debug=True)
    #    cd to folder (where application.py resides)
    #    run >python application.py
