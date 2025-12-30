from stockfish import Stockfish

from utils import (
    check_legal_format,
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


def test_extract_from_triple_backticks2():
    input_text = """My next move is:
```d7d5
```
"""
    result = extract_from_triple_backticks(input_text)
    assert result == "d7d5", f"Expected 'd7d5', got '{result}'"

    input_text = """My next move is:
```text
d7d5
```
"""
    result = extract_from_triple_backticks(input_text)
    assert result == "d7d5", f"Expected 'd7d5', got '{result}'"

    input_text = """
**Best move:**
```
g8f6
``` """
    result = extract_from_triple_backticks(input_text)
    assert result == "g8f6", f"Expected 'g8f6', got '{result}'"

    # gpt 5.2
    input_text = """
```
/// b8c6
```
    """
    result = extract_from_triple_backticks(input_text)
    assert result == "b8c6", f"Expected 'b8c6', got '{result}'"


def test_check_legal_format():
    # Valid UCI moves
    assert check_legal_format("e2e4") is True
    assert check_legal_format("c1d3") is True
    assert check_legal_format("f4f5") is True
    assert check_legal_format("a1h8") is True
    assert check_legal_format("h7h8") is True

    # Resign is valid
    assert check_legal_format("resign") is True

    # Misspellings of resign
    assert check_legal_format("Resign") is False
    assert check_legal_format("RESIGN") is False
    assert check_legal_format("resgin") is False
    assert check_legal_format("resgn") is False
    assert check_legal_format("resignn") is False

    # Invalid formats
    assert check_legal_format("e2") is False  # Too short
    assert check_legal_format("e2e4e5") is False  # Too long
    assert check_legal_format("E2E4") is False  # Uppercase
    assert check_legal_format("e9e4") is False  # Invalid row
    assert check_legal_format("i2e4") is False  # Invalid column
    assert check_legal_format("2e4e") is False  # Wrong order
    assert check_legal_format("") is False  # Empty
    assert check_legal_format("move") is False  # Random word


if __name__ == "__main__":
    test_printable_clean_sf_visual_starting_position()
    test_printable_clean_sf_visual_no_dots()
    test_printable_unicode_clean_sf_visual()
    test_extract_from_triple_backticks()
    test_check_legal_format()
    print("All tests passed!")
