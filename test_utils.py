from stockfish import Stockfish
from utils import printable_clean_sf_visual, printable_clean_sf_visual_no_dots, printable_unicode_clean_sf_visual


def test_printable_clean_sf_visual_starting_position():
    sf = Stockfish()
    result = printable_clean_sf_visual(sf)
    expected = 'rnbqkbnr\npppppppp\n........\n........\n........\n........\nPPPPPPPP\nRNBQKBNR'
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"


def test_printable_clean_sf_visual_no_dots():
    sf = Stockfish()
    result = printable_clean_sf_visual_no_dots(sf)
    expected = 'rnbqkbnr\npppppppp\n        \n        \n        \n        \nPPPPPPPP\nRNBQKBNR'
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    assert '.' not in result, "Result should not contain any dots"


def test_printable_unicode_clean_sf_visual():
    sf = Stockfish()
    result = printable_unicode_clean_sf_visual(sf)
    expected = '♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟♟\n........\n........\n........\n........\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖'
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    # Verify no ASCII piece letters remain
    for letter in 'KQRBNPkqrbnp':
        assert letter not in result, f"ASCII piece '{letter}' should be replaced with unicode"


if __name__ == "__main__":
    test_printable_clean_sf_visual_starting_position()
    test_printable_clean_sf_visual_no_dots()
    test_printable_unicode_clean_sf_visual()
    print("All tests passed!")
