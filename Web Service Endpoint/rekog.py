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
from dotenv import load_dotenv
import os

load_dotenv()

key_id = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
reg_ion = os.getenv("AWS_DEFAULT_REGION")

client=boto3.client('rekognition', region_name=reg_ion,
                    aws_access_key_id=key_id,
                    aws_secret_access_key=secret_key)

# Text  Dectection Function

def post_rekog(pic_json):
    
    # Getting list of image file names
    imageURL_list = pic_json.get("image_locations")
    # print(f'imageURL_list {imageURL_list}')
    
    # Empty list to contain list(s) of text blob(s) extracted with "Rekognition"
    # Will contain a list per side (2 lists)
    all_text = []
    
    # Looping through each image
    ctr = 10000
    for imageURL in imageURL_list:
        if imageURL != "":
            # Saving image URL locally
            ctr += 1
            temp_img = str(ctr) + ".jpg"
            urllib.request.urlretrieve(imageURL, temp_img)
            imageFile = './' + temp_img
            
            # Opening locally saved 'imageFile'
            with open(imageFile, 'rb') as image:
                # !!!!!!  WRAP THIS IN A TRY / CATCH !!!!!!!!!
                response = client.detect_text(Image={'Bytes': image.read()})

            # Detected Text (List of Dictionaries)
            textDetections=response['TextDetections']

            # Parsing Through Detected Text and 
            # Making list of Unique Sets of Text Dectected
            text_found = []

            for text in textDetections:
                if text['Confidence'] > 87:
                    text_found.append(text['DetectedText'])
                    # print(text['Confidence'])
            # print(f'text_found: {text_found}')
            
            text_set = list(set(text_found))

            # Appending detected text in image to "all_text" list
            all_text.append(text_set)
        
        else:
            continue
            
    # Flattening 'all_text' (list of lists) into 1 list
    text_list = [blob for sublist in all_text for blob in sublist]
    text_list = list(set(text_list))
    # print(f'text_list: {text_list}')

    # Splitting any text blob that may have digits and numbers together
    unique_list = []
    for each in text_list:
        num_split = re.findall(r'[A-Za-z]+|\d+', each)
        unique_list.append(num_split)

    # Flattening again into one list with just unique values
    unique_list = [blob for sublist in unique_list for blob in sublist]
    unique_list = list(set(unique_list))
    # print(len(unique_list))

    #if len(unique_list) == 0:
    #    unique_list = ['Unable to detect text']


    # Return 'unique_list'    
    return (unique_list)


# __________ M A I N ________________________
if __name__ == '__main__':
    data = {"image_locations": ["https://raw.githubusercontent.com/ed-chin-git/ed-chin-git.github.io/master/sample_pill_image.jpg", ""]}
    print(post_rekog(data))
    


