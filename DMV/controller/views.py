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
        questions = load_corresponding_practice(practiceName)
        # Convert questions to a JSON format for HTML
        questions_json = []
        for q in questions:
            question_dict = {
                "id": int(q.id),
                "question": q.question,
                "a": q.a,
                "b": q.b,
                "c": q.c,
                "d": q.d,
                "answer": q.answer,
                "chose": q.chose
            }
            questions_json.append(question_dict)
        
        return render_template("takePractice.html", user=current_user, questions=questions_json, name=practiceName, points=-1)
    # Process test submission
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_practice(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            elif request.form.get(str(i)) is None:
                flash("You must choose an answer for question {}".format(i+1), "error")
                
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Convert questions to a JSON format for HTML
        questions_json = []
        for q in questions:
            question_dict = {
                "id": int(q.id),
                "question": q.question,
                "a": q.a,
                "b": q.b,
                "c": q.c,
                "d": q.d,
                "answer": q.answer,
                "chose": q.chose
            }
            questions_json.append(question_dict)

        return render_template("takePractice.html", user=current_user, questions=questions_json, name=practiceName, points=count) 




@views.route('/take-exam', methods=["POST", "GET"])
@login_required
def takeExam():
    
    # Taking exam
    if request.method == "GET":
        # get the correct exam name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = load_corresponding_practice(practiceName)
        # Convert questions to a JSON format for HTML
        questions_json = []
        for q in questions:
            question_dict = {
                "id": int(q.id),
                "question": q.question,
                "a": q.a,
                "b": q.b,
                "c": q.c,
                "d": q.d,
                "answer": q.answer,
                "chose": q.chose
            }
            questions_json.append(question_dict)
        
        return render_template("takeExam.html", user=current_user, questions=questions_json, name=practiceName, points=-1)
   
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_practice(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            elif request.form.get(str(i)) is None:
                flash("You must choose an answer for question {}".format(i+1), "error")
                
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Convert questions to a JSON format for HTML
        questions_json = []
        for q in questions:
            question_dict = {
                "id": int(q.id),
                "question": q.question,
                "a": q.a,
                "b": q.b,
                "c": q.c,
                "d": q.d,
                "answer": q.answer,
                "chose": q.chose
            }
            questions_json.append(question_dict)

        return render_template("takeExam.html", user=current_user, questions=questions_json, name=practiceName, points=count) 

@views.route('/take-practice-all-questions', methods=["POST", "GET"])
@login_required
def takePracticeAllQuestions():
    
    # Taking test
    if request.method == "GET":
        # get the correct practice name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = load_corresponding_practice(practiceName)

        return render_template("takePracticeAllQuestions.html", user=current_user, questions=questions, name=practiceName, points=-1)
    # Process test submission
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        questions = load_corresponding_practice(practiceName)

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Insert new score to history
        insert_score(count, practiceName)

        return render_template("takePracticeAllQuestions.html", user=current_user, questions=questions, name=practiceName, points=count) 

@views.route('/take-exam-on-site', methods=["POST", "GET"])
@login_required
def takeExamOnSite():
    
    # Taking exam
    if request.method == "GET":
        # get the correct exam name 
        # practiceName = request.args.get("name")
        # load questions from files and converts to objects
        # questions = load_corresponding_practice(practiceName)
        questions = load_random_exam_questions()
        # return render_template("takeExamOnSite.html", user=current_user, questions=questions, name=practiceName, points=-1)
        return render_template("takeExamOnSite.html", user=current_user, questions=questions, name="Exam", points=-1)
   
    else:
        # get the correct practice name 
        practiceName = request.form["name"]
        # load questions from files and converts to objects
        # questions = load_corresponding_practice(practiceName)
        questions = load_dynamic_exam_answers()

        # Count correct answers and set chosen answer for each question
        count = 0
        for i in range(len(questions)):
            if request.form.get(str(i)) == questions[i].answer:
                count += 1
            questions[i].chose = request.form.get(str(i))   # save the answer that user chose
        
        # Insert new score to history
        insert_score(count, 'exam-score', 'exam')

        return render_template("takeExamOnSite.html", user=current_user, questions=questions, name="Exam", points=count)
    
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


# This function will return list of questions from corresponding practice name
def load_corresponding_practice(name):
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


def load_random_exam_questions():
    theoryPath = "./DMV/resources/exam-theory-bank.csv"
    signsPath = "./DMV/resources/exam-signs-bank.csv"

    df_theory = pd.read_csv(theoryPath)
    df_signs = pd.read_csv(signsPath)

    # final list of questions
    questions = []

    # random 35 theory questions
    theory_questions = df_theory.sample(n=4, replace=False)

    # random 10 signs questions
    signs_questions = df_signs.sample(n=3, replace=False)

    # combine 2 set of questions
    set_questions = pd.concat([theory_questions, signs_questions])

    # shuffle the questions
    shuffled_df = set_questions.sample(frac=1.0, replace=False)

    shuffled_df = shuffled_df.reset_index(drop=True)
    shuffled_df['id'] = shuffled_df.index

    shuffled_df.to_csv("./DMV/resources/dynamic-exam-answers.csv", index=False)

    # read each line, create corresponding object for each question
    for i in range(shuffled_df.shape[0]):
        question = Question(shuffled_df.iloc[i]['id'], shuffled_df.iloc[i]['type'], shuffled_df.iloc[i]['question'], shuffled_df.iloc[i]['a'], shuffled_df.iloc[i]['b'], shuffled_df.iloc[i]['c'], shuffled_df.iloc[i]['d'], shuffled_df.iloc[i]['answer'])
        if pd.notna(shuffled_df.iloc[i]['chose']):
            question.chose = shuffled_df.iloc[i]['chose']
        questions.append(question)

    return questions 

def load_dynamic_exam_answers():
    answerPath = "./DMV/resources/dynamic-exam-answers.csv"

    df = pd.read_csv(answerPath)
    questions = []
    
    # read each line, create corresponding object for each question
    for i in range(df.shape[0]):
        question = Question(df.iloc[i]['id'], df.iloc[i]['type'], df.iloc[i]['question'], df.iloc[i]['a'], df.iloc[i]['b'], df.iloc[i]['c'], df.iloc[i]['d'], df.iloc[i]['answer'])
        if pd.notna(df.iloc[i]['chose']):
            question.chose = df.iloc[i]['chose']
        questions.append(question)

    return questions 
    




