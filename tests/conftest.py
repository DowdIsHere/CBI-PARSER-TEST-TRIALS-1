import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from cbi_widget.placements import Placement, PlacementStore  # noqa: E402


@pytest.fixture
def root() -> Path:
    return ROOT


@pytest.fixture
def store(tmp_path) -> PlacementStore:
    return PlacementStore(tmp_path / "placements.json")


@pytest.fixture
def placement_a() -> Placement:
    return Placement(
        player="Alice",
        spatial="Abstract",
        temporal="Future",
        reference="Self",
        provenance={
            "method": "independence",
            "tier": "LOCKED",
            "domains": ["speech", "tactical", "habits"],
            "date": "2026-05-01",
            "declared_by": "Robert",
        },
    )


@pytest.fixture
def placement_b() -> Placement:
    return Placement(
        player="Bona",
        spatial="Concrete",
        temporal="Past",
        reference="Other",
        provenance={
            "method": "volume-across-variation",
            "tier": "CORROBORATED",
            "domains": ["reflexive play", "speech"],
            "date": "2026-04-12",
            "declared_by": "Robert",
        },
    )


@pytest.fixture
def declared_store(store, placement_a, placement_b) -> PlacementStore:
    store.declare(placement_a)
    store.declare(placement_b)
    return store


# --- Canned drafts ---------------------------------------------------------

INTAKE_SECTIONS = """\
## Pre-Match Intel

**Head-to-Head (H2H) Record:** 1-1 across two prior meetings.

**Handedness:**
- **Alice:** Right-handed, two-handed backhand
- **Bona:** Right-handed, one-handed backhand

**Current Injuries:** None entering this draw.

**Event Context:** ITF W35, indoor hard court.

## Match Metrics

| Metric | Alice | Bona |
|---|---|---|
| Primary Court Surface | Hard | Clay |

## Winning Constants

- **Winning the 1st Set:** protects Alice's early-commitment game.

## Losing Trends

- **The "First Set" Rule:** dropping the opener forces longer builds.
"""

CLEAN_VERDICT = """\
## Parser Architecture Projection

### Player A: Alice
**Parser:** Abstract • Future • Self

- What conditions amplify their architecture: fast indoor courts that pay off early commitment.
- What conditions punish their architecture: wind that denies clean toss timing.

### Player B: Bona
**Parser:** Concrete • Past • Other

- What conditions amplify their architecture: conditions that grant the archive time to mature.
- What conditions punish their architecture: trajectory churn that outpaces the record.

The experience gap is moderate and it leverages Bona, whose recognition of opposing patterns arrives sooner.

## Environmental Precondition Check

### Player A: Alice
- Standard winning path: impose pace and close points early off a clean first strike.
- Precondition that path requires: clean mechanical timing.
- Granted or denied? GRANTED
- Surviving path (only if denied): N/A
- Observable for the surviving path: N/A

### Player B: Bona
- Standard winning path: archive the opponent and exploit confirmed patterns.
- Precondition that path requires: time for patterns to repeat.
- Granted or denied? GRANTED
- Surviving path (only if denied): N/A
- Observable for the surviving path: N/A

## Collision & Live Frame Breakdown

- Player A (Alice) is trying to: change the trajectory before the archive matures.
- Player B (Bona) is trying to: turn Alice's behavior into record.

**The Predictable Misread:** Bona may mistake a response for a pattern.

## Trajectory Resolution

- The match favors Player A (Alice) if: the trajectory keeps changing before the record can be used.
- The match favors Player B (Bona) if: Alice's patterns become repeatable enough to be archived.

**Trajectory Call:** Directional toward Alice — conditional on the trajectory continuing to change before Bona's archive matures, verified at the Section 6 checkpoints.
"""
