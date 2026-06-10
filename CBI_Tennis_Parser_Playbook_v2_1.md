# CBI Tennis Parser Behavior Playbook
**Version 2.1**

*V2.1 changes from V2.0: Step 2 conditions checklist revised (weather→surface sequencing; reward and punish scored separately; experience reframed as magnitude-and-leverage). New Section 6: Trajectory Restoration Checkpoints. New Section 7: What "Decisive" Means. The Ordering (Profile → Conditions → Parser) named at the top of the Core Rule. Step 1 Parser-sourcing relocated upstream: the Parser is fixed and cannot drift; how a placement is sourced and defended lives in the Parser Sourcing Protocol (control / volume-across-variation / independence), and the read engine consumes a supplied placement — it never places one. These name and correct the structure the existing rules already rested on. All V2.0 collision rules and core logic are unchanged — V2 is gospel.*

---

## The Ordering (read first)

Three layers, in this order, feeding forward:

**Profile → Conditions → Parser**

- **Profile is the person.** The fixed, measurable picture of who this player is, independent of any match — the H2H dossier: record, handedness, tendencies, mechanics, physical reality. Identity-level data.
- **Conditions are the environment.** What the person is situated in right now — surface, weather, altitude, ball state, score state, fatigue, the opponent's hand. The world the person is standing in, not the person.
- **The Parser is what this person, in this environment, will do at any given time.** It is the *output* of the first two layers, not a fourth input beside them.

The Parser is **downstream**. Profile and Conditions are inputs that feed it; they cannot override it, because they are what it is made from. Asking whether the surface, the ranking, or the physics "beats" the Parser is a category error — they express *through* the Parser, never around it.

This is why the rules below hold:
- The Profile stays separate from the Parser verdict because it is an *input layer*, not the behavioral read. A Profile fact that becomes the verdict ("she's higher-ranked, she wins") has skipped the two transformations that matter.
- Conditions reward or punish but never *identify* the Parser, because conditions are the *middle* layer — they shape how the orientation expresses, they do not create or replace it.
- A Profile fact matters only if it survives the trip through conditions into "what this person will do here, now." Rankings and favorite-status rarely survive; legibility trend, rally-length, and pressure-point drift do, because they change what the Parser will do next.

"At any given time" is literal: as conditions drift across a match, the same Profile run through changed conditions yields a changed Parser expression. Each checkpoint re-runs the pipeline — same person, updated environment, recompute the behavior. The live readouts that track this (rally length, legibility trend, pressure-point drift) are not a layer — they are the instrument that tells you how far the Profile-through-Conditions expression has progressed.

---

## Core Rule

A Parser is not determined by age, stats, ranking, surface, handedness, or score.

Those are conditions.

A Parser describes the oriented portion of reality that becomes available first.

Once the Parser is known, conditions become predictive.

- **Parser identity** tells you what becomes available.
- **Conditions** tell you how costly that orientation becomes.
- **The opposing Parser** tells you where the misread will happen.

---

## 1. Parser to Tennis Behavior Mapping

### Reference

**Self = Force Game**

The player organizes from their own game. They impose rhythm, pressure, patterns, shot selection, or pace.

*Question:* "What can I make happen?"

---

**Other = Play Other's Game**

The player organizes around the opponent. They read the opponent's discomfort, habits, openings, reactions, and vulnerabilities.

*Question:* "What are you showing me?"

---

**Balanced = The Flow**

The player organizes through the exchange itself. They are not purely imposing or reacting. They move with the match as it develops.

*Question:* "What is the point asking for now?"

*Distinction from Calculated:* The Flow operates in the **live exchange** — it reads what the rally is becoming as it unfolds. Calculated operates in **possibility space** — it weighs what could work given the full situation. The Flow is present-tense engagement; Calculated is situational anticipation. They can look similar from the outside but resolve differently under pressure: The Flow stays inside the moment; Calculated steps back to assess.

---

### Temporal

**Future = Proactive**

The player acts before the thing fully arrives. They move toward what is forming.

*Question:* "Where is this going?"

---

**Past = Reactive**

The player works from what has already happened. They use record, pattern, repetition, proof, and prior response.

*Question:* "What has already shown itself?"

---

**Present = Vibing**

The player is inside the live moment. They feel timing, rhythm, current cues, and immediate flow.

*Question:* "What is happening right now?"

---

### Spatial

**Abstract = Ambitious**

The player sees what could open before it is fully visible. They play toward possibility.

*Question:* "What can this become?"

*Risk:* They may try to open the future before the court has earned it.

---

**Balanced = Calculated**

The player considers what is and what is possible given the circumstances. This includes surface, lefty/righty matchup, experience, fatigue, score pressure, current rhythm, opponent tendencies, and match constraints.

*Question:* "Given the full situation, what can work from here?"

