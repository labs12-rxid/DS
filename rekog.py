'''
Python Script to dectect imprinted text on pill images using AWS Rekognition.
Set up for passing just 1 image. 
Will need to be refactored to pass 2 images based on URL or JSON given by WEB.

Source code:
https://github.com/labs12-rxid/DS/blob/master/text_detection_AWSRekognition.ipynb
'''

# from skimage.exposure import rescale_intensity
# from skimage import color
import urllib.request
import json
import re
import boto3
import numpy as np

client=boto3.client('rekognition', region_name='us-east-2',
                    aws_access_key_id = 'AKIASNTIZMKT62P6ONE4',
                    aws_secret_access_key = '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')

# Text  Dectection Function
def post_rekog(pic_url):

    # List of URLs from 'json_urls'
    url_list = json_urls.get("image_locations")
    
    # Empty list to contain list(s) of text text(s) extracted with "Rekognition"
    all_text = []

    # Looping through each image in "photo_sides" list
    for url in url_list:
    
        urllib.request.urlretrieve(url, "./00000001.jpg")

        imageFile='./00000001.jpg'

        # Trying to turn 'imageFile' to grayscale
    #     photo = imageio.imread(imageFile)
    #     bw_photo = rescale_intensity(color.rgb2gray(photo))
    #     bw_photo = bw_photo.astype(np.uint8)
    #     imageio.imwrite('./00000001_bw.jpg', bw_photo)
    #     saved_bwphoto = './00000001_bw.jpg'

        with open(imageFile, 'rb') as image:
            response = client.detect_text(Image={'Bytes': image.read()})

        # Detected Text (List of Dictionaries)
        textDetections=response['TextDetections']

        # Parsing through Detected Text and 
        # making list of Unique Sets of Text Dectected
        text_found = []

        for text in textDetections:
            if text['Confidence'] > 87:
                text_found.append(text['DetectedText'])

        text_set = list(set(text_found))
        # print(text_set)
        
        # Appending detected text in image to "all_text" list
        all_text.append(text_set)

    # Flattening 'all_text' (list of lists) into 1 list
    text_list = [txt for sublist in all_text for txt in sublist]
    text_list = list(set(text_list))
    # print(f'text_list: {text_list}')
    
    # Splitting any text blob that may have digits and numbers together
    unique_list = []
    for each in text_list:
        num_split = re.findall(r'[A-Za-z]+|\d+', each)
        unique_list.append(num_split)
        
    # Flattening again into one list with just unique values
    unique_list = [txt for sublist in unique_list for txt in sublist]
    unique_list = list(set(unique_list))
    # print(len(unique_list))
    
    if len(unique_list) == 0:
        unique_list = ['Unable to detect text']
    
    # Return 'unique_list' as JSON    
    return json.dumps(unique_list)