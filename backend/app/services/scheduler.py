from datetime import date, datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func, select

from app.core.database import SessionLocal
from app.models import GraceDay, Notification, Streak, StudyLog, Task, User, UserSettings
from app.services.achievements import check_and_award
from app.services.email import send_email


def _check_missed_tasks():
    """Runs every 15 min. Marks tasks as 'missed' if their date has passed and they are still pending."""
    db = SessionLocal()
    try:
        yesterday = date.today() - timedelta(days=1)
        tasks = db.scalars(
            select(Task).where(Task.date <= yesterday, Task.status == "pending")
        ).all()
        for task in tasks:
            task.status = "missed"
        db.commit()
    finally:
        db.close()


def _update_streaks():
    """Runs daily at midnight UTC. Updates streak counts based on study logs."""
    db = SessionLocal()
    try:
        users = db.scalars(select(User)).all()
        yesterday = date.today() - timedelta(days=1)
        for user in users:
            streak = db.scalar(select(Streak).where(Streak.user_id == user.id))
            if not streak:
                streak = Streak(user_id=user.id)
                db.add(streak)
                db.flush()

            log = db.scalar(
                select(StudyLog).where(
                    StudyLog.user_id == user.id, StudyLog.log_date == yesterday
                )
            )
            if log and (log.study_hours + log.practice_hours) >= user.daily_target_hours:
                streak.current_streak += 1
                streak.total_completed_days += 1
                streak.last_completed_date = yesterday
                if streak.current_streak > streak.longest_streak:
                    streak.longest_streak = streak.current_streak
            else:
                grace = db.scalar(
                    select(GraceDay).where(
                        GraceDay.user_id == user.id, GraceDay.used_date == yesterday
                    )
                )
                if not grace:
                    streak.current_streak = 0

            check_and_award(db, user.id)
        db.commit()
    finally:
        db.close()


def _send_daily_reminders():
    """Runs daily at 7:00 AM UTC. Sends email reminders about today's tasks."""
    db = SessionLocal()
    try:
        today = date.today()
        users = db.scalars(select(User)).all()
        for user in users:
            settings = db.scalar(
                select(UserSettings).where(UserSettings.user_id == user.id)
            )
            if not settings or not settings.email_reminders:
                continue
            task_count = (
                db.scalar(
                    select(func.count(Task.id)).where(
                        Task.user_id == user.id,
                        Task.date == today,
                        Task.status == "pending",
                    )
                )
                or 0
            )
            if task_count > 0:
                send_email(
                    user.email,
                    f"Momentum: You have {task_count} tasks today",
                    "daily_reminder.html",
                    {
                        "name": user.full_name,
                        "task_count": task_count,
                        "year": datetime.utcnow().year,
                    },
                )
    finally:
        db.close()


def _send_streak_warnings():
    """Runs daily at 8:00 PM UTC. Warns users at risk of losing their streak."""
    db = SessionLocal()
    try:
        today = date.today()
        users = db.scalars(select(User)).all()
        for user in users:
            streak = db.scalar(select(Streak).where(Streak.user_id == user.id))
            if not streak or streak.current_streak < 3:
                continue
            log = db.scalar(
                select(StudyLog).where(
                    StudyLog.user_id == user.id, StudyLog.log_date == today
                )
            )
            if not log:
                db.add(
                    Notification(
                        user_id=user.id,
                        kind="streak_warning",
                        title="Streak at Risk!",
                        message=f"You have a {streak.current_streak}-day streak. Log your study hours today to keep it alive!",
                    )
                )
        db.commit()
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(
        _check_missed_tasks,
        "interval",
        minutes=15,
        id="check-missed",
        replace_existing=True,
    )
    scheduler.add_job(
        _update_streaks,
        "cron",
        hour=0,
        minute=5,
        id="update-streaks",
        replace_existing=True,
    )
    scheduler.add_job(
        _send_daily_reminders,
        "cron",
        hour=7,
        minute=0,
        id="daily-reminders",
        replace_existing=True,
    )
    scheduler.add_job(
        _send_streak_warnings,
        "cron",
        hour=20,
        minute=0,
        id="streak-warnings",
        replace_existing=True,
    )
    scheduler.start()
    return scheduler
