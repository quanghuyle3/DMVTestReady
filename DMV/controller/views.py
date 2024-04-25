from flask import Flask, render_template, Blueprint, request, redirect, url_for, jsonify
from flask_login import  login_required, current_user
import pandas as pd
import os
from ..models import Question, Practice_scores, Exam_scores
from ..import db
import os
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from flask import current_app, after_this_request


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

#GET request for showing profile
@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user = current_user)

#GET request for updating profile page
@views.route('/update_profile_page')
@login_required
def update_profile_page():
    return render_template("update_profile.html", user=current_user)

#updating profile and setting new data
@views.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    new_first_name = request.form.get('first_name')
    current_user.first_name = new_first_name
    db.session.commit()
    return redirect(url_for('views.profile'))


import json

from flask import flash

@views.route('/tester', methods=["POST", "GET"])
def test():
    if request.method == "GET":
        return render_template("test.html", user=current_user)
    else:
        result = request.form.get("result")
        people_json = request.form.get("people")  # Get the JSON string from the form
        people = json.loads(people_json)  # Parse the JSON string to get the list of people
        print(people)
        return render_template("tester1.html", user=current_user, result = result)




@views.route('/take-practice', methods=["POST", "GET"])
@login_required
def takePractice():
    if request.method == "GET":
        # Convert questions to a JSON format for HTML
        practiceName = request.args.get("name")
        #loading questions from given practice 
        questions = load_corresponding_practice(practiceName)
        questions_json = []
        # Convert questions to a JSON format for JS
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
        
        return render_template("takePractice.html", user=current_user, questions=questions_json, name=practiceName, points = -1)
    #After submitting the practice
    else:
        practiceName = request.form.get("name")

        #getting questions
        question_json = request.form.get("questions")
        post_questions = json.loads(question_json)
        correct = 0
        #calculating correct answers
        for i in range(len(post_questions)):
            if post_questions[i]["chose"] == "green":
                correct = correct +1 
        
        #adding too database
        insert_score(correct, practiceName) 
        #redirecting to history  
        return redirect(url_for('views.score_history'))







