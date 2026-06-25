# AssignmentAssessor: Smart Academic Planner

## Video Demo

## Description

AssignmentAssessor is a desktop application built with **Python**, **CustomTkinter**, and **PostgreSQL** that helps students organize coursework, prioritize assignments, and generate personalized study plans. The application provides a graphical user interface where users can securely create an account, manage assignments, and view recommendations based on workload and upcoming deadlines.

Unlike a traditional to-do list, AssignmentAssessor evaluates each assignment using a custom priority algorithm that considers assignment difficulty, estimated completion time, and the number of days remaining before the due date. This allows students to focus on the assignments that require the most attention first.

The application follows a layered architecture that separates the graphical interface from the business logic and database operations. Authentication, task management, validation, and database queries are organized into separate modules, making the project easier to maintain and expand.

---

## User Accounts

AssignmentAssessor supports multiple users through PostgreSQL.

Users can:

* Register a new account with a securely hashed password
* Log in to an existing account
* Maintain their own independent assignment list

Passwords are hashed before being stored in the database, ensuring that plaintext passwords are never saved.

---

## Adding Assignments

Users can create both incomplete and completed assignments.

For incomplete assignments, the application records:

* Course name
* Assignment name
* Difficulty (1–5)
* Estimated hours required
* Due date

For completed assignments, the application records:

* Course name
* Assignment name
* Difficulty (1–5)
* Hours used
* Date completed

Extensive validation ensures that all user input is properly formatted before it is written to the database.

---

## Viewing Assignments

Assignments are displayed alphabetically and clearly indicate whether they are completed or incomplete.

Incomplete assignments automatically display if they are overdue, while completed assignments display the date they were finished.

---

## Editing and Deleting Assignments

Users can modify existing assignments through the graphical interface.

Assignments may be:

* Updated
* Marked as completed or incomplete
* Deleted

All changes are immediately synchronized with the PostgreSQL database using CRUD operations.

---

## Priority Calculation

AssignmentAssessor prioritizes incomplete assignments using the following formula:

Priority = (Difficulty × Estimated Hours) / Days Remaining

Assignments with higher priority scores appear before less urgent assignments. Overdue assignments are automatically placed at the top of the priority list.

---

## Study Plan Generation

The application generates personalized study recommendations based on assignment priority.

For each incomplete assignment, AssignmentAssessor calculates:

Hours Per Day = Estimated Hours / Days Remaining

This helps students distribute their workload more effectively while ensuring that approaching deadlines receive the most attention.

---

## Database Design

AssignmentAssessor uses PostgreSQL as its persistent data store.

The project implements full CRUD functionality through dedicated query modules:

* Create users and assignments
* Retrieve user-specific assignments
* Update assignment information
* Delete assignments

Database access is separated from the GUI using dedicated `user_queries.py` and `task_queries.py` modules.

---

## Testing

The project includes automated tests using **pytest**.

Tests verify important application logic including:

* Difficulty validation
* Numeric input validation
* Due date validation
* Completion date validation
* Priority calculations
* Study plan calculations

These tests help ensure that AssignmentAssessor behaves correctly as new features are added.

---

## Technologies Used

* Python
* CustomTkinter
* PostgreSQL
* Psycopg
* python-dotenv
* pytest

---

## Future Improvements

Future versions of AssignmentAssessor may include:

* Assignment categories and tags
* GPA and grade tracking
* Calendar integration
* Email or desktop reminders
* Study history analytics
* Data visualizations showing workload over time
* Cloud synchronization across devices
