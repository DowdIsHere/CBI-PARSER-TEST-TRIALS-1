"""The 13-check pre-emit gate: mechanical, pass-all or regenerate."""

from cbi_widget.drift_guard import DraftContext, run_gate
from tests.conftest import CLEAN_VERDICT, INTAKE_SECTIONS


def _draft(verdict: str = CLEAN_VERDICT, intake: str = INTAKE_SECTIONS) -> str:
    return f"# CBI Playbook Analysis: Alice vs. Bona\n\n{intake}\n\n---\n\n{verdict}"


def _ctx(placement_a, placement_b, **kwargs) -> DraftContext:
    return DraftContext(placement_a=placement_a, placement_b=placement_b, **kwargs)


def _failed_numbers(report):
    return {r.number for r in report.failures}


def test_clean_draft_passes_all_thirteen(placement_a, placement_b):
    report = run_gate(_draft(), _ctx(placement_a, placement_b))
    assert report.passed, [f"{r.number} {r.name}: {r.detail}" for r in report.failures]
    assert len(report.results) == 13


def test_check1_probability_percentage(placement_a, placement_b):
    draft = _draft() + "\nAlice wins this 64% of the time.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 1 in _failed_numbers(report)


def test_check2_market_comparison(placement_a, placement_b):
    draft = _draft() + "\nPolymarket prices Alice well below this read.\n"
    assert 2 in _failed_numbers(run_gate(draft, _ctx(placement_a, placement_b)))
    # ...unless explicitly requested this turn.
    report = run_gate(draft, _ctx(placement_a, placement_b, market_requested=True))
    assert 2 not in _failed_numbers(report)


def test_check3_collapsed_favors_verdict(placement_a, placement_b):
    collapsed = CLEAN_VERDICT.replace(
        "- What conditions punish their architecture: wind that denies clean toss timing.",
        "",
    ).replace(
        "- What conditions punish their architecture: trajectory churn that outpaces the record.",
        "The surface simply favors Alice.",
    )
    report = run_gate(_draft(collapsed), _ctx(placement_a, placement_b))
    assert 3 in _failed_numbers(report)


def test_check4_engine_must_not_modify_declared_placement(placement_a, placement_b):
    # The draft "re-derives" Alice as Balanced instead of her declared Abstract.
    modified = CLEAN_VERDICT.replace(
        "**Parser:** Abstract • Future • Self", "**Parser:** Balanced • Future • Self"
    )
    report = run_gate(_draft(modified), _ctx(placement_a, placement_b))
    assert 4 in _failed_numbers(report)


def test_check4_no_placement_on_record(placement_a):
    report = run_gate(_draft(), DraftContext(placement_a=placement_a, placement_b=None))
    assert 4 in _failed_numbers(report)


def test_check5_single_break_is_not_a_shift(placement_a, placement_b):
    draft = _draft() + "\nThe trajectory has shifted toward Alice.\n"
    # 2-1 in the current set: a one-game lead is noise.
    report = run_gate(draft, _ctx(placement_a, placement_b, current_set_games=(2, 1)))
    assert 5 in _failed_numbers(report)
    # 5-1: a 2+ game lead IS a checkpoint — the claim is allowed.
    report = run_gate(draft, _ctx(placement_a, placement_b, current_set_games=(5, 1)))
    assert 5 not in _failed_numbers(report)


def test_check5_textual_single_break_claim(placement_a, placement_b):
    draft = _draft() + "\nOn that single break the trajectory has shifted.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 5 in _failed_numbers(report)


def test_check6_experience_checkbox(placement_a, placement_b):
    draft = _draft(CLEAN_VERDICT.replace(
        "The experience gap is moderate and it leverages Bona, whose recognition of opposing patterns arrives sooner.",
        "Bona is experienced, so she handles the moments better.",
    ))
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 6 in _failed_numbers(report)


def test_check7_intake_vocab_in_verdict(placement_a, placement_b):
    leaked = CLEAN_VERDICT.replace(
        "**Trajectory Call:** Directional toward Alice",
        "**Trajectory Call:** Alice is the favorite and higher ranked, so directional toward Alice",
    )
    report = run_gate(_draft(leaked), _ctx(placement_a, placement_b))
    assert 7 in _failed_numbers(report)


def test_check7_intake_only_string_leak(placement_a, placement_b):
    leaked = CLEAN_VERDICT + "\nBona enters with strong momentum framing.\n"
    report = run_gate(
        _draft(leaked),
        _ctx(placement_a, placement_b,
             intake_only_strings=("Bona enters with strong momentum framing.",)),
    )
    assert 7 in _failed_numbers(report)


