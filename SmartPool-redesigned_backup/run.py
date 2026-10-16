"""
SmartPool one-command launcher.

Starts the backend (FastAPI) AND serves the ready-built website from the same
address, so you only need ONE window and no Node.js:

    python run.py          ->  opens http://127.0.0.1:8000

Normally you just double-click RUN_SMARTPOOL.bat (Windows) or run
./run_smartpool.sh (Mac/Linux), which call this file for you.
"""
import os
import socket
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "frontend", "dist")
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def fail(message: str) -> None:
    print("\n" + "=" * 62 + "\n" + message + "\n" + "=" * 62 + "\n")
    sys.exit(1)


try:
    import uvicorn
    from fastapi.staticfiles import StaticFiles
    from backend.main import app
except ModuleNotFoundError as err:
    fail(
        f"A Python package is missing: '{err.name}'.\n\n"
        "Fix: run RUN_SMARTPOOL.bat (it installs everything), or type:\n"
        "    python -m pip install -r requirements-demo.txt"
    )

if not os.path.isfile(os.path.join(DIST, "index.html")):
    fail(
        "The built website was not found at frontend/dist/index.html.\n\n"
        "Fix (needs Node.js):\n"
        "    cd frontend\n    npm ci\n    npm run build"
    )


def free_port(start: int = 8000) -> int:
    """First port from `start` that nothing is listening on."""
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.3)
            if probe.connect_ex(("127.0.0.1", port)) != 0:
                return port
    fail("Could not find a free port between 8000 and 8019. Close other servers and retry.")


# Mounted LAST so that every /api/... and /ws/... route defined in backend/main.py
# is matched first; anything else is served from the built website.
app.mount("/", StaticFiles(directory=DIST, html=True), name="smartpool-ui")

port = free_port()
url = f"http://127.0.0.1:{port}"
print(f"\n  SmartPool is starting.\n  Open:  {url}\n  API docs:  {url}/docs\n  Stop:  press Ctrl+C in this window\n")
threading.Timer(1.5, lambda: webbrowser.open(url)).start()
uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
