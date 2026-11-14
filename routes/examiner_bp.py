from flask import Blueprint,render_template, request, redirect,url_for,session,flash

from db import db
from models import User, Examination



examiner_bp= Blueprint(
    "examiner",__name__,url_prefix="/api/examiner"
)



@examiner_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return "I AM ADMIN"