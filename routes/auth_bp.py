from flask import Blueprint,render_template, request, redirect,url_for,session,flash

from db import db
from models import User, Examination


auth_bp= Blueprint(
    "auth",__name__,url_prefix="/api/auth"
)


@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        data=request.form
        email= data.get("email")
        password= data.get("password")

        user=User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.status != "Approved":
                return redirect(url_for("auth.login"))

        session["user_id"]=user.id
        session["role"]=user.role
        session["name"]=user.name


        if user.role == "Admin":
            return redirect(url_for("admin.dashboard"))
        elif user.role == "Examiner":
            return redirect(url_for("examiner.dashboard"))
        elif user.role == "Student":
            return redirect(url_for("student.dashboard"))

    return render_template("auth/login.html")



@auth_bp.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        data=request.form
        name= data.get("user_name")
        email= data.get("email")
        password= data.get("password")
        phone= data.get("phone")
        role= data.get("role")

        if not name or not email or not password:
            flash("Please Fill all the credentials correct")
            return redirect(url_for("auth.register"))

        if role not in ["Student"]:
            flash("Please select correct role")
            return redirect(url_for("auth.register"))


        if role not in ["Student"]:
            flash("Please select correct role")
            return redirect(url_for("auth.register"))


        if len(password) < 8:
            flash("length is smaller than expected")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already Existed")
            return redirect(url_for("auth.register"))           



            
        user=User(
            name=name,email=email,role="Student",phone=phone,status="Pending" if role=="Examiner" else "Approved"
        )


        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        if role == "Student":
            flash("Login to get access to book slot")
            return redirect(url_for("auth.login"))
        



    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Successfully Logout")
    return redirect(url_for("auth.login"))

    

 