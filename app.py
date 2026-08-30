from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

import json
import os

from classroom_service import (
    get_courses,
    get_coursework
)

from submission_processor import (
    process_assignment
)

from batch_processor import (
    process_submissions,
    save_reports
)


app = Flask(__name__)


@app.route("/")
def dashboard():

    courses = get_courses()

    return render_template(
        "dashboard.html",
        courses=courses
    )


@app.route("/assignments/<course_id>")
def assignments(course_id):

    coursework = get_coursework(
        course_id
    )

    assignments = []

    for assignment in coursework:

        assignments.append({
            "id": assignment.get("id"),
            "title": assignment.get("title")
        })

    return {
        "assignments": assignments
    }


@app.route("/run-check", methods=["POST"])
def run_check():

    course_id = request.form.get(
        "course_id"
    )

    coursework_id = request.form.get(
        "coursework_id"
    )

    print(
        "Course:",
        course_id
    )

    print(
        "Assignment:",
        coursework_id
    )

    submissions = process_assignment(
        course_id,
        coursework_id
    )

    if len(submissions) < 2:

        return "Not enough submissions to compare."

    reports = process_submissions(
        submissions
    )

    save_reports(
        reports
    )

    return redirect(
        url_for("results")
    )


@app.route("/results")
def results():

    report_path = (
        "reports/plagiarism_report.json"
    )

    reports = []

    if os.path.exists(report_path):

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as file:

            reports = json.load(file)

    return render_template(
        "results.html",
        reports=reports
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )