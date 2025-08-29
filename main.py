
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

from fastapi import HTTPException, Query
from typing import Dict, Any, Optional

# Example workflows storage (replace with real exports from n8n)
WORKFLOWS: Dict[str, Dict[str, Any]] = {
    "welcome-email": {
        "id": "welcome-email",
        "name": "Welcome Email Autoresponder",
        "description": "Sends a welcome email when a contact is created.",
        "categories": ["email", "crm"],
        "tags": ["starter"],
        "workflow": {
            "nodes": [],          # paste "nodes"[] from your n8n export here
            "connections": {}     # paste "connections"{} from your n8n export here
        }
    }
}

CATEGORIES = [
    {"id": "email", "name": "Email"},
    {"id": "crm", "name": "CRM"},
]

COLLECTIONS = [
    {"id": "starters", "name": "Starters", "workflowIds": ["welcome-email"]},
]

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/templates/search")
def search_templates(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = 1,
    rows: int = 50,
):
    items = list(WORKFLOWS.values())
    if search:
        s = search.lower()
        items = [w for w in items if s in w["name"].lower() or s in w["description"].lower()]
    if category:
        items = [w for w in items if category in w.get("categories", [])]
    start = (page - 1) * rows
    end = start + rows
    return {"items": items[start:end]}

@app.get("/templates/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    wf = WORKFLOWS.get(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Not Found")
    return wf

@app.get("/templates/categories")
def get_categories():
    return {"items": CATEGORIES}

@app.get("/templates/collections")
def get_collections(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    items = COLLECTIONS
    if search:
        s = search.lower()
        items = [c for c in items if s in c["name"].lower()]
    if category:
        items = [c for c in items if any(category in WORKFLOWS[w]["categories"] for w in c["workflowIds"] if w in WORKFLOWS)]
    return {"items": items}

@app.get("/templates/collections/{collection_id}")
def get_collection(collection_id: str):
    col = next((c for c in COLLECTIONS if c["id"] == collection_id), None)
    if not col:
        raise HTTPException(status_code=404, detail="Not Found")
    return col

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/templates/search")
def search_templates():
    return [
        {"id": "welcome-email", "name": "Welcome Email", "description": "Send a welcome email"},
        {"id": "slack-alert", "name": "Slack Alert", "description": "Send alerts to Slack"}
    ]

from fastapi import HTTPException

# Replace the nodes/connections with a real export later.
WORKFLOWS = {
    "welcome-email": {
        "id": "welcome-email",
        "name": "Welcome Email Autoresponder",
        "description": "Sends a welcome email when a contact is created.",
        "categories": ["email", "crm"],
        "tags": ["starter"],
        "workflow": {
            "nodes": [],
            "connections": {}
        }
    }
}

@app.get("/templates/workflows/{workflow_id}")
def get_workflow(workflow_id: str):
    wf = WORKFLOWS.get(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Not Found")
    return wf

# --- categories ---
CATEGORIES = [
    {"id": "email", "name": "Email"},
    {"id": "crm", "name": "CRM"},
]

@app.get("/templates/categories")
def get_categories():
    return {"items": CATEGORIES}

# --- collections (optional) ---
COLLECTIONS = [
    {"id": "starters", "name": "Starters", "workflowIds": ["welcome-email"]},
]

@app.get("/templates/collections")
def get_collections():
    return {"items": COLLECTIONS}

@app.get("/templates/collections/{collection_id}")
def get_collection(collection_id: str):
    for c in COLLECTIONS:
        if c["id"] == collection_id:
            return c
    raise HTTPException(status_code=404, detail="Not Found")
