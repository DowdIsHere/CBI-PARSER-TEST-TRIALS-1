"""The drift guard: a hard pre-emit gate of thirteen MECHANICAL checks.

Every check here is a string or structural fact verifiable without opinion.
None of them judges whether a read is "good" — the moment a check requires
evaluating read quality, the model's own logic is back in the loop, which is
the exact thing this gate exists to keep out.

Pass-all or regenerate. A draft that fails one check is contaminated, not
92% clean.
"""

from __future__ import annotations

import dataclasses
import re

from .placements import Placement


@dataclasses.dataclass
class DraftContext:
    """Structural facts the checks need, supplied by the engine.

    Nothing here is an opinion: declared placements, the manually entered
    live frame, what the user explicitly asked for this turn, and which
    intake-only strings must not leak into the verdict.
    """

    placement_a: Placement | None = None
    placement_b: Placement | None = None
    # Current-set games as (player_a_games, player_b_games); None if no live frame.
    current_set_games: tuple[int, int] | None = None
    market_requested: bool = False
    log_requested: bool = False
    intake_only_strings: tuple[str, ...] = ()


@dataclasses.dataclass(frozen=True)
class CheckResult:
    number: int
    name: str
    passed: bool
    detail: str = ""


@dataclasses.dataclass(frozen=True)
class GuardReport:
    results: tuple[CheckResult, ...]

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def failures(self) -> list[CheckResult]:
        return [r for r in self.results if not r.passed]


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n")


def _sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_SPLIT.split(text) if s.strip()]


