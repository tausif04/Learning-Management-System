# LearnHub — Django + React LMS

A complete beginner-friendly Learning Management System with a Django REST Framework backend and React/Vite frontend.

## Features

- JWT authentication: signup, login, refresh, logout/session handling
- Protected React routes
- Course catalog
- Course details with modules and lessons
- Course enrollment
- Mark lessons complete/incomplete
- Automatic course progress percentage
- User profile editing
- Enrolled-course dashboard
- Responsive UI
- CORS-enabled API

## Project structure

```text
lms-project/
├── backend/       # Django + DRF + SimpleJWT
├── frontend/      # React + Vite + Axios + React Router
└── README.md
```

## Backend setup

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base: `http://127.0.0.1:8000/api/`

### API endpoints

- `POST /api/auth/signup/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET/PATCH /api/profile/`
- `GET /api/courses/`
- `GET /api/courses/<id>/`
- `POST /api/courses/<id>/enroll/`
- `GET /api/enrollments/`
- `POST /api/lessons/<id>/complete/`
- Django admin: `/admin/`

Create courses/modules/lessons from Django admin, then enroll users from the frontend.

## Frontend setup

```bash
cd frontend
npm install
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
npm run dev
```

Set `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

For the deployed backend, use:

```env
VITE_API_URL=https://lms-backend-xpwc.onrender.com/api
```

The supplied deployed backend currently returned HTTP 503 during project preparation, so the frontend is intentionally configured through `VITE_API_URL` rather than hard-coding an assumed schema.

## Deployment

### Backend — Render

- Root directory: `backend`
- Build command: `./build.sh`
- Start command: `gunicorn lms_api.wsgi:application`
- Add `DATABASE_URL` and production secret/configuration if using PostgreSQL.
- Set `DEBUG=False` and a secure `SECRET_KEY` for production.

For a production deployment, replace SQLite with PostgreSQL and restrict `ALLOWED_HOSTS` and CORS origins.

### Frontend — Vercel/Netlify

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_URL=<your backend>/api`

## Notes

This project is designed to be submission-ready as a full-stack LMS foundation. The backend is self-contained and can replace or complement the unavailable deployed API. If the original OSTAD boilerplate has additional endpoint names, only the API service layer needs adaptation.
