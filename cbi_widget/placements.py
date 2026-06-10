"""External Parser placement store and the pre-read presence gate.

Placements live OUTSIDE the match, in a JSON store the read engine reads.
A placement arrives here only by user declaration (Parser Sourcing Protocol,
upstream). The gate checks PRESENCE, not quality: it never evaluates,
re-derives, caps, or second-guesses a declared placement, and it never
places one from any in-match signal. The provenance record (method, tier,
domains, date) travels with the placement but is never adjudicated at read
time — any consequence of a sub-LOCKED tier is applied by the human.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

SPATIAL = ("Concrete", "Balanced", "Abstract")
TEMPORAL = ("Past", "Present", "Future")
REFERENCE = ("Self", "Balanced", "Other")


class MissingParserError(Exception):
    """Raised when a read is attempted without a supplied placement.

    The refusal is correct behavior — Step 1 of the Core Rule made
    non-optional.
    """

    def __init__(self, players: list[str]):
        self.players = players
        names = " and ".join(players)
        super().__init__(
            f"No Parser placement has been supplied for {names}. "
            "STOPPING — no read is produced. Declare the placement(s) first "
            "(identified upstream via the Parser Print Identifier manual under "
            "the Parser Sourcing Protocol). The read engine does not place a "
            "Parser from match behavior, stats, ranking, style, surface, "
            "handedness, age, or score."
        )


@dataclasses.dataclass(frozen=True)
class Placement:
    player: str
    spatial: str
    temporal: str
    reference: str
    provenance: dict

    @property
    def triple(self) -> tuple[str, str, str]:
        return (self.spatial, self.temporal, self.reference)

    def label(self) -> str:
        return f"{self.spatial} • {self.temporal} • {self.reference}"


def _validate_axes(spatial: str, temporal: str, reference: str) -> None:
    # Container-level input validation only (is this a real axis value?),
    # not an evaluation of the placement itself.
    problems = []
    if spatial not in SPATIAL:
        problems.append(f"spatial must be one of {SPATIAL}, got {spatial!r}")
    if temporal not in TEMPORAL:
        problems.append(f"temporal must be one of {TEMPORAL}, got {temporal!r}")
    if reference not in REFERENCE:
        problems.append(f"reference must be one of {REFERENCE}, got {reference!r}")
    if problems:
        raise ValueError("; ".join(problems))


class PlacementStore:
    """JSON-file-backed store of user-declared placements."""

    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> dict:
        if not self.path.is_file():
            return {"players": {}}
        return json.loads(self.path.read_text())

    def _save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    def declare(self, placement: Placement) -> None:
        """Record a user-declared placement, with its provenance, as given."""
        _validate_axes(placement.spatial, placement.temporal, placement.reference)
        data = self._load()
        data["players"][placement.player] = {
            "spatial": placement.spatial,
            "temporal": placement.temporal,
            "reference": placement.reference,
            "provenance": placement.provenance,
        }
        self._save(data)

    def get(self, player: str) -> Placement | None:
        record = self._load()["players"].get(player)
        if record is None:
            return None
        return Placement(
            player=player,
            spatial=record["spatial"],
            temporal=record["temporal"],
            reference=record["reference"],
            provenance=record.get("provenance", {}),
        )

    def all_players(self) -> list[str]:
        return sorted(self._load()["players"])


def presence_gate(store: PlacementStore, player_a: str, player_b: str) -> tuple[Placement, Placement]:
    """The input contract: a hard gate run before any read.

    Both placements supplied -> returns them as given.
    Either absent -> MissingParserError. There is no fallback path.
    """
    a = store.get(player_a)
    b = store.get(player_b)
    missing = [p for p, found in ((player_a, a), (player_b, b)) if found is None]
    if missing:
        raise MissingParserError(missing)
    return a, b
