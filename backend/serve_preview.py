"""Sandbox-only launcher: serves the FastAPI ORCA Box plus the prebuilt
Flutter web bundle (frontend/web_dist) from a single origin so the browser
can hit /api/* without cross-origin/localhost issues.
Not used in production; run with `uvicorn serve_preview:app`.
"""
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from main import app  # noqa: E402

WEB_DIST = Path(__file__).resolve().parent.parent / "frontend" / "web_dist"
if WEB_DIST.is_dir():
    # main.py defines GET "/" returning JSON; drop it so index.html is served.
    app.router.routes[:] = [
        r for r in app.router.routes if getattr(r, "path", None) != "/"
    ]
    app.mount("/", StaticFiles(directory=str(WEB_DIST), html=True), name="web")
