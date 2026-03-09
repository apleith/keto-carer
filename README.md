# keto-carer

A self-hosted, AI-assisted keto diet management app for personal use. No subscriptions. Runs on your dev computer, accessible on your home network.

## Features

- **Multi-user profiles** — up to 4 users, each with personalized macro goals and preferences
- **Meal planning** — AI-suggested meals based on per-user ingredient ratings (1–10 scale)
- **Grocery lists** — auto-generated from meal plans
- **Macro & nutrition tracking** — per meal/snack/beverage via USDA FoodData Central
- **Medication & supplement tracking** — schedules, dosage, and keto interaction notes
- **Water intake tracking** — daily goals with progress
- **Progress tracking** — weight, measurements, lab results, trend charts
- **Lab result ingestion** — PDF upload or manual entry with AI interpretation
- **Push notifications** — via [ntfy.sh](https://ntfy.sh) (works off home network too)
- **Weekly research pulls** — AI-summarized keto/supplement research, auto-updated
- **AI assistant** — powered by Claude API or local Ollama (swappable via config)

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Python 3.13 + FastAPI |
| Frontend | React + Vite + TypeScript |
| Styling | Tailwind CSS v4 |
| Database | SQLite + SQLAlchemy (async) |
| AI | LiteLLM → Claude API or Ollama |
| Notifications | ntfy.sh cloud relay |
| Background jobs | APScheduler |
| PDF parsing | pdfplumber |
| Nutrition data | USDA FoodData Central + Open Food Facts fallback |
| Package manager | uv (Python), pnpm (Node) |

---

## Project Structure

```
keto-carer/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/routes/              # One file per domain
│   │   ├── users.py
│   │   ├── meals.py
│   │   ├── nutrition.py
│   │   ├── medications.py
│   │   ├── water.py
│   │   ├── progress.py
│   │   ├── grocery.py
│   │   ├── ai.py                # Chat, meal suggestions, Ollama management
│   │   └── notifications.py
│   ├── core/
│   │   ├── config.py            # Settings from .env
│   │   ├── database.py          # SQLAlchemy async engine + session
│   │   └── scheduler.py         # APScheduler setup
│   ├── models/                  # SQLAlchemy ORM models (14 tables)
│   ├── schemas/                 # Pydantic request/response schemas
│   └── services/
│       ├── ai_service.py        # LiteLLM abstraction (Claude + Ollama)
│       ├── nutrition_service.py # USDA FoodData Central + Open Food Facts
│       ├── notification_service.py  # ntfy.sh push notifications
│       ├── research_service.py  # Weekly research pull scheduler job
│       └── pdf_service.py       # Lab result PDF text extraction
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Routing
│   │   ├── components/Layout.tsx # Sidebar nav
│   │   ├── pages/               # Dashboard, Meals, Grocery, Progress, Meds, Water, Settings
│   │   ├── hooks/
│   │   └── lib/
│   │       ├── api.ts           # Axios client → /api/v1
│   │       └── utils.ts         # cn() helper
│   ├── index.html
│   ├── vite.config.ts           # Proxy /api → backend:8000, host 0.0.0.0 for LAN
│   └── package.json
├── data/
│   ├── keto-carer.db            # SQLite database (auto-created on first run)
│   └── uploads/                 # Lab result PDFs
├── .env                         # Local config (not committed)
├── .env.example                 # Template — copy to .env to start
└── .gitignore
```

---

## Setup

### Prerequisites

- Python 3.13+
- Node.js 22+ and pnpm (`npm install -g pnpm`)
- [uv](https://docs.astral.sh/uv/) (`pip install uv`)
- [Ollama](https://ollama.com) installed locally (optional — needed if `AI_PROVIDER=ollama`)
- [ntfy app](https://ntfy.sh) on your phone (optional — for push notifications)

### 1. Clone & configure

```bash
git clone https://github.com/apleith/keto-carer.git
cd keto-carer
cp .env.example .env
# Edit .env — set AI_PROVIDER, ANTHROPIC_API_KEY or OLLAMA_MODEL, USDA_API_KEY
```

### 2. Backend

```bash
cd backend
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

> **First run:** SQLite database and all tables are auto-created in `data/keto-carer.db`.

### 3. Frontend

> **Note for Google Drive users:** Node's `node_modules` requires symlink support which Google Drive's virtual filesystem does not provide. Install from a local path or configure your Drive client to exclude `node_modules` from sync before running `pnpm install`.

```bash
cd frontend
pnpm install
pnpm dev
```

Frontend runs at `http://localhost:5173` and proxies `/api` to the backend.
Accessible on your LAN at `http://<your-machine-ip>:5173`.

### 4. Pull an Ollama model (if using local AI)

```bash
ollama pull llama3.2
```

Or use the in-app Settings page to manage Ollama models once the UI is built out.

---

## Environment Variables

See [.env.example](.env.example) for all options. Key ones:

| Variable | Default | Description |
|---|---|---|
| `AI_PROVIDER` | `ollama` | `claude` or `ollama` |
| `ANTHROPIC_API_KEY` | *(empty)* | Required if `AI_PROVIDER=claude` |
| `OLLAMA_MODEL` | `llama3.2` | Model name for Ollama |
| `USDA_API_KEY` | `DEMO_KEY` | [Get a free key](https://fdc.nal.usda.gov/api-guide.html) for higher rate limits |
| `NTFY_BASE_URL` | `https://ntfy.sh` | ntfy server (use default for cloud) |

---

## Notifications Setup (ntfy)

1. Install the [ntfy app](https://ntfy.sh) on each user's phone
2. Each user picks a unique topic name (e.g. `keto-alex-abc123`)
3. Subscribe to that topic in the ntfy app
4. Enter the topic in the app's Settings page per user

The backend POSTs to ntfy's cloud servers — no port forwarding or public IP needed. Notifications arrive even when the phone is off home Wi-Fi.

---

## API Reference

Interactive Swagger docs available at `http://localhost:8000/docs` when the backend is running.

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Server health + AI provider info |
| GET/POST | `/api/v1/users/` | User profiles |
| GET/POST | `/api/v1/meals/` | Meal recipes |
| POST | `/api/v1/meals/logs/` | Log a meal |
| GET | `/api/v1/nutrition/search?q=` | USDA food search |
| GET/POST | `/api/v1/medications/` | Medications & supplements |
| GET/POST | `/api/v1/water/` | Water logs |
| GET | `/api/v1/water/today-total` | Today's water total |
| GET/POST | `/api/v1/progress/` | Body measurements |
| POST | `/api/v1/progress/labs/upload/` | Upload lab result PDF |
| GET/POST | `/api/v1/grocery/` | Grocery lists |
| GET | `/api/v1/ai/meal-suggestions` | AI meal recommendations |
| POST | `/api/v1/ai/chat` | Free-form AI chat |
| GET | `/api/v1/ai/ollama/models` | List installed Ollama models |
| POST | `/api/v1/notifications/test` | Send test push notification |

---

## Build Phases

| Phase | Status | Description |
|---|---|---|
| 1 | ✅ Complete | Scaffolding, database models, backend API, services, frontend shell |
| 2 | Pending | All UI pages built out (Dashboard, Meals, Grocery, Progress, Meds, Water, Settings) |
| 3 | Pending | USDA nutrition search integrated into UI |
| 4 | Pending | ntfy notification scheduling per user |
| 5 | Pending | PDF lab result upload + AI interpretation UI |
| 6 | Pending | APScheduler research pull + in-app research feed |
| 7 | Pending | Mobile polish, simplified UX mode for less tech-savvy users |

---

## Known Issues / Notes

- **Google Drive + node_modules:** pnpm/npm require symlink support. See Setup step 3 for the workaround.
- **DEMO_KEY rate limits:** USDA FoodData Central's demo key allows 30 req/min. [Register for a free key](https://fdc.nal.usda.gov/api-guide.html) to increase limits.
- **`desktop.ini` in `.git/refs/`:** Google Drive may sync `desktop.ini` files into `.git/refs/`, causing broken ref warnings. Clean with: `find .git/refs -name "desktop.ini" -delete`
- `AI_PROVIDER` can be toggled by changing `.env` and restarting the backend — no code changes needed.
