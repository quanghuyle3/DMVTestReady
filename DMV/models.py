from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

# Model for Users
class User(db.Model, UserMixin): #UserMixin is specific for USER
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

# Model for Practice Scores

class Practice_scores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='practice_scores')
    practice_name = db.Column(db.String(150))
    score = db.Column(db.Integer) 
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
# Model for Exam Scores
class Exam_scores(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='exam_scores')
    exam_name = db.Column(db.String(150))
    score = db.Column(db.Integer) 
    timestamp = db.Column(db.DateTime, default=datetime.now)
    

# Model for question
class Question:
    def __init__(self, id, type, question, a, b, c, d, answer, chose=''):
        self.id = id
        self.type = type
        self.question = question 
        self.a = a
        self.b = b 
        self.c = c 
        self.d = d 
        self.answer = answer 
        self.chose = chose