
# Goals

* Let me experiment with chess, UCI
* experiment with solving chess using LLMs and different board representations

Run `controller1.py`, decide on who is player1 and player2, currently player1 is stockfish (level 0) and player2 is an LLM.

Note that the ELO control doesn't seem to work which is annoying!

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

# Next steps

* do resigned games e.g. glm  4.7 have fewer moves?
* how good are commentaries?
* need more than 3 games per model! e.g. 3 more games?
* for stockfish does a e.g. 1500 elo game beat the level 0 config?

# Todo

* integrate the check for a legal clean move
* add unit test to make a full prompt in llm_openai module inc FEN and board


## games 20260102

* Stockfish (skill level 0) vs LLM (z-ai/glm-4.7) over 3 games Term1
* Stockfish (skill level 0) vs LLM (anthropic/claude-opus-4.5) over 3 games Term2
* Stockfish (skill level 0) vs LLM (deepseek/deepseek-v3.1-terminus) over 3 games Term3
* Stockfish (skill level 0) vs LLM (openai/gpt-5.2) over 3 games Term4

## games 20251230

* does sf 100 lose to sf 500 consistently? 2/3 for black, 4-10 min games
* does sf 100 lose to sf 1000 consistently? 0/3 for black, 4-20 min games
* does sf 100 lose to sf 3000 consistently? 2/3 for black, 4-19 min games, 2/3 and 7-28min games
* does sf 250 lose to gpt 5.2? Term3, not sure whta I'll get from this (circa 30 min games)
* does skill level 0 lose to skill level 5? Term1, 3/3 for black 1-5min games 20260101T18_29_36 20260101T19_17_34 3/3 for black 1-5 min per game
* does skill level 0 beat gpt 5.2?
  * Term6 Stockfish (skill level 0) vs LLM (openai/gpt-5.2) over 3 games
* does skill level 0 beat glm 4.7? 
  * Stockfish (skill level 0) vs LLM (z-ai/glm-4.7) over 3 games Term2, cut out due to resign issue, trying again
* does skill level 0 beat opus 4.5? Term5
  * Stockfish (skill level 0) vs LLM (anthropic/claude-opus-4.5) over 3 games
* deos skill level 0 beat deepseek terminus?  Stockfish (skill level 0) vs LLM (deepseek/deepseek-v3.1-terminus) over 3 games note it only does 1 game and resigns and exits!, 
  * Stockfish (skill level 0) vs LLM (deepseek/deepseek-v3.1-terminus) over 3 games Term4 now resign fixed

player1, player2, player1 wins, player2 resigns
sf 0, sf 5, 3, 0
sf 0, glm 4.7, 3, 3
sf 0, deepseek 3.1 terminus, 3, 3
sf 0, claude opus 4.5, 3, 2
sf 0, gpt 5.2, 3, 2



# Notes

## stockfish

* https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html
  * ponder False means don't think during opponents time (default False)
  * UCI Limit Strength honours low UCI Elo
  * Minimum Thinking Time is 20ms by default and could be smaller
* arguably you can't get below elo 1350! https://www.reddit.com/r/ComputerChess/comments/ql1m20/stockfish_strength/
* https://official-stockfish.github.io/docs/stockfish-wiki/Stockfish-FAQ.html#how-do-skill-level-and-uci-elo-work
* https://official-stockfish.github.io/docs/stockfish-wiki/UCI-&-Commands.html#skill-level

## db

* `sqlite3 expt.sqlite "SELECT * FROM game_moves;`
* `select * from game_moves where move_attempt > 0;`

## git

* `git switch -c new-branch`


# 20251223

* using elo 250 stockfish, it beats 3.1 terminus and glm 4.7
* `model = 'deepseek/deepseek-v3.1-terminus'` likes to write explanations, it can't just give a move. It also writes e.g. e4-e5 or **e7e6**
* model llama 4 scout - plays what looks like a sensible move but it doesn't wrap it in ``` !
* model glm 4.7 - seems to play ok
* elo 250 vs gpt 5.2 results in a balck win! at elo 250 it can resign or lose. it still makes illegal moves


## 20251217

* p_vs_p.py player vs player

Note that black castle top-right is 'e8g8', also e1g1 for white. black e8c8 (castle queenside?)

Note that we need a WHITE terminal if we're working with unicode graphics, else they appear to be inverted


## 20251201

i installed stockfish (synaptic) and stockfish via pypi
https://pypi.org/project/stockfish/

pip install openai

https://fen2png.com/

possibly a very short stalemate
https://www.chess.com/forum/view/more-puzzles/stalemate-in-10-moves
https://www.chess.com/forum/view/game-showcase/the-shortest-stalemate
