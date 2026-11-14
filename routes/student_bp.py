

from flask import Blueprint,render_template, request, redirect,url_for,session,flash

from db import db
from models import User, Examination



student_bp= Blueprint(
    "student",__name__,url_prefix="/api/student"
)



@student_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return "I am a Student"