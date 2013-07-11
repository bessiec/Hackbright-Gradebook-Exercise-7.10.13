import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,)) # Where we call the desired github handle, NEED TUPLE
    print github,'THIS IS THE GITHUB'
    row = DB.fetchone() # calls each line one at a time
    return row
#Student: %s %s
#Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN

# CONN = "Connection" AND invoking 'sqlite3' calls the sqlite application
    CONN = sqlite3.connect("hackbright.db")
# Here, a cursor is similar to a file handler
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    #At this point, data won't persist, so we need to commit to the database connection, not cursor
    CONN.commit()
    print 'Successfully added student: %s %s' % (first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added new project %s" % (title)

def find_project(title):
    query = """SELECT student_github,grade,max_grade,description FROM Grades JOIN Projects ON title=project_title WHERE project_title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchall()
    return row
    # print """\
    # Project: %s
    # Text: %s
    # Maximum Grade: %d""" % (row[0], row[1], row[2])

def grades_by_student(github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    return row
        # for card in row:
        #     print "Project: %s - Grade: %d" %(card[0],card[1])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            input_string = raw_input("HBA Database> Enter github of a student> ")
            get_student_by_github(input_string) 
        elif command == "new_student":
            input_string = raw_input("HBA Database> Enter first and last name and github> ")
            tokens = input_string.split()
            make_new_student(tokens[0], tokens[1], tokens[2])
        elif command == "add project":
            input_string = raw_input("HBA Database> Enter first and last name and github> ")
            tokens = input_string.split()
            make_new_project(tokens[0], tokens[1], tokens[2])
        elif command == "project":
            input_string = raw_input("HBA Database> Enter title of a project> ")
            find_project(input_string)             

    CONN.close() # similar to closing a file after opening it in a file handler

if __name__ == "__main__":
    main()
