# Admin Panel

## Access

| | |
|---|---|
| URL | `http://localhost:8080/admin/login.html` |
| Email | `admin@sunpluspower.in` |
| Password | `SunPlusAdmin2026!` |

Credentials are seeded automatically on backend startup from `ADMIN_SEED_EMAIL` / `ADMIN_SEED_PASSWORD` in `backend/.env` (see `backend/app/main.py`, `startup_db_seeding`).

## Running it locally

```bash
# Backend (from backend/)
source venv_mac/bin/activate   # or create one: python3 -m venv venv_mac && pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend (from frontend/)
python3 -m http.server 8080
```

Then open `http://localhost:8080/admin/login.html`.

The backend uses a local SQLite file (`backend/temp.db`) in this mode, not the production database — data entered here won't appear on the real deployed site.

If you see "Failed to fetch" errors on any admin page, check `ALLOWED_ORIGINS` in `backend/.env` includes the origin the frontend is actually served from (e.g. `http://localhost:8080`), then restart the backend — CORS origins are only read at startup.

## Pages

| Page | Path | Purpose |
|---|---|---|
| Dashboard Overview | `/admin/dashboard.html` | Stats summary — leads, distributors, tickets, projects, jobs |
| Submissions Inbox | `/admin/submissions.html` | General leads, distributor applications, warranty logs, complaints, job applications |
| Sales Console | `/admin/sales.html` | Sales leads + distributor pipeline |
| Projects Manager | `/admin/projects.html` | Add / edit / delete portfolio projects |
| Insights & Blogs | `/admin/blogs.html` | Write / manage blog articles |
| Careers & Jobs | `/admin/careers.html` | Add / edit / delete job openings |

## Design system

All admin pages share one layout: light-glass header (logo, notifications, admin profile, logout), dark sidebar with a red left-border active state, white content cards, and a shared footer. Brand accent is `--color-primary` (`#a40213`, defined in `frontend/assets/css/variables.css`) — don't introduce other reds; use `text-primary` / `bg-primary` / `bg-primary-dark` Tailwind classes so it stays wired to the CSS variable.

## Production deployment

For the Docker/production setup (Nginx + FastAPI + Postgres, served on port 80), see the main [README.md](./README.md).
