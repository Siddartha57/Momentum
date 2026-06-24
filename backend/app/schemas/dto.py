from datetime import date, time

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    timezone: str = "UTC"
    daily_target_hours: float = Field(default=1, ge=0.25, le=16)
    preferred_study_time: time | None = None


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    timezone: str
    daily_target_hours: float
    preferred_study_time: time | None = None
    email_verified: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    remember_me: bool = False


class GoalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str | None = None
    category: str = "Personal Development"
    start_date: date
    end_date: date
    priority: str = "medium"
    daily_study_time: float = Field(default=1, ge=0.25, le=16)
    weekly_off_day: str = "Sunday"
    difficulty: str = "medium"


class GoalRead(GoalCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    name: str = Field(min_length=2, max_length=180)
    description: str | None = None
    goal_id: int | None = None
    date: date
    start_time: time | None = None
    end_time: time | None = None
    estimated_duration: float = Field(default=1, ge=0.05, le=24)
    notes: str | None = None
    concept: str | None = None

class TaskCompleteRequest(BaseModel):
    attachment_data: str | None = None


class TaskRead(TaskCreate):
    id: int
    status: str
    sort_order: int
    attachment_data: str | None = None

    class Config:
        from_attributes = True


class StudyLogCreate(BaseModel):
    goal_id: int | None = None
    log_date: date
    study_hours: float = Field(default=0, ge=0, le=24)
    work_hours: float = Field(default=0, ge=0, le=24)
    practice_hours: float = Field(default=0, ge=0, le=24)
    tasks_completed: int = Field(default=0, ge=0)
    notes: str | None = None


class JournalCreate(BaseModel):
    entry_date: date
    title: str = Field(min_length=2, max_length=180)
    notes: str
    learnings: str | None = None
    challenges: str | None = None
    tomorrow_plan: str | None = None


class SettingsUpdate(BaseModel):
    theme: str = "dark"
    email_reminders: bool = True
    push_notifications: bool = True
    weekly_summary: bool = True


class GraceDayCreate(BaseModel):
    used_date: date
    reason: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=72)


class AvatarUpdate(BaseModel):
    avatar_url: str


class RoadmapUpdate(BaseModel):
    overview: str
    milestones_json: str

class RoadmapGenerateRequest(BaseModel):
    concepts: list[str]
