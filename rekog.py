'''
Python Script to detect imprinted text on pill images using AWS Rekognition.
Set up for passing just 1 image. 
Will need to be refactored to pass 2 images based on URL or JSON given by WEB.

Source code:
https://github.com/labs12-rxid/DS/blob/master/text_detection_AWSRekognition.ipynb
'''

import urllib.request
import json
import re
import boto3
import numpy as np

key_id = ''
secret_key = ''
reg_ion = ''
file = open('aws.rekog.pwd', 'r')
ctr = 1
for line in file:
    line = line.replace('\n', '')
    if ctr == 1: key_id = line
    if ctr == 2: secret_key = line
    if ctr == 3: reg_ion = line
    ctr = ctr + 1
client=boto3.client('rekognition', region_name=reg_ion,
                    aws_access_key_id=key_id,
                    aws_secret_access_key=secret_key)

# Text  Dectection Function
def post_rekog(pic_url):
    url = pic_url.get("image_file")
    urllib.request.urlretrieve(url, "./00000001.jpg")
    imageFile='./00000001.jpg'
    
    with open(imageFile, 'rb') as image:
        response = client.detect_text(Image={'Bytes': image.read()})
    
    # Detected Text (List of Dictionaries)
    textDetections=response['TextDetections']

    # Parsing Through Detected Text and 
    # Making list of Unique Sets of Text Dectected
    text_found = []

    for text in textDetections:
        if text['Confidence'] > 87:
            text_found.append(text['DetectedText'])

    text_set = list(set(text_found))
#     print(text_set)
    
    # Splitting any text blob that may have digits and numbers together
    unique_list = []
#     for each in text_list:
    for each in text_set:
        num_split = re.findall(r'[A-Za-z]+|\d+', each)
        unique_list.append(num_split)
        
    # Flattening again into one list with just unique values
    unique_list = [blob for sublist in unique_list for blob in sublist]
    unique_list = list(set(unique_list))
#     print(len(unique_list))
    
    if len(unique_list) == 0:
        unique_list = ['Unable to detect text']
    
    # Return 'unique_list' as JSON    
    return json.dumps(unique_list)