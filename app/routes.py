# routes.py
from flask import render_template, request, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import Student, Grade, Course
from app.forms import StudentForm, GradeForm
from app.models import User  # Assuming you have a User model

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/average_scores')
def average_scores():
    # Fetch all students and their grades
    students = Student.query.all()

    # Create a dictionary to store average scores for each student
    average_scores = {}

    # Calculate the average score for each student
    for student in students:
        grades = Grade.query.filter_by(student=student).all()
        if grades:
            total_score = sum(int(grade.grade) for grade in grades)
            average_score = total_score / len(grades)
            average_scores[student.id] = average_score
        else:
            average_scores[student.id] = None

    return render_template('average_scores.html', average_scores=average_scores)


@app.route('/students', methods=['GET', 'POST'])
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

# Modify the dashboard route to pass dynamic data to the template
@app.route('/dashboard')
def dashboard():
    # Assume you have some data to display on the dashboard
    data = {'username': 'John Doe', 'role': 'Admin'}
    return render_template('dashboard.html', data=data)


@app.route('/students/<int:student_id>/grades', methods=['GET', 'POST'])
def view_grades(student_id):
    student = Student.query.get_or_404(student_id)
    form = GradeForm()

    if form.validate_on_submit():
        subject = form.subject.data
        grade = form.grade.data

        new_grade = Grade(subject=subject, grade=grade, student=student)
        db.session.add(new_grade)
        db.session.commit()

    grades = Grade.query.filter_by(student=student).all()

    return render_template('view_grades.html', student=student, form=form, grades=grades)



@app.route('/courses', methods=['GET'])
def courses():
    # Fetch all courses from the database (replace this with your actual query)
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/view_grades/<int:student_id>')
def view_grades(student_id):
    student = Student.query.get(student_id)  # Query the database for the specific student
    return render_template('view_grades.html', student=student)


@app.route('/students/<int:student_id>/view_grades', methods=['GET'])
def view_grades_for_student(student_id):
    # Fetch the student by ID
    student = Student.query.get_or_404(student_id)

    # Fetch grades for the specific student
    grades = Grade.query.filter_by(student=student).all()

    # Render the template with the student and grades
    return render_template('view_grades.html', student=student, grades=grades)



@app.route('/view_grades', methods=['GET'])
def view_grades():
    grades = Grade.query.all()
    print(grades)  # Check if grades are fetched from the database
    return render_template('view_grades.html', grades=grades)


@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(name=form.name.data, age=form.age.data)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('add_student.html', form=form)

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.age = form.age.data
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('edit_student.html', form=form, student=student)

@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))
