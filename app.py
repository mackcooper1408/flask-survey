from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey, personality_quiz
from surveys import surveys as survey_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_home():
    """Home Page"""
    surveys = survey_dict
    return render_template("/survey_start.html", surveys=surveys)


@app.route("/begin", methods=["POST"])
def survey_redirect():

    session["responses"] = list()
    session["current_survey"] = request.form["answer"]
    survey = request.form["answer"]
    return redirect(url_for("handle_questions", survey=survey, num=0))


@app.route("/<survey>/question/<int:num>")
def handle_questions(survey, num):
    """Handling the questions"""
    current_survey = None
    for key in survey_dict:
        if survey == key:
            current_survey = survey_dict[key]

    if len(session["responses"]) == len(current_survey.questions):
        flash("You're done... Get over it...")
        return redirect("/thanks")

    if num is not len(session["responses"]):
        num = len(session["responses"])
        flash(f"You are on question {num} you dummy!")
        return redirect(f"/question/{num}")

    question = current_survey.questions[num]
    return render_template("/question.html", question=question)


@app.route("/answer", methods=["POST"])
def store_answer():
    answer = request.form["answer"]

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    question_count = len(responses)

    survey = session["current_survey"]

    return redirect(f"/{survey}/question/{question_count}")


@app.route("/thanks")
def thank_client():

    return render_template("/completion.html")
