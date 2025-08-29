
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List

app = FastAPI(title="n8n Templates API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ---- Minimal demo data (replace with your own exports) ----
WORKFLOWS = {
    "welcome-email": {
        "id": "welcome-email",
        "name": "Welcome Email Autoresponder",
        "description": "Sends a welcome email when a contact is created.",
        "categories": ["email", "crm"],
        "tags": ["starter", "marketing"],
        # Minimal n8n workflow export stub. Replace with a real export when ready.
        "workflow": {"nodes": [], "connections": {}}
    }
}

COLLECTIONS = [
    {"id": "marketing", "name": "Marketing", "workflowIds": ["welcome-email"]},
]

CATEGORIES = [
    {"id": "email", "name": "Email"},
    {"id": "crm", "name": "CRM"},
]

# ---- Endpoints n8n expects ----

@app.get("/templates/search")
def search(q: str = "") -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    for wf in WORKFLOWS.values():
        haystack = (wf["name"] + " " + wf["description"]).lower()
        if q == "" or q.lower() in haystack:
            items.append({"id": wf["id"], "name": wf["name"], "description": wf["description"]})
    return {"items": items}

@app.get("/templates/workflows/{workflow_id}")
def get_workflow(workflow_id: str) -> Dict[str, Any]:
    wf = WORKFLOWS.get(workflow_id)
    if not wf:
        return {"error": "not found"}
    return wf

@app.get("/templates/collections")
def list_collections() -> Dict[str, List[Dict[str, Any]]]:
    return {"items": COLLECTIONS}

@app.get("/templates/collections/{collection_id}")
def get_collection(collection_id: str) -> Dict[str, Any]:
    col = next((c for c in COLLECTIONS if c["id"] == collection_id), None)
    if not col:
        return {"error": "not found"}
    return col

@app.get("/templates/categories")
def list_categories() -> Dict[str, List[Dict[str, str]]]:
    return {"items": CATEGORIES}
