from flask import Flask, render_template, Blueprint, request, redirect
from flask_login import  login_required, current_user
import pandas as pd
import os

views = Blueprint("views",__name__)

@views.route('/practice')
# @login_required
def practice():
    return render_template("practice.html",user = current_user)

@views.route('/')
# @login_required
def index():
    return render_template("index.html", user = current_user)

@views.route('/take-practice', methods=["POST", "GET"])
@login_required
def takePractice():
    
    # Taking test
    if request.method == "GET":
        # get the correct practice name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)
        
        return render_template("takePractice.html", user = current_user, questions=questions, name=practiceName, points=-1)
    # Process test submission
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form[str(i)] == questions[i].answer:
                count += 1
                
            questions[i].chose = request.form[str(i)]   # save the answer that user chose

        return render_template("takePractice.html", user = current_user, questions=questions, name=practiceName, points=count) 
    

# This function will return list of questions from corresponding resource
def load_corresponding_resource(name):
    # concat correct file path and file name
    filePath =  "./DMV/resources/" + name + ".csv"
    
    # read csv file using pandas, getting data in form of dataframe
    df = pd.read_csv(filePath)  
    # final list of questions
    questions = []
    
    # read each line, create corresponding object for each question
    for i in range(df.shape[0]):
        question = Question(df.iloc[i]['id'], df.iloc[i]['question'], df.iloc[i]['a'], df.iloc[i]['b'], df.iloc[i]['c'], df.iloc[i]['d'], df.iloc[i]['answer'])
        if pd.notna(df.iloc[i]['chose']):
            question.chose = df.iloc[i]['chose']
        questions.append(question)

    return questions 

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

