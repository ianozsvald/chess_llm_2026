SF_PATH = "/usr/games/stockfish"


def printable_clean_sf_visual(sf):
    """Remove visual noise from stockfish visual display"""
    cleaner = (
        sf.get_board_visual()
        .replace("-", "")
        .replace("   ", ".")
        .replace(" ", "")
        .replace("+", "")
        .replace("|", "")
        .replace("a.b.c.d.e.f.g.h", "")
        .replace("8", "")
        .replace("7", "")
        .replace("6", "")
        .replace("5", "")
        .replace("4", "")
        .replace("3", "")
        .replace("2", "")
        .replace("1", "")
    )
    # strip initial and trailing carriage returns and the doubled returns
    cleaner2 = cleaner[1:].replace("\n\n", "\n")[:-2]
    assert len(cleaner2) == (8 * 8 + 7), "expected 8x8 board with carriage returns"
    return cleaner2


def printable_clean_sf_visual_no_dots(sf):
    """Same as printable_clean_sf_visual but with spaces instead of dots"""
    return printable_clean_sf_visual(sf).replace(".", " ")


def printable_unicode_clean_sf_visual(sf):
    """Same as printable_clean_sf_visual but with unicode chess symbols"""
    board = printable_clean_sf_visual(sf)
    # White pieces (uppercase)
    board = board.replace("K", "♔")
    board = board.replace("Q", "♕")
    board = board.replace("R", "♖")
    board = board.replace("B", "♗")
    board = board.replace("N", "♘")
    board = board.replace("P", "♙")
    # Black pieces (lowercase)
    board = board.replace("k", "♚")
    board = board.replace("q", "♛")
    board = board.replace("r", "♜")
    board = board.replace("b", "♝")
    board = board.replace("n", "♞")
    board = board.replace("p", "♟")
    return board


def extract_from_triple_backticks(text):
    """Extract content enclosed in triple backticks from multiline text.

    Expects the text to end with lines containing triple backticks surrounding content.
    Returns the extracted content, or None if no triple backticks found.
    """
    import re

    # Find all occurrences of triple backticks with content between them
    # This handles both single-line (```content```) and multi-line formats
    pattern = r"```(?:\w*\n)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    # Return the last match (the one at the end), stripped of whitespace
    return matches[-1].strip()
