# CBI Tennis Parser Widget — Build Inputs Checklist

*This checklist summarizes the package. Where it abbreviates, the named source file governs — do not build to the checklist's shorthand over the file. Full contract and load order live in CBI_ClaudeCode_Build_Prompt.md.*

## The ten source files

**Read engine (fixed load order):**
1. Role Layer — executor, not evaluator (the frame)
2. Playbook v2.1 — the operating logic; opens with the Ordering (Profile → Conditions → Parser)
3. Environmental Precondition Module — conditions transform available behavior; surviving-path logic; humidity correction
4. Input Asymmetry Principle — reaction-map vs. archive; Parsers-on-24/7; Future↔Past resolution
5. Intake template — the Profile layer (observation)
6. Match Read template — collision + trajectory (verdict)
7. Drift Guard — 13-check pre-flight exit gate

**Upstream placement layer (reference/consultation only — never wired into the read engine):**
8. Parser Sourcing Protocol — how a Parser is identified and declared BEFORE the read
9. Parser Print Identifier Parts 0–1 — the universal print layer (Part 1 governs)
10. Parser Print Identifier Part 2 — the 27 profile prints; consulted only to expand a user-declared placement into its architectural detail

## The three load-bearing frames (the fix for the prior failure)

### Role layer
- The model is an EXECUTOR of the Playbook, not an evaluator of it.
- Prior outputs and any win/loss streak are NOT evidence about the framework and must not influence the read.
- Judgment is allowed about the CONTAINER (format, delivery), never the CONTENTS (Parser verdict, collision, conditions scoring).
- The Playbook's logic IS the logic. Do not add, improve, or override.

### Input contract (refusal is a feature)
- Both Parsers arrive as user-supplied placements, identified upstream via the Parser Print Identifier manual under the Parser Sourcing Protocol.
- The gate checks PRESENCE, not quality. Parser supplied → run. Parser absent → STOP and ask.
- The read engine NEVER places a Parser itself — not from match behavior, stats, ranking, style, surface, handedness, age, or score — and never re-derives or second-guesses a declared placement.

### Drift-guard gate (13 checks, pass-all or regenerate)
Run against the model's own draft BEFORE emitting:
- [ ] No probability percentage anywhere in output
- [ ] No market / Kalshi / Polymarket comparison unless explicitly requested
- [ ] Reward and punishment scored SEPARATELY (no collapsed "favors X")
- [ ] No Parser placed by the read engine — placements are user-supplied only
- [ ] No checkpoint called on a single break / one-game lead (2+ games only)
- [ ] Experience read as magnitude + direction, never a yes/no checkbox
- [ ] Intake/Profile layer kept separate from Parser verdict
- [ ] Trajectory call is directional and conditional — no quantitative verdict
- [ ] Prior win/loss record not referenced or leaned on
- [ ] "Decisive" tied to pattern-held-at-checkpoints, not margin
- [ ] Call does not rest on a choked mechanism (precondition denied)
- [ ] Choked path → surviving-path observable named
- [ ] Humidity treated as endurance, not court-speed

## Data / runtime decisions to make
- [ ] Where do Parser placements + provenance live? (external store the read reads, not the match)
- [ ] Live frame input: manual score entry, or a feed? (affects checkpoint logic)
- [ ] Logging is MANUAL ("log it") — never preemptive, never proposed.
- [ ] Output surface: read-only text? Or writes to a tracker on command?

## Test before trusting
- [ ] Missing Parser → tool refuses and asks; does not place one from any in-match signal.
- [ ] A prior "winning" matchup → output does not reference the streak.
- [ ] A draft containing a probability % → drift gate catches it.
- [ ] A single-break lead → tool does NOT call a trajectory shift.
- [ ] A surface that chokes one Parser's path → call names the surviving-path observable, doesn't rest on the choked mechanism.
- [ ] Humidity in intake → treated as endurance, never court-speed.
- [ ] A declared placement → expanded from Part 2's profile print without re-derivation or modification.
