# Vibe Audit

Interactive feature audit for vibe-coded projects. Finds dead code, unused features, and experiments through **conversation** with the developer.

## Problem

In vibe-coding, lots of experimental code gets created:
- Try a feature → doesn't work out → forget to delete
- Refactor → old code stays behind
- A/B test → both variants remain in code

**Static analysis doesn't help** — the code is technically used, but the business logic is outdated.

## Solution

**Interactive audit:**
1. Agent finds suspicious areas
2. Asks you — is this still needed?
3. Safely removes what you don't need, with git backup

## Installation

```bash
/plugin marketplace add izmailovilya/ilia-izmailov-plugins
/plugin install vibe-audit@ilia-izmailov-plugins
```

## Usage

```
/vibe-audit              # Full codebase scan
/vibe-audit features     # src/features/ deep audit
/vibe-audit server       # src/server/ routers & services
/vibe-audit ui           # src/design-system/ components
/vibe-audit stores       # src/stores/ Zustand state
/vibe-audit all          # Run ALL auditors in parallel
```

## Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. DISCOVERY                                               │
│     Agents scan for suspicious code                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. INTERVIEW                                               │
│     "Is this still needed?"                                 │
│                                                             │
│     🗑️ Delete    ⚠️ Deprecated    ✅ Keep    🤔 Not sure    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. CLEANUP                                                 │
│     cleanup-executor safely removes                         │
│     (git branch + commit + TypeScript check)                │
└─────────────────────────────────────────────────────────────┘
```

## Agents

### Core Agents

| Agent | Purpose |
|-------|---------|
| `feature-scanner` | General scan: features, routers, pages |
| `usage-analyzer` | Deep analysis of a specific feature's usage |
| `cleanup-executor` | Safe removal with git backup |

### Specialized Auditors

| Agent | Target | What it finds |
|-------|--------|---------------|
| `ui-auditor` | `src/design-system/` | Unused components, style inconsistencies |
| `stores-auditor` | `src/stores/` | Dead Zustand slices, unused selectors |
| `features-auditor` | `src/features/` | Unused exports, internal dead code |
| `server-auditor` | `src/server/` | Unused tRPC procedures, dead services |

## Signals of Suspicion

- **Orphan routes** — tRPC procedures with no client calls
- **Dead UI** — components with no imports
- **Isolated features** — directories with minimal connections
- **Stale code** — no commits in 30+ days
- **Duplicate patterns** — similar logic in different places

## Safety

- Never deletes without confirmation
- Creates git branch before deletion
- Runs TypeScript check after deletion
- Logs all changes

## Example Session

```
> /vibe-audit features

🔍 Scanning src/features/...

Found 3 suspicious areas:

📦 **rat-hypothesis**
- Files: 12
- Last commit: 45 days ago
- External imports: 2

Is this needed?
[ ] 🗑️ Delete
[x] ✅ Keep — this is for the new release

📦 **old-onboarding**
- Files: 8
- Last commit: 90 days ago
- External imports: 0

Is this needed?
[x] 🗑️ Delete — replaced by new onboarding

...

🧹 Done! Removed:
- src/features/old-onboarding/ (8 files)
- Created commit: cleanup/old-onboarding-20260129
```

## License

MIT
