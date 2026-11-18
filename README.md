# Examination Management Portal (EMP)

A role-based web application for managing academic examinations, examiner assignments, examination slots, student bookings, and evaluation records.

The Examination Management Portal (EMP) streamlines examination administration for educational institutions. It replaces spreadsheet-, email-, and manually coordinated workflows with a centralized platform for administrators, examiners, and students.

EMP supports the complete examination workflow: course and examination creation, examiner assignment, slot scheduling, student booking, evaluation, and result publication.

## Table of Contents

- [Technology Stack](#technology-stack)
- [Project Constraints](#project-constraints)
- [User Roles](#user-roles)
- [Database Design](#database-design)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Core Application Rules](#core-application-rules)
- [Security and Data Validation](#security-and-data-validation)
- [Development Milestones](#development-milestones)
- [Git Workflow](#git-workflow)
- [Future Enhancements](#future-enhancements)
- [Project Information](#project-information)

## Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Backend programming |
| Flask 3.0 | Web application framework |
| Flask-SQLAlchemy | ORM and database management |
| SQLAlchemy 2.0 | Database models and relationships |
| SQLite | Database |
| Jinja2 | Server-side templating |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap | Responsive UI |
| Werkzeug | Password hashing and security |
| Flask-Migrate | Database migrations |

## Project Constraints

- Flask must be used for backend development.
- SQLite is the only permitted database.
- Jinja2, HTML, CSS, and Bootstrap are used for the frontend.
- JavaScript must not be used to implement core requirements.
- Database tables must be created programmatically.
- The application must run locally.

## User Roles

### Admin

The Admin is the predefined superuser responsible for managing the entire examination system.

- View dashboard statistics.
- Create, edit, and manage courses.
- Create and manage examinations.
- Create and manage examination rubrics.
- Approve or deactivate examiner accounts.
- Configure examination timelines.
- Open and close examiner slot creation.
- Open and close student slot booking.
- View all examination slots and bookings.
- Search students, examiners, examinations, and bookings.
- Reschedule examination bookings.
- Change examiner assignments when required.
- Access historical examination records.

### Examiner

Examiners are faculty members responsible for conducting examinations and evaluating students.

- Register and log in.
- Access the dashboard after Admin approval.
- Update examiner profile.
- View assigned examinations.
- Create examination slots during the permitted period.
- Update or remove slots before booking starts.
- View students booked into their slots.
- Evaluate students using examination rubrics.
- Submit marks and remarks.
- View created slots and pending evaluations.

### Student

Students can register, explore examinations, book slots, and access their examination results.

- Register and log in.
- Update profile.
- View available examinations.
- Search and filter examinations.
- View available examination slots.
- Book examination slots.
- Cancel bookings before the booking deadline.
- View upcoming examinations and schedules.
- View booking and examination history.
- Access published results and evaluation feedback.

## Database Design

EMP uses SQLite with Flask-SQLAlchemy for database operations. All tables are created programmatically through the application initialization process.

### Models

| Model | Description |
| --- | --- |
| `User` | Stores Admin, Examiner, and Student account details |
| `ExaminerProfile` | Stores examiner-specific information |
| `Course` | Stores course information |
| `Examination` | Stores examination details and timelines |
| `ExaminationRubric` | Defines examination evaluation criteria |
| `ExaminationSlot` | Stores examiner-created examination slots |
| `Booking` | Stores student examination bookings |
| `Evaluation` | Stores overall examination marks and remarks |
| `EvaluationDetail` | Stores marks awarded for individual rubric criteria |

### Relationships

- **User → ExaminerProfile:** One-to-One
- **Course → Examination:** One-to-Many
- **Examination → ExaminationRubric:** One-to-Many
- **Examination → ExaminationSlot:** One-to-Many
- **User (Examiner) → ExaminationSlot:** One-to-Many
- **User (Student) → Booking:** One-to-Many
- **ExaminationSlot → Booking:** One-to-Many
- **Booking → Evaluation:** One-to-One
- **Evaluation → EvaluationDetail:** One-to-Many
- **ExaminationRubric → EvaluationDetail:** One-to-Many

### Status Values

| Entity | Supported statuses |
| --- | --- |
| User | Pending, Approved, Deactivated, Blocked |
| Examination | Draft, Slot Creation, Booking Open, Closed, Completed, Cancelled |
| Slot | Available, Full, Cancelled, Completed |
| Booking | Booked, Cancelled, Completed |

## Project Structure

```text
Examination-Management-Portal/
├── README.md
├── app.py
├── db.py
├── models.py
├── init_db.py
├── seed_data.py
├── requirements.txt
├── config/
│   └── config.py
├── instance/
│   └── exam_portal.db
├── routes/
│   ├── admin_bp.py
│   ├── auth_bp.py
│   ├── examiner_bp.py
│   ├── student_bp.py
│   └── utils.py
├── static/
│   └── css/
└── templates/
    ├── Admin/
    │   ├── bookings.html
    │   ├── courses.html
    │   ├── dashboard.html
    │   ├── dashboard_cards.html
    │   ├── edit_rubric.html
    │   ├── examination.html
    │   ├── examiners.html
    │   ├── history.html
    │   ├── rubrics.html
    │   ├── search.html
    │   ├── sidebar.html
    │   └── students.html
    ├── Examiner/
    │   ├── dashboard.html
    │   ├── dashboard_cards.html
    │   ├── evaluate.html
    │   ├── examinations.html
    │   ├── my_slots.html
    │   ├── sidebar.html
    │   ├── slots.html
    │   └── students.html
    ├── Student/
    │   ├── dashboard.html
    │   ├── dashboard_cards.html
    │   ├── examination_slots.html
    │   ├── examinations.html
    │   ├── overview.html
    │   ├── profile_modal.html
    │   ├── results.html
    │   ├── schedule.html
    │   └── sidebar.html
    └── auth/
        ├── login.html
        └── register.html
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Examination-Management-Portal
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
```

macOS / Linux:

```bash
source venv/bin/activate
```

Windows:

```bat
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

If the application uses environment variables, create a `.env` file in the project root:

```ini
SECRET_KEY=replace_with_a_secure_secret_key
```

Do not commit sensitive configuration values to GitHub.

### 5. Initialize the database

```bash
python3 init_db.py
```

This creates the database tables programmatically from the SQLAlchemy models.

### 6. Insert initial data

If configured to populate initial application data, run:

```bash
python3 seed_data.py
```

The initial Admin account should be created programmatically; Admin registration is not permitted.

### 7. Run the application

```bash
python3 app.py
```

Open `http://127.0.0.1:5000/` in a browser.

> **Note:** Database initialization and seed commands assume that the corresponding scripts contain executable entry points.

## Core Application Rules

1. Only approved examiners can access the examiner dashboard.
2. Examiners can create slots only during the slot creation period.
3. Students can book slots only during the booking period.
4. A slot must never exceed its maximum student capacity.
5. A slot becomes full automatically when its capacity is reached.
6. A student cannot book multiple slots for the same examination.
7. Students can cancel bookings only before the booking deadline.
8. Examiners can evaluate only students booked into their own slots.
9. Students can view only their own examination and booking records.
10. Only published evaluation results should be visible to students.
11. Admin can reschedule bookings and change examiner assignments when necessary.
12. Historical booking and evaluation records should be maintained.

## Security and Data Validation

- Passwords are stored as secure hashes using Werkzeug.
- Role-based access control protects restricted dashboards.
- Unique email addresses prevent duplicate user accounts.
- Database constraints enforce valid roles and statuses.
- Foreign keys maintain relationships between database tables.
- Examination slot capacity is validated before booking.
- Server-side validation is used for important application operations.
- Sensitive configuration values should be stored in environment variables.

## Development Milestones

The project is developed in multiple milestones as part of Modern Application Development I (MAD-I).

| Milestone | Description |
| --- | --- |
| Milestone 0 | GitHub Repository Setup |
| Milestone 1 | Database Models and Schema Setup |
| Milestone 2 | Authentication and Role-Based Access |
| Milestone 3 | Admin Dashboard and Examination Management |
| Milestone 4 | Examiner Dashboard and Slot Management |
| Milestone 5 | Student Dashboard and Slot Booking |
| Milestone 6 | Booking History and Evaluation Tracking |

Each milestone is maintained through Git commits and pushed to the GitHub repository.

## Git Workflow

Use Git and GitHub for version control and milestone tracking.

```bash
# Check working tree status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your milestone commit message"

# Push changes
git push origin main
```

Use separate branches for major features:

```bash
git checkout -b feature/examiner-dashboard
```

After completing a feature:

```bash
git add .
git commit -m "Implement examiner dashboard"
git push origin feature/examiner-dashboard
```

## Future Enhancements

- Advanced examination analytics.
- Improved dashboard visualizations.
- Automated examination notifications.
- Exportable examination reports.
- Enhanced search and filtering.
- Additional examination performance statistics.

## Project Information

| Item | Value |
| --- | --- |
| Project Name | Examination Management Portal (EMP) |
| Course | Modern Application Development I (MAD-I) |
| Backend | Flask |
| Database | SQLite |
| Frontend | HTML, CSS, Bootstrap, and Jinja2 |
| ORM | Flask-SQLAlchemy |
| Execution | Local development environment |

---


