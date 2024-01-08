# routes.py
from flask import render_template, redirect, url_for, request
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
