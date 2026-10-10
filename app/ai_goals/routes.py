from datetime import date, timedelta

from flask import render_template, flash
from flask_login import login_required, current_user

from app.ai_goals import ai_goals
from app.ai_goals.utils import parse_ai_response
from app.extensions import db
from app.ai.gemini import ask_ai
from app.ai_goals.models import AIGoal
from app.ai_goals.forms import AIGoalForm
from app.ai_goals.prompt_builder import build_goal_prompt

from app.models import Goal, Task


def extract_daily_tasks(value):
    """Convert AI-generated daily tasks into a clean list."""

    if not value:
        return []

    if isinstance(value, list):
        lines = value
    else:
        lines = str(value).splitlines()

    tasks = []

    for line in lines:
        line = str(line).strip()

        if not line:
            continue

        # Remove bullet symbols.
        while line.startswith(("-", "*", "•", "✓")):
            line = line[1:].strip()

        # Remove numbering such as 1. or 2)
        while (
            len(line) > 1
            and line[0].isdigit()
            and line[1] in [".", ")", ":"]
        ):
            line = line[2:].strip()

        if line and line not in tasks:
            tasks.append(line)

    return tasks


@ai_goals.route("/", methods=["GET", "POST"])
@login_required
def index():

    form = AIGoalForm()
    parsed = None
    ai_result = None

    if form.validate_on_submit():

        goal_text = (form.goal.data or "").strip()
        category_text = form.category.data or "Other"
        current_value = (form.current_value.data or "").strip()
        target_value = (form.target_value.data or "").strip()
        notes = (form.notes.data or "").strip()

        if not goal_text:
            flash("Please enter your goal.", "warning")

        else:
            try:
                # ----------------------------------
                # 1. Build the AI prompt
                # ----------------------------------
                prompt = build_goal_prompt(
                    goal=goal_text,
                    category=category_text,
                    current=current_value,
                    target=target_value,
                    notes=notes
                )

                # ----------------------------------
                # 2. Generate the AI response
                # ----------------------------------
                ai_result = ask_ai(prompt)

                if not ai_result or not str(ai_result).strip():
                    raise ValueError(
                        "The AI returned an empty response. Please try again."
                    )

                # ----------------------------------
                # 3. Parse the AI response
                # ----------------------------------
                parsed = parse_ai_response(ai_result)

                if not isinstance(parsed, dict):
                    parsed = {}

                # Preserve the raw response if parsing
                # doesn't return the expected fields.
                if not parsed:
                    parsed = {
                        "AI Plan": str(ai_result)
                    }

                # Read estimated duration safely.
                try:
                    estimated_days = int(
                        parsed.get("Estimated Days", 0) or 0
                    )
                except (TypeError, ValueError):
                    estimated_days = 0

                estimated_days = max(0, estimated_days)

                # Read plan sections.
                daily_tasks_value = parsed.get(
                    "Daily Tasks",
                    parsed.get("Daily Plan", "")
                )

                weekly_goal_value = parsed.get(
                    "Weekly Target",
                    parsed.get("Weekly Goal", "")
                )

                diet_plan_value = parsed.get("Diet Plan", "")
                water_intake_value = parsed.get("Water Intake", "")
                workout_plan_value = parsed.get("Workout Plan", "")

                motivation_value = parsed.get(
                    "Motivation",
                    parsed.get("Conclusion", "")
                )

                # ----------------------------------
                # 4. Save the AI Goal Coach plan
                # ----------------------------------
                ai_goal = AIGoal(
                    user_id=current_user.id,
                    goal=goal_text,
                    category=category_text,
                    current_value=current_value,
                    target_value=target_value,
                    estimated_days=estimated_days,
                    progress=0,
                    completed=False,
                    ai_response=str(ai_result),
                    daily_tasks=(
                        "\n".join(daily_tasks_value)
                        if isinstance(daily_tasks_value, list)
                        else str(daily_tasks_value or "")
                    ),
                    weekly_goal=(
                        "\n".join(weekly_goal_value)
                        if isinstance(weekly_goal_value, list)
                        else str(weekly_goal_value or "")
                    ),
                    diet_plan=str(diet_plan_value or ""),
                    water_intake=str(water_intake_value or ""),
                    workout_plan=str(workout_plan_value or ""),
                    motivation=str(motivation_value or "")
                )

                db.session.add(ai_goal)

                # ----------------------------------
                # 5. Save the goal in the existing
                #    Goals module
                # ----------------------------------
                existing_goal = Goal(
                    title=goal_text,
                    description=str(motivation_value or ""),
                    completed=False,
                    user_id=current_user.id
                )

                if estimated_days > 0:
                    existing_goal.target_date = (
                        date.today()
                        + timedelta(days=estimated_days)
                    )

                db.session.add(existing_goal)

                # Generate the Goal ID before creating tasks.
                db.session.flush()

                # ----------------------------------
                # 6. Save AI-generated tasks
                # ----------------------------------
                daily_tasks = extract_daily_tasks(
                    daily_tasks_value
                )

                for task_title in daily_tasks:

                    task = Task(
                    title=task_title[:200],
                    description=f"AI-generated task for: {goal_text}",
                    priority="Medium",
                    completed=False,
                    user_id=current_user.id
                    )
                    db.session.add(task)
                # ----------------------------------
                # 7. Save all records together
                # ----------------------------------
                db.session.commit()

                flash(
                    "Your AI plan has been generated successfully!",
                    "success"
                )

            except Exception as e:
                db.session.rollback()

                print("AI GOAL ERROR:", repr(e))

                flash(
                    f"Unable to generate the AI plan: {str(e)}",
                    "danger"
                )

    # ----------------------------------
    # 8. Load existing Goals
    # ----------------------------------
    goals = Goal.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Goal.id.desc()
    ).all()

    total_goals = len(goals)

    completed_goals = Goal.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    latest_goal = goals[0] if goals else None

    progress = (
        100 if latest_goal and latest_goal.completed else 0
    )

    # ----------------------------------
    # 9. Render the page
    # ----------------------------------
    return render_template(
        "ai_goals/index.html",
        form=form,
        parsed=parsed,
        ai_result=ai_result,
        goals=goals,
        total_goals=total_goals,
        ai_plans=total_goals,
        completed_goals=completed_goals,
        progress=progress
    )