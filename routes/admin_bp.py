from flask import Blueprint,render_template, request, redirect,url_for,session,flash

from db import db
from models import User, Examination



admin_bp= Blueprint(
    "admin",__name__,url_prefix="/api/admin"
)



@admin_bp.route("/dashboard",methods=["GET"])
def dashboard():
    return "I AM ADMIN"