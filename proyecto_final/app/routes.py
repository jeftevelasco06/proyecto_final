from flask import Blueprint, render_template, redirect, url_for, request, session
from . import db
from .models import User, Question

main = Blueprint('main', __name__)

@main.route('/')
def index():
    preguntas = Question.query.all()
    return render_template('index.html', preguntas=preguntas)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nuevo = User(username=request.form['username'], password=request.form['password'])
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@main.route('/ask', methods=['GET', 'POST'])
def ask():
    # Verifica si el usuario está logueado
    if 'user_id' not in session:
        return redirect(url_for('main.login'))  # Redirige al login si no hay sesión

    if request.method == 'POST':
        nueva = Question(
            title=request.form['title'],
            content=request.form['content'],
            user_id=session['user_id']
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('ask.html')

