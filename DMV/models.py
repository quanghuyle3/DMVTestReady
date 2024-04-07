from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin): #UserMixin is specific for USER
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    

# Model for question
class Question:
    def __init__(self, id, question, a, b, c, d, answer, chose=''):
        self.id = id
        self.question = question 
        self.a = a
        self.b = b 
        self.c = c 
        self.d = d 
        self.answer = answer 
        self.chose = chose