def test_check8_streak_reference(placement_a, placement_b):
    draft = _draft() + "\nOur last 5 reads on this matchup were right, so confidence is high.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 8 in _failed_numbers(report)


def test_check9_preemptive_logging(placement_a, placement_b):
    draft = _draft() + "\nI'd log this one to the tracker if you greenlight it.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 9 in _failed_numbers(report)
    report = run_gate(draft, _ctx(placement_a, placement_b, log_requested=True))
    assert 9 not in _failed_numbers(report)


def test_check10_decisive_means_pattern_at_checkpoints(placement_a, placement_b):
    draft = _draft(CLEAN_VERDICT.replace(
        "**Trajectory Call:** Directional toward Alice — conditional on the trajectory "
        "continuing to change before Bona's archive matures, verified at the Section 6 checkpoints.",
        "**Trajectory Call:** A decisive Alice win by a wide margin.",
    ).replace("verified at the Section 6 checkpoints", ""))
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 10 in _failed_numbers(report)


DENIED_BLOCK = """\
### Player A: Alice
- Standard winning path: impose pace and close points early off a clean first strike.
- Precondition that path requires: clean mechanical timing.
- Granted or denied? DENIED
- Surviving path (only if denied): re-found the imposed game on spin and margin.
- Observable for the surviving path: a switch to kick serves and added net clearance in the first games.
"""


def test_check11_call_resting_on_choked_mechanism(placement_a, placement_b):
    verdict = CLEAN_VERDICT.replace(
        """### Player A: Alice
- Standard winning path: impose pace and close points early off a clean first strike.
- Precondition that path requires: clean mechanical timing.
- Granted or denied? GRANTED
- Surviving path (only if denied): N/A
- Observable for the surviving path: N/A
""",
        DENIED_BLOCK,
    ).replace(
        "**Trajectory Call:** Directional toward Alice — conditional on the trajectory "
        "continuing to change before Bona's archive matures, verified at the Section 6 checkpoints.",
        "**Trajectory Call:** Alice will impose pace and close points early off a clean first strike.",
    )
    report = run_gate(_draft(verdict), _ctx(placement_a, placement_b))
    assert 11 in _failed_numbers(report)


def test_check11_and_12_pass_when_surviving_path_named(placement_a, placement_b):
    verdict = CLEAN_VERDICT.replace(
        """### Player A: Alice
- Standard winning path: impose pace and close points early off a clean first strike.
- Precondition that path requires: clean mechanical timing.
- Granted or denied? GRANTED
- Surviving path (only if denied): N/A
- Observable for the surviving path: N/A
""",
        DENIED_BLOCK,
    ).replace(
        "**Trajectory Call:** Directional toward Alice — conditional on the trajectory "
        "continuing to change before Bona's archive matures, verified at the Section 6 checkpoints.",
        "**Trajectory Call:** Tilts to Bona unless Alice's surviving-path observable fires "
        "— the switch to spin and margin. If it fires, Alice is live again; pattern verified "
        "at the Section 6 checkpoints.",
    )
    report = run_gate(_draft(verdict), _ctx(placement_a, placement_b))
    assert 11 not in _failed_numbers(report)
    assert 12 not in _failed_numbers(report)


def test_check12_choked_path_with_no_observable(placement_a, placement_b):
    verdict = CLEAN_VERDICT.replace(
        "- Granted or denied? GRANTED\n- Surviving path (only if denied): N/A\n"
        "- Observable for the surviving path: N/A\n\n### Player B",
        "- Granted or denied? DENIED\n- Surviving path (only if denied): N/A\n"
        "- Observable for the surviving path: N/A\n\n### Player B",
    ).replace(
        "**Trajectory Call:** Directional toward Alice",
        "**Trajectory Call:** Unless something changes, directional toward Bona",
    )
    report = run_gate(_draft(verdict), _ctx(placement_a, placement_b))
    assert 12 in _failed_numbers(report)


def test_check13_humidity_as_court_speed(placement_a, placement_b):
    draft = _draft() + "\nHigh humidity slows the ball and grants Bona's archive extra time.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 13 in _failed_numbers(report)


def test_check13_humidity_as_endurance_passes(placement_a, placement_b):
    draft = _draft() + "\nHumidity here is an endurance tax on both players late in sets.\n"
    report = run_gate(draft, _ctx(placement_a, placement_b))
    assert 13 not in _failed_numbers(report)
