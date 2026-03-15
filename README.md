# QuizAI Backend — FastAPI

AI-powered quiz platform for Indian students. Fully async Python backend.

---

## 📁 Project Structure

```
quizai-backend/
├── main.py                        # FastAPI app + lifespan
├── requirements.txt
├── .env.example                   # Copy to .env and fill values
│
├── db/
│   └── database.py                # Async SQLAlchemy engine + session
│
├── models/
│   └── models.py                  # User, Score, DailyQuiz ORM models
│
├── routers/
│   ├── auth.py                    # POST /auth/signup, /auth/login, GET /auth/me
│   ├── quiz.py                    # POST /quiz/generate
│   ├── scores.py                  # POST /scores/save, GET /scores/history, /scores/stats
│   └── daily.py                   # GET /daily/today, POST /daily/submit
│
└── services/
    ├── anthropic_service.py       # Server-side Anthropic API call (API key safe here)
    ├── auth_service.py            # JWT create/decode, bcrypt, DB helpers
    └── scheduler_service.py       # APScheduler — daily quiz at 7 AM IST
```

---

## ⚡ Setup

```bash
# 1. Clone and enter directory
cd quizai-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY and SECRET_KEY

# 5. Run server
uvicorn main:app --reload --port 8000
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (never expose to frontend) |
| `SECRET_KEY` | Random string for JWT signing |
| `ALGORITHM` | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry (default: 10080 = 7 days) |
| `DATABASE_URL` | SQLite by default, swap for PostgreSQL in prod |
| `CORS_ORIGINS` | Comma-separated frontend URLs |

---

## 📡 API Endpoints

### Auth
| Method | URL | Description |
|---|---|---|
| POST | `/auth/signup` | Register new user |
| POST | `/auth/login` | Login → get JWT token |
| GET | `/auth/me` | Get current user info |

### Quiz
| Method | URL | Description |
|---|---|---|
| POST | `/quiz/generate` | Generate 5 AI questions (authenticated) |

**Request body:**
```json
{ "topic": "Science", "difficulty": "Medium" }
```

### Scores
| Method | URL | Description |
|---|---|---|
| POST | `/scores/save` | Save quiz result |
| GET | `/scores/history` | Get score history (filter by topic) |
| GET | `/scores/stats` | Get stats (avg %, best %, favourite topic) |

### Daily Quiz
| Method | URL | Description |
|---|---|---|
| GET | `/daily/today` | Get today's scheduled quiz |
| POST | `/daily/submit` | Submit daily quiz score |

---

## 🗄️ Database

- Default: **SQLite** (zero config, good for dev)
- Production: Change `DATABASE_URL` to PostgreSQL:
  ```
  DATABASE_URL=postgresql+asyncpg://user:pass@localhost/quizai
  pip install asyncpg
  ```

---

## 📅 Scheduler

- Runs at **7:00 AM IST** every day
- Picks a random topic + difficulty
- Generates quiz for all active users
- Uses APScheduler with AsyncIOScheduler

---

## 🔐 Security Notes

- **API key** is only in `.env`, never sent to frontend
- Passwords hashed with **bcrypt**
- JWT tokens expire in 7 days (configurable)
- CORS restricted to `CORS_ORIGINS`

---

## 🌐 Frontend Integration

Update your React app to call backend instead of Anthropic directly:

```js
// Instead of calling Anthropic directly:
const res = await fetch("http://localhost:8000/quiz/generate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`   // JWT from login
  },
  body: JSON.stringify({ topic, difficulty })
});
const data = await res.json();
const questions = data.questions;
```

---

## 🚀 Production Deployment

- Use **PostgreSQL** instead of SQLite
- Set `APP_ENV=production`
- Deploy on **Railway / Render / AWS EC2**
- Use **gunicorn** with uvicorn workers:
  ```bash
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
  ```
