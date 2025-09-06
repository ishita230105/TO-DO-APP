from datetime import date, datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
# Ensure instance folder exists (SQLite will be stored here)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(Path(app.instance_path) / "todo.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    priority = db.Column(db.Integer, default=3)  # 1-10
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def status_tag(self):
        if self.completed:
            return "Completed"
        if self.due_date:
            today = date.today()
            if self.due_date < today:
                return "Overdue"
            if self.due_date == today:
                return "Today"
        return "Upcoming"

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()
    filter_ = request.args.get("filter", "all")
    sort = request.args.get("sort", "created")

    tasks = Task.query

    if q:
        tasks = tasks.filter(Task.title.ilike(f"%{q}%"))

    if filter_ == "today":
        tasks = tasks.filter(Task.completed == False, Task.due_date == date.today())  # noqa: E712
    elif filter_ == "overdue":
        tasks = tasks.filter(Task.completed == False, Task.due_date < date.today())   # noqa: E712
    elif filter_ == "completed":
        tasks = tasks.filter(Task.completed.is_(True))

    if sort == "due":
        tasks = tasks.order_by(Task.due_date.is_(None), Task.due_date.asc())
    elif sort == "priority":
        tasks = tasks.order_by(Task.priority.desc(), Task.created_at.desc())
    else:
        tasks = tasks.order_by(Task.created_at.desc())

    tasks = tasks.all()

    total = Task.query.count()
    done = Task.query.filter_by(completed=True).count()
    pct = int((done / total) * 100) if total else 0

    return render_template("index.html",
                           tasks=tasks, q=q, filter_=filter_, sort=sort,
                           progress_pct=pct)

@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "3").strip()
    due = request.form.get("due_date", "").strip()
    if not title:
        return redirect(url_for("index"))

    try:
        priority = max(1, min(10, int(priority)))
    except ValueError:
        priority = 3

    due_date = None
    if due:
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            pass

    db.session.add(Task(title=title, priority=priority, due_date=due_date))
    db.session.commit()
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify({"ok": True, "completed": task.completed})

@app.post("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"ok": True})

@app.post("/edit/<int:task_id>")
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "").strip()
    due = request.form.get("due_date", "").strip()

    if title:
        task.title = title
    if priority:
        try:
            task.priority = max(1, min(10, int(priority)))
        except ValueError:
            pass
    if due:
        try:
            task.due_date = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            task.due_date = None
    elif due == "":
        task.due_date = None

    db.session.commit()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)