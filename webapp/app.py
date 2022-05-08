from email.mime import image
from fileinput import filename
import json
from flask import Flask, render_template, url_for, flash, jsonify,request
from forms import InputForm
import requests, secrets, ast, os
import shutil


app = Flask(__name__)
app.config['SECRET_KEY'] = '36d2fcd2731047780f1b3f9025e1b59f'

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rm_files(folder):
    for filename in os.listdir(folder):
        os.remove(os.path.join(folder, filename))


def save_image(image_data):
     random_hex = secrets.token_hex(8)
     _, f_ext = os.path.splitext(image_data.filename)
     picture_fn = random_hex + f_ext
     picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
     image_data.save(picture_path)
     return picture_fn

def restorer(image_file):
    restored_image=""
    return restored_image

@app.route('/')
def main():
    return render_template('home.html')


@app.route("/upload", methods=['POST', 'GET'])
def input_pic():
    form  = InputForm()
    
    rm_files('static/images')

    file=request.files['file']
    msg=""
    if file and allowed_file(file.filename):
        image_fn = save_image(file)
        image_file = url_for('static', filename = 'images/' + image_fn)
        print(image_file)
        return render_template("uploaded_image.html",image_file=image_file)

    else:
        msg="Error in uploaded file"
    
    return jsonify(msg)
        

        


        # if form.validate_on_submit():
        #     
        #     restored_image=restorer(image_file)

        #     #return render_template('restore.html',orignal_image=image_file,restored_image=restored_image)

        #     return render_template('restore.html',orignal_image=image_file,restored_image=image_file)
    


if __name__ == '__main__':
    app.run(debug=True)


