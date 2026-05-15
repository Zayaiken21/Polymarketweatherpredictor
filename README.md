# Agent Cyclone - Poly Market Bot

## LLM routing
- Default: Ollama.
- Optional fallback: OpenAI.
- Set `LLM_PROVIDER=ollama` or `LLM_PROVIDER=openai`.
- If Ollama is slow or unavailable, OpenAI can be used only when `OPENAI_API_KEY` exists.

## Service discovery
The app auto-loads Python files ending in:
- `_service.py`
- `_tools.py`

All functions from those files are registered in a central runtime registry.

## Registry files
- `core/service_registry.py`
- `core/module_loader.py`

## Usage
Call:
- `auto_discover(".")`

Then inspect:
- `registry.services`
- `registry.tools`
- `registry.all_functions()`

## Polymarket
- Public market data is read from public endpoints.
- Wallet balance and portfolio data use authenticated Polymarket calls.
- Heartbeats can be sent during active management sessions.