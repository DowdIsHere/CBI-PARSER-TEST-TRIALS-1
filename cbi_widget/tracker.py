"""Manual tracker logging.

A read is written to the tracker ONLY on the literal instruction "log it".
Nothing in the read engine calls this module; logging is never proposed,
never preemptive, never automatic.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def log_it(tracker_path: Path, read_text: str, note: str = "") -> None:
    """Append the read to the tracker. Called only by the explicit 'log it'
    command."""
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "logged_at": datetime.now(timezone.utc).isoformat(),
        "note": note,
        "read": read_text,
    }
    with tracker_path.open("a") as f:
        f.write(json.dumps(entry) + "\n")
