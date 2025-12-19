import random

from stockfish import Stockfish

import utils
from llm_openai import call_llm

SF_PATH = "/usr/games/stockfish"

# get_evaluation - type cp and a value, or mate and value, mate value 0 is end?


class SF:
    def __init__(self, skill_level=1):
        sf_params = {"Skill Level": skill_level}
        sfi = Stockfish(path=SF_PATH, parameters=sf_params)
        self.sfi = sfi

    def get_next_move(self, moves):
        self.sfi.set_position(moves)
        mv = self.sfi.get_best_move()
        print(f"SF proposes: {mv}")
        return mv


class SFBadBot:
    """Makes random or bad moves"""

    def __init__(self, skill_level=1):
        sf_params = {"Skill Level": skill_level}
        sfi = Stockfish(path=SF_PATH, parameters=sf_params)
        self.sfi = sfi

    def get_next_move(self, moves):
        # self.sfi.set_position(moves)
        # mv = self.sfi.get_best_move()
        mv = "nuffin"
        print(f"SFBadBot proposes: {mv}")
        return mv


class LLM1:
    def __init__(self):
        # we need a stockfish to describe the board state
        sfi = Stockfish(path=SF_PATH)
        self.sfi = sfi

    def get_next_move(self, moves):
        assert not is_even(len(moves))
        self.sfi.set_position(moves)
        # get a board position like
        # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        fen = self.sfi.get_fen_position()
        mv = call_llm("black", moves, fen=fen)
        return mv


class Human:
    def __init__(self):
        pass

    def get_next_move(self, moves):
        mv = input()
        return mv


# sf_params = {"Minimum Thinking Time": 0.01}
# sf_params = {'Skill Level': 1} # seems to be equiv to elo 1350!
sf_params = {"UCI_Elo": 250}
sf_checker = Stockfish(path=SF_PATH, parameters=sf_params)

visualiser_routine = utils.printable_clean_sf_visual
visualiser_routine = utils.printable_unicode_clean_sf_visual

moves = []  # ["e2e4", ] # "e7e5"]
# moves = moves_end_white_win[:210]

# player1 = Human()
# player2 = SF(UCI_Elo=250)

player1 = SF(skill_level=1)
player2 = LLM1()

# player1 = SF(skill_level=1)
# player2 = SFBadBot()
# player2 = LLM1()


def get_a_move(sf_checker, moves, player):
    """Get a legal move, choose randomly if forced to"""
    n = 0
    while True:
        # mv = input('Move:')
        sf_checker.set_position(moves)
        mv = player.get_next_move(moves)
        # if mv == 'quit':
        #    sys.exit()
        if sf_checker.is_move_correct(mv):
            break
        else:
            print(f"Bad move: {mv} {n}")
            n += 1
        if n == 10:
            # too many bad moves
            legal_good_moves = sf_checker.get_top_moves(10)
            # [{'Move': 'd2d4', 'Centipawn': 39, 'Mate': None},
            # {'Move': 'e2e4', 'Centipawn': 38, 'Mate': None},
            # ...
            random.shuffle(legal_good_moves)
            mv = legal_good_moves[0]["Move"]
            break
    return mv


def is_even(n):
    return int(n / 2) == n / 2


while True:
    print("Moves:", moves)
    sf_checker.set_position(moves)
    print(visualiser_routine(sf_checker))

    assert is_even(len(moves)), (
        f"For player1 we expect 0, 2, 4 etc moves, got {len(moves)}"
    )
    mv1 = get_a_move(sf_checker, moves, player1)
    sf_checker.make_moves_from_current_position([mv1])
    eval1 = sf_checker.get_evaluation()
    print(eval1)
    moves.append(mv1)
    if eval1["type"] == "mate" and eval1["value"] == 0:
        print("mate for white")
        break

    assert not is_even(len(moves)), (
        f"For player2 we expect 1, 3, 5 etc moves, got {len(moves)}"
    )
    mv2 = get_a_move(sf_checker, moves, player2)
    sf_checker.make_moves_from_current_position([mv2])
    eval2 = sf_checker.get_evaluation()
    print(eval2)
    moves.append(mv2)
    if eval2["type"] == "mate" and eval2["value"] == 0:
        print("mate for black")
        break


# sf.is_move_correct('e1d2') # if blocked
# sf.get_top_moves(10)
