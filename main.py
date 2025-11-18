# main.py - SUPER CLEAN & FAST
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from exploreit_ai import ExploreItAI
from datetime import datetime

app = FastAPI(title="ExploreIt Pakistan", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ai = ExploreItAI()  # Fresh events every week!

@app.get("/")
def home():
    return {
        "message": "ExploreIt Pakistan - Fresh Events Every Week!",
        "week": datetime.now().isocalendar()[1],
        "total_events_this_week": len(ai.events_data),
        "tip": "Events change every Monday automatically!"
    }

@app.get("/events")
def events(q: str = None):
    if q:
        results = ai.search(q)
        return {"success": True, "query": q, "count": len(results), "events": results}
    else:
        all_events = ai.get_all_events()
        return {"success": True, "count": len(all_events), "events": all_events}