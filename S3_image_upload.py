#!/usr/bin/env python
# coding: utf-8

# # Image File Uploads to S3 Bucket

import boto3
import os

s3_resource = boto3.resource('s3')

# directory with pill images
path = './data/train/train/' 
# bucket name
# img_bucket_name = 'secondpythonbucket6ce9cccf-c429-471c-99a1-f36e849ee381'
img_bucket_name = 'firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad/train'

# previously uploaded image to be skipped
# img_inS3 = '3bdd37a9-ecb9-36f2-e054-00144ff88e88.jpg'


# counting files uploaded
# n_count = 0 
# # Looping through files to upload into S3 bucket
# for filename in os.listdir(path):
#     # Skipping file already uploaded previous test run
#     if filename != img_inS3:
#         s3_resource.Object(img_bucket_name, 
#                            filename).upload_file(
#                            Filename=f'./pillbox_images/{filename}')
#         n_count += 1

# print(f'Number of files uploaded: {n_count}')

# counting files uploaded
n_count = 0 
# Looping through files to upload into S3 bucket
for filename in os.listdir(path):
        s3_resource.Object(img_bucket_name, 
                filename).upload_file(
                Filename=path + filename)
        n_count += 1
print(f'Number of files uploaded: {n_count}')