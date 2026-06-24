from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Achievement, Goal, GraceDay, JournalEntry, Notification, Streak, StudyLog, Task, User, UserSettings,Roadmap
from app.schemas import (
    AvatarUpdate,
    ForgotPasswordRequest,
    GoalCreate,
    GoalCreate,
    GoalRead,
    GraceDayCreate,
    JournalCreate,
    LoginRequest,
    ResetPasswordRequest,
    RoadmapUpdate,
    RoadmapGenerateRequest,
    SettingsUpdate,
    StudyLogCreate,
    TaskCreate,
    TaskCompleteRequest,
    TaskRead,
    Token,
    UserCreate,
    UserRead,
)
from app.services.accountability import accountability_score, grace_days_remaining
from app.services.achievements import check_and_award
from app.services.email import send_email
from app.services.roadmap import generate_roadmap
from app.core.config import settings

router = APIRouter(prefix="/api")


@router.post("/auth/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> Token:
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        timezone=payload.timezone,
        daily_target_hours=payload.daily_target_hours,
        preferred_study_time=payload.preferred_study_time,
    )
    db.add(user)
    db.flush()
    db.add(UserSettings(user_id=user.id))
    db.commit()

    # Send verification email
    verify_token = create_access_token(user.email, minutes=1440)
    verify_link = f"{settings.frontend_url}/verify-email?token={verify_token}"
    send_email(user.email, "Verify your Momentum account", "verify_email.html", {"name": user.full_name, "verify_link": verify_link})

    return Token(access_token=create_access_token(user.email))


