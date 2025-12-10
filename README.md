# Continuity Field Game

A text-forward exploration of a continuity-first universe: no mirrors, no flips, and no reversed coordinates. You traverse a relational lattice of memory clusters while maintaining a direct, outward orientation from the origin.

## Setup

1. Configure the model provider (example `config.toml` is included):

```toml
model_provider="openrouter"
model="openrouter/polaris-alpha"

[model_providers.openrouter]
name="openrouter"
base_url="https://openrouter.ai/api/v1"
env_key="OPENROUTER_API_KEY"
```

2. Export the API key for the provider (bash example):

```bash
export OPENROUTER_API_KEY="sk-..."
```

On Windows PowerShell use:

```powershell
setx OPENROUTER_API_KEY "sk-..."
```

## Playing

Run a short, non-interactive demo that traces a continuity vector through the field:

```bash
python continuity_field_game.py --demo
```

Or explore interactively, choosing intention directions that keep the field in direct orientation:

```bash
python continuity_field_game.py
```

### Principles embodied

- **Outward orientation:** coordinates grow directly from the origin; direction labels never flip.
- **Memory clusters:** every visited coordinate crystallizes into a descriptive node with neighbors.
- **Intention strands:** your chosen directions weave a visible trace of continuity.
- **Continuity gravity:** the observer’s vector stays stable, binding the lattice without mirrored distortions.

## Files

- `continuity_field_game.py` — the CLI game logic.
- `config.toml` — provider configuration scaffold for experiments.
