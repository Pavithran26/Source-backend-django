# Source ERP - Backend (Django)

The backend service for the Source Coconut ERP, built with Python, Django, and Django Rest Framework.

## 🚀 Technology Stack
- **Framework**: Django 5.1
- **API**: Django Rest Framework (DRF)
- **Database**: SQLite (Local), PostgreSQL (Production/Railway)
- **Authentication**: JWT (SimpleJWT)
- **Deployment**: Railway / Vercel

## 📦 Core Modules
- **Users**: Custom UserProfile, roles (Admin, Supervisor, Worker), and Profile Image support.
- **Land**: Land owner management and Land Lease (Gudhagai) tracking with EMI/Ledger logic.
- **Employee**: Field staff and worker master records with wage tracking.
- **Vehicle**: Registration and transport tracking.
- **Worklog**: Daily harvesting logs linking lands, supervisors, and workers.
- **Sales**: Sales ledger linked to buyers, lands, and worklogs.
- **Expenses**: General operational expense tracking.

## 🛠️ Local Setup

1. **Clone and Enter Directory**:
   ```bash
   cd Source-backend-django
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file based on `.env.example`:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   FRONTEND_URL=http://localhost:3000
   ```

5. **Migrations & Superuser**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## ☁️ Deployment

### Railway (Recommended)
This repo includes a `railway.toml`. When deploying to Railway, ensure you:
1. Link a PostgreSQL service.
2. Set `DATABASE_URL` to `${{Postgres.DATABASE_URL}}`.
3. Set `DJANGO_ALLOWED_HOSTS` to your Railway domain.

### Vercel
The project is configured for Vercel using `bszone_backend/vercel_app.py`. Note that SQLite data is not persistent on Vercel; use an external Postgres for production data.

## 🛡️ License
Private Repository.
