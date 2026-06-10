"""CBI Tennis Parser Widget.

An execution tool, not an analysis assistant. It loads the seven read-engine
documents as separate context modules in a fixed order, gates every read on
the PRESENCE of two user-supplied Parser placements, runs intake and verdict
as separate passes, and refuses to emit any draft that fails the 13-check
drift guard.
"""

__all__ = [
    "modules",
    "placements",
    "part2",
    "drift_guard",
    "engine",
    "model",
    "tracker",
]
