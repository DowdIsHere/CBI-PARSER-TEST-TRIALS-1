"""The input contract: refusal is a feature. Presence, not quality."""

import pytest

from cbi_widget.placements import (
    MissingParserError,
    Placement,
    PlacementStore,
    presence_gate,
)


def test_missing_both_parsers_refuses(store):
    with pytest.raises(MissingParserError) as exc:
        presence_gate(store, "Alice", "Bona")
    assert "Alice and Bona" in str(exc.value)
    assert "no read is produced" in str(exc.value)
    # The refusal names every banned inference source.
    for banned in ("match behavior", "stats", "ranking", "style", "surface",
                   "handedness", "age", "score"):
        assert banned in str(exc.value)


def test_missing_one_parser_refuses_and_names_it(store, placement_a):
    store.declare(placement_a)
    with pytest.raises(MissingParserError) as exc:
        presence_gate(store, "Alice", "Bona")
    assert exc.value.players == ["Bona"]


def test_both_present_passes_through_as_given(declared_store, placement_a, placement_b):
    a, b = presence_gate(declared_store, "Alice", "Bona")
    assert a.triple == placement_a.triple
    assert b.triple == placement_b.triple
    # Provenance travels with the placement, unadjudicated: a sub-LOCKED
    # tier does not gate the read.
    assert b.provenance["tier"] == "CORROBORATED"


def test_gate_checks_presence_not_quality(store):
    # Even a PROVISIONAL single-domain placement passes the gate — quality
    # consequences are the human's, applied at declaration/logging time.
    store.declare(Placement(
        player="Alice", spatial="Balanced", temporal="Present", reference="Balanced",
        provenance={"method": "control", "tier": "PROVISIONAL", "domains": ["speech"]},
    ))
    store.declare(Placement(
        player="Bona", spatial="Concrete", temporal="Past", reference="Self",
        provenance={"method": "independence", "tier": "LOCKED"},
    ))
    a, b = presence_gate(store, "Alice", "Bona")
    assert a.provenance["tier"] == "PROVISIONAL"


def test_invalid_axis_value_is_rejected_at_declaration(store):
    with pytest.raises(ValueError):
        store.declare(Placement(
            player="Alice", spatial="Fast", temporal="Past", reference="Self",
            provenance={},
        ))
