import datetime
import math
import os
import pathlib
import random
import sys

from stockfish import Stockfish

import db
import utils
from llm_openai import call_llm
from utils import SF_PATH

# from stockfish import Stockfish; sfx=Stockfish(path="/usr/games/stockfish", parameters={"UCI_Elo": 100})


# get_evaluation - type cp (centipawn) and a value, or mate and value, mate value 0 is end?


class SF:
    # def __init__(self, uci_elo=500):
    def __init__(self, skill_level=0):
        sf_params = {"Skill Level": skill_level}
        # self.uci_elo = uci_elo
        # print(f"Making SF bot with elo {uci_elo}")
        # sf_params = {"UCI_Elo": uci_elo}
        self.sfi = Stockfish(path=SF_PATH, parameters=sf_params)
        # 'UCI_LimitStrength': 'true', set from false to true when elo set in get_parameters
        # assert self.sfi.get_parameters()['UCI_LimitStrength'] == 'true'

    def get_next_move(self, moves):
        self.sfi.set_position(moves)
        mv = self.sfi.get_best_move()
        print(f"SF proposes: {mv}")
        return mv

    def __str__(self):
        # return f"Stockfish (ELO {self.sfi.get_parameters()['UCI_Elo']})"
        return f"Stockfish (skill level {self.sfi.get_parameters()['Skill Level']})"


class SFBadBot:
    """Makes random or bad moves"""

    def __init__(self, skill_level=0):
        sf_params = {"Skill Level": skill_level}
        # def __init__(self, uci_elo=250):
        # sf_params = {"Skill Level": skill_level}
        # self.uci_elo = uci_elo
        # sf_params = {"UCI_Elo": uci_elo}
        sfi = Stockfish(path=SF_PATH, parameters=sf_params)
        self.sfi = sfi

    def get_next_move(self, moves):
        # self.sfi.set_position(moves)
        # mv = "nuffin"
        mv = None
        print(f"SFBadBot proposes: {mv}")
        return mv

    def __str__(self):
        # return f"Stockfish BadBot (ELO {self.uci_elo})"
        return f"Stockfish (skill level {self.sfi.get_parameters()['Skill Level']})"


class LLM:
    def __init__(self, visualiser_routine, model_name):
        # we need a stockfish to describe the board state
        self.model_name = model_name
        sfi = Stockfish(path=SF_PATH)
        self.sfi = sfi
        self.visualiser_routine = visualiser_routine

    def get_next_move(self, moves):
        assert not is_even(len(moves))
        self.sfi.set_position(moves)
        # get a board position like
        # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        fen = self.sfi.get_fen_position()
        board_render = self.visualiser_routine(self.sfi)
        mv = call_llm(
            "black",
            moves,
            fen=fen,
            board_render=board_render,
            model_name=self.model_name,
        )
        return mv

    def __str__(self):
        return f"LLM ({self.model_name})"


class Human:
    def __init__(self):
        pass

    def get_next_move(self, moves):
        mv = input()
        return mv

    def __str__(self):
        return "Human"


def get_a_move(sf_checker, moves, player, db_filename):
    """Get a legal move, choose randomly if forced to"""
    n = 0
    MAX_BAD_MOVES = 3
    is_legal_move = False
    move_was_rnd_choice = False
    while True:
        # mv = input('Move:')
        sf_checker.set_position(moves)
        mv = player.get_next_move(moves)
        if mv == "quit":
            sys.exit()
        if mv == "resign":
            is_legal_move = True
            break
        if sf_checker.is_move_correct(mv):
            is_legal_move = True
            break
        else:
            print(f"--Bad move: `{mv}` on try {n} of {MAX_BAD_MOVES}--")
            n += 1
        if n == MAX_BAD_MOVES:
            # too many bad moves
            legal_good_moves = sf_checker.get_top_moves(10)
            move_was_rnd_choice = True
            # [{'Move': 'd2d4', 'Centipawn': 39, 'Mate': None},
            # {'Move': 'e2e4', 'Centipawn': 38, 'Mate': None},
            # ...
            random.shuffle(legal_good_moves)
            mv = legal_good_moves[0]["Move"]
            assert sf_checker.is_move_correct(mv), f"We expect mv {mv} to be legal"
            print(
                "---Too many bad moves, had to choose a random good move instead\n--------\n"
            )
            break

    move = len(moves)
    game_step = int(move / 2)
    is_white = is_even(move)
    engine = type(player).__name__
    move_attempt = n

    db.write_row(
        db_filename,
        game_step,
        move,
        is_white,
        is_legal_move,
        engine,
        move_attempt,
        move_was_rnd_choice,
        uci_move=mv,
    )
    return mv


