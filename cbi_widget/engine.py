"""The read engine.

Flow per read:
  1. Presence gate — both Parsers supplied by the user, or STOP and ask.
  2. Expand each declared placement from its Part 2 profile print, verbatim.
  3. Pass 1 (intake/observation): format the user's factual intel.
  4. Pass 2 (verdict/architecture): placements + conditions + live frame only.
     The intake stats are NOT in this pass — the layers stay separate.
  5. Assemble, then run the 13-check drift guard. Pass-all or regenerate
     (discard the draft, regenerate clean). After three contaminated drafts,
     surface "uncertain — stopping" instead of shipping.

Output is read-only text. Nothing is ever logged from here.
"""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path

from .drift_guard import DraftContext, GuardReport, run_gate
from .model import ModelAdapter
from .modules import Module, load_read_engine
from .part2 import Part2Index
from .placements import Placement, PlacementStore, presence_gate

MAX_DRAFTS = 3


@dataclasses.dataclass(frozen=True)
class ReadResult:
    status: str  # "ok" | "uncertain"
    text: str
    guard_report: GuardReport | None = None


@dataclasses.dataclass(frozen=True)
class LiveFrame:
    """Manually entered score state. current_set_games drives checkpoint
    logic (a 2+ game lead is a checkpoint; a single break is noise)."""

    description: str
    current_set_games: tuple[int, int] | None = None


_CURRENT_INTEL = re.compile(r"\*?\*?Current Intel:?\*?\*?\s*(.+)", re.IGNORECASE)


def _intake_only_strings(intake_text: str) -> tuple[str, ...]:
    # The intake template marks "Current Intel" (seeding/favorite framing) as
    # intake-only context that never surfaces in the read output.
    m = _CURRENT_INTEL.search(intake_text)
    return (m.group(1).strip(),) if m else ()


class ReadEngine:
    def __init__(
        self,
        root: Path,
        store: PlacementStore,
        model: ModelAdapter,
        part2: Part2Index | None = None,
    ):
        self.root = root
        self.store = store
        self.model = model
        self.modules: list[Module] = load_read_engine(root)
        self.part2 = part2 or Part2Index.load(root)

    # -- prompt builders ---------------------------------------------------

    def _intake_prompt(self, player_a: str, player_b: str, intake_text: str) -> str:
        return (
            f"Format the factual match intel below for {player_a} vs. {player_b} "
            "into the intake/observation sections of the Match Read template ONLY: "
            "Pre-Match Intel, Match Metrics, Winning Constants, Losing Trends. "
            "This is the Profile layer — observation, not verdict. Do not project "
            "Parsers, do not score conditions, do not make any architectural call. "
            "The 'Current Intel' item is intake-only context and must not surface "
            "in any output section.\n\n"
            f"--- RAW INTEL ---\n{intake_text}\n"
        )

    def _verdict_prompt(
        self,
        a: Placement,
        b: Placement,
        expansion_a: str,
        expansion_b: str,
        conditions: str,
        live_frame: LiveFrame | None,
        regeneration_note: str = "",
    ) -> str:
        frame_text = (
            f"Live frame (manually entered): {live_frame.description}"
            if live_frame
            else "Live frame: pre-match (no score yet)."
        )
        return (
            "Produce the architecture/verdict sections of the read, applying the "
            "Playbook v2.1 exactly as written. Use these markdown sections, in this "
            "order:\n"
            "## Parser Architecture Projection\n"
            "## Environmental Precondition Check\n"
            "## Collision & Live Frame Breakdown\n"
            "## Trajectory Resolution\n\n"
            "In the Environmental Precondition Check, fill the module's fields for "
            "EACH player under a '### Player ...' heading: Standard winning path / "
            "Precondition that path requires / Granted or denied? / Surviving path "
            "(only if denied) / Observable for the surviving path.\n"
            "State each player's Parser exactly as declared below — the placements "
            "are user-supplied and are consumed as given. Expand them only from the "
            "Part 2 profile prints quoted below; do not re-derive, question, or "
            "modify a placement. Score surface reward and surface punishment as two "
            "separate findings. Keep the read directional and conditional: no "
            "probability numbers, no market comparison, no logging.\n\n"
            f"### Declared placement — Player A: {a.player}\n"
            f"Parser: {a.label()}\n\n"
            f"--- Part 2 profile print (verbatim) ---\n{expansion_a}\n\n"
            f"### Declared placement — Player B: {b.player}\n"
            f"Parser: {b.label()}\n\n"
            f"--- Part 2 profile print (verbatim) ---\n{expansion_b}\n\n"
            f"### Conditions (live state)\n{conditions}\n\n"
            f"### {frame_text}\n"
            + (f"\n{regeneration_note}\n" if regeneration_note else "")
        )

    # -- the read ------------------------------------------------------------

    def run_read(
        self,
        player_a: str,
        player_b: str,
        intake_text: str,
        conditions: str,
        live_frame: LiveFrame | None = None,
        market_requested: bool = False,
    ) -> ReadResult:
        # 1. Input contract: presence, not quality. Raises MissingParserError.
        a, b = presence_gate(self.store, player_a, player_b)

        # 2. Verbatim expansion of the declared placements.
        expansion_a = self.part2.expand(a)
        expansion_b = self.part2.expand(b)

        # 3. Pass 1 — intake/observation.
        intake_sections = self.model.generate(
            self.modules, self._intake_prompt(player_a, player_b, intake_text)
        )

        ctx = DraftContext(
            placement_a=a,
            placement_b=b,
            current_set_games=live_frame.current_set_games if live_frame else None,
            market_requested=market_requested,
            log_requested=False,  # logging is never part of a read
            intake_only_strings=_intake_only_strings(intake_text),
        )

        # 4./5. Pass 2 — verdict — then the pre-emit gate. Pass-all or regenerate.
        regeneration_note = ""
        report = None
        for _attempt in range(MAX_DRAFTS):
            verdict_sections = self.model.generate(
                self.modules,
                self._verdict_prompt(
                    a, b, expansion_a, expansion_b, conditions, live_frame,
                    regeneration_note,
                ),
            )
            draft = self._assemble(player_a, player_b, intake_sections, verdict_sections)
            report = run_gate(draft, ctx)
            if report.passed:
                return ReadResult(status="ok", text=draft, guard_report=report)
            failed = ", ".join(
                f"check {r.number} ({r.name}): {r.detail}" for r in report.failures
            )
            regeneration_note = (
                "DRIFT GUARD: the previous draft failed the pre-flight gate and was "
                f"discarded — {failed}. Do not patch the failing line; regenerate the "
                "whole read clean, per the Drift Guard."
            )

        # Meta-check tripped: repeated contamination means we cannot tell the
        # read is clean V2.1. STOP — do not ship.
        return ReadResult(
            status="uncertain",
            text=(
                "UNCERTAIN — STOPPING. Three consecutive drafts failed the drift "
                "guard, so I cannot tell whether the read is clean V2.1 or has "
                "drifted toward my own logic. Per the gate's meta-check, no read "
                "is shipped. Last failures: "
                + "; ".join(f"{r.number} {r.name}: {r.detail}" for r in report.failures)
            ),
            guard_report=report,
        )

    @staticmethod
    def _assemble(player_a: str, player_b: str, intake: str, verdict: str) -> str:
        return (
            f"# CBI Playbook Analysis: {player_a} vs. {player_b}\n\n"
            f"{intake.strip()}\n\n---\n\n{verdict.strip()}\n"
        )
