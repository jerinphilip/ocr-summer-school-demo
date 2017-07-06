from flask import Flask, request, redirect, url_for, render_template
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from hashlib import sha224
import os
from OCR import OCR

#sys.path.insert(0, '.')

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
            filename, as_attachment=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), db.ForeignKey('language.name'))
    fname = db.Column(db.Text)
    processed = db.Column(db.Boolean, default=False)

class Output(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Integer, db.ForeignKey('image.id'))
    output = db.Column(db.Text)

    def __repr__(self):
        return "{image: %s, output: %s}"%(self.image, self.output)

class Language(db.Model):
    name = db.Column(db.String(80), primary_key=True)

@app.route('/enqueue', methods=['GET', 'POST'])
def image_upload():
    if request.method == 'GET':
        langs = Language.query.all()
        return render_template('upload.html', langs=langs)
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
            db.session.commit()
            text = OCR(floc, lang)  
            output_object = Output(image=image_object.id, output=text)
            db.session.add(output_object)
            db.session.commit()
            return render_template('output.html', output=output_object, image=image_object)

@app.route('/result/<output_id>', methods=['GET'])
def result(output_id):
    output = Output.query.get(output_id)
    image = Image.query.get(output.image)
    return render_template('output.html', output=output, image=image)

@app.route('/view', methods=['GET'])
def view_queue():
    images = Image.query.all()
    return render_template('gallery.html', images=images)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
