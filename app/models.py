from .extensions import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash =  db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    enrollmentDate = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=True)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Student {self.firstName} {self.lastName}>'

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacherId = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    hireDate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200))
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Teacher {self.firstName} {self.lastName}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))