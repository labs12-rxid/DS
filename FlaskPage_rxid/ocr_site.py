from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import requests
import os
import uuid
import boto3


app = Flask(__name__)

posts = [
    {
        'title': "Let's find your pill",
    }
]

# app.config["IMAGE_UPLOADS"] = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]

# Function to check if image file is among the ones we allow
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

# Function to add uploaded/saved image files to S3 bucket
s3_resource = boto3.resource('s3')
# bucket name
img_bucket_name = 'firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad'

def add_to_s3(image_file, filepath):
    # Looping through files to upload into S3 bucket
    s3_resource.Object(img_bucket_name, 
                        image_file).upload_file(
                        Filename=filepath)





@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # Objects needed to upload to S3 and get results from database
    url = 'http://rxid-ds.us-east-2.elasticbeanstalk.com/rekog'
    s3_path = "https://s3.us-east-2.amazonaws.com/firstpythonbucketac60bb97-95e1-43e5-98e6-0ca294ec9aad/"
    data = {"image_locations": ["", ""]}
    response = requests.post(url, data)

    if request.method == "POST":
        if request.files:
            target = os.path.join(APP_ROOT, 'images/')
            print(target)
            # making "image" directory if does not exist
            if not os.path.isdir(target):
                os.mkdir(target)
                print("Made new 'image' directory")

            image_list = request.files.getlist("image")
            # making sure we only get upto 2 images
            if len(image_list) > 2: 
                # cutting number images to just 2
                image_list = image_list[:2] 

            i=0 # index to replace "" in data dict for S3 url
            for image in image_list:
                print(f'Image list: {len(image_list)}')
                print(f"image: {image}")
                filename = image.filename
                # if file does not have a name
                if filename == "":
                    print("Image file must have a filename")
                    return redirect(request.url)
                # if it's not an image file with expected extension
                if not allowed_image(filename):
                    print("Your image has a file extension that is not allowed")
                    return redirect(request.url)
                else:
                    # file extension
                    ext = filename.rsplit(".", 1)[1] 
                    # new unique file name
                    new_filename = str(uuid.uuid4()) + "." + str(ext) 
                    destination = "/".join([target, new_filename])
                    image.save(destination)
                    print(f"Destination: {destination}")
                    # function to add "destination" file to S3 bucket
                    print("---->>> Should have added to S3")
                    add_to_s3(new_filename, destination) 
                    data["image_locations"][i] = s3_path + new_filename
                    print(data)
    data = str(data)
    print(data)
    return render_template("results.html", response=response)


@app.route("/about")
def about():
    return render_template("about.html", title="About")



if __name__ == "__main__":
    app.run(debug=True)