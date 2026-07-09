# SunPlus Power Solar EPC Platform

A full-stack, enterprise-grade, responsive website and ERP management console for **SunPlus Power India Pvt. Ltd.**, a solar EPC (Engineering, Procurement, and Construction) firm based in Lucknow, Uttar Pradesh.

## 🛠️ Technical Stack
* **Frontend**: Plain HTML5, Vanilla JavaScript, and compiled Tailwind CSS. No React/Vue or external Tailwind CDNs are used.
* **Backend**: FastAPI (Python 3.11+), SQLAlchemy ORM, SQLite (local development/testing) & PostgreSQL (production containerization).
* **Database migrations**: Alembic versioning.
* **Security & Auth**: JWT (JSON Web Tokens) with direct `bcrypt` password hashing (compatible with Python 3.14+).
* **Containerization**: Docker Compose using Nginx (routing reverse proxy & static files server) + FastAPI + PostgreSQL.

---

## 📂 Project Anatomy
```text
sunplus_power_v2/
├── backend/
│   ├── app/
│   │   ├── core/         # Config, database engine, security helper, rate limiters
│   │   ├── models/       # Declarative SQLAlchemy models (12 tables)
│   │   ├── schemas/      # Pydantic schemas for data validations
│   │   ├── services/     # ROI Calculation, SMTP non-blocking alerts, File constraints
│   │   ├── routers/      # Auth routers, public APIs, and admin CRUD dashboards
│   │   └── main.py       # FastAPI application initializations & auto-seeding
│   ├── tests/            # Isolated Pytest test suite (auth, calculator, forms)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # Hand-written HTML pages with variables.css + base.css
│   ├── admin/            # Secure admin console dashboards (login, CRUD tables)
│   ├── assets/
│   │   ├── css/          # Variables, resets, custom sheets, and compiled stylesheets
│   │   └── js/           # Dynamic API clients, ROI charts, CRUD controllers
│   └── index.html
├── docker-compose.yml    # Full-stack orchestrator config
├── nginx.conf            # Nginx reverse proxy routes
├── tailwind.config.js    # Tailwind scanner configuration
└── README.md
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the `backend/` directory (a template is provided in `backend/.env.example`):
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/sunplus_db
SECRET_KEY=1e7bde935a8bc34f9a0d8102d8479e0a294d1b8de09e20a06ef8bb213a863ff8
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database Auto-Seeding Credentials
ADMIN_SEED_EMAIL=admin@sunpluspower.in
ADMIN_SEED_PASSWORD=SunPlusAdmin2026!

# SMTP Configuration (Fallback logs if variables are omitted)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@sunpluspower.in
SMTP_PASSWORD=yoursecretpasswordhere
SMTP_FROM=alerts@sunpluspower.in
```

---

## 🚀 Running the Project

### Option A: Standard Docker Deployment (Recommended)
Launch the entire system (Frontend static server, Backend API, PostgreSQL database, and migrations) with one command:
```bash
docker-compose up --build
```
* **Frontend Site**: Open `http://localhost`
* **Admin Control Panel**: Open `http://localhost/admin/login.html` (Credentials: `admin@sunpluspower.in` / `SunPlusAdmin2026!`)
* **API Documentation**: Open `http://localhost:8000/docs`

---

### Option B: Local Host Development Setup

#### 1. Compile CSS assets
Ensure Node.js is installed locally, then compile and bundle style classes:
```bash
npm install
npm run build:css
```

#### 2. Start the Backend API
Install dependencies and run the FastAPI server (it automatically initializes a local SQLite file `temp.db` if no Postgres credentials are provided):
```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --port 8000
```

#### 3. View the Frontend
Since frontend routes resolve relative to `/api/`, open the files using a local development server or configure Nginx locally. Alternatively, open `index.html` directly (for pages fetching public APIs like projects and careers).

---

## 🧪 Running Automated Tests
The backend features an isolated test suite using Pytest that overrides database connections using an in-memory SQLite database (`sqlite:///:memory:`).

To execute the test suite:
```bash
cd backend
py -m pytest
```

---

## 🔒 Security & Constraints Implementation Details
1. **SlowAPI Rate Limiter**: Rate-limits public POST endpoints (`/api/leads`, `/api/calculator/submit`, etc.) to mitigate denial-of-service spamming.
2. **File Size/Type Constraints**: Resume document uploads are constrained to PDF/DOC files under 5MB. Support ticket photo uploads are restricted to common image extensions.
3. **SMTP Non-Blocking Delivery**: Email dispatches are spawned inside background worker threads using FastAPI `BackgroundTasks`, preventing mail-server lag from delaying API responses.
4. **Token Authentication**: Protected paths are wrapped in dependency `get_current_admin` which decodes bearer JWT keys and verifies caller privileges.
