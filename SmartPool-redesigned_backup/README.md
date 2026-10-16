# SmartPool — A better way together

Premium React interface for the existing Pune–Mumbai ride-pooling engine.

## Quick start (easiest way, one window)

You do **not** need Node.js. The website is already built and the backend serves it.

**Windows:** extract the ZIP into a new folder, then double-click **RUN_SMARTPOOL.bat**.
**Mac / Linux:** extract the ZIP, open a terminal in the folder and run `./run_smartpool.sh`.

1. The first run installs the Python packages (needs internet, about a minute). Python 3.10 or newer must be installed; on Windows tick **"Add python.exe to PATH"** in the installer.
2. Your browser opens at **http://127.0.0.1:8000**. The header should say **"Engine connected"**.
3. Keep the black window open while you use the app. Close it (or press Ctrl+C) to stop.

The interactive API documentation is at http://127.0.0.1:8000/docs.

If you prefer typing commands instead of double-clicking:

```bat
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-demo.txt
.venv\Scripts\python run.py
```

Map tiles need internet whenever used. No map API key is required.
If port 8000 is busy, `run.py` automatically picks the next free port and prints the address.
Do not open `frontend/dist/index.html` by double-clicking it: the app needs the backend server.

## Developer mode (only if you want to edit the frontend)

Needs Node.js LTS. Use two terminals; the page then lives at http://localhost:3000 with hot reload:

```bat
py -m pip install -r requirements-demo.txt
py -m uvicorn backend.main:app --reload --port 8000
```

```bat
cd frontend
npm ci
npm run dev
```

START_BACKEND.bat and START_FRONTEND.bat do the same thing. After changing frontend code, run `npm run build` so that RUN_SMARTPOOL shows your changes.

## Two-minute judge demonstration

1. Select **Dispatch** at the top (bottom navigation on phones).
2. On an empty queue, click **Golden Corridor**, then **Dispatch batch**.
3. Open **Live corridor map**. Recenter, inspect stop markers, and play the clearly labelled simulation.
4. Open **Drive** to see next stops, the pickup/drop-off timeline, and simulated seat occupancy.
5. Return to **Dispatch → Fairness Lab**: Rahul ₹504, Priya ₹728, Aman ₹868; total ₹2,100.
6. Open **Convenience Shield → Test Vikram insertion** to show the fixed 18.1% rejection scenario.
7. Open **What-If Sandbox**, adjust tolerance or add a candidate, and evaluate with the backend.
8. Open **Benchmark scorecard → Load benchmark**. Explain that this existing endpoint supplies a fixed fixture, not a newly measured benchmark.

To demonstrate a passenger: choose **Ride**, enter a name and forward corridor trip, and press **Find a shared ride**. The request is added to the actual server queue. Press **Match current batch** for manual dispatch. A successful response shows that passenger’s fare and route; a single-rider result is explicitly identified. To test shared passenger matching, add another overlapping request from Dispatch before dispatching.

## What changed

- White map-first passenger interface with booking sheet, matching state, trip result, fare explanation and companion list.
- Dark driver console with optimized timeline, next stop, simulation controls and seat occupancy.
- Dark admin sidebar with all six technical sections, real queue controls, fare comparisons and charts.
- Responsive layouts and mobile bottom navigation; keyboard focus, labels and reduced-motion support.
- Leaflet OpenStreetMap tiles, attribution, zoom, fitBounds, location request, safe text popups, pickup/drop-off markers and labelled corridor lines.
- API adapter carries canonical node IDs and uses actual seat counts from dispatch request metadata.
- Production frontend build included in frontend/dist.

## Backend compatibility and honest limits

The backend is the **fixed version** (carpool-backend-fixed). Compared with the earlier backend, `engine.py` is unchanged, and `main.py` now:

- uses Pydantic v2 style validation (`min_length`), so it works with current FastAPI;
- accepts alternative field names for bookings (`pickup`, `from`, `dropoff`, `to`, `name`...) instead of failing with HTTP 422;
- matches place names case-insensitively and adds `GET /api/locations` for dropdowns;
- gives clearer errors for same-place and wrong-direction trips;
- starts uvicorn from the end of the file, after every route is registered.

`run.py` (new, in the project root) imports that backend unchanged and only adds the website on top. `requirements-demo.txt` uses plain `uvicorn` plus `websockets`, which installs reliably on Windows; `backend/requirements.txt` (with `uvicorn[standard]`) is kept as supplied.

- Existing booking, queue, dispatch, Golden demo, health, node, rejection, benchmark, optimization and WebSocket routes are used.
- The queue is in-memory and dispatch is manual. A server restart clears requests. The heartbeat is not an automatic batching countdown.
- There is no private-booking, cancellation, authentication, payment, live GPS or driver assignment API. The UI does not claim to provide these.
- A successful result is a demo route computation, not an actual transport reservation.
- Routes connect the backend's simplified corridor coordinates. They are not road-following or turn-by-turn navigation. Vehicle movement advances through model stops.
- State for the displayed trip lives in this browser session. Reloading loses the displayed trip. Another browser can update the queue, but this API has no endpoint to retrieve another browser’s dispatched trip.
- Golden Corridor replaces the server queue, so the UI only allows loading it when the queue is empty.
- The rejection endpoint is a fixed Vikram scenario. Its SOLO_DISPATCH field is illustrative and does not create a private ride.
- The benchmark endpoint returns fixed constants. The UI labels them as a fixture, not a new Monte Carlo run.
- Booking and batch dispatch enforce at most 15% detour. The What-If optimization endpoint can evaluate a relaxed cap up to 25%; it is explicitly separate from booking policy.
- What-If calls the existing optimize endpoint, which writes backend/snapshot.json as it already did. It does not replace the displayed trip or alter the booking queue.
- The engine prices each named request, not each seat; the UI preserves these results. Seat counts are used for queue admission and displayed occupancy.
- Backend miles/coordinates are authoritative; fixed screenshot numbers are never used as fallback fares.

## Verify

```bat
cd frontend
npm run build
cd ..
py -m pip install httpx
py -m unittest discover -s tests -v
py tests/export_fixture.py
node tests/check_frontend_adapter.mjs
```

See TEST_RESULTS.md for checks performed and remaining limits.
