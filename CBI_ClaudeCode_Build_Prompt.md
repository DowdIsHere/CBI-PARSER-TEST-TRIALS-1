# Build Prompt for Claude Code — CBI Tennis Parser Widget

Paste this as your opening instruction to Claude Code. All ten source files
listed below should be in the project directory before you start.

---

## What you are building

A CBI Tennis Parser plugin that takes two user-supplied Parser placements
plus a completed intake sheet, applies the CBI Tennis Parser Behavior Playbook
v2.1 exactly as written, and emits a directional, conditional Match Read. It is
an execution tool, not an analysis assistant.

## Source files (already in the project — do not rewrite their logic)

**Read engine (the widget's runtime — fixed load order):**
1. `CBI_Role_Layer.md` — the frame: executor, not evaluator
2. `CBI_Tennis_Parser_Playbook_v2_1.md` — the operating logic (opens with the Ordering: Profile → Conditions → Parser)
3. `CBI_Environmental_Precondition_Module.md` — V2.1 extension of Step 2 + Trajectory Call (precondition check, surviving-path logic, humidity correction, drift checks 11–13)
4. `CBI_Input_Asymmetry_Principle.md` — V2.1 companion: reaction-map vs. archive, Parsers-on-24/7, the Future↔Past resolution mechanism
5. `CBI_Intel_Intake_Template.md` — factual/historical intake (the Profile layer)
6. `CBI_Match_Read_Template.md` — the verdict layer (mirrors Section 8 of the Playbook)
7. `CBI_Drift_Guard.md` — the pre-flight exit gate (13 checks)

**Upstream placement layer (reference and consultation only — NOT wired into the read engine):**
8. `CBI_Parser_Sourcing_Protocol.md` — how a Parser is identified and declared BEFORE the read
9. `Parser_Print_Identifier_Part0_Part1_DRAFT.md` — the universal print layer (Part 1 governs)
10. `Parser_Print_Identifier_Part2_FULL.md` — the 27 profile prints. The read engine consults this ONLY to expand a user-declared placement into its architectural detail (cognitive advantages, HIGH/LOW-block tells). It never uses it to identify or place a Parser.

## Hard constraints — read before writing any code

### 1. Keep the files SEPARATE. Do not merge them.
The role layer, the Playbook, the templates, and the drift guard are distinct
on purpose. Do NOT collapse them into one prompt blob "for convenience." The
separation is the architecture. If you find yourself combining them, stop.

### 2. Load order is fixed and must be enforced at runtime:
   Role Layer → Playbook v2.1 (opens with the Ordering) → Environmental Precondition Module → Input Asymmetry Principle → Intake template → Match Read template → Drift Guard (exit gate)
The Role Layer sits ABOVE the Playbook — it is the frame the Playbook runs
inside, not a rule within it. The placement-layer files (8–10) are NOT in the
runtime load order: Part 2 is consulted only to expand a user-declared
placement into its profile detail; the Sourcing Protocol and Parts 0–1 are
used only when the user explicitly runs a placement consultation, never at
read time.

### 3. Keep the drift guard DUMB on purpose.
Every check in the drift guard is mechanical — a string or structural fact
verifiable without opinion. Do NOT add checks that ask the model to judge
whether a read is "good" or high-quality. The moment a check requires evaluating
read quality, you have reopened the door to the model's own logic, which is the
exact thing this tool exists to keep out.

### 4. The input contract is a refusal, not a fallback.
Both Parsers arrive as user-supplied placements, identified upstream via the
Parser Print Identifier manual under the Parser Sourcing Protocol. The gate
checks PRESENCE, not quality: if either player's Parser has not been supplied,
the tool STOPS and asks. It never places a Parser itself — not from match
behavior, stats, ranking, style, surface, handedness, age, or score — and it
never adjudicates, re-derives, or second-guesses a placement the user has
declared. Build the refusal as a hard gate before any read runs.

### 5. The model is an executor, not an analyst.
Prior outputs and any win/loss streak are NOT evidence about the framework and
must not influence a read. Do not build any feature that surfaces past results
to the model at read time. The streak is not the model's data.

### 6. No probability numbers, no market comparison, no preemptive logging.
Reads are directional and conditional. No percentages, no "strong advantage,"
no Kalshi/Polymarket/line comparison unless the user explicitly asks this turn.
Logging happens only on the literal instruction "log it" — never proposed,
never preemptive.

## Build steps

1. Scaffold the plugin with the seven read-engine files loaded as separate,
   distinct context modules in the fixed order above, and the three
   placement-layer files available as reference only.
2. Implement the input contract as a pre-read gate: verify both Parsers have
   been supplied by the user; if either is missing, halt and request it.
   Presence only — do not evaluate the placement.
3. Wire the read flow: intake (observation) and Parser verdict (architecture)
   as SEPARATE passes — intake data must not leak into the verdict.
4. Implement the drift guard as a pre-emit gate: run all thirteen checks against
   the draft; pass-all or regenerate. Surface a "uncertain — stopping" state if
   the meta-check trips.
5. Output surface: read-only text by default. Tracker writes only on "log it."

## Tests to write and pass before calling it done

- Missing Parser → tool refuses and asks; does not place one from any in-match
  signal (behavior, stats, ranking, style, surface, handedness, age, score).
- A matchup the model has "seen win before" → output contains zero reference to
  any prior record or streak.
- A draft containing a probability % → drift guard catches it and regenerates.
- A single-break lead → tool does NOT call a trajectory shift (2+ games only).
- Reward and punish on the same surface → reported as two separate findings,
  never collapsed into "favors X."
- Intake/STATS data → never blended into the Parser verdict.
- A surface that chokes one Parser's standard winning path → call does NOT rest on
  the choked mechanism; read names the surviving path AND its in-match observable.
- Humidity in the intake → treated as an endurance condition, never as a
  court-slowing / ball-speed factor.
- A Past player leading early against a Future player → read does NOT treat the
  early lead as a confirmed pattern; watches legibility trend, not the scoreboard;
  reaches for input-asymmetry before environment when the lead evaporates.
- A declared placement → read engine expands it from Part 2's profile print
  without re-deriving, questioning, or modifying the placement.
- The read engine never sources its own Parser; placements arrive pre-declared
  by the user (provenance travels with the placement but is never adjudicated
  at read time).

## What NOT to do

- Do not improve, extend, or "modernize" the Playbook logic. Apply it verbatim.
- Do not merge the role layer into the Playbook.
- Do not add quality-judgment checks to the drift guard.
- Do not add a probability output, a confidence score, or a market overlay.
- Do not build auto-logging or "I'd log this if you greenlight" behavior.
- If unsure whether a feature respects the framework or inserts your own logic:
  ask before building it. Drift is the primary known failure mode.
