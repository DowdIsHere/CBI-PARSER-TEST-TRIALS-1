# CBI Tennis Parser — Environmental Precondition Module
**V2.1 add-on. Drop-in. Does not replace any V2.1 logic — it gives Step 2's "does the surface punish the Parser?" question teeth, and converts a choked path into a named what-to-watch-for instead of a dead read.**

---

## Why this exists

A read can score the conditions correctly and still make a confident wrong call if it lets a collision rule (Section 3–5) override its own conditions scoring. The failure is not missing environment data — it is naming a punishing condition and then resting the Trajectory Call on a mechanism that condition has already shut down.

This module fixes that. Under the Ordering (Profile → Conditions → Parser), conditions are the *middle* layer: they sit between the person and the behavior and shape how the orientation expresses. So environment never "wins" the match and never overrides a Parser — it is upstream input, not a competing force. What it can do is **transform the person's available behavior so that the standard winning path does not render** — and when it does, the read narrows to the surviving path and names the observable that tells you, in-match, whether that path is live.

**This is not a gateway. A gateway auto-picks the favored player and throws away half the architecture. This keeps both Parsers fully live and converts a shut path into a watch-for.**

---

## The core principle

A collision rule states a winning *mechanism* ("Past catches Future when Future leaves enough history"). Every mechanism has a **precondition** — something the conditions layer must grant for that mechanism to render. If the live conditions deny the precondition, the mechanism has no runway. The collision rule stays true in the abstract; it simply cannot resolve as called under these conditions — because the Parser is the output of Profile *through* Conditions, and these conditions transform the output away from that path.

So before any Trajectory Call:

1. Name each architecture's **standard winning path** and the **precondition** it requires.
2. Check the live surface state: is that precondition **granted or denied**?
3. If denied, name the architecture's **surviving path** — the narrower way it can still win under hostile conditions.
4. Name the **observable** for the surviving path — the specific, watchable in-match event that tells you the choked path has reopened (or stayed shut).
5. The Trajectory Call may rest only on paths whose precondition is available. If a path is choked, the call states the surviving-path observable so that if it activates, it is already named — not improvised mid-match.

---

## Step 2 addition: the precondition check

Run this for BOTH players, after establishing the surface's live state (per existing Step 2 — weather → surface state first).

For each Parser, fill:

- **Standard winning path:** [the mechanism this architecture normally wins by]
- **Precondition that path requires:** [what the surface state must grant — e.g., time to archive, clean timing, stable board, repeatable patterns]
- **Does the live surface grant or deny it?** [granted / denied — scored against the actual live state]
- **Surviving path (only if denied):** [the narrower way this architecture can still win when its standard precondition is choked]
- **Observable for the surviving path:** [the specific watchable event that signals the surviving path is live]

The surviving path is always still an **architectural** move — something this Parser's orientation makes available — never "play better" or "get lucky."

---

## Worked example (illustrative — a genuine precondition-shut)

This example is hypothetical, built to show what a *real* precondition-shut looks like. (For why the Hanatani/Jang W15 Tokyo match is NOT a clean example of this, see the correction note below — that match looked like an environment story and turned out to be something else.)

**Live conditions:** Sustained 20+ mph crosswind, outdoor hard court. Wind is a disruption modifier, not a tempo factor — it denies clean ball-toss and clean flight timing.

### Player A — Abstract • Future • Self (Force Game, first-strike)
- **Standard winning path:** Impose pace and close points early with flat, low-margin hitting off a clean serve.
- **Precondition it requires:** Clean mechanical timing — a stable toss and predictable flight to hit flat and close to the lines.
- **Granted or denied?** DENIED. Sustained crosswind destroys the toss and pushes flat low-margin balls off-line; the first-strike path can't render reliably.
- **Surviving path:** Re-found the Force Game on *spin and margin* — kick/slice serves that don't need a high toss, heavier topspin that the wind can't push out as easily. Still imposing (Self), still proactive, but through spin rather than flat pace.
- **Observable:** Does Player A switch to spin serves and add net-clearance/margin inside the first few games, or keep going for the flat first-strike and spraying? The switch = surviving path live. Stubborn flat hitting into the wind = path stays shut.

### Player B — Balanced • Present • Balanced (The Flow)
- **Standard winning path:** Move with the live exchange, let the rally tell them what it's becoming.
- **Precondition it requires:** A live exchange to read — rallies that actually develop.
- **Granted or denied?** GRANTED. Wind extends rallies and rewards the player who stays inside the moment and adjusts shot to shot; The Flow's precondition is fully met.
- **Surviving path:** N/A — standard path available.
- **Observable:** N/A.

### Trajectory Call (clean V2.1)
Player A's flat first-strike path is shut by the wind; the call may NOT rest on "imposes pace and closes early." The read tilts to Player B (The Flow, fully enabled) **unless Player A's surviving-path observable fires** — i.e., A re-founds the Force Game on spin and margin. If A makes that architectural switch, A is live again; if A keeps forcing flat into the wind, the path stays shut.

