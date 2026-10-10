from flask import render_template
from flask_login import login_required, current_user
from app.utils.weather import get_weather
from . import dashboard
from app.models import Note, Task
from flask import render_template, request, jsonify
from datetime import datetime
from app.models import Goal
from app.utils.weather import get_weather
@dashboard.route("/")
@login_required
def home():

    total_notes = Note.query.filter_by(
        user_id=current_user.id
    ).count()

    total_tasks = Task.query.filter_by(
        user_id=current_user.id
    ).count()

    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    pending_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).count()

    recent_notes = (
        Note.query
        .filter_by(user_id=current_user.id)
        .order_by(Note.created_at.desc())
        .limit(5)
        .all()
    )

    recent_tasks = (
        Task.query
        .filter_by(user_id=current_user.id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )

    if total_tasks > 0:
        progress = int(
            (completed_tasks / total_tasks) * 100
        )
    else:
        progress = 0

    high_priority_tasks = (
        Task.query.filter_by(
            user_id=current_user.id,
            priority="High",
            completed=False
        )
        .limit(5)
        .all()
    )
    total_goals = Goal.query.filter_by(
        user_id=current_user.id
    ).count()
    
    completed_goals = Goal.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()
    
    if total_goals > 0:
        goal_progress = int(
            (completed_goals / total_goals) * 100
        )
    else:
        goal_progress = 0
    
    
    
    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "🌅 Good Morning"
    elif current_hour < 17:
        greeting = "☀️ Good Afternoon"
    else:
        greeting = "🌙 Good Evening"
    # -----------------------------
# AI Suggestions
# -----------------------------

    suggestions = []

    if pending_tasks > 0:
        suggestions.append(
            f"📌 You have {pending_tasks} pending tasks."
        )
    
    if progress < 70:
        suggestions.append(
            "🎯 Complete more tasks to increase your productivity."
        )
    
    if total_notes < 5:
        suggestions.append(
            "📝 Add more notes to organize your work."
        )
    
    if not suggestions:
        suggestions.append(
            "✅ Excellent! Everything is on track."
        )
    return render_template(
    "dashboard/index.html",
    total_notes=total_notes,
    total_tasks=total_tasks,
    completed_tasks=completed_tasks,
    pending_tasks=pending_tasks,
    recent_notes=recent_notes,
    recent_tasks=recent_tasks,
    high_priority_tasks=high_priority_tasks,
    progress=progress,
    suggestions=suggestions,
    goal_progress=goal_progress,
    weather=None
)
@dashboard.route("/weather", methods=["POST"])
@login_required
def weather():
    try:
        data = request.get_json(force=True)

        lat = data.get("lat")
        lon = data.get("lon")

        print("Latitude :", lat)
        print("Longitude:", lon)

        weather = get_weather(lat, lon)

        if weather is None:
            return jsonify({
                "success": False,
                "message": "Unable to fetch weather"
            }), 500

        return jsonify({
            "success": True,
            "weather": weather
        })

    except Exception as e:
        import traceback
        traceback.print_exc()   # <-- Complete error terminal lo print avutundi

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500