@views.route('/take-exam', methods=["POST", "GET"])
@login_required
def takeExam():
    #questions = randomize_questions()
    #print(questions)
    # Showing Questions
    if request.method == "GET":
        # get the correct exam name 
        practiceName = request.args.get("name")
        # load questions from files and converts to objects
        questions = randomize_questions()
        # Convert questions to a JSON format for JS
        questions_json = []
        for q in questions :
            question_dict = {
                "id": int(q.id),
                "type":q.type,
                "question": q.question,
                "a": q.a,
                "b": q.b,
                "c": q.c,
                "d": q.d,
                "answer": q.answer,
                "chose": q.chose
            }
            questions_json.append(question_dict)
        
        return render_template("takeExam.html", user=current_user, questions=questions_json, name=practiceName)
   #after submitting exam
    else:
        # get the correct practice name 
        # Print all chosen answers
        examName = request.form.get("name")
        
        #getting questions from HTML
        question_json = request.form.get("questions")
        post_questions = json.loads(question_json)
        correct = 0
        #calculating correct answers
        for i in range(len(post_questions)):
            if post_questions[i]["chose"] == "green":
                correct = correct +1 
        #adding to database
        insert_score(correct, examName, 'exam')  
        #redirecting to history  
        return redirect(url_for('views.score_history'))



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
    has_history = 1 if practice_scores or exam_scores else -1
    


    @after_this_request
    def add_seaborn_plot(response):
        # Create Seaborn plot for practice scores
        matplotlib.use('Agg')
        
        #checking if practice_scores is empty or not
        if practice_scores:
            #creating DataFrame from data
            practice_data = pd.DataFrame({
                'Practice Date': [score.timestamp.strftime('%Y-%m-%d') for score in practice_scores],
                'Practice Score': [score.score for score in practice_scores]
            })
        else:
            #create an empty DataFrame
            practice_data = pd.DataFrame(columns=['Practice Date', 'Practice Score'])
            practice_data.loc[0] = ['2024-04-24', 0]  # Dummy date and score

        #checking if practice_scores is empty or not
        if practice_scores:
            #creating plot from data
            sns.catplot(data=practice_data, x='Practice Date', y='Practice Score', kind='point')
        else:
            #creating plot from dummy data
            sns.catplot(data=practice_data, x='Practice Date', y='Practice Score', kind='point', color='b', alpha=0)


        # Ensure the 'static' directory exists
        
        static_dir = os.path.join(current_app.root_path, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # Save the practice plot as an image file with full path
        practice_plot_path = os.path.join(static_dir, 'practice_plot.png')
        plt.savefig(practice_plot_path)

        # Close the plot to prevent GUI issues
        plt.close()
        
        # Pass the image URL to the response
        response.practice_image_url = practice_plot_path

        #checking if exam_scores is empty or not
        if exam_scores:
            #creating DataFrame from data
            exam_data = pd.DataFrame({
                'Exam Date': [score.timestamp.strftime('%Y-%m-%d') for score in exam_scores],
                'Exam Score': [score.score for score in exam_scores]
            })
        else:
            # Create an empty DataFrame
            exam_data = pd.DataFrame(columns=['Exam Date', 'Exam Score'])
            exam_data.loc[0] = ['2024-04-24', 0]  # Dummy date and score
        #checking if exam_scores is empty or not
        if exam_scores:
            #creating plot from data
            sns.catplot(data=exam_data, x='Exam Date', y='Exam Score', kind='point')
        else:
            #creating plot from dummy data
            sns.catplot(data=exam_data, x='Exam Date', y='Exam Score', kind='point', color='b', alpha=0)
        
        # Save the exam plot as an image file with full path
        exam_plot_path = os.path.join(static_dir, 'exam_plot.png')
        plt.savefig(exam_plot_path)

        # Close the plot to prevent GUI issues
        plt.close()
        
        # Pass the image URL to the response
        response.exam_image_url = exam_plot_path
        
        return response
    
    return render_template("scoreHistory.html", user=current_user, practice_scores=practice_scores, exam_scores=exam_scores, has_history = has_history)







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
    

    db.session.add(new_score)
    db.session.commit()


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
    


import random


def randomize_questions():
    directory = "./DMV/resources/"
    # Collection of files of signs questions
    practice_files1 = [file for file in os.listdir(directory) if file.startswith('practice-signs') and file.endswith('.csv')]
    # Collection of files of theory questions
    practice_files2 = [file for file in os.listdir(directory) if file.startswith('practice') and file.endswith('.csv') and not file.startswith('practice-signs')]


    # Collecting 10 questions from each collections
    questions_from_set1 = collect_questions(practice_files1, 10, directory)
    questions_from_set2 = collect_questions(practice_files2, 10, directory)

    # Combining both collections
    all_questions = questions_from_set1 + questions_from_set2

    # Mixing questions
    random.shuffle(all_questions)

    return all_questions

#create questions
def create_question_from_row(row):
    return Question(
        id=int(row['id']),
        type=row['type'],
        question=row['question'],
        a=row['a'],
        b=row['b'],
        c=row['c'],
        d=row['d'],
        answer=row['answer'],
        chose=row.get('chose', '')
    )

def collect_questions(file_list, count, directory):
    questions = []
    # Collecting questions until reaching count
    for file in file_list:
        if len(questions) >= count:
            break  # Stop if we've collected enough questions

        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        
        # Determine the number of questions to sample considering the remaining slots
        sample_size = min(count - len(questions), len(df))
        if sample_size > 0:
            sample_df = df.sample(sample_size)
            # Convert sampled rows into Question objects using apply() and add them to the list
            question_objects = sample_df.apply(create_question_from_row, axis=1).tolist()
            questions.extend(question_objects)

    return questions



