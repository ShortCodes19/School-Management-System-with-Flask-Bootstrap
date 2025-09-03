from . import views_bp
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from ..extensions import db
from ..models import Student, Teacher
import datetime

@views_bp.route('/')
def home():
    return render_template('index.html')

@views_bp.route('/home')
@login_required
def dashboard():
    active_students_count = Student.query.filter_by(isActive=True).count()
    active_teacher_count = Teacher.query.filter_by(isActive=True).count()
    return render_template('dashboard.html', user=current_user, active_students_count=active_students_count, active_teacher_count=active_teacher_count)

@views_bp.route('/add_students', methods=['GET', 'POST'])
def add_students():
    if request.method == 'POST':
        studentId = request.form.get('studentId')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phone = request.form.get('phone')
        dob_str = request.form.get('dob')
        enrollmentDate_str = request.form.get('enrollmentDate')
        address = request.form.get('address')
        isActive = request.form.get('isActive') == 'on'

        # Convert date strings to date objects
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        enrollmentDate = datetime.datetime.strptime(enrollmentDate_str, '%Y-%m-%d').date() if enrollmentDate_str else None

        new_student = Student(
            studentId=studentId,
            email=email,
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            dob=dob,
            enrollmentDate=enrollmentDate,
            address=address,
            isActive=isActive
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('views.list_students'))
    return render_template('students/add_students.html', title='Add Students')

@views_bp.route('/students')
def list_students():
    search = request.args.get('search')
    if search:
        students = Student.query.filter(
            Student.firstName.contains(search) |
            Student.lastName.contains(search) |
            Student.email.contains(search)
        ).all()
    else:
        students = Student.query.all()

    return render_template('students/list_students.html', students=students, title='Students List')

@views_bp.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.studentId = request.form.get('studentId')
        student.email = request.form.get('email')
        student.firstName = request.form.get('firstName')
        student.lastName = request.form.get('lastName')
        student.phone = request.form.get('phone')
        dob_str = request.form.get('dob')
        enrollmentDate_str = request.form.get('enrollmentDate')
        student.address = request.form.get('address')
        student.isActive = request.form.get('isActive') == 'on'

        student.dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        student.enrollmentDate = datetime.datetime.strptime(enrollmentDate_str, '%Y-%m-%d').date() if enrollmentDate_str else None

        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('views.list_students'))
    return render_template('students/update_student.html', student=student, title='Update Student')

@views_bp.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('views.list_students'))

@views_bp.route('/add_teachers', methods=['GET', 'POST'])
def add_teachers():
    if request.method == 'POST':
        teacherId = request.form.get('teacherID')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phone = request.form.get('phone')
        department = request.form.get('department')
        dob_str = request.form.get('dob')
        hireDate_str = request.form.get('hireDate')
        address = request.form.get('address')
        isActive = request.form.get('isActive') == 'on'

        #Covert date string to date Ojects
        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        hireDate = datetime.datetime.strptime(hireDate_str, '%Y-%m-%d').date() if hireDate_str else None

        new_teacher = Teacher(
            teacherId=teacherId,
            firstName=firstName,
            lastName=lastName,
            email=email,
            phone=phone,
            department=department,
            dob=dob,
            hireDate=hireDate,
            address=address,
            isActive=isActive
        )
        db.session.add(new_teacher)
        db.session.commit()
        flash('Teacher Added Successfully!' 'success')
        return redirect(url_for('views.list_teachers'))
    return render_template('teachers/add_teachers.html', title='Add Teachers')

@views_bp.route('/update_teachers/<int:teacher_id>', methods=['GET', 'POST'])
def update_teachers(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    if request.method == 'POST':
        teacher.teacherId = request.form.get('teacherID')
        teacher.email = request.form.get('email')
        teacher.firstName = request.form.get('firstName')
        teacher.lastName = request.form.get('lastName')
        teacher.phone = request.form.get('phone')
        teacher.department = request.form.get('department')
        teacher.address = request.form.get('address')
        teacher.isActive = request.form.get('isActive') == 'on'
        dob_str = request.form.get('dob')
        hireDate_Str = request.form.get('hireDate')

        dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        hireDate = datetime.datetime.strptime(hireDate_Str, '%Y-%m-%d').date() if hireDate_Str else None

        db.session.commit()
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('views.list_teachers'))
    return render_template('teachers/update_teachers.html', teacher=teacher, title='Update Teacher')


@views_bp.route('/delete_teachers/<int:teacher_id>', methods=['GET', 'POST'])
def delete_teachers(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('views.list_teachers'))



@views_bp.route('/list_teachers')
def list_teachers():
    search = request.args.get('search')
    if search:
        teachers = Teacher.query.filter(
            Teacher.firstName.contains(search) |
            Teacher.lastName.contains(search) |
            Teacher.email.contains(search)
        ).all()
    else:
        teachers = Teacher.query.all()
    return render_template('teachers/list_teachers.html', teachers=teachers, title='List Teachers')