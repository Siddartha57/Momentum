import json
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models import Goal, Roadmap, Task


def generate_roadmap(db: Session, goal: Goal) -> Roadmap:
    days = max((goal.end_date - goal.start_date).days + 1, 1)
    active_days = [
        goal.start_date + timedelta(days=offset)
        for offset in range(days)
        if (goal.start_date + timedelta(days=offset)).strftime("%A") != goal.weekly_off_day
    ]
    weeks = max((len(active_days) + 6) // 7, 1)
    milestones = [
        {"week": week, "title": f"Week {week} milestone", "focus": f"Build momentum for {goal.name}"}
        for week in range(1, weeks + 1)
    ]
    roadmap = Roadmap(
        goal_id=goal.id,
        overview=f"{goal.name} is divided into {weeks} weekly milestones across {len(active_days)} active days.",
        milestones_json=json.dumps(milestones),
    )
    db.add(roadmap)
    for index, task_date in enumerate(active_days, start=1):
        db.add(
            Task(
                user_id=goal.user_id,
                goal_id=goal.id,
                name=f"{goal.name}: focused session {index}",
                description=f"Complete a {goal.daily_study_time:g} hour {goal.difficulty} practice block.",
                date=task_date,
                estimated_duration=goal.daily_study_time,
                sort_order=index,
            )
        )
    db.commit()
    db.refresh(roadmap)
    return roadmap
