# Django Scaffold

An opinionated starter for Django projects: Jinja2 templates, a Vite + Tailwind + HTMX + Alpine frontend, PostgreSQL, S3-compatible media storage, and a custom email-based user model, all wired up and ready to build on.

## Stack

| Area | Choice |
| --- | --- |
| Framework | Django 6.1+ on Python 3.14+ |
| Database | PostgreSQL (`psycopg` 3) |
| Templates | Jinja2 (Django templates remain available) |
| Frontend | Vite, Tailwind CSS 4, HTMX, Alpine.js, Lucide icons, via `django-vite` |
| Background jobs | Procrastinate (`procrastinate.contrib.django`) |
| API | `django-ninja` (`NinjaAPI` instance in `apps/api`, served under `/api/`) |
| Media storage | S3-compatible, via `django-storages` |
| Static files | WhiteNoise |
| Config | `django-environ` and per-environment `.env` files |
| Dev tooling | `django-browser-reload`, `django-stubs` |
| Packaging | [uv](https://docs.astral.sh/uv/) |

## Project layout

```
apps/
  accounts/      Custom User model (email login), its manager and initial migration
  api/           django-ninja API (`v1` instance in api.py)
  core/          Shared app; hosts the `dev` management command
config/
  settings/      base, development, staging, production, testing
  jinja2.py      Jinja2 environment and template helpers
  urls.py        Root URL conf
frontend/        Vite project (src/main.js, src/styles.css)
jinja2/          Global Jinja2 templates (base.html.j2)
manage.py
```

## Getting started

### Prerequisites

- Python 3.14+ and [uv](https://docs.astral.sh/uv/)
- Node.js and npm
- A PostgreSQL database
- An S3-compatible bucket (the default storage backend is S3, so the S3 settings are required even in development)

### Setup

```sh
# Python dependencies
uv sync

# Frontend dependencies
cd frontend
npm install
cd ..

# Environment
cp .env.example .env     # then fill in the values

# Database
uv run python manage.py migrate
uv run python manage.py createsuperuser

# Run Django and the Vite dev server together
uv run python manage.py dev
```

The site is served at <http://127.0.0.1:8000/> and the Vite dev server runs on `localhost:5173`. `manage.py dev` accepts the same optional `addrport` argument as `runserver` (e.g. `manage.py dev 0.0.0.0:9000`).

## Configuration

### Environments

`PYTHON_ENV` selects the settings module in `manage.py`:

| `PYTHON_ENV` | Settings module | Extra env file |
| --- | --- | --- |
| `development` (default) | `config.settings.development` | `.env.development` |
| `testing` | `config.settings.testing` | `.env.testing` |
| `staging` | `config.settings.staging` | `.env.staging` |
| `production` | `config.settings.production` | `.env.production` |

Each environment module loads its own `.env.<environment>` file, then imports `config.settings.base`, which loads `.env`. Values set in the environment-specific file win over `.env`.

Development overrides: `DEBUG = True`, `django-browser-reload` enabled, plain static file storage, and emails printed to the console.

### Environment variables

See [.env.example](.env.example) for the full list.

| Variable | Purpose |
| --- | --- |
| `PYTHON_ENV` | Environment name (see above) |
| `SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Allowed hosts (defaults to `localhost`, `127.0.0.1`) |
| `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` | PostgreSQL connection |
| `S3_ENDPOINT`, `S3_REGION`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET` | Media storage |
| `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_STARTTLS`, `SMTP_FROM` | Outgoing email |
| `VITE_DEV_MODE` | Force Vite dev mode on or off (defaults to on in `development`) |

## Frontend

The Vite project lives in [frontend/](frontend/). Its entry point is [frontend/src/main.js](frontend/src/main.js), which starts Alpine, exposes HTMX, renders Lucide icons (and re-renders them after each HTMX swap), and imports the Tailwind stylesheet.

- **Development:** `manage.py dev` starts Vite for you. Templates load assets from the dev server with HMR.
- **Production:** build the bundle, then collect static files.

  ```sh
  cd frontend && npm run build
  cd .. && uv run python manage.py collectstatic
  ```

  The build is written to `static/vite/` with a manifest that `django-vite` reads.

## Templates

Templates use Jinja2. [config/jinja2.py](config/jinja2.py) adds helpers on top of the usual Django globals (`static`, `url`, `now`, `DEBUG`) and `vite_assets()`:

- **Global templates** live in the top-level `jinja2/` directory and are referenced with `global_layout()`, `global_macro()` and `global_partial()`.
- **App templates** live in `apps/<app>/jinja2/` and are referenced from within the same app with `layout()`, `macro()` and `partial()`, which resolve to `layouts/`, `macros/` and `partials/` subdirectories.

[jinja2/base.html.j2](jinja2/base.html.j2) is the base layout. It loads the Vite assets and sets the CSRF header for HTMX requests.

## Users

[apps/accounts](apps/accounts) defines a custom `User` model (`AUTH_USER_MODEL = 'accounts.User'`) that logs in by email instead of username, with `is_active`, `is_staff`, and created and updated timestamps. It is stored in the `users` table.

## API

[apps/api](apps/api) holds a `NinjaAPI` instance (`v1` in [apps/api/api.py](apps/api/api.py)) and a URLconf that mounts it at `v1/`. [config/urls.py](config/urls.py) includes it under `api/`, so endpoints you add to `v1` are served at `/api/v1/...` and the interactive docs are at `/api/v1/docs`. It has no endpoints yet.

## Adding an app

1. Create it under `apps/` (`uv run python manage.py startapp <name> apps/<name>`).
2. Set `name = 'apps.<name>'` in its `AppConfig` and add it to `INSTALLED_APPS` in [config/settings/base.py](config/settings/base.py).
3. Add an `urls.py` and include it from [config/urls.py](config/urls.py).

## Status

This is a scaffold. The `accounts`, `core` and `api` apps have no views or endpoints yet, and no license has been chosen.
