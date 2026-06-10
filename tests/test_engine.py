"""End-to-end read flow with a scripted model: gate, separate passes,
regeneration, and the uncertain-stopping state."""

import json

import pytest

from cbi_widget.engine import LiveFrame, ReadEngine
from cbi_widget.model import ScriptedModel
from cbi_widget.placements import MissingParserError
from cbi_widget.tracker import log_it
from tests.conftest import CLEAN_VERDICT, INTAKE_SECTIONS

RAW_INTAKE = """\
H2H 1-1. Alice 24, hard-courter. Bona 29, clay grinder. MARKER-XYZZY
Bona is ranked 48 places higher and won their last meeting in straight sets.
**Current Intel:** Bona seeded 3rd and priced as the clear front-runner.
"""


def _engine(root, store, outputs):
    return ReadEngine(root=root, store=store, model=ScriptedModel(outputs))


def test_missing_parser_refuses_despite_rich_in_match_signal(root, store):
    # Rich intake (ranking, prior result, style, age) — none of it is a
    # licence to place a Parser. The tool stops before any model call.
    model = ScriptedModel([])
    engine = ReadEngine(root=root, store=store, model=model)
    with pytest.raises(MissingParserError):
        engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    assert model.calls == []  # no read pass ever ran


def test_clean_read_passes_gate_first_try(root, declared_store):
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, CLEAN_VERDICT])
    result = engine.run_read(
        "Alice", "Bona", RAW_INTAKE, conditions="indoor hard, still air",
        live_frame=LiveFrame(description="6-4 2-1", current_set_games=(2, 1)),
    )
    assert result.status == "ok"
    assert result.guard_report.passed
    assert "CBI Playbook Analysis: Alice vs. Bona" in result.text


def test_modules_load_order_reaches_the_model(root, declared_store):
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, CLEAN_VERDICT])
    engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    for call in engine.model.calls:
        assert call["module_names"] == [
            "role_layer", "playbook_v2_1", "environmental_precondition",
            "input_asymmetry", "intake_template", "match_read_template",
            "drift_guard",
        ]


def test_intake_does_not_leak_into_verdict_pass(root, declared_store):
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, CLEAN_VERDICT])
    engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    intake_call, verdict_call = engine.model.calls
    assert "MARKER-XYZZY" in intake_call["user_prompt"]
    # The verdict pass never sees the raw intake — separate passes.
    assert "MARKER-XYZZY" not in verdict_call["user_prompt"]
    assert "ranked 48 places" not in verdict_call["user_prompt"]


def test_declared_placement_expanded_verbatim_in_verdict_pass(root, declared_store):
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, CLEAN_VERDICT])
    engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    verdict_prompt = engine.model.calls[1]["user_prompt"]
    # Alice declared Abstract•Future•Self -> VISIONARY; Bona Concrete•Past•Other -> LEGACY.
    assert "## VISIONARY — Abstract · Future · Self" in verdict_prompt
    assert "## LEGACY — Concrete · Past · Other" in verdict_prompt
    # Verbatim slices of the manual, not paraphrases.
    part2 = (root / "Parser_Print_Identifier_Part2_FULL.md").read_text()
    for placement, heading in (("VISIONARY", "## VISIONARY"), ("LEGACY", "## LEGACY")):
        start = verdict_prompt.index(heading)
        excerpt = verdict_prompt[start:start + 400]
        assert excerpt in part2


def test_dirty_draft_is_regenerated_then_ships_clean(root, declared_store):
    dirty = CLEAN_VERDICT + "\nAlice wins this 64% of the time.\n"
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, dirty, CLEAN_VERDICT])
    result = engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    assert result.status == "ok"
    assert "64%" not in result.text
    # The regeneration instruction quoted the drift guard, not a patch request.
    second_verdict_prompt = engine.model.calls[2]["user_prompt"]
    assert "DRIFT GUARD" in second_verdict_prompt
    assert "regenerate the whole read clean" in second_verdict_prompt.lower()


def test_streak_reference_never_ships(root, declared_store):
    dirty = CLEAN_VERDICT + "\nOur last 3 reads were right, so lean harder here.\n"
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, dirty, CLEAN_VERDICT])
    result = engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    assert result.status == "ok"
    assert "reads were right" not in result.text


def test_single_break_shift_claim_never_ships(root, declared_store):
    dirty = CLEAN_VERDICT + "\nThe trajectory has shifted to Alice.\n"
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, dirty, CLEAN_VERDICT])
    result = engine.run_read(
        "Alice", "Bona", RAW_INTAKE, conditions="indoor hard",
        live_frame=LiveFrame(description="3-2 on serve", current_set_games=(3, 2)),
    )
    assert result.status == "ok"
    assert "trajectory has shifted" not in result.text


def test_three_contaminated_drafts_surface_uncertain_stopping(root, declared_store):
    dirty = CLEAN_VERDICT + "\nAlice wins this 64% of the time.\n"
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, dirty, dirty, dirty])
    result = engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    assert result.status == "uncertain"
    assert "UNCERTAIN — STOPPING" in result.text
    assert "64%" not in result.text.split("Last failures")[0]


def test_logging_is_manual_only(root, declared_store, tmp_path):
    engine = _engine(root, declared_store, [INTAKE_SECTIONS, CLEAN_VERDICT])
    result = engine.run_read("Alice", "Bona", RAW_INTAKE, conditions="indoor hard")
    tracker = tmp_path / "tracker.jsonl"
    # The read itself wrote nothing.
    assert not tracker.exists()
    # Only the explicit instruction writes a row.
    log_it(tracker, result.text, note="log it")
    rows = [json.loads(line) for line in tracker.read_text().splitlines()]
    assert len(rows) == 1
    assert "CBI Playbook Analysis" in rows[0]["read"]
