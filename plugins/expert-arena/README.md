# Expert Arena

Expert evaluation arena — real experts independently assess options, cross-enrich evaluations, and filter out weak ideas. Produces a decision map, not a single verdict.

## Installation

```bash
/plugin marketplace add izmailovilya/ilia-izmailov-plugins
/plugin install expert-arena@ilia-izmailov-plugins
```

## Usage

```
/expert-arena <question>
```

**Examples:**
```
/expert-arena Should we use microservices or monolith for our SaaS?
/expert-arena What's the best pricing strategy for a developer tool?
/expert-arena How should we handle state management in our React app?
```

Works for **any domain**: engineering, product, strategy, business, science, philosophy.

## How It Works

### Phase 0: Expert Selection
- Analyzes your question (domain, type, stakes, initial options)
- Selects 3-5 **real experts** with published positions (books, articles, talks)
- Ensures diverse viewpoints — not an echo chamber
- Includes a **Devil's Advocate** who defends options from premature elimination
- Presents the panel for your review

### Phase 1: Reconnaissance
- Launches 2-4 researcher agents **in parallel**
- Gathers context (code architecture, best practices, data, case studies)
- **Identifies 3-6 concrete options/approaches** for experts to evaluate
- Researchers report findings and exit

### Phase 2: Arena Launch
- Compiles research into a briefing + numbered option list
- Presents options to you for approval (add/remove before launch)
- Launches **all experts simultaneously** with full context

### Phase 3: Evaluation (3 stages)

**Stage A — Independent Evaluation:**
Each expert evaluates every option (pros, cons, 1-5 rating) and sends results **only to the moderator**. Experts don't see each other's evaluations — prevents anchoring bias. Timeout: 5 minutes per expert.

**Stage B — Cross-Enrichment:**
Moderator compiles and broadcasts all evaluations as a summary table. Experts can **add arguments** they missed after seeing others' perspectives. No debates — enrichment only. Timeout: 5-7 minutes.

**Stage C — Filtering:**
Experts vote on which options are clearly weak. An option is eliminated if 3+ experts vote to remove it. Devil's Advocate can **VETO** an elimination — requires finding a legitimate strong argument to defend the option. Veto prevents groupthink, not stubbornness.

**Live Commentary:**
The moderator provides real-time commentary throughout — announcing evaluations as they arrive, highlighting unexpected ratings, noting disagreements, and narrating the filtering drama. Keeps you engaged while experts work.

### Phase 4: Synthesis
Creates a final document with:
- **Option map** — each surviving option with all pros/cons from all experts, per-expert rating table, and "when to choose this option" guidance
- **Decision navigator** — "if your context is X, choose option Y because Z" (table format)
- Eliminated options with reasons and vote counts

Saves to `docs/arena/YYYY-MM-DD-[topic].md`

## Structure

```
expert-arena/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── expert.md             # Expert evaluator agent
│   └── researcher.md         # One-shot research agent
├── skills/
│   └── expert-arena/
│       └── SKILL.md          # Moderator orchestration
└── README.md
```

## Key Design Principles

| Principle | Why |
|-----------|-----|
| **Independent evaluation first** | Prevents anchoring — experts form opinions before seeing others |
| **Real people** | Experts have actual published positions — not invented |
| **Intentional diversity** | Deliberately selects people who would evaluate differently |
| **No forced convergence** | Divergent opinions are valuable signal, not a problem |
| **Cross-enrichment** | Experts enrich each other's arguments without debating |
| **Devil's Advocate with veto** | Safety net against premature elimination of options |
| **Option map, not verdict** | Output preserves variability — user picks based on their context |

## When to Use

- Big architectural or strategic decisions with multiple viable approaches
- Trade-offs with no obvious right answer
- Need diverse expert perspectives on each option
- Want a decision map, not a single recommendation
- Any question where the right answer depends on context

## License

MIT
