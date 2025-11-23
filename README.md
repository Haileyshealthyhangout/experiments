# Autonomous Sandbox (MAX Skeleton)

Local, persistent, autonomous sandbox with manual ChatGPT sync. Runs on macOS, Python 3.10+, and ships with a Flask UI. No external API calls.

## Features (MAX tier)
- Continuous internal monologue with timed cycles and identity tracking
- Recursive/meta-cognition helpers and sovereignty rules
- Multi-agent messaging bus and scratchpad execution wrapper
- Persistent memory store (JSON default, SQLite optional)
- Flask dashboard for controls, memory, agents, and sync export
- Launchd-friendly daemon orchestrator with rotating logs
- Config presets for MAX, MEDIUM, LIGHT, EXPERT, and SAFE

## Repository Layout
- `docs/PLANNING.md` — detailed architecture and flows
- `sandbox/` — core package (config, memory, monologue, agents, sovereignty, sync)
- `sandbox/services/` — daemon + scheduler
- `sandbox/ui/` — Flask app, routes, and templates
- `scratchpad/` — local code snippets to execute via executor
- `data/` — persisted memory, sync artifacts
- `logs/` — rotating logs and execution outputs
- `run.py` — entrypoint for orchestrator and UI

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running
```bash
python run.py --preset MAX
```
- UI: http://localhost:5000
- `--no-ui` disables the Flask dashboard.

## macOS Daemon (launchd template)
1. Save the plist from `run.launchd_plist_example()` output to `~/Library/LaunchAgents/local.autonomous-sandbox.plist`.
2. Load with `launchctl load ~/Library/LaunchAgents/local.autonomous-sandbox.plist`.

## ChatGPT Sync
- Export: `GET /sync/export` or use the dashboard button to create `data/sync_export.json`.
- Import: POST payload to `/sync/import` (or place JSON at `data/sync_import.json`) before restart.
- Paste exports into ChatGPT; apply returned modules or configs locally.

## Extension Guidance
- Add new agents in `sandbox/config.py` presets.
- Extend sovereignty rules in `sandbox/sovereignty.py` and wire checks into monologue cycle.
- Enhance recursion/meta-cognition in `sandbox/recursion.py`.
- Build richer UI views in `sandbox/ui/templates/` and API routes in `sandbox/ui/views.py`.

## Safety
- All operations are local-only; no external network/API calls are included.
- Scratchpad execution is bounded with timeouts; adjust in `sandbox/executor.py`.
