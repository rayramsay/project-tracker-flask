from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def get_homepage():
    """Displays home page with all students and all projects."""
    students = hackbright.get_students()
    projects = hackbright.get_projects()
    return render_template("index.html",
                           students=students,
                           projects=projects)

@app.route("/search-student-form")
def get_search_student_form():
    """Display student search form."""

    return render_template("student_search.html")


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


@app.route("/add-form")
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


@app.route("/search-project-form")
def get_search_project_form():
    """Display project search form."""

    return render_template("project_search.html")


@app.route("/search-project")
def get_project():
    """Show information about a project."""

    project_name = request.args.get('project_name','Markov')

    title, description, max_grade = hackbright.get_project_by_title(project_name)

    students_grades = hackbright.get_grades_by_title(project_name)

    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            students_grades=students_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
