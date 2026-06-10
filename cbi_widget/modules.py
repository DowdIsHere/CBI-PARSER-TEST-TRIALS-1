"""Module loader for the CBI read engine.

The seven read-engine documents are loaded as SEPARATE, named context
modules in a fixed order. They are never concatenated into one blob —
the separation is the architecture. The three placement-layer documents
are available as reference only and are never wired into the runtime
load order.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

# Fixed runtime load order. Do not reorder, merge, or extend.
READ_ENGINE_ORDER: tuple[tuple[str, str], ...] = (
    ("role_layer", "CBI_Role_Layer.md"),
    ("playbook_v2_1", "CBI_Tennis_Parser_Playbook_v2_1.md"),
    ("environmental_precondition", "CBI_Environmental_Precondition_Module.md"),
    ("input_asymmetry", "CBI_Input_Asymmetry_Principle.md"),
    ("intake_template", "CBI_Intel_Intake_Template.md"),
    ("match_read_template", "CBI_Match_Read_Template.md"),
    ("drift_guard", "CBI_Drift_Guard.md"),
)

# Upstream placement layer — reference/consultation only. NOT in the load order.
REFERENCE_FILES: tuple[tuple[str, str], ...] = (
    ("parser_sourcing_protocol", "CBI_Parser_Sourcing_Protocol.md"),
    ("print_identifier_part0_1", "Parser_Print_Identifier_Part0_Part1_DRAFT.md"),
    ("print_identifier_part2", "Parser_Print_Identifier_Part2_FULL.md"),
)


@dataclasses.dataclass(frozen=True)
class Module:
    name: str
    path: Path
    text: str


def load_read_engine(root: Path) -> list[Module]:
    """Load the seven read-engine documents as distinct modules, in order.

    Returns a list — one Module per document. Callers must pass these to the
    model as separate blocks; never join them into a single string.
    """
    modules = []
    for name, filename in READ_ENGINE_ORDER:
        path = root / filename
        if not path.is_file():
            raise FileNotFoundError(
                f"Read-engine module '{name}' missing: {path}. "
                "All seven source files must be present before any read runs."
            )
        modules.append(Module(name=name, path=path, text=path.read_text()))
    return modules


def load_reference(root: Path, name: str) -> Module:
    """Load one placement-layer reference document on demand."""
    for ref_name, filename in REFERENCE_FILES:
        if ref_name == name:
            path = root / filename
            if not path.is_file():
                raise FileNotFoundError(f"Reference document missing: {path}")
            return Module(name=name, path=path, text=path.read_text())
    raise KeyError(f"Unknown reference document: {name}")
