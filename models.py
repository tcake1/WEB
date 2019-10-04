# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee


db = SQLAlchemy()
whooshee = Whooshee()


@whooshee.register_model('controlled_collection')
class Minwon(db.Model):
    __tablename__ = 'minwon_table'
    index = db.Column('index',db.Integer, nullable=False, primary_key=True)
    site_no = title = db.Column('site_no',db.Integer)
    site_index = db.Column('site_index', db.Integer)
    title = db.Column('title', db.Text)
    date = db.Column('date',db.Date)
    view = db.Column('view', db.Integer)
    question = db.Column('question',db.Text)
    part = db.Column('part',db.Text)
    ans_date = db.Column('ans_date',db.Date)
    ans = db.Column('ans', db.Text)
    collection = db.Column('collection',db.Text)
    controlled_collection = db.Column('controlled_collection',db.Text)
    topic = db.Column('topic',db.Integer)

    def __str__(self):
        return self.controlled_collection