def is_even(n):
    return int(n / 2) == n / 2


def play_game(moves, sf_checker, visualiser_routine, player1, player2, db_filename):
    # moves = []  # ["e2e4", ] # "e7e5"]
    # if not moves:
    #    moves = []
    game_end_reason = ""
    while True:
        print(f"(Pair) Move nbr: {math.ceil((len(moves) + 1) / 2)}")
        print("Moves:", moves)
        sf_checker.set_position(moves)
        print(visualiser_routine(sf_checker))

        assert is_even(len(moves)), (
            f"For player1 we expect 0, 2, 4 etc moves, got {len(moves)}"
        )
        mv1 = get_a_move(sf_checker, moves, player1, db_filename)
        if mv1 == "resign":
            game_end_reason = "black wins, white resigns"
            break
        sf_checker.make_moves_from_current_position([mv1])
        eval1 = sf_checker.get_evaluation()
        print(eval1)
        moves.append(mv1)
        if eval1["type"] == "mate" and eval1["value"] == 0:
            # print("mate for white")
            game_end_reason = "mate for white"
            break

        assert not is_even(len(moves)), (
            f"For player2 we expect 1, 3, 5 etc moves, got {len(moves)}"
        )
        mv2 = get_a_move(sf_checker, moves, player2, db_filename)
        if mv2 == "resign":
            game_end_reason = "white wins, black resigns"
            break
        sf_checker.make_moves_from_current_position([mv2])
        eval2 = sf_checker.get_evaluation()
        print(eval2)
        moves.append(mv2)
        if eval2["type"] == "mate" and eval2["value"] == 0:
            # print("mate for black")
            game_end_reason = "mate for black"
            break
    print(f"Game outcome: {game_end_reason}")
    return game_end_reason


def write_outcome(db_filename, dt_end, dt_start, game_end_reason, player1, player2):
    f.write(f"Made: {db_filename}\n")
    f.write(f"{player1} vs {player2}\n")
    f.write(f"Game took {dt_end - dt_start}\n")
    f.write(f"{game_end_reason=}\n")


def make_players():
    # player1 = Human()
    # player2 = SF(UCI_Elo=250)

    # player1 = SF(uci_elo=250)
    # model = "anthropic/claude-opus-4.5"
    # model = "z-ai/glm-4.7"
    # model = "deepseek/deepseek-v3.1-terminus"
    model = "openai/gpt-5.2"
    player2 = LLM(visualiser_routine, model)
    # player2 = SFBadBot()

    player1 = SF(skill_level=0)
    # player2 = SF(skill_level=5)

    # player1 = SF(skill_level=1)
    # player2 = SFBadBot()
    # player2 = LLM1()
    return player1, player2


if __name__ == "__main__":
    # sf_params = {'Skill Level': 1} # seems to be equiv to elo 1350!
    sf_checker = Stockfish(path=SF_PATH)

    visualiser_routine = utils.printable_clean_sf_visual
    visualiser_routine = utils.printable_unicode_clean_sf_visual

    # moves = moves_end_white_win[:210]

    MAX_ITERATIONS = 3

    dt_start = datetime.datetime.now(datetime.UTC)
    expt_folder_name = utils.create_timestamped_folder()
    expt_folder = pathlib.Path(expt_folder_name)
    for game_nbr in range(MAX_ITERATIONS):
        player1, player2 = make_players()
        print(f"{player1} vs {player2} over {MAX_ITERATIONS} games")
        print(f"{game_nbr=}")
        db_folder = expt_folder / str(game_nbr)
        os.makedirs(db_folder, exist_ok=False)
        db_filename = db_folder / "moves.sqlite"
        db.create_table(db_filename)
        print(f"Made: {db_filename}")

        moves = []
        # we can force a certain game here:
        # import game_samples
        # moves = game_samples.moves_end_white_win2[:-2] # all but last two moves, white to start
        game_end_reason = play_game(
            moves, sf_checker, visualiser_routine, player1, player2, db_filename
        )
        dt_end = datetime.datetime.now(datetime.UTC)
        print(f"Game took {dt_end - dt_start}")
        with open(pathlib.Path(expt_folder_name) / "report.txt", "a") as f:
            write_outcome(
                db_filename, dt_end, dt_start, game_end_reason, player1, player2
            )

    print(f"Outcome in:\n{expt_folder}")

# sf.is_move_correct('e1d2') # if blocked
# sf.get_top_moves(10)