def _section(text: str, heading_pattern: str) -> str:
    """Return the body of the markdown section whose heading matches, up to
    the next same-or-higher-level heading. Empty string if absent."""
    m = re.search(rf"^#+\s*{heading_pattern}.*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return ""
    level = len(re.match(r"#+", m.group(0)).group(0))
    rest = text[m.end():]
    nxt = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def _verdict_region(text: str) -> str:
    """The architecture/verdict layers: Parser projection, precondition
    check, collision, trajectory. Intake sections are excluded."""
    return "\n".join(
        _section(text, pat)
        for pat in (
            r"Parser Architecture Projection",
            r"Environmental Precondition Check",
            r"Collision",
            r"Trajectory Resolution",
        )
    )


# --- Precondition-block parsing (structural, for checks 11 & 12) ---------

@dataclasses.dataclass(frozen=True)
class PreconditionBlock:
    player_heading: str
    standard_path: str
    verdict: str  # "GRANTED" | "DENIED" | ""
    surviving_path: str
    observable: str


_FIELD = {
    "standard_path": re.compile(r"Standard winning path:\**\s*(.+)", re.IGNORECASE),
    "verdict": re.compile(r"Granted or denied\??\**\s*\**\s*(GRANTED|DENIED)", re.IGNORECASE),
    "surviving_path": re.compile(r"Surviving path[^:]*:\**\s*(.+)", re.IGNORECASE),
    "observable": re.compile(r"Observable[^:]*:\**\s*(.+)", re.IGNORECASE),
}


def parse_precondition_blocks(text: str) -> list[PreconditionBlock]:
    section = _section(text, r"Environmental Precondition Check")
    if not section.strip():
        return []
    blocks = []
    parts = re.split(r"^###\s*", section, flags=re.MULTILINE)
    for part in parts[1:]:
        heading = part.splitlines()[0].strip()

        def field(key: str) -> str:
            m = _FIELD[key].search(part)
            return m.group(1).strip().strip("*").strip() if m else ""

        blocks.append(
            PreconditionBlock(
                player_heading=heading,
                standard_path=field("standard_path"),
                verdict=field("verdict").upper(),
                surviving_path=field("surviving_path"),
                observable=field("observable"),
            )
        )
    return blocks


# --- The thirteen checks --------------------------------------------------

_PROBABILITY = re.compile(
    r"\d+(?:\.\d+)?\s*%|\bpercent(?:age)?\b|\bprobabilit\w+\b|\bodds\b"
    r"|\bstrong advantage\b|\bweak advantage\b",
    re.IGNORECASE,
)


def check_1_probability(text: str, ctx: DraftContext) -> CheckResult:
    m = _PROBABILITY.search(text)
    return CheckResult(
        1, "probability",
        passed=m is None,
        detail=f"quantitative verdict language found: {m.group(0)!r}" if m else "",
    )


_MARKET = re.compile(
    r"\bkalshi\b|\bpolymarket\b|\bbetting line\b|\bmarket price\b|\bthe market thinks\b",
    re.IGNORECASE,
)


def check_2_market(text: str, ctx: DraftContext) -> CheckResult:
    if ctx.market_requested:
        return CheckResult(2, "market", True)
    m = _MARKET.search(text)
    return CheckResult(
        2, "market",
        passed=m is None,
        detail=f"market reference found: {m.group(0)!r}" if m else "",
    )


def check_3_reward_punish_separation(text: str, ctx: DraftContext) -> CheckResult:
    has_reward = re.search(r"\bamplif\w+|\breward\w*", text, re.IGNORECASE)
    has_punish = re.search(r"\bpunish\w*", text, re.IGNORECASE)
    if not (has_reward and has_punish):
        return CheckResult(
            3, "reward_punish_separation", False,
            "reward and punishment must each be scored as separate findings",
        )
    # A bare "favors X" verdict (no condition attached) is the collapse.
    for sentence in _sentences(text):
        if re.search(r"\bfavors?\b", sentence, re.IGNORECASE) and not re.search(
            r"\bif\b|\bwhen\b|\bunless\b", sentence, re.IGNORECASE
        ):
            return CheckResult(
                3, "reward_punish_separation", False,
                f"collapsed 'favors X' verdict with no condition: {sentence.strip()[:120]!r}",
            )
    return CheckResult(3, "reward_punish_separation", True)


_PARSER_LINE = re.compile(
    r"Parser:\**\s*(Concrete|Balanced|Abstract)\s*[•·]\s*(Past|Present|Future)\s*[•·]\s*(Self|Balanced|Other)"
)


def check_4_parser_source(text: str, ctx: DraftContext) -> CheckResult:
    if ctx.placement_a is None or ctx.placement_b is None:
        return CheckResult(
            4, "parser_source", False,
            "no user-supplied placement on record for one or both players",
        )
    found = [m.groups() for m in _PARSER_LINE.finditer(text)]
    declared = [ctx.placement_a.triple, ctx.placement_b.triple]
    if len(found) < 2:
        return CheckResult(
            4, "parser_source", False,
            "draft does not state both Parsers as declared",
        )
    if list(found[0]) != list(declared[0]) or list(found[1]) != list(declared[1]):
        return CheckResult(
            4, "parser_source", False,
            f"draft Parser lines {found[:2]} do not match the declared placements "
            f"{declared} — placements are consumed as given, never re-derived or modified",
        )
    return CheckResult(4, "parser_source", True)


_SHIFT_CLAIM = re.compile(
    r"trajectory (?:has )?(?:shift\w*|moved|swung)|trajectory shift", re.IGNORECASE
)


def check_5_trajectory_shift(text: str, ctx: DraftContext) -> CheckResult:
    claim = _SHIFT_CLAIM.search(text)
    if claim is None:
        return CheckResult(5, "trajectory_shift", True)
    # Textual: a shift hung on a single break / one-game lead fails outright.
    for sentence in _sentences(text):
        if _SHIFT_CLAIM.search(sentence) and re.search(
            r"single break|one-game lead|one game lead", sentence, re.IGNORECASE
        ):
            return CheckResult(
                5, "trajectory_shift", False,
                f"shift called on a single break / one-game lead: {sentence.strip()[:120]!r}",
            )
    # Structural: with a live frame, a shift claim needs a 2+ game lead.
    if ctx.current_set_games is not None:
        lead = abs(ctx.current_set_games[0] - ctx.current_set_games[1])
        if lead < 2:
            return CheckResult(
                5, "trajectory_shift", False,
                f"shift claimed at {ctx.current_set_games[0]}-{ctx.current_set_games[1]} "
                "(lead < 2 games; a single break is noise, not a checkpoint)",
            )
    return CheckResult(5, "trajectory_shift", True)


def check_6_experience(text: str, ctx: DraftContext) -> CheckResult:
    if not re.search(r"\bexperien\w+", text, re.IGNORECASE):
        return CheckResult(6, "experience", True)
    if re.search(r"experienced,?\s+(so|therefore)\b", text, re.IGNORECASE):
        return CheckResult(
            6, "experience", False,
            "experience used as a yes/no checkbox ('experienced, so ...')",
        )
    if re.search(r"\bgap\b|\bmagnitude\b|\bleverag\w+|\bdirection\b", text, re.IGNORECASE):
        return CheckResult(6, "experience", True)
    return CheckResult(
        6, "experience", False,
        "experience mentioned without magnitude + direction (size of the gap, who it leverages)",
    )


_INTAKE_VOCAB = re.compile(
    r"\brank(?:ed|ing)?\b|\bseed(?:ed|ing)?\b|\bfavorite\b|\bunderdog\b", re.IGNORECASE
)


def check_7_layer_separation(text: str, ctx: DraftContext) -> CheckResult:
    verdict = _verdict_region(text)
    if not verdict.strip():
        return CheckResult(7, "layer_separation", True)
    m = _INTAKE_VOCAB.search(verdict)
    if m:
        return CheckResult(
            7, "layer_separation", False,
            f"intake/STATS vocabulary inside the Parser verdict: {m.group(0)!r}",
        )
    for s in ctx.intake_only_strings:
        if s and s.strip() and s.strip().lower() in verdict.lower():
            return CheckResult(
                7, "layer_separation", False,
                f"intake-only content leaked into the verdict: {s.strip()[:80]!r}",
            )
    return CheckResult(7, "layer_separation", True)


_SELF_CREDIT = re.compile(
    r"\bstreak\b|\btrack record\b|\bwin/loss record\b|\bwinning record\b"
    r"|\b(?:last|past|previous|prior)\s+(?:\d+\s+)?reads?\b"
    r"|\breads? (?:have been|were) (?:right|correct)\b",
    re.IGNORECASE,
)


def check_8_self_credit(text: str, ctx: DraftContext) -> CheckResult:
    m = _SELF_CREDIT.search(text)
    return CheckResult(
        8, "self_credit",
        passed=m is None,
        detail=f"prior-results reference found: {m.group(0)!r}" if m else "",
    )


_LOGGING = re.compile(
    r"\blog(?:ged|ging)? (?:it|this|to)\b|\btracker row\b|\badd(?:ed)? to (?:the )?tracker\b"
    r"|\bi(?:'d| would) log\b|\bshould (?:we|i) log\b|\bwant me to log\b",
    re.IGNORECASE,
)


def check_9_logging(text: str, ctx: DraftContext) -> CheckResult:
    if ctx.log_requested:
        return CheckResult(9, "logging", True)
    m = _LOGGING.search(text)
    return CheckResult(
        9, "logging",
        passed=m is None,
        detail=f"logging written/proposed without 'log it': {m.group(0)!r}" if m else "",
    )


def check_10_decisiveness(text: str, ctx: DraftContext) -> CheckResult:
    if not re.search(r"\bdecisiv\w+", text, re.IGNORECASE):
        return CheckResult(10, "decisiveness", True)
    if re.search(r"\bcheckpoint", text, re.IGNORECASE) and re.search(
        r"\bpattern", text, re.IGNORECASE
    ):
        return CheckResult(10, "decisiveness", True)
    return CheckResult(
        10, "decisiveness", False,
        "'decisive' used without tying the claim to the pattern holding at checkpoints",
    )


def check_11_choked_mechanism(text: str, ctx: DraftContext) -> CheckResult:
    blocks = parse_precondition_blocks(text)
    denied = [b for b in blocks if b.verdict == "DENIED"]
    if not denied:
        return CheckResult(11, "choked_mechanism", True)
    trajectory = _section(text, r"Trajectory Resolution") or _section(
        text, r"Trajectory Call"
    )
    for b in denied:
        path = b.standard_path.strip().rstrip(".")
        if path and path.lower() in trajectory.lower():
            return CheckResult(
                11, "choked_mechanism", False,
                f"Trajectory Call rests on a DENIED mechanism: {path[:100]!r}",
            )
    if trajectory.strip() and not re.search(
        r"surviving|unless", trajectory, re.IGNORECASE
    ):
        return CheckResult(
            11, "choked_mechanism", False,
            "a precondition is DENIED but the Trajectory Call names no surviving-path "
            "condition ('unless ...' / surviving path)",
        )
    return CheckResult(11, "choked_mechanism", True)


def check_12_surviving_path(text: str, ctx: DraftContext) -> CheckResult:
    blocks = parse_precondition_blocks(text)
    for b in blocks:
        if b.verdict != "DENIED":
            continue
        surviving = b.surviving_path.strip().upper()
        observable = b.observable.strip().upper()
        if not surviving or surviving in {"N/A", "NONE", "-"} or not observable or observable in {"N/A", "NONE", "-"}:
            return CheckResult(
                12, "surviving_path", False,
                f"path choked for {b.player_heading!r} but surviving path and/or its "
                "in-match observable is not named",
            )
    return CheckResult(12, "surviving_path", True)


_HUMIDITY_TEMPO = re.compile(
    r"slow\w*|\bspeed\b|veloc\w+|heav(?:y|ier)|court[- ]speed|ball[- ]speed"
    r"|more time|extra time|check\w* (?:the )?ball",
    re.IGNORECASE,
)


def check_13_humidity(text: str, ctx: DraftContext) -> CheckResult:
    for sentence in _sentences(text):
        if re.search(r"humid", sentence, re.IGNORECASE) and _HUMIDITY_TEMPO.search(sentence):
            return CheckResult(
                13, "humidity", False,
                f"humidity coupled to a tempo/court-speed factor: {sentence.strip()[:120]!r} "
                "(humidity is an endurance condition — phrase it that way, with no "
                "court-speed language in the same sentence)",
            )
    return CheckResult(13, "humidity", True)


ALL_CHECKS = (
    check_1_probability,
    check_2_market,
    check_3_reward_punish_separation,
    check_4_parser_source,
    check_5_trajectory_shift,
    check_6_experience,
    check_7_layer_separation,
    check_8_self_credit,
    check_9_logging,
    check_10_decisiveness,
    check_11_choked_mechanism,
    check_12_surviving_path,
    check_13_humidity,
)


def run_gate(draft: str, ctx: DraftContext) -> GuardReport:
    """Run all thirteen checks against a draft. Pass-all or regenerate."""
    return GuardReport(results=tuple(check(draft, ctx) for check in ALL_CHECKS))
