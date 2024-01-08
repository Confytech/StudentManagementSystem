# routes.py
from flask import render_template, request
from app import app, db
from app.models import Student, Grade, Course
from app.forms import StudentForm, GradeForm

@app.route('/students', methods=['GET', 'POST'])
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

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
