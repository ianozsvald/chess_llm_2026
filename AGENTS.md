# Repository Guidelines

## Project Structure & Module Organization
The project currently revolves around `p_vs_p.py`, which runs the Stockfish-backed CLI. Keep throwaway experiments in this file, but extract reusable logic into a package such as `expt_chess/` to protect the entry point from clutter. Store repeatable FEN/PGN fixtures in `assets/` and expand documentation either here or under `docs/` as the codebase grows.

## Build, Test, and Development Commands
- `python3 -m venv .venv` — create the local environment recommended in `README.md`.
- `source .venv/bin/activate` — activate it before installing or running anything.
- `pip install --upgrade pip stockfish` — install the Python wrapper and ensure `/usr/games/stockfish` exists or adjust the path passed to `Stockfish(...)`.
- `python p_vs_p.py` — launch the REPL, enter moves, and confirm responses.

## Coding Style & Naming Conventions
Follow standard Python style: four spaces, lowercase `snake_case` for functions and variables, and `PascalCase` only for classes. Keep lines below 88 characters, group imports by origin, and add concise docstrings for helpers that mutate board state. Prefer descriptive names such as `current_line` over one-letter move holders.

## Testing Guidelines
Automated tests are not yet present; seed a `tests/` folder with `pytest` cases that replay known mini-games and assert `get_evaluation()` outputs. When you lack coverage, run `python trial1.py` with a deterministic move list (for example ["e2e4", "e7e5", "g1f3"]) and log the evaluation to the pull request for traceability.

## Commit & Pull Request Guidelines
Use imperative, sub-50 character commit subjects (e.g., `Refine move prompt`) and expand on behavior changes or dependency updates in the body. PRs should describe the scenario exercised (`python trial1.py`, `pytest`), note engine configuration changes, and attach CLI transcripts when the user flow shifts.

## Stockfish & Configuration Tips
If Stockfish lives outside `/usr/games/stockfish`, update the constructor argument near the top of `trial1.py` and call it out in the PR. Track commonly tweaked parameters (skill level, minimum thinking time) in a shared constant so collaborators can reason about defaults quickly.
