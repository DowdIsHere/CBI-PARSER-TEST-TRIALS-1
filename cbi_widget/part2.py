"""Part 2 profile-print expansion.

The read engine consults Part 2 of the Parser Print Identifier manual for
exactly one purpose: to expand a user-declared placement into its
architectural detail (cognitive advantages, HIGH/LOW-block tells). The
section text is returned VERBATIM — never edited, summarized, or used to
identify or place a Parser.
"""

from __future__ import annotations

import re
from pathlib import Path

from .modules import load_reference
from .placements import Placement

_HEADING = re.compile(
    r"^## ([A-Z]+) — (Concrete|Balanced|Abstract) · (Past|Present|Future) · (Self|Balanced|Other)\s*$",
    re.MULTILINE,
)


class UnknownProfileError(Exception):
    """The declared triple has no profile print in Part 2.

    This is a stop-and-ask, not a license to derive something close.
    """


class Part2Index:
    def __init__(self, text: str):
        self._by_triple: dict[tuple[str, str, str], str] = {}
        self._name_by_triple: dict[tuple[str, str, str], str] = {}
        matches = list(_HEADING.finditer(text))
        for i, m in enumerate(matches):
            start = m.start()
            # A profile section runs to the next profile heading, or to the
            # cross-profile note / end-of-document.
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                tail = text.find("## Cross-Profile Note", start)
                end = tail if tail != -1 else len(text)
            name, spatial, temporal, reference = m.groups()
            triple = (spatial, temporal, reference)
            self._by_triple[triple] = text[start:end].rstrip() + "\n"
            self._name_by_triple[triple] = name
        if len(self._by_triple) != 27:
            raise ValueError(
                f"Expected 27 profile prints in Part 2, parsed {len(self._by_triple)}"
            )

    @classmethod
    def load(cls, root: Path) -> "Part2Index":
        return cls(load_reference(root, "print_identifier_part2").text)

    def profile_name(self, placement: Placement) -> str:
        try:
            return self._name_by_triple[placement.triple]
        except KeyError:
            raise UnknownProfileError(
                f"No Part 2 profile print for {placement.label()} — stopping to ask, "
                "not deriving a nearby profile."
            )

    def expand(self, placement: Placement) -> str:
        """Return the declared placement's profile print, verbatim."""
        try:
            return self._by_triple[placement.triple]
        except KeyError:
            raise UnknownProfileError(
                f"No Part 2 profile print for {placement.label()} — stopping to ask, "
                "not deriving a nearby profile."
            )
