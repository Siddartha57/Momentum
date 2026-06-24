# Momentum — Smart Accountability Platform

A premium goal tracking platform for roadmaps, streaks, grace days, reminders, analytics, journaling, Pomodoro focus, and achievement loops.

## Tech Stack

| Layer     | Technology |
|-----------|-----------|
| Frontend  | React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Recharts |
| Backend   | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database  | SQLite (dev) / PostgreSQL (prod) |
| Auth      | JWT via python-jose, bcrypt password hashing |
| Email     | Gmail SMTP via smtplib + Jinja2 templates |
| Scheduler | APScheduler (background jobs) |
| Deploy    | Frontend → Vercel, Backend → Railway |

## Features

### Authentication & Profile
- Register / Login with JWT tokens
- Forgot Password with email reset link
- Email Verification on registration
- Avatar upload (base64)
- Logout

### Goal & Roadmap Management
- Create goals with category, priority, difficulty, study time, weekly off day
- Auto-generated roadmaps with weekly milestones
- Auto-generated daily task schedules
- Edit / Delete / Pause / Resume / Complete goals
- Edit roadmap milestones

### Task Management
- View tasks by date with filter
- Create / Edit / Delete / Complete tasks
- Auto mark missed tasks (via scheduler)

### Pomodoro Timer
- **25/5 mode** — 25 min work, 5 min break
- **50/10 mode** — 50 min work, 10 min break
- **Custom mode** — configurable work/break durations
- Auto-transition from work to break
- Log study session on completion

### Study Tracker & Analytics
- Log study hours, work hours, practice hours
- 30-day study progress chart (area chart)
- Task completion bar chart
- Accountability score (weighted: consistency 40%, study 30%, tasks 30%)
- 120-day calendar heatmap

### Streak & Grace System
- Daily streak tracking with auto-update
- Grace days (3/month) to protect streaks
- Supported reasons: Health, Travel, Emergency, Family Function, Personal Reason

### Achievement System (Gamification)
- **First Goal** — Create your first goal
- **7 Day Streak** — Maintain 7 consecutive days
- **30 Day Streak** — Maintain 30 consecutive days
- **100 Hours Logged** — Accumulate 100 study hours
- **Goal Completed** — Complete any goal
- **Consistency Champion** — Achieve 90%+ accountability score
- Progress tracking with notification on unlock

### Daily Journal
- Create entries with notes, learnings, challenges, tomorrow's plan
- Browse past entries

### Email Automation
- Welcome email on registration
- Daily task reminders (7:00 AM UTC)
- Streak-at-risk warnings (8:00 PM UTC)
- Weekly accountability summaries

### Notification Center
- In-app notifications for achievements, streak warnings
- Mark as read

### Settings
- Profile card with email verification status
- Theme selection (dark/light)
- Toggle email reminders, push notifications, weekly summary
- Grace day consumption

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Backend runs at http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173

## Deployment

### Backend → Railway (Free Tier)
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Add a PostgreSQL database plugin
4. Connect your GitHub repo (select the `backend` folder as root)
5. Set these environment variables in Railway:
   - `DATABASE_URL` — auto-provided by Railway PostgreSQL plugin
   - `SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_urlsafe(64))"`
   - `ENVIRONMENT` = `production`
   - `FRONTEND_URL` = `https://your-app.vercel.app`
   - `SMTP_HOST` = `smtp.gmail.com`
   - `SMTP_PORT` = `587`
   - `SMTP_USER` = your Gmail
   - `SMTP_PASSWORD` = your app password
   - `SMTP_FROM` = your Gmail
6. Railway will auto-detect the `Dockerfile` and deploy

### Frontend → Vercel (Free Tier)
1. Go to [vercel.com](https://vercel.com) and import your GitHub repo
2. Set root directory to `frontend`
3. Framework preset: Vite
4. Add environment variable:
   - `VITE_API_URL` = `https://your-railway-backend.up.railway.app`
5. Deploy

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login |
| POST | /api/auth/forgot-password | Request password reset |
| POST | /api/auth/reset-password | Reset password with token |
| GET | /api/auth/verify-email | Verify email with token |
| GET | /api/me | Get current user profile |
| PUT | /api/me/avatar | Update avatar |
| POST | /api/goals | Create goal + roadmap |
| GET | /api/goals | List goals |
| PUT | /api/goals/:id | Update goal |
| DELETE | /api/goals/:id | Delete goal |
| PATCH | /api/goals/:id/status | Update goal status |
| GET | /api/roadmaps/:id | Get roadmap |
| PUT | /api/roadmaps/:id | Update roadmap |
| POST | /api/tasks | Create task |
| GET | /api/tasks | List tasks (filter by date) |
| PUT | /api/tasks/:id | Update task |
| DELETE | /api/tasks/:id | Delete task |
| PATCH | /api/tasks/:id/complete | Complete task |
| POST | /api/study-logs | Log study session |
| POST | /api/grace-days | Use a grace day |
| GET | /api/analytics | Get accountability analytics |
| POST | /api/journal | Create journal entry |
| GET | /api/journal | List journal entries |
| GET | /api/achievements | List achievements |
| GET | /api/notifications | List notifications |
| PATCH | /api/notifications/:id/read | Mark notification read |
| GET | /api/settings | Get user settings |
| PUT | /api/settings | Update settings |
| GET | /api/quotes/random | Get random quote |
| GET | /health | Health check |
