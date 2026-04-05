# Source Backend Django

## Environment

Create `backend-django/.env` for local backend settings.

Current frontend origin:

```env
FRONTEND_URL=https://source-frontend-omega.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://source-frontend-omega.vercel.app
```

The backend now loads `backend-django/.env` automatically.

## Railway Postgres

The backend already uses `DATABASE_URL`, so Railway Postgres works without extra database code changes.

Set these variables in your Railway backend service:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
FRONTEND_URL=https://source-frontend-omega.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://source-frontend-omega.vercel.app
```

If your Railway database service has a different name, replace `Postgres` with that exact service name.

For local development, you can leave `DATABASE_URL` unset and Django will fall back to `db.sqlite3`.

## Vercel notes

For Vercel deployments:

```env
DEBUG=False
FRONTEND_URL=https://source-frontend-omega.vercel.app
DJANGO_CSRF_TRUSTED_ORIGINS=https://source-frontend-omega.vercel.app
DJANGO_ALLOWED_HOSTS=source-backend-django.vercel.app
```

`DJANGO_ALLOWED_HOSTS` must contain host names only. Do not include `https://` or a trailing `/`.

The backend also auto-adds Vercel system hostnames such as `VERCEL_URL` and `VERCEL_PROJECT_PRODUCTION_URL` when they are available at runtime.