*Strength:* Calculated players often have exits. They can shift without becoming chaotic.

---

**Concrete = Chess Player**

The player works from confirmed circumstances. They use established patterns, confirmed responses, known positions, proven weaknesses, and reliable sequences.

*Question:* "Given what has been confirmed, what sequence follows?"

*Risk:* Chess Player needs the board to remain stable long enough for the sequence to mature.

---

## 2. How to Read a Match

### Step 1: Start with the known Parser

Do not build the Parser from stats.

Use the known profile first.

**Where the Parser comes from.**

The Parser is fixed. It cannot drift — not within a match under fatigue or score pressure, and not across years. What looks like drift is never the Parser moving; it is the same fixed Parser expressing through changed conditions. This is *why* conditions can mimic: the print is rigid, so when behavior shifts, it was conditions bending the expression, never the print bending itself.

The Parser arrives at this Playbook as a **supplied placement** — identified upstream via the Parser Print Identifier manual under the Parser Sourcing Protocol, and declared by the user. The read engine starts from the supplied Parser and expands it using that profile's print (Part 2 of the manual). It never places a Parser itself — not from match behavior, stats, ranking, style, surface, handedness, age, or score. If either player's Parser has not been supplied, stop and request it before reading.

How a placement is sourced and defended lives in one place only: the Parser Sourcing Protocol. It sits upstream of this Playbook and is not re-run, re-derived, or second-guessed at read time.

Example:

- Abstract • Future • Self = Ambitious • Proactive • Force Game
- Concrete • Past • Other = Chess Player • Reactive • Play Other's Game

---

### Step 2: Add the conditions

Conditions do not identify the Parser. They pressure the Parser.

Establish the surface's live state first, then ask what that state does to each Parser. Reward and punishment are scored **separately** — the same surface can do both to the same player.

Ask:

- **Does the weather affect the surface?**
 Heat, humidity, wind, and sun change how the surface plays before they change anything about the player. Establish the surface's actual live state for this match before reading anything else. A "clay court" in cool damp air and a "clay court" baking in afternoon heat are two different surfaces.

- **Does the surface and surface conditions reward the Parser's behavior?**
 Given the live surface state, does this orientation get paid off? Where does the surface hand this Parser its preferred reality?

- **Does the surface and surface conditions punish the Parser's behavior?**
 Given the live surface state, does this orientation become expensive? Score this independently of reward. A surface can reward a Parser's weapon and punish a different part of the same Parser's behavior at the same time. Do not collapse reward and punishment into a single "favors X" verdict — that collapse is where false reads come from.

- **Does the opponent's hand disrupt it?**
 Lefty/righty asymmetry, and whether the opponent's handedness specifically attacks the wing this Parser depends on.

- **Does the score make the Parser's normal move expensive?**
 At the current or anticipated score state, does the Parser's natural move cost more than it usually does?

- **How much experience does each player have, and how much weight does it give them?**
 Experience is not a yes/no question. Of course experience helps. The real question is the size of the gap and which player it leverages. More experience means more weight behind delivering their own Parser, AND faster recognition of the opponent's game when they see it — which enables quicker adjustment. Read the experience gap as a magnitude and a direction, never as a checkbox.

- **Does fatigue make the Parser overuse its strength?**
 Under accumulated load, does the Parser lean harder on its dominant axis in a way that becomes legible or self-defeating?

---

### Step 3: Predict the misread

The misread is not random. It comes from Parser-vs-Parser orientation.

Ask:

- What will this player think the opponent is doing?
- What part of the opponent's behavior will become visible first?
- What causal piece might they miss?
- Are they mistaking a response for a pattern?
- Are they waiting for a behavior they were previously causing?

---

### Step 4: Watch the causal loop

The scoreboard is noise unless it connects to the loop.

The real question is:

- Who is causing the other player to shift?
- Does the other player know what caused the shift?
- Has the player adapted, or are they solving the previous version of the match?

---

## 3. Temporal Collision Rules

### Future vs Past

Future moves with trajectory. Past turns behavior into record.

- **Future wins when:** The trajectory keeps changing before the Past player can use the record.
- **Past wins when:** The Future player's patterns become repeatable enough to be archived.

*Clean line:* Past can catch Future only when Future leaves enough history.

---

### Future vs Present

Future sees where the match is going. Present feels what is happening now.

- **Future wins when:** The match moves before the Present player can act on the cue.
- **Present wins when:** The Future player leaks enough live evidence to be caught.

*Clean line:* Present cannot see the future, but it can catch the traces forming now.

---

### Past vs Present

Past uses what has already been confirmed. Present moves with the live moment.

- **Past wins when:** The present keeps repeating known patterns.
- **Present wins when:** The live situation contradicts the record.

*Clean line:* Past owns repetition. Present owns the moment when repetition breaks.

---

