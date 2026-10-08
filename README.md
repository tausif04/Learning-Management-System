# LearnFlow LMS — Django REST + React

A complete Learning Management System built from the provided LMS API requirements and the supplied React + Tailwind boilerplate.

## What changed from the earlier version

The first implementation used a custom API shape. This version was rebuilt around the supplied LMS API documentation:

- `/api/token/`
- `/api/token/refresh/`
- `/api/token/verify/`
- `/api/user/auth/`
- `/api/user/profile/student/`
- `/api/user/profile/teacher/`
- `/api/categories/`
- `/api/courses/`
- `/api/lessons/`
- `/api/materials/`
- `/api/enrollments/`
- `/api/enrollments/enroll/`
- `/api/questions/`

Additional endpoints were added only where the project plan requires behavior that the supplied API documentation does not expose directly, especially lesson completion/progress.

## Features

### Authentication
- Register
- Login with JWT
- Access-token refresh
- Protected routes
- Logout/session cleanup

### Dashboard
- Enrolled courses
- Course progress
- Completed-course count
- Average learning progress
- Continue-learning cards

### Course catalog
- Course cards
- Search
- Category filter
- Instructor information
- Enrollment state

### Course details
- Course description
- Instructor
- Lesson list
- Lesson content
- Video links
- Downloadable materials
- Enrollment
- Mark lesson complete/incomplete
- Progress calculation
- Course Q&A

### Profile
- Edit name/email/bio
- Avatar URL
- Role display
- Enrolled-course progress

### Backend
- Django REST Framework
- SimpleJWT
- SQLite locally / PostgreSQL on Render
- CORS
- Django admin
- Demo seed command

## Project structure

```text
LMS-Django-React/
├── backend/
│   ├── lms_api/
│   │   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── build.sh
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── lib/
│   │   └── pages/
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
└── render.yaml
```

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Demo account:

```text
username: instructor
password: password123
```

### Frontend

```bash
cd frontend
npm install
```

Create `.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Run:

```bash
npm run dev
```

## Deployment

### Backend — Render

Set the backend root directory to `backend`.

Build command:

```bash
./build.sh
```

Start command:

```bash
gunicorn lms_api.wsgi:application
```

Set:

```env
DEBUG=False
DJANGO_SECRET_KEY=<strong-secret>
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=https://<your-vercel-app>.vercel.app
DATABASE_URL=<Render PostgreSQL connection string>
```

### Frontend — Vercel

Set:

```env
VITE_API_URL=https://<your-backend>.onrender.com/api
```

The included `vercel.json` handles React Router history fallback.

## API alignment

The supplied documentation uses the deployed backend base URL:

`https://lms-backend-xpwc.onrender.com`

This frontend can point to that deployment simply by setting:

```env
VITE_API_URL=https://lms-backend-xpwc.onrender.com/api
```

The supplied documentation does not define a lesson-completion endpoint, so this implementation adds:

```text
POST   /api/lessons/<id>/complete/
DELETE /api/lessons/<id>/complete/
GET    /api/progress/
```

These endpoints are required to make the project-plan requirement “mark lessons as completed” and course progress functional.
