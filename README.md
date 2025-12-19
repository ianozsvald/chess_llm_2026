
# Goals

* Let me experiment with chess, UCI
* experiment with solving chess using LLMs and different board representations

# Setup

```
# created this using basepython conda env and a python -m venv .venv
conda activate basepython312
expt_chess$ . .venv/bin/activate
pip install -r requirements.txt
```

# Tests

`pytest` will run all your tests. If you setup `pre-commit` then any commits will kick off `isort`, `ruff` and `pytest`.

```
fswatch -r -x *.py | while read file event; do
    clear
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Change detected in $file ($event)"
    pytest
    sleep 1
done
```

## `coverage`

`python -m pytest --cov=. --cov-report=html` will run an HTML coverage report, view with `open htmlcov/index.html` in a browser.



## pre-commit

```
# pre-commit, on .pre-commit-config.yaml
# note we don't need ruff & isort in the main requirements.txt file
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-commit
```


# Notes

## git

* `git switch -c new-branch`



## 20251217

* p_vs_p.py player vs player

Note that black castle top-right is 'e8g8', also e1g1 for white.

Note that we need a WHITE terminal if we're working with unicode graphics, else they appear to be inverted


## 20251201

i installed stockfish (synaptic) and stockfish via pypi
https://pypi.org/project/stockfish/

pip install openai

https://fen2png.com/

possibly a very short stalemate
https://www.chess.com/forum/view/more-puzzles/stalemate-in-10-moves
https://www.chess.com/forum/view/game-showcase/the-shortest-stalemate
