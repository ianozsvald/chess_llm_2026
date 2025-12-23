from stockfish import Stockfish

from utils import (
    extract_from_triple_backticks,
    printable_clean_sf_visual,
    printable_clean_sf_visual_no_dots,
    printable_unicode_clean_sf_visual,
)


def test_printable_clean_sf_visual_starting_position():
    sf = Stockfish()
    result = printable_clean_sf_visual(sf)
    expected = (
        "rnbqkbnr\npppppppp\n........\n........\n........\n........\nPPPPPPPP\nRNBQKBNR"
    )
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"


def test_printable_clean_sf_visual_no_dots():
    sf = Stockfish()
    result = printable_clean_sf_visual_no_dots(sf)
    expected = (
        "rnbqkbnr\npppppppp\n        \n        \n        \n        \nPPPPPPPP\nRNBQKBNR"
    )
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    assert "." not in result, "Result should not contain any dots"


def test_printable_unicode_clean_sf_visual():
    sf = Stockfish()
    result = printable_unicode_clean_sf_visual(sf)
    expected = (
        "♜♞♝♛♚♝♞♜\n♟♟♟♟♟♟♟♟\n........\n........\n........\n........\n♙♙♙♙♙♙♙♙\n♖♘♗♕♔♗♘♖"
    )
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    # Verify no ASCII piece letters remain
    for letter in "KQRBNPkqrbnp":
        assert letter not in result, (
            f"ASCII piece '{letter}' should be replaced with unicode"
        )


def test_extract_from_triple_backticks():
    input_text = """Looking at the position:

- Black's dark-squared bishop is attacked by the knight on h4. If Bg6, the knight can capture it.
- If Bg6, Nh4xg6 ruins Black's pawn structure after hxg6.
- Better to move the bishop to a safe square where it keeps its activity.

From the FEN `rn1qkbnr/ppp1pppp/8/3p1b2/7N/6P1/PPPPPP1P/RNBQKB1R b KQkq - 3 3`, the bishop is on f5 and knight on h4 attacks it.

Safe squares: g4, e6, d7, c8, h7, g6 (but g6 allows Nh4xf5 after a future f3, maybe not ideal).

Best is probably **e7e6** to defend d5 and keep the bishop's options open. But then g4 hangs? Wait, with knight on h4, if Bg4, f3 traps the bishop. So g4 is dangerous.

Actually, maybe **g7g6** first, to threaten Nh4 with tempo and force the knight to move before playing Bg7 fianchetto? But that loses a tempo on development.

However, the immediate problem: after g7g6, knight can go to f3, no big deal. Another idea: Bc8 to reposition.

But strongest seems **Bf5-g4** immediately — but f3 is not possible for White because knight blocks f3 square? No, knight is on h4, f3 is free for White's pawn. So Bg4 is bad due to f3.

Best retreat: **Bf5-e6** covers d5 and is safe from pawn attacks.

Also possible: **Bf5-c8**, but that's passive. **Bf5-d7** is also safe and keeps the bishop.

Between e6 and d7, e6 is more active, supports d5, and prevents White's e2-e4. Solid choice.

So my move:

```f5e6```
"""
    result = extract_from_triple_backticks(input_text)
    assert result == "f5e6", f"Expected 'f5e6', got '{result}'"


if __name__ == "__main__":
    test_printable_clean_sf_visual_starting_position()
    test_printable_clean_sf_visual_no_dots()
    test_printable_unicode_clean_sf_visual()
    test_extract_from_triple_backticks()
    print("All tests passed!")
