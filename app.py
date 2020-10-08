from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = list()


@app.route("/")
def show_home():
    """Home Page"""

    return render_template("/survey_start.html")

@app.route("/begin", methods=["POST"])
def survey_redict():

    return redirect("/question/0")


@app.route("/question/<num>")
def handle_questions(num):
    """Handling the questions"""

    question = survey.questions[int(num)]

    return render_template("/question.html", question=question)

@app.route("/answer", methods=["POST"])
def store_answer():

    answer = request.form["answer"]
    responses.append(answer)
    question_count = len(responses)
    if question_count == len(survey.questions):

        return redirect("/thanks")

    return redirect(f"/question/{question_count}")

@app.route("/thanks")
def thank_client():

    return render_template("/completion.html")


