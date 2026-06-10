# CBI Tennis Parser Widget

An execution tool, not an analysis assistant. It takes two **user-supplied
Parser placements** plus a completed intake sheet, applies the CBI Tennis
Parser Behavior Playbook v2.1 exactly as written, and emits a directional,
conditional Match Read.

Built to the contract in `CBI_ClaudeCode_Build_Prompt.md`. The ten source
documents in the repository root are the logic — this code never rewrites,
merges, or "improves" them.

## Architecture

```
cbi_widget/
  modules.py      Seven read-engine docs loaded as SEPARATE modules, fixed order:
                  Role Layer → Playbook v2.1 → Environmental Precondition →
                  Input Asymmetry → Intake template → Match Read template →
                  Drift Guard. The three placement-layer docs (Sourcing
                  Protocol, Parts 0–1, Part 2) are reference-only — never in
                  the runtime load order.
  placements.py   External placement store (data/placements.json) + the
                  presence gate. Placements arrive only by user declaration;
                  provenance travels with them but is never adjudicated.
  part2.py        Expands a declared placement into its Part 2 profile print,
                  VERBATIM. Never identifies or places a Parser.
  drift_guard.py  The 13-check pre-emit gate. Every check is mechanical — a
                  string or structural fact. Pass-all or regenerate.
  engine.py       The read flow: presence gate → verbatim expansion →
                  intake pass and verdict pass as SEPARATE model passes
                  (raw intake never enters the verdict pass) → drift guard →
                  ship, regenerate, or "uncertain — stopping".
  model.py        Model adapters. The Anthropic adapter sends one system text
                  block per module, in order — separation preserved at the
                  API level. ScriptedModel is the test double.
  tracker.py      Manual logging. Called only by the literal "log it".
  cli.py          declare / show / read / log it.
```

## The three load-bearing frames

1. **Role layer.** The model is an executor of the Playbook, not an evaluator
   of it. The engine never surfaces past results to the model; the drift
   guard fails any draft that leans on a streak or prior record.
2. **Input contract — refusal is a feature.** The gate checks PRESENCE, not
   quality. Parser supplied → run. Parser absent → STOP and ask (before the
   model adapter is even constructed). The read engine never places a Parser
   from match behavior, stats, ranking, style, surface, handedness, age, or
   score, and never re-derives a declared placement (drift check 4 verifies
   the shipped draft states the placements exactly as declared).
3. **Drift guard.** Thirteen mechanical checks run against the engine's own
   draft before anything is emitted. A failed check discards the draft and
   regenerates clean (the failure list is quoted to the model as the guard's
   own instruction, not as a patch request). Three contaminated drafts in a
   row trip the meta-check: the tool surfaces "UNCERTAIN — STOPPING" instead
   of shipping.

## Runtime decisions (from the build checklist)

- **Placements + provenance** live in `data/placements.json` — an external
  store the read reads, not the match. Declared via `cbi declare`, with the
  sourcing method (control / volume-across-variation / independence), tier,
  domains, and date recorded as given.
- **Live frame** is manual score entry (`--score "6-4 2-1"`). The last pair
  is the current set; it feeds the checkpoint logic (a 2+ game lead is a
  checkpoint, a single break is noise).
- **Logging is manual.** Only the literal `cbi log it` writes a tracker row
  (`data/tracker.jsonl`). The engine never logs, never proposes logging.
- **Output surface** is read-only text. The only write on command is the
  tracker, on "log it".

## Usage

```sh
# Declare placements (identified upstream via the Parser Print Identifier
# manual under the Parser Sourcing Protocol — the widget does not source).
python3 -m cbi_widget.cli declare --player "Hugo Grenier" \
  --spatial Concrete --temporal Past --reference Balanced \
  --method independence --tier CORROBORATED \
  --domains "speech,tactical" --date 2026-06-01 --declared-by Robert

# Run a read (requires ANTHROPIC_API_KEY; refuses first if a Parser is missing).
python3 -m cbi_widget.cli read --player-a "Hugo Grenier" --player-b "Other Player" \
  --intake intake.md --conditions "red clay, cool damp evening" --score "6-4 2-1"

# Log the last read — only on the literal instruction.
python3 -m cbi_widget.cli log it --note "post-match"
```

## Tests

```sh
python3 -m pytest tests/
```

The suite covers the build prompt's pre-trust checklist: missing-Parser
refusal (with no model call), no streak references shipped, probability %
caught and regenerated, single-break leads never called as trajectory
shifts, reward/punish kept as separate findings, intake never blended into
the verdict pass or sections, choked-path calls forced onto the surviving
path with its observable named, humidity-as-court-speed rejected, verbatim
Part 2 expansion of declared placements, fixed module load order, and
manual-only logging.
