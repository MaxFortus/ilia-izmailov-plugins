# Expert Arena: Optimizing /team-verify for Autonomy, Transparency & Resilience

> **Status:** Consensus reached
> **Date:** 2026-03-04
> **Experts:** Martin Fowler, Charity Majors, Jessie Frazelle, Dan Abramov, Nassim Taleb

---

## Verdict

The /team-verify system has sound architecture (3 parallel verifiers + orchestrator) but 9 gaps that can cause **false completion** (feature declared done without real verification), **unbounded loops** (infinite fix-retry cycles), and **silent failures** (checks lost or misrouted). The panel reached consensus on 10 core fixes and a new pipeline architecture.

**Key principle (Dan Abramov):** "The system should never auto-complete a decision the user should make, and should never declare confidence it hasn't earned."

---

## Ход дебатов

### Opening positions
- **Fowler** framed /team-verify as a Deployment Pipeline stage with Preconditions → Execution → Gating → Reporting.
- **Charity** attacked: "the system is flying blind" — demanded structured events, state machine, confidence scoring.
- **Jessie** proposed infrastructure patterns: circuit breaker, readiness probes, agent-level retry, self-healing (auto-generate missing plan).
- **Dan** focused on DX: "the problem isn't the agents — it's the transitions where the user loses control." Argued "user IS the circuit breaker."
- **Taleb** identified 4 systemic fragilities: death spiral, SKIP-as-Pass illusion, automation bias (100% confidence in 30% of risk surface), and missing BROKEN status. Used Challenger disaster analogy.

### Key confrontations

**Dan vs Everyone on "user as circuit breaker":**
- Charity countered: "User is NOT watching during 30-minute autonomous runs"
- Fowler, Jessie, Taleb piled on: pipeline needs built-in limits
- Dan conceded — accepted built-in circuit breaker, shifted to "user decides AFTER system stops"

