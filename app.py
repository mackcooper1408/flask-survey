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

    session["responses"] = list()

    return render_template("/survey_start.html")


@app.route("/begin", methods=["POST"])
def survey_redict():

    return redirect("/question/0")


@app.route("/question/<num>")
def handle_questions(num):
    """Handling the questions"""

    num = int(num)
  
    if len(session["responses"]) == len(survey.questions):
        
        return redirect("/thanks")

    if num is not len(session["responses"]):
        num = len(session["responses"])
        return redirect(f"/question/{num}")
    question = survey.questions[num]
    breakpoint()
    return render_template("/question.html", question=question)


@app.route("/answer", methods=["POST"])
def store_answer():
    answer = request.form["answer"]

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    question_count = len(responses)
    # breakpoint()
    if question_count == len(survey.questions):

        return redirect("/thanks")

    return redirect(f"/question/{question_count}")


@app.route("/thanks")
def thank_client():

    return render_template("/completion.html")
