from flask import Flask, render_template, Blueprint, request, redirect, url_for, jsonify
from flask_login import  login_required, current_user
import pandas as pd
import os
from ..models import Question, Practice_scores, Exam_scores
from ..import db

views = Blueprint("views",__name__)

@views.route('/practice')
@login_required
def practice():
    return render_template("practice.html",user = current_user)

@views.route('/exam')
@login_required
def exam():
    return render_template("exam.html",user = current_user)

@views.route('/')
# @login_required
def index():
    return render_template("index.html", user = current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user = current_user)

@views.route('/update_profile_page')
@login_required
def update_profile_page():
    return render_template("update_profile.html", user=current_user)

@views.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    new_first_name = request.form.get('first_name')
    current_user.first_name = new_first_name
    db.session.commit()
    return redirect(url_for('views.profile'))

import json

from flask import flash


@views.route('/take-practice', methods=["POST", "GET"])
@login_required
def takePractice():
    
    # Taking test
    if request.method == "GET":
        # get the correct practice name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)

        return render_template("takePractice.html", user=current_user, questions=questions, name=practiceName, points=-1)
    # Process test submission
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Insert new score to history
        insert_score(count, practiceName)

        return render_template("takePractice.html", user=current_user, questions=questions, name=practiceName, points=count) 




@views.route('/take-exam', methods=["POST", "GET"])
@login_required
def takeExam():
    
    # Taking exam
    if request.method == "GET":
        # get the correct exam name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)
        return render_template("takeExam.html", user=current_user, questions=questions, name=practiceName, points=-1)
   
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_resource(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Insert new score to history
        insert_score(count, 'exam-score', 'exam')

        return render_template("takeExam.html", user=current_user, questions=questions, name=practiceName, points=count) 


@views.route('/score-history')
@login_required
def score_history():

    practice_scores = current_user.practice_scores
    exam_scores = current_user.exam_scores
     
    return render_template("scoreHistory.html", user=current_user, practice_scores=practice_scores, exam_scores=exam_scores)

# This function will insert either practice or exam score
# name: practice name OR exam name
def insert_score(score, name, type='practice'):
    if type == "practice":
        new_score = Practice_scores(
            user_id=current_user.id,
            practice_name=name,
            score=score
        )
    elif type == "exam":
        new_score = Exam_scores(
            user_id=current_user.id,
            exam_name=name,
            score=score
        )
    
    print("Score object created")

    db.session.add(new_score)
    db.session.commit()
    print("Score object inserted")


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
        question = Question(df.iloc[i]['id'], df.iloc[i]['type'], df.iloc[i]['question'], df.iloc[i]['a'], df.iloc[i]['b'], df.iloc[i]['c'], df.iloc[i]['d'], df.iloc[i]['answer'])
        if pd.notna(df.iloc[i]['chose']):
            question.chose = df.iloc[i]['chose']
        questions.append(question)

    return questions 


