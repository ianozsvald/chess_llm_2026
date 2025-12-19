import sys
from stockfish import Stockfish

#sf_params = {"Minimum Thinking Time": 0.01}
sf_params = {'Skill Level': 1}
sf = Stockfish(path="/usr/games/stockfish", parameters=sf_params)

moves = [] # ["e2e4", ] # "e7e5"]

sf.set_position(moves)

while True:
    print(sf.get_board_visual()) 
    while True:
        mv = input('Move:')
        if mv == 'quit':
            sys.exit()
        if sf.is_move_correct(mv):
            break
        else:
            print('That move was bad')
    sf.make_moves_from_current_position([mv])
    print(sf.get_evaluation())
    moves.append(mv)
    if False:
        # their move
        mv = sf.get_best_move()
        sf.make_moves_from_current_position([mv])
        moves.append(mv)
    print("Moves:", moves)


# sf.is_move_correct('e1d2') # if blocked
# sf.get_top_moves(10)
