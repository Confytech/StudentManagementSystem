from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sqlalchemy import inspect
from models import Course, Grade, User
from forms import StudentForm, GradeForm, LoginForm
from models import db, Student  # Import db and Student from models.py

import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19145569@localhost/confytech'
app.config['SECRET_KEY'] = '52087318ea97c1280f2fe2bb4d13327ef85802c2f27f1a1d'

db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Add this part for Login and Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create an instance of the LoginForm class
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('students.html'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/')
@login_required
def index():
    # This is just a placeholder. Replace it with your actual home page logic.
    return render_template('students.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('students.html'))


# Add this part to check the database
@app.route('/check_database')
def check_database():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
    return render_template('check_database.html', tables=tables)


# CRUD operations for students
@app.route('/students', methods=['GET', 'POST'])
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)


# Route for adding a grade to a student
@app.route('/students/add_grade/<int:student_id>', methods=['GET', 'POST'])
def add_grade(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        subject = request.form.get('subject')
        grade_value = request.form.get('grade')

        new_grade = Grade(subject=subject, grade=grade_value, student_id=student_id)
        db.session.add(new_grade)
        db.session.commit()

        return redirect(url_for('students'))

    return render_template('add_grade.html', student=student)


# Route for handling grades
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == 'POST':
        # Process and store form data in the Grade table
        # Example: grade = Grade(subject=request.form['subject'], grade=request.form['grade'])
        # db.session.add(grade)
        # db.session.commit()
        return redirect(url_for('view_grades'))
    return render_template('grades.html')  # Adjust the template name as needed


# Route for viewing all grades
@app.route('/view_grades')
def view_grades():
    grades = Grade.query.all()
    return render_template('view_grades.html', grades=grades)


# Add this route in app.py
@app.route('/students/view_grades/<int:student_id>', methods=['GET'])
def view_student_grades(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_grades.html', student=student)


# Route for viewing courses
@app.route('/courses')
def courses():
    return render_template('courses.html')  # Update with your actual template


# Add this part for adding courses
@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        # Process the form data and add the course to the database
        # ...

        # Redirect to the courses page or wherever appropriate
        return redirect(url_for('courses'))

    # If it's a GET request, render the 'add_course' template
    return render_template('add_course.html')


# In your app.py or wherever you define routes
from flask import render_template

# ... (other imports and configurations)

# Route for viewing courses
@app.route('/courses', methods=['GET'])
def view_courses():
    # Fetch all courses from the database (replace this with your actual query)
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


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

# Ensure the app is run only when this script is executed
if __name__ == '__main__':
    app.run(debug=True)
