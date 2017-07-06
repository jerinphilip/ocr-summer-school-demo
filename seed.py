from flask_sqlalchemy import SQLAlchemy
import flask
import os
from app import db, app
from app import Language

def seed_lang():
    with open("seed_data/lang.txt") as fp:
        langs = fp.read().splitlines()
        for pair in langs:
            code, lang = pair.split(',')
            lang_object = Language(name=lang)
            db.session.add(lang_object)

if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "save.db")
    os.remove(db_path)
    db.create_all()
    seed_lang()
    db.session.commit()
