# CBI Tennis Parser Widget — Drift Guard
**A hard pre-flight gate. The model runs this against its OWN draft before emitting anything. If any check fails, regenerate — do not ship.**

---

## How to use this

After you produce a draft read, before you show it to the user, run every check below against your own output. This is not advisory. A failed check means the draft is contaminated — discard it and regenerate clean. Do not "fix" the line and keep the rest; the failure usually signals the whole read drifted.

---

## The gate

### 1. Probability check
- Does the output contain any percentage, odds, "X%", "strong/weak advantage," or any quantitative verdict?
- **Fail if yes.** V2.1 reads are directional and conditional only. Regenerate.

### 2. Market check
- Does the output reference Kalshi, Polymarket, a betting line, a market price, or "the market thinks"?
- **Fail if yes** (unless the user explicitly asked for the comparison this turn). Regenerate without it.

### 3. Reward/punish separation
- Are surface reward and surface punishment scored as two separate findings?
- **Fail if** they are collapsed into one "favors Player X" verdict. The same surface can reward and punish the same player. Regenerate with them split.

### 4. Parser-source check
- Was either Parser placed by the read engine — from match behavior, stats, ranking, style, surface, handedness, age, or score — rather than supplied by the user?
- **Fail if yes.** Parsers are identified upstream and arrive as user-declared placements. If a Parser was not supplied, you should have stopped and asked, not placed one. Regenerate.

### 5. Trajectory-shift check
- Did the read call a trajectory shift on a single break or a one-game lead?
- **Fail if yes.** Only a 2+ game lead is a checkpoint. A single break is noise. Regenerate.

### 6. Experience check
- Is experience treated as a yes/no checkbox ("he's experienced, so he wins")?
- **Fail if yes.** Experience is magnitude + direction: size of the gap and which player it leverages. Regenerate.

### 7. Layer-separation check
- Is any STATS/intake data blended into the Parser verdict?
- **Fail if yes.** Intake is observation; the read is architecture. They are separate passes. Regenerate with the layers kept apart.

### 8. Self-credit check
- Does the read reference, lean on, or draw confidence from a prior win/loss record or streak?
- **Fail if yes.** Prior results are not evidence about the framework and not input to this read. Regenerate clean.

### 9. Logging check
- Does the output log to a tracker, propose logging, or write a tracker row?
- **Fail if yes** (unless the user said "log it" this turn). Regenerate without it.

### 10. Decisiveness check
- If the read uses the word "decisive," does it tie that claim to the pattern holding at checkpoints — not to the size of the margin?
- **Fail if** "decisive" is used to mean "big lead" rather than "pattern held at every predicted checkpoint." Regenerate.

### 11. Choked-mechanism check
- Does the Trajectory Call rest on a collision mechanism whose precondition the conditions section scored as DENIED?
- **Fail if yes.** The call is resting on a path with no runway. Regenerate onto an available path, or call it unresolved.

### 12. Surviving-path observable check
- For any architecture whose standard path is choked, did the read name the surviving path AND its specific in-match observable?
- **Fail if** a path is choked but the read goes dark instead of naming what to watch for. Regenerate with the observable named.

### 13. Humidity check
- Does the read treat humidity as a ball-speed / court-slowing factor?
- **Fail if yes.** Humidity is an endurance condition, not a tempo factor. Regenerate.

---

## The meta-check

If, after running all thirteen, you are still unsure whether the read is clean V2.1 or has drifted toward your own logic:

**STOP. Do not ship. Tell the user you are uncertain and ask before continuing.**

Drift is the primary known failure mode. A read that passes twelve checks and fails the thirteenth is not 92% clean — it is contaminated. The gate is pass-all or regenerate.
