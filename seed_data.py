
from db import db
from models import User


def create_admin():
    admin=User.query.filter_by(email="admin13@gmail.com").first()
    if admin is None:
        admin = User(
            name="Exam Admin",
            email="admin13@gmail.com",
            role="Admin",
            status="Approved",
        )

        admin.set_password("admin123")
        db.session.add(admin) 
        db.session.commit()
        print("Admin Account Created")
    else:    
        print("Admin ALready Exist")

    
 


from db import db
from datetime import datetime, timezone, date, time
from models import (
    User,
    ExaminerProfile,
    Course,
    Examination,
    ExaminationRubric,
    ExaminationSlot,
    Booking,
    Evaluation,
    EvaluationDetail
)


def create_admin():
    admin=User.query.filter_by(email="admin13@gmail.com").first()
    if admin is None:
        admin = User(
            name="Exam Admin",
            email="admin13@gmail.com",
            role="Admin",
            status="Approved",
        )

        admin.set_password("admin123")
        db.session.add(admin) 
        db.session.commit()
        print("Admin Account Created")
    else:    
        print("Admin ALready Exist")

    

def seed_data():
    print("🌱 Starting database seeding...")

    try:
        # 1. Create Users (Students and Examiners)
        # Note: Admin can be created via your existing create_admin() function.
        
        users_data = [
            # Examiners
            {
                "name": "Dr. Alice Smith",
                "email": "alice.smith@university.edu",
                "role": "Examiner",
                "status": "Approved",
                "phone": "9876543210",
                "profile": {
                    "department": "Computer Science",
                    "designation": "Associate Professor",
                    "employee_id": "EMP101",
                    "qualification": "Ph.D. in Computer Science"
                }
            },
            {
                "name": "Prof. Bob Jones",
                "email": "bob.jones@university.edu",
                "role": "Examiner",
                "status": "Approved",
                "phone": "9876543211",
                "profile": {
                    "department": "Information Technology",
                    "designation": "Professor",
                    "employee_id": "EMP102",
                    "qualification": "Ph.D. in Software Engineering"
                }
            },
            # Students
            {
                "name": "John Doe",
                "email": "john.doe@student.edu",
                "role": "Student",
                "status": "Approved",
                "phone": "9123456789"
            },
            {
                "name": "Jane Eyre",
                "email": "jane.eyre@student.edu",
                "role": "Student",
                "status": "Approved",
                "phone": "9123456788"
            },
            {
                "name": "Samwise Gamgee",
                "email": "sam.gamgee@student.edu",
                "role": "Student",
                "status": "Approved",
                "phone": "9123456787"
            }
        ]

        created_users = {}
        for u_data in users_data:
            profile_data = u_data.pop("profile", None)
            user = User.query.filter_by(email=u_data["email"]).first()
            if not user:
                user = User(**u_data)
                user.set_password("password123")
                db.session.add(user)
                db.session.flush() # Flush to get user.id

                if profile_data:
                    profile = ExaminerProfile(user_id=user.id, **profile_data)
                    db.session.add(profile)

            created_users[user.email] = user

        # 2. Create Courses
        courses_data = [
            {
                "course_code": "CS101",
                "course_name": "Introduction to Python Programming",
                "description": "Fundamental concepts of programming using Python.",
                "status": "Active"
            },
            {
                "course_code": "IT202",
                "course_name": "Database Management Systems",
                "description": "Relational databases, SQL, and normalization.",
                "status": "Active"
            }
        ]

        created_courses = []
        for c_data in courses_data:
            course = Course.query.filter_by(course_code=c_data["course_code"]).first()
            if not course:
                course = Course(**c_data)
                db.session.add(course)
                db.session.flush()
            created_courses.append(course)

        # 3. Create Examinations
        examinations_data = [
            {
                "course_id": created_courses[0].id,
                "name": "CS101 Final Project Viva",
                "examination_type": "Viva",
                "duration_in_minutes": 30,
                "maximum_marks": 50.0,
                "status": "Booking Open"
            },
            {
                "course_id": created_courses[1].id,
                "name": "IT202 Practical Assessment",
                "examination_type": "Practical",
                "duration_in_minutes": 45,
                "maximum_marks": 100.0,
                "status": "Booking Open"
            }
        ]

        created_exams = []
        for e_data in examinations_data:
            # Check if exam exists by name & course
            exam = Examination.query.filter_by(name=e_data["name"]).first()
            if not exam:
                exam = Examination(**e_data)
                db.session.add(exam)
                db.session.flush()
            created_exams.append(exam)

        # 4. Create Examination Rubrics
        rubrics_data = [
            # Rubrics for Exam 1 (Viva - Total weightage 100%)
            {"examination_id": created_exams[0].id, "criterion_name": "Code Quality", "maximum_marks": 25.0, "weightage": 50.0, "description": "Clean and readable code."},
            {"explanation_id": created_exams[0].id, "criterion_name": "Explanation & Logic", "maximum_marks": 25.0, "weightage": 50.0, "description": "Ability to explain implementation."},
            
            # Rubrics for Exam 2 (Practical - Total weightage 100%)
            {"examination_id": created_exams[1].id, "criterion_name": "Query Optimization", "maximum_marks": 50.0, "weightage": 50.0, "description": "Efficiency of SQL queries."},
            {"explanation_id": created_exams[1].id, "criterion_name": "Schema Design", "maximum_marks": 50.0, "weightage": 50.0, "description": "Normalization and constraints adherence."}
        ]

        created_rubrics = []
        for r_data in rubrics_data:
            # Clean up key name typo if any
            r_data.pop("explanation_id", None)
            rubric = ExaminationRubric.query.filter_by(
                examination_id=r_data["examination_id"], 
                criterion_name=r_data["criterion_name"]
            ).first()
            if not rubric:
                rubric = ExaminationRubric(**r_data)
                db.session.add(rubric)
                db.session.flush()
            created_rubrics.append(rubric)

        # 5. Create Examination Slots
        slots_data = [
            {
                "examination_id": created_exams[0].id,
                "examiner_id": created_users["alice.smith@university.edu"].id,
                "date": date(2026, 11, 10),
                "start_time": time(10, 0),
                "end_time": time(10, 30),
                "maximum_capacity": 1,
                "status": "Available",
                "meeting_link": "https://meet.google.com/abc-defg-hij"
            },
            {
                "examination_id": created_exams[1].id,
                "examiner_id": created_users["bob.jones@university.edu"].id,
                "date": date(2026, 11, 11),
                "start_time": time(14, 0),
                "end_time": time(14, 45),
                "maximum_capacity": 2,
                "status": "Available",
                "meeting_link": "https://zoom.us/j/1234567890"
            }
        ]

        created_slots = []
        for s_data in slots_data:
            slot = ExaminationSlot.query.filter_by(
                examination_id=s_data["examination_id"],
                examiner_id=s_data["examiner_id"],
                date=s_data["date"],
                start_time=s_data["start_time"]
            ).first()
            if not slot:
                slot = ExaminationSlot(**s_data)
                db.session.add(slot)
                db.session.flush()
            created_slots.append(slot)

        # 6. Create Bookings
        bookings_data = [
            {
                "student_id": created_users["john.doe@student.edu"].id,
                "slot_id": created_slots[0].id,
                "status": "Booked"
            },
            {
                "student_id": created_users["jane.eyre@student.edu"].id,
                "slot_id": created_slots[1].id,
                "status": "Booked"
            }
        ]

        created_bookings = []
        for b_data in bookings_data:
            booking = Booking.query.filter_by(
                student_id=b_data["student_id"],
                slot_id=b_data["slot_id"]
            ).first()
            if not booking:
                booking = Booking(**b_data)
                db.session.add(booking)
                db.session.flush()
            created_bookings.append(booking)

        # 7. Create Evaluations & Evaluation Details (for the first booking as an example)
        eval_exists = Evaluation.query.filter_by(booking_id=created_bookings[0].id).first()
        if not eval_exists:
            evaluation = Evaluation(
                booking_id=created_bookings[0].id,
                examiner_id=created_users["alice.smith@university.edu"].id,
                total_marks=45.0,
                remarks="Excellent understanding of core concepts and clean code structure.",
                is_published=True,
                evaluated_at=datetime.now(timezone.utc)
            )
            db.session.add(evaluation)
            db.session.flush()

            # Add evaluation details for the rubrics linked to exam 0
            exam_0_rubrics = [r for r in created_rubrics if r.examination_id == created_exams[0].id]
            
            detail_1 = EvaluationDetail(
                evaluation_id=evaluation.id,
                rubric_id=exam_0_rubrics[0].id,
                marks_awarded=23.0
            )
            detail_2 = EvaluationDetail(
                evaluation_id=evaluation.id,
                rubric_id=exam_0_rubrics[1].id,
                marks_awarded=22.0
            )
            db.session.add_all([detail_1, detail_2])

        db.session.commit()
        print("✅ Database seeding completed successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error during database seeding: {e}")
        raise e

    

