from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

posts = [
    {
        'title': "Let's find your pill",
    }
]

app.config["IMAGE_UPLOADS"] = os.path.dirname(os.path.abspath(__file__))
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "": # if file does not have a name
                print("Image file must have a filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("Your image has a file extension that is not allowed")
                return redirect(request.url)
            else:
                new_filename = secure_filename(image.filename)
                print(new_filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], new_filename))
            print("--> Image saved <--")
            return redirect(request.url)

    return render_template("home.html", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")



if __name__ == "__main__":
    app.run(debug=True)