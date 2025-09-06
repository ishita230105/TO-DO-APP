To-Do App

A simple and beautiful task manager built with Flask, SQLite, and Bootstrap.
Easily add, edit, delete, and track your tasks with priorities and due dates.

Features:

- Add, edit, delete, and complete tasks

- Priority levels (1–10) with color badges

- Due dates with Overdue / Today / Upcoming status

- Search, filter, and sort tasks

- Progress tracking with a completion bar

- Responsive and mobile-friendly

Tech Stack:

- Backend: Python (Flask)

- Database: SQLite

- Frontend: HTML, CSS, JS (Bootstrap 5)

Installation

Clone the repository:

git clone <repo-url>
cd todoapp


Create & activate virtual environment:

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the app:

python app.py

Open in browser:
http://127.0.0.1:5000

📂 Project Structure
todoapp/
├── app.py       
├── requirements.txt
├── templates/      
├── static/    
└── instance/   

Usage:

Add Task → Enter title, priority, and optional due date

Manage Tasks → Mark complete, edit, or delete

Search & Filter → Find tasks quickly

Status → Tasks are auto-tagged as Today, Overdue, Upcoming
