# Smartpocket AI Backend

## Run

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` and `JWT_SECRET_KEY`.
4. Start: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
5. Serve the frontend through a local web server, for example VS Code Live Server on port 5500. Do not open protected pages only as `file://` unless `null` remains in allowed origins.

Interactive API docs are available at `/docs` while the server runs.

Demo account is created automatically on startup:
- username: `demo`
- password: `demo1234`

Replace your existing `js/app.js` and `js/recommend.js` with the files under `frontend-js/`, then apply `FRONTEND_PATCHES.md` because fetch-based APIs are asynchronous.
