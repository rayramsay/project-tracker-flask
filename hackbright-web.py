from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/search-student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    try:
        first, last, github = hackbright.get_student_by_github(github)
    except:
        return "You need to enter a github user name."

    projects_grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            projects_grades=projects_grades)

@app.route("/show-search-form")
def get_search_student_form():
    """Display search form."""

    return render_template("student_search.html")

@app.route("/show-add-form")
def get_add_student_form():
    """Display a new student form."""
    return render_template("student_add.html")


@app.route("/add-student", methods=['POST'])
def add_student():
    """Add a student to the database."""
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    github = request.form.get('github')

    # Before adding to database, make sure all fields contain text.
    if fname and lname and github:
        hackbright.make_new_student(fname, lname, github)
    else:
        return "You need to provide all fields."

    return render_template("student_add_success.html",
        fname=fname, lname=lname, github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
