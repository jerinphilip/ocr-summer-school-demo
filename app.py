from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from hashlib import sha224
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///save.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()

def fresh_name(name, ext):
    return sha224(name)[:20] + '.ext'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(10), db.ForeignKey('language.code'))
    fname = db.Column(db.Text)

class Output(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Integer, db.ForeignKey('image.id'))
    output = db.Column(db.Text)

class Language(db.Model):
    name = db.Column(db.String(80))
    code = db.Column(db.String(10), primary_key=True)

@app.route('/queue', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        if 'input_image' not in request.files:
            flash("No file upload found!")
            return redirect(request.url)

        image = request.files['input_image']
        if not image.filename:
            flash("No file upload found!")
            return redirect(request.url)
        if image:
            fname = secure_filename(image.filename)
            floc = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            image.save(floc)
            return "Success"

app.run(host='0.0.0.0', port=8080)