### Same-Temporal Matches

When both players share temporal orientation, the temporal dimension becomes invisible. The match resolves on Spatial and Reference. This is where pure cognitive architecture shows clearest — neither player has temporal advantage, so the misread has to come from somewhere else.

---

## 4. Spatial Collision Rules

### Ambitious vs Chess Player (Abstract vs Concrete)

Ambitious changes the trajectory. Chess Player builds from confirmed sequences.

- **Ambitious wins when:** The board changes before the sequence matures.
- **Chess Player wins when:** Ambition becomes repeatable enough to confirm.

*Clean line:* Chess Player can solve the board. Ambitious keeps changing what the board is becoming.

---

### Ambitious vs Calculated (Abstract vs Balanced)

Ambitious sees what could become possible. Calculated sees what is possible given the circumstances.

- **Ambitious wins when:** The player expands the match beyond the current constraints.
- **Calculated wins when:** The player knows which possibilities are actually playable under the conditions.

*Clean line:* Ambitious opens futures. Calculated knows which futures survive contact.

---

### Calculated vs Chess Player (Balanced vs Concrete)

Calculated considers the whole situation. Chess Player works from confirmed facts.

- **Calculated wins when:** The player changes the equation before the confirmed sequence completes.
- **Chess Player wins when:** The player locks the match into proven cause-and-effect.

*Clean line:* Calculated has exits. Chess Player has sequences.

---

### Same-Spatial Matches

When both players share spatial orientation, the spatial dimension becomes invisible. Two Ambitious players play a match of escalating possibility. Two Chess Players play a match of confirmed sequences. Two Calculated players play a match of mutual exits. The decisive friction shifts to Temporal and Reference.

---

## 5. Reference Collision Rules

### Force Game vs Play Other's Game (Self vs Other)

Force Game imposes. Play Other's Game reads.

- **Force Game wins when:** The imposed pressure creates more than the opponent can organize.
- **Play Other's Game wins when:** The imposed pressure becomes readable.

*Clean line:* Self creates the problem. Other tries to make the problem readable.

---

### Force Game vs The Flow (Self vs Balanced)

Force Game tries to shape the match. The Flow moves with the match.

- **Force Game wins when:** The player's pressure becomes the match structure.
- **The Flow wins when:** The match refuses to stay inside the forced structure.

*Clean line:* Self tries to own the match. Flow waits for the match to stop belonging to Self.

---

### Play Other's Game vs The Flow (Other vs Balanced)

Play Other's Game needs an opponent to read. The Flow does not always give a stable target.

- **Play Other's Game wins when:** The opponent becomes consistent enough to map.
- **The Flow wins when:** The match keeps changing without giving the Other player a fixed person-pattern to exploit.

*Clean line:* Other reads the player. Flow reads the exchange.

---

### Same-Reference Matches

When both players share reference orientation, the reference dimension becomes invisible. Two Force Game players play a match of mutual imposition — whoever's pressure structures the match wins. Two Play Other's Game players play a match of mutual reading — whoever stays illegible longer wins. Two Flow players play a match where the rally itself becomes the player. The decisive friction shifts to Temporal and Spatial.

---

## 6. Trajectory Restoration Checkpoints

*(New in V2.1)*

The collision rules tell you who holds the trajectory. They do not, by themselves, tell you when the trajectory has actually shifted versus when the scoreboard is just noisy. Restoration checkpoints close that gap.

A restoration checkpoint is a score state where you verify whether the prescribed pattern is still holding. At each checkpoint, the read either:

- **Confirms** — the architecture asserted where the collision predicted it would. Trajectory holds.
- **Falsifies** — the trajectory broke where it should not have. The pattern did not hold.

For each checkpoint, name what the trailing player must do to restore the trajectory. If they cannot do the named architectural move, the trajectory locks for the leader. If they can, the trajectory is live again.

The restoration move is always an **architectural** move — something the trailing Parser must do that its orientation makes available — not a generic "play better" or "serve bigger."

### How to write checkpoints for a match

For the specific collision in front of you, write the checkpoints that matter. Examples of the form (fill in the architectural move per the actual Parsers):

- **If P1 wins set 1:** To restore the trajectory, P2 must [specific architectural move their Parser makes available — e.g., for a Reader: force the rally length out far enough that the archive matures; for The Flow: break the forced structure P1 has imposed]. If P2 cannot, the trajectory locks for P1.

- **If P2 leads set 2 by 2+ games (a lead of ≥2, not a single break that can be traded back):** The trajectory has shifted toward P2. To recover it, P1 must [architectural move]. A one-game or single-break lead is noise; a 2+ game lead is a checkpoint.

- **At the first deciding-set break point:** This is the highest-value checkpoint. Whoever holds the trajectory here, under maximum pressure, is asserting the architecture exactly where the collision predicted. Name which player the read says should win this point, and watch whether they do.

