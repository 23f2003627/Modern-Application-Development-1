
from flask import Flask, redirect, url_for, render_template
from config.config import Config
from db import db
from seed_data import create_admin

from routes.auth_bp import auth_bp
from routes.admin_bp import admin_bp
from routes.examiner_bp import examiner_bp
from routes.student_bp import student_bp


app = Flask(__name__)  # WSGI

app.config.from_object(Config)

db.init_app(app)


# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(examiner_bp)
app.register_blueprint(student_bp)


# Create database tables
with app.app_context():
    from models import *
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
