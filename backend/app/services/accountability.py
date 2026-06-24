from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import GraceDay, StudyLog, Task, User


def grace_days_remaining(db: Session, user_id: int, today: date | None = None) -> int:
    today = today or date.today()
    used = db.scalar(
        select(func.count(GraceDay.id)).where(
            GraceDay.user_id == user_id,
            func.extract('year', GraceDay.used_date) == today.year,
            func.extract('month', GraceDay.used_date) == today.month,
        )
    )
    return max(3 - int(used or 0), 0)


def accountability_score(db: Session, user: User) -> dict:
    since = date.today() - timedelta(days=29)
    logs = db.scalars(select(StudyLog).where(StudyLog.user_id == user.id, StudyLog.log_date >= since)).all()
    tasks = db.scalars(select(Task).where(Task.user_id == user.id, Task.date >= since)).all()
    days_met = sum(1 for log in logs if log.study_hours + log.practice_hours >= user.daily_target_hours)
    consistency = min(days_met / 30, 1) * 100
    study_hours = min(sum(log.study_hours + log.practice_hours for log in logs) / (user.daily_target_hours * 30), 1) * 100
    completion = 100 if not tasks else (sum(1 for task in tasks if task.status == "completed") / len(tasks)) * 100
    score = round((consistency * 0.4) + (study_hours * 0.3) + (completion * 0.3))
    label = "Excellent" if score >= 90 else "Good" if score >= 70 else "Average" if score >= 50 else "Needs Improvement"
    return {"score": score, "label": label, "consistency": round(consistency), "study_hours": round(study_hours), "task_completion": round(completion)}