- **After any momentum cluster (3+ consecutive games):** Confirm whether the cluster tracks the predicted collision (pattern holding) or runs against it (pattern breaking). A cluster that runs against the read is a falsification signal, not a fluke to be explained away.

### The rule for lead sizes

- A **single break / one-game lead** is tradeable. It is not yet a trajectory shift. Do not call a checkpoint on it.
- A **2+ game lead (≥2)** is a checkpoint. The trajectory has moved and must be actively restored, not merely traded back.

---

## 7. What "Decisive" Means

*(New in V2.1)*

"Decisive" is a claim about a **pattern holding**, not about the margin.

A close, back-and-forth match can be decisive — if a prescribed pattern holds throughout. The decisiveness lives in the pattern, not in the scoreline gap.

- A 7-6, 6-7, 7-6 match where one player keeps holding trajectory at exactly the pressure points the collision predicts, and the other keeps failing to convert at the moments the read says they will fail, **is decisive.** The architecture is winning the match point by point precisely where it is supposed to. The closeness is the surface; the pattern underneath is decisive.

- A close match where the lead oscillates **without tracking the predicted collision** — where the player the read called favored keeps losing trajectory at the points they were supposed to own — is **not decisive, and the oscillation is the falsification signal.** The back-and-forth that does not follow the pattern is evidence the read was wrong.

So the question that separates a real "decisive" call from a wrong one is never "was the match close?" It is:

> **Did the prescribed pattern hold at every checkpoint where the collision predicted it would?**

### Why close matches are the proving ground

A blowout tells you almost nothing about whether the pattern holds under pressure, because there was no pressure. A 7-6 third set decided by the prescribed pattern reasserting at every break point is the strongest possible confirmation the read was right — it gave the most checkpoints under the most pressure, and the pattern held through all of them.

### The red flag

If a read produces a strong directional word and the match then oscillates back and forth **without the pattern reasserting at the checkpoints**, treat that as falsification in progress, not as variance. Do not retrofit the read to explain the oscillation. The pattern either held at the checkpoints or it did not.

---

## 8. Match Read Template

Use this for every match.

### Player A

**Parser:** Spatial • Temporal • Reference

**Tennis behavior:**
- Ambitious / Calculated / Chess Player
- Proactive / Reactive / Vibing
- Force Game / Play Other's Game / The Flow

**What becomes available first:** "…"

**What they are likely to do under pressure:** "…"

**What they may miss:** "…"

**What conditions amplify their architecture:** "…"

**What conditions punish their architecture:** "…"

---

### Player B

**Parser:** Spatial • Temporal • Reference

**Tennis behavior:**
- Ambitious / Calculated / Chess Player
- Proactive / Reactive / Vibing
- Force Game / Play Other's Game / The Flow

**What becomes available first:** "…"

**What they are likely to do under pressure:** "…"

**What they may miss:** "…"

**What conditions amplify their architecture:** "…"

**What conditions punish their architecture:** "…"

---

### Collision

**Player A is trying to:** "…"

**Player B is trying to:** "…"

**The predictable misread:** "…"

**The match favors Player A if:** "…"

**The match favors Player B if:** "…"

**Trajectory call:** "…" *(directional and conditional — no probability number)*

**Restoration checkpoints:** *(per Section 6 — name the checkpoints and the architectural move required at each)*

---

## 9. Core Warnings

**Do not say:**

- "He is young, so he is Future."
- "She plays clay, so she is Concrete."
- "He is ranked higher, so he is Calculated."
- "She is left-handed, so she is Chess Player."

Those are not Parser reads.

**Say instead:**

Given the known Parser, these conditions may reward or punish the behavior.

**Also do not:**

- Output a probability percentage. V2 reads are directional and conditional.
- Compare the read to a market price unless explicitly asked.
- Collapse "reward" and "punish" into a single "favors X" verdict.
- Treat experience as a yes/no checkbox.
- Call a single break or one-game lead a trajectory shift.

---

## 10. Cleanest Summary

- Parser identity is architecture.
- Parser behavior is architecture under pressure.
- Conditions shape expression — establish the surface's live state first, then score reward and punishment separately.
- Opponent Parser predicts the misread.
- Trajectory shifts are verified at checkpoints; a 2+ game lead is a checkpoint, a single break is noise.
- "Decisive" means the pattern held at every checkpoint, not that the margin was large.
- The match resolves when one player's Parser is operating in conditions that reward it AND they understand the causal loop the opponent is missing AND the prescribed pattern holds through the checkpoints.

---

*CBI Tennis Parser Behavior Playbook v2.1*
*Developed by J.D. Mercer | Based on the Cognition Blocks Intelligence (CBI) Framework*
*© 2026 Cognition Blocks LLC. All rights reserved.*