@router.post("/auth/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)) -> dict:
    user = db.scalar(select(User).where(User.email == payload.email))
    if user:
        reset_token = create_access_token(user.email, minutes=60)
        reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"
        send_email(user.email, "Reset your Momentum password", "reset_password.html", {"name": user.full_name, "reset_link": reset_link})
    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/auth/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)) -> dict:
    from app.core.security import decode_token
    email = decode_token(payload.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password has been reset successfully."}


@router.get("/auth/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)) -> dict:
    from app.core.security import decode_token
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email_verified = True
    db.commit()
    return {"message": "Email verified successfully."}


@router.post("/auth/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    minutes = 60 * 24 * 30 if payload.remember_me else None
    return Token(access_token=create_access_token(user.email, minutes))


@router.get("/me", response_model=UserRead)
def me(user: Annotated[User, Depends(current_user)]) -> User:
    return user

from pydantic import BaseModel
class UserUpdate(BaseModel):
    full_name: str | None = None
    daily_target_hours: float | None = None

@router.put("/me", response_model=UserRead)
def update_me(payload: UserUpdate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)):
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.daily_target_hours is not None:
        user.daily_target_hours = payload.daily_target_hours
    db.commit()
    return user



@router.put("/me/avatar")
def update_avatar(payload: AvatarUpdate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    user.avatar_url = payload.avatar_url
    db.commit()
    return {"avatar_url": user.avatar_url}


@router.post("/goals", response_model=GoalRead)
def create_goal(payload: GoalCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> Goal:
    goal = Goal(user_id=user.id, **payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    check_and_award(db, user.id)
    return goal

@router.post("/goals/{goal_id}/roadmap")
def create_roadmap_manual(goal_id: int, payload: RoadmapGenerateRequest, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    import json
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    milestones = [
        {"week": index + 1, "title": f"Concept: {concept}", "focus": concept}
        for index, concept in enumerate(payload.concepts)
    ]
    roadmap = Roadmap(
        goal_id=goal.id,
        overview=f"Roadmap mapped into {len(payload.concepts)} core concepts.",
        milestones_json=json.dumps(milestones),
    )
    db.add(roadmap)
    db.commit()
    return {"status": "roadmap_created"}


@router.get("/goals", response_model=list[GoalRead])
def list_goals(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db), status_filter: str | None = Query(None)) -> list[Goal]:
    stmt = select(Goal).where(Goal.user_id == user.id)
    if status_filter:
        stmt = stmt.where(Goal.status == status_filter)
    return list(db.scalars(stmt.order_by(Goal.created_at.desc())).all())


@router.put("/goals/{goal_id}", response_model=GoalRead)
def update_goal(goal_id: int, payload: GoalCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> Goal:
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in payload.model_dump().items():
        setattr(goal, k, v)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/goals/{goal_id}")
def delete_goal(goal_id: int, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(goal)
    db.commit()
    return {"status": "deleted"}


@router.patch("/goals/{goal_id}/status")
def update_goal_status(goal_id: int, status_value: str, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal.status = status_value
    db.commit()
    return {"status": goal.status}


@router.get("/roadmaps/{goal_id}")
def get_roadmap(goal_id: int, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal or not goal.roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return {"overview": goal.roadmap.overview, "milestones": goal.roadmap.milestones_json}


@router.put("/roadmaps/{goal_id}")
def update_roadmap(goal_id: int, payload: RoadmapUpdate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    goal = db.scalar(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    if not goal or not goal.roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    goal.roadmap.overview = payload.overview
    goal.roadmap.milestones_json = payload.milestones_json
    db.commit()
    return {"overview": goal.roadmap.overview, "milestones": goal.roadmap.milestones_json}


@router.post("/tasks")
def create_task(payload: TaskCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    task = Task(user_id=user.id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status}


@router.get("/tasks")
def list_tasks(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db), day: date | None = None, q: str | None = None) -> list[dict]:
    stmt = select(Task).where(Task.user_id == user.id)
    if day:
        stmt = stmt.where(Task.date == day)
    if q:
        stmt = stmt.where(Task.name.ilike(f"%{q}%"))
    tasks = db.scalars(stmt.order_by(Task.date, Task.sort_order)).all()
    return [{"id": t.id, "name": t.name, "date": t.date, "status": t.status, "estimated_duration": t.estimated_duration, "notes": t.notes, "concept": t.concept, "attachment_data": t.attachment_data} for t in tasks]


@router.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for k, v in payload.model_dump().items():
        setattr(task, k, v)
    db.commit()
    return {"id": task.id, "status": task.status}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "deleted"}


@router.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, payload: TaskCompleteRequest, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    task = db.scalar(select(Task).where(Task.id == task_id, Task.user_id == user.id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "completed"
    if payload.attachment_data:
        task.attachment_data = payload.attachment_data
    db.commit()
    return {"status": task.status}


@router.post("/study-logs")
def create_study_log(payload: StudyLogCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    log = StudyLog(user_id=user.id, **payload.model_dump())
    db.add(log)
    db.commit()
    check_and_award(db, user.id)
    return {"id": log.id}


@router.post("/grace-days")
def use_grace_day(payload: GraceDayCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    allowed = {"Health", "Travel", "Emergency", "Family Function", "Personal Reason"}
    if payload.reason not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported grace day reason")
    if grace_days_remaining(db, user.id, payload.used_date) <= 0:
        raise HTTPException(status_code=400, detail="No grace days remaining this month")
    db.add(GraceDay(user_id=user.id, **payload.model_dump()))
    db.commit()
    return {"remaining": grace_days_remaining(db, user.id, payload.used_date)}


@router.get("/analytics")
def analytics(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    logs = db.scalars(select(StudyLog).where(StudyLog.user_id == user.id).order_by(StudyLog.log_date)).all()
    tasks_total = db.scalar(select(func.count(Task.id)).where(Task.user_id == user.id)) or 0
    tasks_done = db.scalar(select(func.count(Task.id)).where(Task.user_id == user.id, Task.status == "completed")) or 0
    streak = db.scalar(select(Streak).where(Streak.user_id == user.id))
    return {
        "accountability": accountability_score(db, user),
        "grace_days_remaining": grace_days_remaining(db, user.id),
        "streak": {"current": streak.current_streak if streak else 0, "longest": streak.longest_streak if streak else 0},
        "daily_study_hours": [{"date": log.log_date.isoformat(), "hours": log.study_hours + log.practice_hours} for log in logs[-30:]],
        "task_completion": round((tasks_done / tasks_total) * 100) if tasks_total else 0,
    }


@router.post("/journal")
def create_journal(payload: JournalCreate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    entry = JournalEntry(user_id=user.id, **payload.model_dump())
    db.add(entry)
    db.commit()
    return {"id": entry.id}


@router.get("/journal")
def list_journal(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db), q: str | None = None) -> list[dict]:
    stmt = select(JournalEntry).where(JournalEntry.user_id == user.id)
    if q:
        stmt = stmt.where(JournalEntry.title.ilike(f"%{q}%"))
    entries = db.scalars(stmt.order_by(JournalEntry.entry_date.desc())).all()
    return [{"id": e.id, "date": e.entry_date, "title": e.title, "notes": e.notes, "learnings": e.learnings, "challenges": e.challenges, "tomorrow_plan": e.tomorrow_plan} for e in entries]


@router.get("/achievements")
def achievements(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(Achievement).where(Achievement.user_id == user.id)).all()
    return [{"code": row.code, "title": row.title, "progress": row.progress, "unlocked_at": row.unlocked_at} for row in rows]


@router.get("/notifications")
def notifications(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())).all()
    return [{"id": row.id, "kind": row.kind, "title": row.title, "message": row.message, "read": row.read} for row in rows]


@router.patch("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    row = db.scalar(select(Notification).where(Notification.id == notification_id, Notification.user_id == user.id))
    if not row:
        raise HTTPException(status_code=404, detail="Notification not found")
    row.read = True
    db.commit()
    return {"read": True}


@router.get("/settings")
def get_settings(user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    row = db.scalar(select(UserSettings).where(UserSettings.user_id == user.id))
    return {"theme": row.theme, "email_reminders": row.email_reminders, "push_notifications": row.push_notifications, "weekly_summary": row.weekly_summary}


@router.put("/settings")
def update_settings(payload: SettingsUpdate, user: Annotated[User, Depends(current_user)], db: Session = Depends(get_db)) -> dict:
    row = db.scalar(select(UserSettings).where(UserSettings.user_id == user.id))
    for key, value in payload.model_dump().items():
        setattr(row, key, value)
    db.commit()
    return payload.model_dump()


@router.get("/quotes/random")
def quote() -> dict:
    quotes = [
        "Small promises kept daily become identity.",
        "Consistency is quieter than motivation and far more durable.",
        "Protect the session. The score will follow.",
    ]
    return {"quote": quotes[datetime.utcnow().day % len(quotes)]}
