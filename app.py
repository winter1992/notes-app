from flask import Flask, render_template, redirect, url_for, request, session, abort
from models import db, Note, User
from forms import NoteForm
from flask_wtf import CSRFProtect
from forms import AuthForm
from sqlalchemy import text
from werkzeug.security import check_password_hash
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_secret_key"  # для CSRF

# Используем переменную окружения DATABASE_URL, если она есть, иначе - fallback на SQLite (для совместимости)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'notes.db')}")
# Если DATABASE_URL начинается с "postgres://", заменим на "postgresql://" (для совместимости с SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://notes_user:password123@localhost:5432/notes_app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # если используется HTTPS
    SESSION_COOKIE_SAMESITE='Lax'
)

db.init_app(app)

csrf = CSRFProtect(app)

# Middleware для безопасности
@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Server"] = "SecureServer"  # скрываем Werkzeug/Flask
    return response

# Имитация "аутентификации": фиксированный пользователь
@app.before_request
def mock_login():
    if "user_id" not in session:
        session["user_id"] = 1


@app.route("/", methods=["GET", "POST"])
def index():
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=session["user_id"]  # владелец
        )
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for("index"))

    notes = Note.query.filter_by(user_id=session["user_id"]).all()
    return render_template("index.html", form=form, notes=notes)


@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    note = Note.query.filter_by(id=note_id, user_id=session["user_id"]).first()
    if not note:
        abort(403)  # защита от IDOR

    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", form=form, note=note)


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    note = Note.query.filter_by(id=note_id, user_id=session["user_id"]).first()
    if not note:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = AuthForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        # Безопасно: хешируем пароль и используем ORM
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return "Registered", 201
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = AuthForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        # ORM: параметры будут подставлены драйвером — безопасно
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            return "Login OK", 200, {"Content-Type": "text/plain"}
        return "Invalid", 401, {"Content-Type": "text/plain"}

    return render_template("login.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
