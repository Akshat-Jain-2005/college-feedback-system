from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User, Feedback, Course
from sqlalchemy import func

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'teacher':
                return redirect(url_for('routes_bp.teacher_summary'))
            else:
                return redirect(url_for('routes_bp.submit_feedback'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error="Email already exists.")

        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes_bp.login'))
    return render_template('register.html')


@routes_bp.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'user_id' not in session:
        return redirect(url_for('routes_bp.login'))

    if request.method == 'POST':
        course_id = request.form['course_id']
        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])
        q4 = int(request.form['q4'])
        q5 = int(request.form['q5'])
        q6 = int(request.form['q6'])
        review = request.form['review']

        feedback = Feedback(
            user_id=session['user_id'],
            course_id=course_id,
            q1=q1,
            q2=q2,
            q3=q3,
            q4=q4,
            q5=q5,
            q6=q6,
            review=review
        )
        db.session.add(feedback)
        db.session.commit()

        return render_template("thank_you.html")
    return render_template('feedback.html')


@routes_bp.route('/teacher_summary')
def teacher_summary():
    if 'user_id' not in session or session.get('role') != 'teacher':
        return redirect(url_for('routes_bp.login'))

    summaries = db.session.query(
        Feedback.course_id,
        func.avg(Feedback.q1).label("avg_q1"),
        func.avg(Feedback.q2).label("avg_q2"),
        func.avg(Feedback.q3).label("avg_q3"),
        func.avg(Feedback.q4).label("avg_q4"),
        func.avg(Feedback.q5).label("avg_q5"),
        func.avg(Feedback.q6).label("avg_q6"),
        func.count(Feedback.id).label("total_reviews")
    ).group_by(Feedback.course_id).all()

    question_labels = [
        "Clarity",
        "Communication",
        "Engagement",
        "Relevance",
        "Practical Use",
        "Instructor Support"
    ]

    return render_template("teacher_summary.html", summaries=summaries, question_labels=question_labels)
