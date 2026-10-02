import os
import logging
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EMAIL_FORMAT = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "DEV-ONLY-change-this-secret-key"),
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(BASE_DIR, "secureboard.db"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # True when deployed behind HTTPS
    MAX_CONTENT_LENGTH=64 * 1024,
)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["300 per hour"],
    storage_uri="memory://",
)

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "security.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    comments = db.relationship("Comment", backref="author", lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class LoginForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Length(max=120), Regexp(EMAIL_FORMAT, message="E-mail inválido.")],
    )
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Entrar")

class CommentForm(FlaskForm):
    body = TextAreaField("Comentário", validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField("Publicar")

class UserForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Length(max=120), Regexp(EMAIL_FORMAT, message="E-mail inválido.")],
    )
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=12, max=128)])
    submit = SubmitField("Criar usuário")

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            abort(401)
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            abort(401)
        if user.role != "admin":
            logging.warning("AUTHZ_DENIED user=%s path=%s ip=%s", user.id, request.path, get_remote_address())
            abort(403)
        return fn(*args, **kwargs)
    return wrapper

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    return response

@app.context_processor
def inject_user():
    return {"current_user": current_user()}

@app.route("/")
def index():
    comments = Comment.query.order_by(Comment.created_at.desc()).limit(50).all()
    return render_template("index.html", comments=comments)

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session.clear()
            session["user_id"] = user.id
            session.permanent = True
            logging.info("LOGIN_SUCCESS user=%s ip=%s", user.id, get_remote_address())
            return redirect(url_for("index"))

        logging.warning("LOGIN_FAILURE email=%s ip=%s", form.email.data[:120], get_remote_address())
        flash("Credenciais inválidas.", "error")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    uid = session.get("user_id")
    session.clear()
    logging.info("LOGOUT user=%s ip=%s", uid, get_remote_address())
    flash("Sessão encerrada.", "success")
    return redirect(url_for("index"))

@app.route("/comment", methods=["POST"])
@login_required
@limiter.limit("20 per minute")
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        c = Comment(body=form.body.data.strip(), user_id=current_user().id)
        db.session.add(c)
        db.session.commit()
        logging.info("COMMENT_CREATE user=%s comment=%s ip=%s",
                     current_user().id, c.id, get_remote_address())
        flash("Comentário publicado.", "success")
    else:
        flash("Comentário inválido.", "error")
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin():
    users = User.query.order_by(User.id).all()
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template("admin.html", users=users, comments=comments)

@app.route("/admin/users/new", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado.", "error")
        else:
            user = User(
                email=email,
                password_hash=generate_password_hash(form.password.data),
                role="user"
            )
            db.session.add(user)
            db.session.commit()
            logging.info("USER_CREATE admin=%s new_user=%s", current_user().id, user.id)
            flash("Usuário criado.", "success")
            return redirect(url_for("admin"))
    return render_template("create_user.html", form=form)

@app.errorhandler(400)
def bad_request(e):
    return render_template("error.html", code=400, message="Requisição inválida."), 400

@app.errorhandler(401)
def unauthorized(e):
    return render_template("error.html", code=401, message="Autenticação necessária."), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code=403, message="Acesso não autorizado."), 403

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404, message="Recurso não encontrado."), 404

@app.errorhandler(429)
def rate_limit(e):
    return render_template("error.html", code=429, message="Limite de requisições atingido."), 429

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    logging.exception("INTERNAL_ERROR ip=%s path=%s", get_remote_address(), request.path)
    return render_template("error.html", code=500, message="Erro interno."), 500

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Apenas para laboratório. Não usar o servidor Flask de desenvolvimento em produção.
    app.run(host="0.0.0.0", port=5000, debug=False)
