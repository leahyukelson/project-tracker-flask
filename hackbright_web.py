"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def index():
  """Show homepage with links to all students and all projects. """
  
  students = hackbright.get_all_students()
  projects = hackbright.get_all_projects()

  return render_template("index.html", students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_all_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student. """

    return render_template("student_search.html")


@app.route("/project")
def get_project():
    """Show information about a project."""

    project_title = request.args.get('project_title')

    title, description, max_grade = hackbright.get_project_by_title(project_title)
    grades = hackbright.get_grades_by_title(project_title)

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           grades=grades)


@app.route("/project-search")
def get_project_form():
    """Show form for searching for a project. """

    return render_template("project_search.html")


@app.route("/student-add")
def student_add():
    """Form to add a student."""
    return render_template("student_add.html")

@app.route("/student-add-success", methods=['POST'])
def student_add_success():
    """Add a student."""
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)
    return render_template("student_add_success.html",
                           github=github)

@app.route("/project-add")
def project_add():
    """Form to add a project."""
    return render_template("project_add.html")


@app.route("/project-add-success", methods=['POST'])
def project_add_success():
    """Add a project."""
    project_title = request.form.get("project_title")
    project_description = request.form.get("project_description")
    max_grade = request.form.get("max_grade")

    hackbright.create_project(project_title, project_description, max_grade)
    return render_template("project_add_success.html",
                           project_title=project_title)





if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
