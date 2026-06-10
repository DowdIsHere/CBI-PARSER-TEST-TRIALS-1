"""Load order is fixed; placement layer stays out of the runtime; Part 2
expansions are verbatim."""

import pytest

from cbi_widget.modules import READ_ENGINE_ORDER, REFERENCE_FILES, load_read_engine
from cbi_widget.part2 import Part2Index, UnknownProfileError
from cbi_widget.placements import Placement


def test_fixed_load_order(root):
    modules = load_read_engine(root)
    assert [m.name for m in modules] == [
        "role_layer",
        "playbook_v2_1",
        "environmental_precondition",
        "input_asymmetry",
        "intake_template",
        "match_read_template",
        "drift_guard",
    ]
    # Seven separate modules — never one blob.
    assert len(modules) == 7
    assert len({m.text for m in modules}) == 7


def test_placement_layer_not_in_runtime_order():
    runtime_files = {f for _, f in READ_ENGINE_ORDER}
    reference_files = {f for _, f in REFERENCE_FILES}
    assert runtime_files.isdisjoint(reference_files)
    assert "CBI_Parser_Sourcing_Protocol.md" in reference_files
    assert "Parser_Print_Identifier_Part2_FULL.md" in reference_files


def test_part2_has_all_27_profiles(root):
    index = Part2Index.load(root)
    assert len(index._by_triple) == 27


def test_expansion_is_verbatim(root):
    index = Part2Index.load(root)
    seasoned = Placement(
        player="X", spatial="Concrete", temporal="Past", reference="Balanced",
        provenance={},
    )
    text = index.expand(seasoned)
    assert text.startswith("## SEASONED — Concrete · Past · Balanced")
    # Verbatim: the expansion is an exact slice of the source document.
    source = (root / "Parser_Print_Identifier_Part2_FULL.md").read_text()
    assert text.rstrip() in source
    assert index.profile_name(seasoned) == "SEASONED"


def test_unknown_triple_stops_instead_of_deriving(root):
    index = Part2Index.load(root)
    # Forge an impossible triple by bypassing axis validation.
    bogus = Placement.__new__(Placement)
    object.__setattr__(bogus, "player", "X")
    object.__setattr__(bogus, "spatial", "Quantum")
    object.__setattr__(bogus, "temporal", "Past")
    object.__setattr__(bogus, "reference", "Self")
    object.__setattr__(bogus, "provenance", {})
    with pytest.raises(UnknownProfileError):
        index.expand(bogus)