**Charity vs Dan+Jessie on structured events:**
- Charity wanted JSON event streams + confidence scoring
- Dan: "This is a local dev tool, not production infrastructure"
- Jessie: "Agree on goals, JSON is premature"
- Charity conceded JSON events, held firm on per-check evidence
- **Converged:** structured prose with evidence (Martin's "Verification Manifest")

**Jessie vs Fowler+Taleb on self-healing:**
- Jessie proposed auto-generating missing plan from package.json
- Fowler: "Auto-generated plan gives false confidence"
- Taleb: "Never present minimal verification as full verification"
- **Jessie conceded** auto-generation, accepted fail-loud

**Taleb vs Dan on SKIP blocking:**
- Taleb: "SKIP must BLOCK completion — absence of evidence != evidence of absence"
- Dan initially resisted, then proposed UX compromise: inline AskUserQuestion by category
- **Converged:** SKIPs block with lightweight acknowledgment, grouped by category
- Fowler added: split SKIP(capability) vs SKIP(n/a) — don't block backend features on Chrome

**Fowler ↔ Charity on observability:**
- Charity pushed for audit trail; Fowler initially resisted
- Charity argued: LLM agents can hallucinate results — need integrity check
- **Fowler conceded** audit column → proposed "Verification Manifest" as lightweight implementation
- **Charity accepted** manifest over full event system

### Position changes
| Expert | Changed from | Changed to | Convinced by |
|--------|-------------|-----------|--------------|
| Dan | User is circuit breaker | Built-in limits + user decides after stop | Charity, Fowler, Jessie |
| Dan | SKIP = non-blocking | SKIP = blocking with inline ack | Taleb |
| Charity | JSON event streams | Structured prose with per-check evidence | Dan, Jessie, Fowler |
| Charity | Confidence scoring | Coverage categories with absence reporting | Taleb |
| Jessie | Auto-generate missing plan | Fail loud with actionable message | Fowler, Taleb |
| Jessie | Agent-level retry | Orchestrator-level retry | Fowler, Charity |
| Fowler | No audit trail needed | Verification Manifest | Charity |
| Taleb | Pure fail-fast on missing plan | Honest choice (minimal vs abort) | Dan (DX argument) |

---

## Consensus Recommendations (All 5 Agree)

### P0 — Must Fix

**1. Circuit breaker: 3-iteration hard cap on fix-verify loops**
- After 3 attempts, STOP and escalate to human with full retry trace
- Each iteration emits progress: "Run 2/3: fixed check-3, still failing: check-7"
- **Taleb VETO protects this** — cannot be overridden

**2. Human Checks + SKIPs block completion**
- After auto-checks complete, present outstanding items via AskUserQuestion grouped by category
- Options per category: "Verified manually" / "Not applicable" / "Need to check — pause"
- No TeamDelete until all acknowledged
- If user picks "pause" → team stays alive for re-verification

**3. BROKEN/ENVIRONMENT_ERROR status**
- New status distinct from SKIP and FAIL
- BROKEN = "environment unreliable, results meaningless" (dev server down, node_modules stale, command not found)
- Detection: ECONNREFUSED, "command not found", missing dependencies
- BROKEN blocks completion with action: "fix environment, then re-run"

**4. Expanded status taxonomy**

| Status | Meaning | Action | Blocks? |
|--------|---------|--------|---------|
| PASS | Verified successfully | Auto-proceed | No |
| FAIL | Code problem found | Fix task + re-verify | Yes |
| SKIP (capability) | System can't verify (Chrome missing) | Human must acknowledge | Yes |
| SKIP (n/a) | Check doesn't apply to this feature | Record reason, proceed | No |
| UNCLEAR | Ambiguous result | Routes to Human Checks | Yes |
| DEGRADED | Agent timed out/crashed | Retry once, then Human Checks | Yes |
| BROKEN | Environment unreliable | Fix environment, re-run all | Yes |

**5. VERIFICATION_PLAN.md missing = fail with actionable message**
- Do NOT auto-generate (gives false confidence — 3:2 against auto-generation)
- Error: "VERIFICATION_PLAN.md not found. Should have been created during Phase 1 Step 3."
- From team-feature: this indicates a bug in the planning phase

### P1 — Should Fix

**6. Pre-flight readiness check (Step 0)**
- Before spawning verifiers: check dev server health
- If not running → move browser/API checks to Human Checks with reason
- Don't try to auto-start (too many failure modes)

**7. Per-check evidence in reports**
- Each check reports: status + what was checked + what was found
- Critical for LLM-based verifiers (spec-verifier, browser-verifier) that can hallucinate
- Format: structured markdown, one line per check

**8. Verification Manifest (integrity audit)**
- Orchestrator records: sections parsed, items per section, agents spawned, items reported back
- Key line: "Items sent: 9. Items returned: 9. Delta: 0 (CONSISTENT)"
- Catches dropped or hallucinated results

**9. Strict section matching + warn on unknown**
- Keep exact `##` header matching
- Log WARNING for unrecognized sections: "Section '## Build and Types' not recognized"
- No fuzzy matching — fail loud over guess silently

**10. UNCLEAR routing to Human Checks**
- spec-verifier's UNCLEAR items route to Human Checks with context attached
- "Verifier couldn't determine: {reason}. Please verify: {check}"

### P2 — Nice to Have

**11. Progressive disclosure in reports**
- Level 0: One-line status: `PASS_WITH_CAVEATS — 10/12 passed, 2 human checks`
- Level 1: Summary table by category
- Level 2: Failure details with evidence
- Level 3: Full verification manifest

**12. Verification scope disclosure (what was NOT checked)**
- Report explicitly lists uncovered areas: "NOT verified: cross-task interactions, performance, accessibility"
- Combats automation bias — user sees boundaries of verification

**13. Run number in reports**
- Each report shows attempt N/3 for visible retry state

**14. Filter `- [x]` items during parsing**
- Only process `- [ ]` and plain `- ` items

**15. Plan format validation on write AND read**
- Validate when team-feature writes plan (shift left)
- Validate again when team-verify reads it (catch manual edits)

---

## Аргументы ЗА выбранные решения

| # | Аргумент | Кто привёл | Почему убедительно |
|---|---------|-----------|-------------------|
| 1 | Unbounded loops are fat-tail risk — each "fix" can create new failures | Taleb | Mathematical: without bounds, expected cost is infinite |
| 2 | User is NOT watching during autonomous runs — system must self-limit | Charity | Empirical: team-feature runs 20-30 min, user walks away |
| 3 | SKIP-as-Pass = Challenger disaster pattern ("noted concern" != "verified") | Taleb | Historical precedent for catastrophic failure from this exact pattern |
| 4 | LLM verifiers can hallucinate results — need evidence trail | Charity | Unique to AI agents: unlike CI tools, spec-verifier is non-deterministic |
| 5 | Auto-generated plan gives false confidence about feature-specific checks | Fowler | A plan from package.json only covers build/test, not acceptance criteria |

## Аргументы ПРОТИВ (принятые как допустимые риски)

| # | Аргумент | Кто привёл | Почему допустимо |
|---|---------|-----------|-----------------|
| 1 | Blocking on SKIPs may slow down backend-only features unnecessarily | Fowler | Mitigated by SKIP(n/a) — user can mark Chrome as not applicable |
| 2 | No agent-level retry means transient failures require full re-run | Fowler, Dan | Orchestrator's next iteration catches transients; simplicity wins |
| 3 | 3-retry cap may not be enough for complex features | — | After 3, human debugging is more effective than automated retry |
| 4 | Per-check evidence adds verbosity to reports | Dan | Mitigated by progressive disclosure — evidence is Level 3, not Level 0 |

## Оставшиеся разногласия

| Topic | Position A | Position B | Score |
|-------|-----------|-----------|-------|
| Agent-level retry (1x on timeout) | For: Jessie | Against: Fowler, Dan, Taleb | 1:3 — no retry |
| Confidence scoring per check | For: — | Against: Taleb (VETO), all others | 0:5 — rejected |
| WARN as separate status | For: Jessie | Against: Taleb (merge into PASS_WITH_CAVEATS) | Minor — defer to implementation |

---

## Рекомендация

The /team-verify system should be upgraded with these changes in order:

**Phase 1 (Stop the bleeding):**
1. Add 3-iteration circuit breaker to fix-verify loop in team-feature
2. Add AskUserQuestion blocking gate before TeamDelete for Human Checks + SKIPs
3. Add precondition check for VERIFICATION_PLAN.md existence

**Phase 2 (Make honest):**
4. Expand status taxonomy (7 statuses)
5. Add UNCLEAR → Human Checks routing
6. Add BROKEN detection in verifiers (environment health checks)
7. Add pre-flight readiness probe for dev server

**Phase 3 (Make trustworthy):**
8. Add per-check evidence to verifier output format
9. Add Verification Manifest (integrity audit)
10. Add verification scope disclosure ("NOT verified: ...")
11. Add progressive disclosure to report format

**Key architectural insight (Fowler):**
```
Preconditions → Readiness → Execution → Collection → Integrity → Gating → Report → Human Gate
```

Each stage has a clear purpose, a defined failure mode, and a known escalation path.

## План действий

Implementation touches 5 files:
1. `plugins/agent-teams/skills/team-verify/SKILL.md` — circuit breaker, preconditions, status taxonomy, manifest, progressive disclosure, blocking gate
2. `plugins/agent-teams/skills/team-feature/SKILL.md` — plan existence check, fix-verify loop limit, blocking gate before TeamDelete
3. `plugins/agent-teams/agents/ci-verifier.md` — per-check evidence format, BROKEN detection
4. `plugins/agent-teams/agents/browser-verifier.md` — per-check evidence, BROKEN detection, SKIP split
5. `plugins/agent-teams/agents/spec-verifier.md` — per-check evidence, UNCLEAR routing, BROKEN detection
