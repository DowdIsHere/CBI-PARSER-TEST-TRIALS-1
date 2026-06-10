"""Command-line surface for the CBI Tennis Parser Widget.

Commands:
  declare   Record a user-declared placement (with provenance) in the store.
  show      List declared placements.
  read      Run a match read (read-only text output).
  log it    Append the LAST read to the tracker — the only way anything is
            ever logged.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .engine import LiveFrame, ReadEngine, ReadResult
from .model import AnthropicAdapter
from .placements import MissingParserError, Placement, PlacementStore, presence_gate
from .tracker import log_it

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STORE_PATH = DATA / "placements.json"
LAST_READ_PATH = DATA / "last_read.md"
TRACKER_PATH = DATA / "tracker.jsonl"


def _parse_score(score: str) -> LiveFrame:
    """Manual score entry, e.g. '6-4 2-1' (last pair = current set games)."""
    pairs = re.findall(r"(\d+)\s*-\s*(\d+)", score)
    current = (int(pairs[-1][0]), int(pairs[-1][1])) if pairs else None
    return LiveFrame(description=score, current_set_games=current)


def cmd_declare(args: argparse.Namespace) -> int:
    store = PlacementStore(STORE_PATH)
    provenance = {
        "method": args.method,
        "tier": args.tier,
        "domains": args.domains.split(",") if args.domains else [],
        "date": args.date,
        "declared_by": args.declared_by,
    }
    store.declare(
        Placement(
            player=args.player,
            spatial=args.spatial,
            temporal=args.temporal,
            reference=args.reference,
            provenance=provenance,
        )
    )
    print(f"Declared: {args.player} = {args.spatial} • {args.temporal} • {args.reference} "
          f"({args.tier}, via {args.method})")
    return 0


def cmd_show(_args: argparse.Namespace) -> int:
    store = PlacementStore(STORE_PATH)
    if not STORE_PATH.is_file():
        print("No placements declared yet.")
        return 0
    print(json.dumps(json.loads(STORE_PATH.read_text()), indent=2))
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    store = PlacementStore(STORE_PATH)
    # The input contract runs before anything else — including before the
    # model adapter exists. Parser absent -> STOP and ask; no read runs.
    try:
        presence_gate(store, args.player_a, args.player_b)
    except MissingParserError as e:
        print(str(e))
        return 2
    intake_text = Path(args.intake).read_text() if args.intake else ""
    live_frame = _parse_score(args.score) if args.score else None
    engine = ReadEngine(root=ROOT, store=store, model=AnthropicAdapter(model=args.model))
    try:
        result: ReadResult = engine.run_read(
            player_a=args.player_a,
            player_b=args.player_b,
            intake_text=intake_text,
            conditions=args.conditions,
            live_frame=live_frame,
            market_requested=args.with_market,
        )
    except MissingParserError as e:
        print(str(e))
        return 2
    print(result.text)
    if result.status == "ok":
        DATA.mkdir(parents=True, exist_ok=True)
        LAST_READ_PATH.write_text(result.text)
    return 0 if result.status == "ok" else 3


def cmd_log(args: argparse.Namespace) -> int:
    # Logging happens only on the literal instruction "log it".
    if args.what != "it":
        print("Logging happens only on the literal instruction: log it")
        return 2
    if not LAST_READ_PATH.is_file():
        print("Nothing to log — no read has been produced this session.")
        return 2
    log_it(TRACKER_PATH, LAST_READ_PATH.read_text(), note=args.note)
    print(f"Logged to {TRACKER_PATH}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cbi", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("declare", help="record a user-declared placement")
    p.add_argument("--player", required=True)
    p.add_argument("--spatial", required=True, choices=["Concrete", "Balanced", "Abstract"])
    p.add_argument("--temporal", required=True, choices=["Past", "Present", "Future"])
    p.add_argument("--reference", required=True, choices=["Self", "Balanced", "Other"])
    p.add_argument("--method", required=True,
                   choices=["control", "volume-across-variation", "independence"],
                   help="the defended sourcing mechanism (Parser Sourcing Protocol)")
    p.add_argument("--tier", required=True, choices=["PROVISIONAL", "CORROBORATED", "LOCKED"])
    p.add_argument("--domains", default="", help="comma-separated evidence domains")
    p.add_argument("--date", default="")
    p.add_argument("--declared-by", default="")
    p.set_defaults(func=cmd_declare)

    p = sub.add_parser("show", help="list declared placements")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("read", help="run a match read (read-only output)")
    p.add_argument("--player-a", required=True)
    p.add_argument("--player-b", required=True)
    p.add_argument("--intake", help="path to a completed intake sheet")
    p.add_argument("--conditions", required=True,
                   help="live surface/weather state, e.g. 'red clay, cool damp evening'")
    p.add_argument("--score", help="manual live-frame entry, e.g. '6-4 2-1'")
    p.add_argument("--with-market", action="store_true",
                   help="explicitly request a market comparison this turn")
    p.add_argument("--model", default="claude-opus-4-8")
    p.set_defaults(func=cmd_read)

    p = sub.add_parser("log", help='append the last read to the tracker ("log it" only)')
    p.add_argument("what", help="must be the literal word: it")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_log)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
