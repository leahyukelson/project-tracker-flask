"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])
    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
            INSERT INTO students
            VALUES (:first_name, :last_name, :github)
            """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})

    db.session.commit()

    print "Successfully added student: %s %s" % (first_name,
                                                 last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
    SELECT title, description, max_grade
    FROM projects
    WHERE title = :title
    """
    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    print "Project: %s \nDescription:%s\nMax grade: %s" % (row[0], row[1], row[2])
    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
    SELECT grade
    FROM grades
    WHERE student_github = :github and project_title = :title
    """
    db_cursor = db.session.execute(QUERY, {'github': github,
                                           'title': title})
    row = db_cursor.fetchone()
    print "Grade for %s is %s" % (title, row[0])


def get_all_grades_by_github(github):
    """Print all grades student received for all projects."""

    QUERY = """
    SELECT project_title, grade
    FROM grades
    WHERE student_github = :github
    """
    db_cursor = db.session.execute(QUERY, {'github': github})

    # for row in db_cursor:
    #     print "Grade for %s is %s" % (row[0], row[1])

    return db_cursor.fetchall()


def get_all_students():
    """Print all students in database."""

    QUERY = """
    SELECT first_name, last_name, github
    FROM students
    """
    db_cursor = db.session.execute(QUERY)

    # for row in db_cursor:
    #     print "Grade for %s is %s" % (row[0], row[1])

    return db_cursor.fetchall()


def get_all_projects():
    """Print all projects in database."""

    QUERY = """
    SELECT title
    FROM projects
    """
    db_cursor = db.session.execute(QUERY)

    # for row in db_cursor:
    #     print "Grade for %s is %s" % (row[0], row[1])

    return db_cursor.fetchall()

def get_grades_by_title(title):
    """Get a list of all student grades for a project by its title"""

    QUERY = """
        SELECT student_github, grade
        FROM Grades
        WHERE project_title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    rows = db_cursor.fetchall()

    # for row in rows:
    #     print "Student {acct} received grade of {grade} for {title}".format(
    #         acct=row[0], grade=row[1], title=title)

    return rows


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
            INSERT INTO grades (student_github, project_title, grade)
               VALUES (:student_github, :project_title, :grade)
            """

    db.session.execute(QUERY, {'student_github': github,
                               'project_title': title,
                               'grade': grade})

    db.session.commit()

    print "Successfully added grade for: %s \n%s for %s" % (github, grade, title)


def create_project(title, description, max_grade):
    """Create a new project and print a confirmation."""

    QUERY = """
            INSERT INTO projects (title, description, max_grade)
            VALUES (:title, :description, :max_grade)
            """

    db.session.execute(QUERY, {'title': title,
                               'description': description,
                               'max_grade': max_grade})
    db.session.commit()

    print "Successfully added project %s to projects table." % title


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        try:
            if command == "student":
                github = args[0]
                get_student_by_github(github)

            elif command == "new_student":
                first_name, last_name, github = args   # unpack!
                make_new_student(first_name, last_name, github)

            elif command == "project":
                title = args[0]
                get_project_by_title(title)

            elif command == "new_project":
                title = args[0]
                description = raw_input("Enter Description> ")
                max_grade = raw_input("Enter Max Grade> ")
                create_project(title, description, max_grade)

            elif command == "project_grade":
                github, title = args
                get_grade_by_github_title(github, title)

            elif command == "all_grades":
                github = args[0]
                get_all_grades_by_github(github)

            elif command == "new_grade":
                github, project, grade = args
                assign_grade(github, project, grade)

            else:
                if command != "quit":
                    print "Invalid Entry. Try again."
        except:
            print "Invalid Entry. Try again."

if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()
