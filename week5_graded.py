import os.path
from sqlalchemy import update
from flask import Flask
import sqlalchemy
from flask import render_template
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name =db.Column(db.String, nullable=False)
    last_name =db.Column(db.String)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description=db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id =db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

@app.route("/", methods= ["GET","POST"])
def All_student():
    students = Student.query.all()
    return render_template("all_students.html", students=students)

@app.route("/student/create", methods= ["GET"])
def create_student_get():
    return render_template("add_student.html")

@app.route("/student/create", methods= ["POST"])
def create_student_post():
    try:
        form = request.form
        std_roll_no = form.get("roll")
        std_fname = form.get("f_name")
        std_lname = form.get("l_name")
        student = Student(roll_number=std_roll_no, first_name=std_fname, last_name=std_lname)
        db.session.add(student)
        db.session.flush()
        sid = student.student_id
        course_list = form.getlist("courses")
        course_dict = {"course_1": 1, "course_2": 2, "course_3": 3, "course_4": 4}
        for course in course_list:
            enrollment = Enrollments(estudent_id=sid, ecourse_id=course_dict[course])
            db.session.add(enrollment)
            db.session.flush()
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print("Duplicate")
        return render_template("duplicate_rollnumber.html")
    except Exception as e:
        print("Error", e)
        return render_template("error.html")
    return redirect("/")
@app.route('/student/<student_id>', methods=['GET'])
def students_details_get(student_id):
    student = Student.query.filter(Student.student_id == student_id).first()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id == student_id).all()
    course_ids = [i.ecourse_id for i in enrollments]
    course_list = []
    for index, cid in enumerate(course_ids):
        course = Course.query.filter(Course.course_id == cid).first()
        course_list.append([index + 1, course.course_code, course.course_name, course.course_description])
    return render_template("personal.html", students=student, courses=course_list)


@app.route("/student/<student_id>/delete", methods=["GET"])
def delete_students_get(student_id):
    Student.query.filter(Student.student_id==student_id).delete()
    db.session.commit()
    Enrollments.query.filter(Enrollments.estudent_id==student_id).delete()
    db.session.commit()
    return redirect("/")
    
@app.route('/student/<stud_id>/update', methods=['GET', 'POST'])
def update(stud_id):
    if request.method == 'GET':
        Stu = Student.query.get(stud_id)
        return render_template('update.html', student=Stu)

    elif request.method == 'POST':
        first_name = request.form['f_name']
        print(first_name)
        last_name = request.form['l_name']
        
        Stu = Student.query.get(stud_id)
        Stu.first_name = first_name
        Stu.last_name = last_name
        

        Enrollments.query.filter_by(estudent_id=stud_id).delete()
        db.session.flush()
        courses = request.form.getlist('courses')
        for course in courses:
            enroll = Enrollments(estudent_id=stud_id,
                                 ecourse_id=int(course[-1]))
            db.session.add(enroll)

        db.session.commit()
        return redirect('/')


if __name__== "__main__":
    app.run(host= '0.0.0.0',
    debug = True,
    port = 8080)
    