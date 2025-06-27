from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    feedbacks = db.relationship('Feedback', backref='user', lazy=True)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    feedbacks = db.relationship('Feedback', backref='course', lazy=True)


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey('courses.id'), nullable=False)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(2000))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='one_feedback_per_user_per_course'),
    )
