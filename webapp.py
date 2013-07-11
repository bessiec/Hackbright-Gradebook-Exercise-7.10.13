from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    github_only = row[2]
    grades = hackbright_app.grades_by_student(github_only)
    html = render_template("student_info.html", first_name=row[0], last_name=row[1], github=row[2], grades=grades)
    return html

@app.route("/project_list")
def get_projects():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    all_student_projects = hackbright_app.find_project(project)
    project_description = all_student_projects[0][3]
    html = render_template("project_list.html",all_student_projects=all_student_projects,
        project_name=project,project_description=project_description)
    return html

@app.route("/new_student")
def new_student_page():
    return render_template("new_student.html")

@app.route("/create_student")
def create_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    print create_student,"LIST OF FIRSTNAME ETC"
    hackbright_app.make_new_student(first_name,last_name,github)
    return get_student()

@app.route("/new_project")
def new_project_page():
    return render_template("new_project.html")

@app.route("/create_project")
def create_project():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(project, description, max_grade)
    return get_student()

if __name__ == "__main__":
    app.run(debug=True)
