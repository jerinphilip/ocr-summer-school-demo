from flask import Flask, request, redirect, url_for, render_template
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from hashlib import sha224
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///save.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def fresh_name(name, ext):
    return sha224(name)[:20] + '.ext'

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], 
            filename, as_attachment=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('language.code'))
    fname = db.Column(db.Text)
    processed = db.Column(db.Boolean, default=False)

class Output(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Integer, db.ForeignKey('image.id'))
    output = db.Column(db.Text)

class Language(db.Model):
    name = db.Column(db.String(80))
    code = db.Column(db.String(10), primary_key=True)

@app.route('/enqueue', methods=['GET', 'POST'])
def image_upload():
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
            lang = request.form["lang"]

            image_object = Image(code=lang, fname=fname)
            db.session.add(image_object)
            text = OCR(floc, lang)
            output_object = Output(image=image_object, text=text)
            db.session.add(output_object)
            db.session.commit()
            return render_template('output.html', image=image_object, text=text)

@app.route('/result', methods=['GET'])
def result():
    render_template('output.html', output=output)

@app.route('/queue', methods=['GET'])
def view_queue():
    images = Image.query.all()
    return render_template('gallery.html', images=images)
    
