"""Thin FastAPI wrapper around the CBI Tennis Parser Widget.

Exposes the four CLI commands as HTTP endpoints so the widget can run
on Railway (or any container host).  All logic lives in cbi_widget/;
this file is pure routing.

Environment variables required:
  ANTHROPIC_API_KEY   forwarded to AnthropicAdapter by the engine
  DATA_DIR (optional) override for the data directory. If unset, a Railway
                      volume mounted at /data is used automatically when
                      present; otherwise ./data (ephemeral).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent


def _default_data_dir() -> Path:
    if "DATA_DIR" in os.environ:
        return Path(os.environ["DATA_DIR"])
    volume = Path("/data")
    if volume.is_dir():
        return volume
    return ROOT / "data"


def _usable_data_dir() -> tuple[Path, str | None]:
    """A bad DATA_DIR or unwritable volume must not kill the boot — fall back
    to the ephemeral ./data and report the problem via /health instead."""
    preferred = _default_data_dir()
    try:
        preferred.mkdir(parents=True, exist_ok=True)
        probe = preferred / ".write_probe"
        probe.write_text("")
        probe.unlink()
        return preferred, None
    except OSError as e:
        fallback = ROOT / "data"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback, f"{preferred} unusable ({e}); using ephemeral {fallback}"


DATA, DATA_WARNING = _usable_data_dir()

STORE_PATH = DATA / "placements.json"
LAST_READ_PATH = DATA / "last_read.md"
TRACKER_PATH = DATA / "tracker.jsonl"

app = FastAPI(title="CBI Tennis Parser Widget")


# -- request models -----------------------------------------------------------


class DeclareRequest(BaseModel):
    player: str
    spatial: str
    temporal: str
    reference: str
    method: str
    tier: str
    domains: str = ""
    date: str = ""
    declared_by: str = ""


class ReadRequest(BaseModel):
    player_a: str
    player_b: str
    conditions: str
    intake: Optional[str] = None
    score: Optional[str] = None
    with_market: bool = False
    model: str = "claude-opus-4-8"


class LogRequest(BaseModel):
    note: str = ""


# -- endpoints ----------------------------------------------------------------


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api")
def api_index():
    return {
        "service": "CBI Tennis Parser Widget",
        "endpoints": {
            "GET /health": "service status",
            "POST /declare": "record a user-declared placement",
            "GET /show": "list declared placements",
            "POST /read": "run a match read",
            "POST /log": "append the last read to the tracker",
            "GET /docs": "interactive API docs",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "data_dir": str(DATA),
        "data_warning": DATA_WARNING,
        "persistent": not DATA.is_relative_to(ROOT),
        "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
    }


@app.post("/declare")
def declare(req: DeclareRequest):
    from cbi_widget.placements import Placement, PlacementStore
    store = PlacementStore(STORE_PATH)
    provenance = {
        "method": req.method,
        "tier": req.tier,
        "domains": req.domains.split(",") if req.domains else [],
        "date": req.date,
        "declared_by": req.declared_by,
    }
    store.declare(Placement(
        player=req.player,
        spatial=req.spatial,
        temporal=req.temporal,
        reference=req.reference,
        provenance=provenance,
    ))
    return {
        "status": "ok",
        "player": req.player,
        "placement": f"{req.spatial} • {req.temporal} • {req.reference}",
        "tier": req.tier,
    }


@app.get("/show")
def show():
    import json
    if not STORE_PATH.is_file():
        return {"players": {}}
    return json.loads(STORE_PATH.read_text())


@app.post("/read")
def read(req: ReadRequest):
    from cbi_widget.engine import LiveFrame, ReadEngine
    from cbi_widget.model import AnthropicAdapter
    from cbi_widget.placements import MissingParserError, PlacementStore, presence_gate

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY is not set — add it in Service → Variables "
                   "and redeploy. GET /health reports api_key_set.",
        )

    store = PlacementStore(STORE_PATH)
    try:
        presence_gate(store, req.player_a, req.player_b)
    except MissingParserError as e:
        raise HTTPException(status_code=422, detail=str(e))

    live_frame = None
    if req.score:
        pairs = re.findall(r"(\d+)\s*-\s*(\d+)", req.score)
        current = (int(pairs[-1][0]), int(pairs[-1][1])) if pairs else None
        live_frame = LiveFrame(description=req.score, current_set_games=current)

    engine = ReadEngine(
        root=ROOT,
        store=store,
        model=AnthropicAdapter(model=req.model),
    )
    try:
        result = engine.run_read(
            player_a=req.player_a,
            player_b=req.player_b,
            intake_text=req.intake or "",
            conditions=req.conditions,
            live_frame=live_frame,
            market_requested=req.with_market,
        )
    except MissingParserError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if result.status == "uncertain":
        raise HTTPException(status_code=503, detail=result.text)

    LAST_READ_PATH.write_text(result.text)
    return {"status": "ok", "read": result.text}


@app.post("/log")
def log(req: LogRequest):
    from cbi_widget.tracker import log_it
    if not LAST_READ_PATH.is_file():
        raise HTTPException(
            status_code=400,
            detail="Nothing to log — no read has been produced this session.",
        )
    log_it(TRACKER_PATH, LAST_READ_PATH.read_text(), note=req.note)
    return {"status": "ok", "tracker": str(TRACKER_PATH)}
