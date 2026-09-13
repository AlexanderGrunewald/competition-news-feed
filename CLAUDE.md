# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is

A Streamlit app that monitors power-tool competitors (for Bosch) by crawling
news/product-launch data via the Tavily search API, storing it, and
displaying it as a browsable feed.

**This is a personal-development project for the user.** The point is for
them to write most of the code themselves and learn by doing. Default to
being a pair-programmer/reviewer, not an implementer:
- Don't write full features or files unless explicitly asked to.
- Prefer explaining approaches, pointing at relevant files/APIs, reviewing
  their code, and answering specific questions.
- If asked for "help" with something, lean toward hints, small snippets, or
  targeted fixes rather than doing the whole thing.
- It's fine to do larger autonomous work (refactors, multi-file changes) when
  they explicitly ask for that — just don't default to it.

## Current stage

Building out the DuckDB persistence layer (`data/database/newsFeed.duckdb`).
Schema is defined (`src/db/schema.sql`: `feeds` / `runs` / `articles` /
`run_articles`, articles deduped by URL, `run_articles` as the join table
carrying per-run relevance score) and wired to run automatically via
`pixi run init-db` (idempotent `CREATE TABLE IF NOT EXISTS`), which `start`
depends on. Not yet built: any Python code that actually reads/writes
through this schema — `tavily_parser.py` still only writes flat JSON, and
the Streamlit pages don't touch the DB yet. That's the next piece.

## Repo map

```
src/
  parser/
    tavily_parser.py     # CompetitorSearchEngine(TavilyClient) — wraps Tavily
                          # search with power-tool-competitor-specific defaults
                          # (monitor_competitor, save_results)
  app/
    🧑‍💻_News_Feed_Monitor.py   # Streamlit entrypoint / main feed page
    pages/
      📰_Create_Feed.py          # Streamlit multipage app: form to configure
                                  # a new competitor feed (name, competitor,
                                  # category, custom query, Tavily params)
demos/
  tavily-examples.py      # scratch/reference script for the Tavily SDK
data/
  database/newsFeed.duckdb  # DuckDB database file (tracked in git; small)
  run_results/*.json         # per-run Tavily search results (gitignored)
tests/
  test_app.py              # Streamlit AppTest smoke tests for the main page
.github/workflows/ci.yml   # lint (flake8) + pytest via pixi, on push/PR to main
pixi.toml / pixi.lock      # env + task runner (see below)
load_env.sh                # sources .env into the pixi environment on activation
```

Note: `src/app/🧑‍💻_News_Feed_Monitor.py` and `src/app/pages/📰_Create_Feed.py`
use emoji-prefixed filenames — this is Streamlit's convention for multipage
app page icons/ordering in the sidebar. Keep that convention if adding pages.

## Environment & commands

Environment/tasks are managed with **pixi**, not pip/venv directly.

- `pixi run start` — run the Streamlit app
  (`streamlit run src/app/🧑‍💻_News_Feed_Monitor.py`)
- `pixi run test` — run pytest
- `pixi run lint` — flake8 (only checks E9/F63/F7/F82 — syntax errors and
  undefined names, not full style)

`.env` holds secrets (e.g. `TAVILY_API_KEY`) and is loaded into the pixi
environment automatically via `load_env.sh` on activation. CI supplies a
dummy `TAVILY_API_KEY` since no real API calls happen in tests.

Key dependencies: `streamlit`, `pandas`, `duckdb`, `tavily-python`, `rich`.
Python 3.14.

## Things to be aware of (don't silently "fix" unless asked)

- `tavily_parser.py`: `save_results` does `from time import time` at module
  level but calls `time.now()` inside the method — that's a bug (`time` here
  is the imported function, not the module; likely meant `datetime`). Leave
  it for the user unless they ask about it.
- `output.json` at the repo root looks like a stray/untracked scratch output
  (from running `demos/tavily-examples.py` or similar) — not part of the
  tracked structure.
- `data/database/newsFeed.duckdb` is currently tracked in git as a binary
  file. Worth flagging to the user if the DB is expected to grow — binary
  DB files in git don't diff/merge well.