**What to watch (named in advance):** A's serve and margin choice in the first few games. Spin + margin = surviving path live. Flat + spray = shut.

**Checkpoints (Section 6):** A single early break either way is noise. The checkpoint is whether A adapts to spin by the time the wind has been a factor for a full service rotation; failing to adapt is falsification of any call that rested on A's flat game.

---

## Correction note — why Hanatani/Jang is NOT a precondition-shut example

The W15 Tokyo match (fast indoor hard court) initially looked like a surface-choke: "the fast court denied Hanatani (Concrete/Past/Other) the time to archive." The point-by-point disproved that. Hanatani led 2-0 and 3-2 with break points beyond — she *had* time and built leads. The surface did NOT shut her path.

The real mechanism was not environmental. It was an **input-asymmetry between Future and Past** (see the companion principle): Future builds a reaction-map from response behavior, continuously and outcome-independent; Past builds an archive from confirmed patterns. Hanatani's early leads were not a pattern she established — they were response-data Jang's architecture was mapping. Hanatani's inexperience tell was mistaking a small early sample for a confirmed pattern and repeating it, which fed the map that beat her.

**Lesson for this module:** do not reach for an environment explanation when the mechanism is actually about what each architecture consumes as input. A fast court does NOT auto-shut a Reactive/Past player — that would be a coefficient in disguise (the inverse of the 1.15x error). Conditions only shut a path when they genuinely deny that architecture's *specific* precondition. Verify the precondition is actually denied (Hanatani's was not — she had time and used it to lead) before narrowing the read.

---

## Humidity correction (factual fix to existing reads)

Existing reads have listed "high-humidity environments that check ball velocity" as a condition that slows the ball and grants a reactive player time. **This is physically backwards and must not be used.** Humid air is slightly LESS dense than dry air, so it marginally *speeds* ball flight, not slows it. Humidity's real effect is a fatigue/endurance tax on the body and, only when there is genuine wetting (rain/dew), heavier balls.

- Do NOT encode humidity as a court-speed / ball-velocity factor.
- Encode humidity as an **endurance condition** (favors the fitter player; makes spin slightly harder to impart) — separate from the tempo axis.
- Genuine slow/"heavy" conditions come from cold air, high barometric pressure, wet/fluffy/worn balls, and high-friction surfaces — not from humidity.

---

## The conditions that actually move the tempo axis (reference, not coefficients)

Stated as direction only — which orientation each rewards/punishes. Scored separately, never collapsed, never numeric.

**Toward FAST / LOW / less reaction time (rewards Proactive/Force/first-strike; punishes the Reactive archive's time requirement):**
- Indoor (removes wind/sun/light variance → reproducibility)
- Heat (less dense air + livelier ball)
- Altitude / thin air (the strongest natural lever; also punishes topspin safety margin)
- Fresh, low-fluff, dry balls
- Grass and fast hard courts (low skidding bounce)

**Toward SLOW / HIGH / more reaction time (rewards Reactive/rhythm/counterpunch; grants the archive its time):**
- Cold air (denser + deader ball)
- High barometric pressure (denser air)
- Wet / fluffy / worn balls
- Clay (high friction, high bounce); freshly watered/rolled clay is slowest
- Damp / dew / evening condensation

**Disruption modifiers (NOT tempo — treat separately):**
- Wind: anti-rhythm, pro-adaptability. Punishes high tosses, flat high-risk hitting, fine net touch; rewards spin, margin, footwork, patience. Can choke a Force Game's clean-timing precondition.
- Sun/glare: localized penalty on the serve/overhead of whichever player faces it; rewards lob use.

**Within-match drift (conditions are not static):** balls fluff and slow over a set; clay dries and speeds up; grass roughens; evening cools and dampens. A read's precondition check can change validity as the match runs.

**Style-relative caveat:** "Court speed" is not absolute. A flat hitter judges speed by reaction time (friction); a topspin player judges it by bounce height (restitution). The same court is read oppositely by different architectures. Never encode a single absolute "fast/slow" verdict for a court — encode what it does to *each* Parser's precondition.

---

## Drift-guard additions

Add to the pre-flight gate. Mechanical, pass-all-or-regenerate, no quality judgment.

**Check 11 — Choked-mechanism check:**
- Does the Trajectory Call rest on a collision mechanism whose precondition the conditions section scored as DENIED?
- **Fail if yes.** The call is resting on a path with no runway. Regenerate onto an available path, or call it unresolved.

**Check 12 — Surviving-path observable check:**
- For any architecture whose standard path is choked, did the read name the surviving path AND its specific in-match observable?
- **Fail if** a path is choked but the read goes dark instead of naming what to watch for. Regenerate with the observable named.

**Check 13 — Humidity check:**
- Does the read treat humidity as a ball-speed / court-slowing factor?
- **Fail if yes.** Humidity is an endurance condition, not a tempo factor. Regenerate.
