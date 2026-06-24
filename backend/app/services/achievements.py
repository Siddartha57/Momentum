from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Achievement, Goal, Notification, Streak, StudyLog, Task, User
from app.services.accountability import accountability_score


BADGE_DEFINITIONS = [
    {"code": "first_goal", "title": "First Goal", "check": "goals_created", "threshold": 1},
    {"code": "streak_7", "title": "7 Day Streak", "check": "current_streak", "threshold": 7},
    {"code": "streak_30", "title": "30 Day Streak", "check": "current_streak", "threshold": 30},
    {"code": "hours_100", "title": "100 Hours Logged", "check": "total_hours", "threshold": 100},
    {"code": "goal_completed", "title": "Goal Completed", "check": "goals_completed", "threshold": 1},
    {"code": "consistency_champion", "title": "Consistency Champion", "check": "acc_score", "threshold": 90},
]


def _get_metric(db: Session, user_id: int, metric: str) -> float:
    if metric == "goals_created":
        return db.scalar(select(func.count(Goal.id)).where(Goal.user_id == user_id)) or 0
    if metric == "current_streak":
        streak = db.scalar(select(Streak).where(Streak.user_id == user_id))
        return streak.current_streak if streak else 0
    if metric == "total_hours":
        result = db.scalar(
            select(func.sum(StudyLog.study_hours + StudyLog.practice_hours)).where(
                StudyLog.user_id == user_id
            )
        )
        return float(result or 0)
    if metric == "goals_completed":
        return db.scalar(
            select(func.count(Goal.id)).where(Goal.user_id == user_id, Goal.status == "completed")
        ) or 0
    if metric == "acc_score":
        user = db.scalar(select(User).where(User.id == user_id))
        if not user:
            return 0
        score_data = accountability_score(db, user)
        return score_data.get("score", 0)
    return 0


def check_and_award(db: Session, user_id: int) -> None:
    for badge in BADGE_DEFINITIONS:
        current_value = _get_metric(db, user_id, badge["check"])
        progress = min((current_value / badge["threshold"]) * 100, 100)

        existing = db.scalar(
            select(Achievement).where(
                Achievement.user_id == user_id, Achievement.code == badge["code"]
            )
        )

        if existing:
            if existing.unlocked_at:
                continue
            existing.progress = progress
            if progress >= 100:
                existing.unlocked_at = datetime.utcnow()
                db.add(
                    Notification(
                        user_id=user_id,
                        kind="achievement",
                        title=f"Achievement Unlocked: {badge['title']}!",
                        message=f"Congratulations! You earned the '{badge['title']}' badge.",
                    )
                )
        else:
            achievement = Achievement(
                user_id=user_id,
                code=badge["code"],
                title=badge["title"],
                progress=progress,
                unlocked_at=datetime.utcnow() if progress >= 100 else None,
            )
            db.add(achievement)
            if progress >= 100:
                db.add(
                    Notification(
                        user_id=user_id,
                        kind="achievement",
                        title=f"Achievement Unlocked: {badge['title']}!",
                        message=f"Congratulations! You earned the '{badge['title']}' badge.",
                    )
                )

    db.flush()
