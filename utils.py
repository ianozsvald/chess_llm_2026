import os
from datetime import datetime, timezone

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
    # Group 1 captures optional language/first-word, Group 2 captures remaining content
    pattern = r"```(\w*)\n?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    if not matches:
        return None

    # Get the last match
    lang_or_content, content = matches[-1]

    # If content is empty, the first group was actually the content (not a language)
    if not content.strip() and lang_or_content:
        result = lang_or_content.strip()
    else:
        result = content.strip()

    # Strip leading comment markers (e.g., "/// " or "// " from GPT 5.2 outputs)
    if result.startswith("///"):
        result = result[3:].strip()
    elif result.startswith("//"):
        result = result[2:].strip()

    return result


def check_legal_format(proposed_move):
    """Check if a move is in valid UCI format or is 'resign'.

    A valid UCI move is exactly 4 characters: lowercase letter, digit,
    lowercase letter, digit (e.g., 'e2e4', 'c1d3').
    The word 'resign' is also accepted.

    Returns True if the format is valid, False otherwise.
    """
    if proposed_move == "resign":
        return True

    if len(proposed_move) != 4:
        return False

    return (
        proposed_move[0] in "abcdefgh"
        and proposed_move[1] in "12345678"
        and proposed_move[2] in "abcdefgh"
        and proposed_move[3] in "12345678"
    )


def create_timestamped_folder():
    """Create a folder named with current UTC datetime and return the folder name."""
    folder_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H_%M_%S")
    os.makedirs("expts/" + folder_name, exist_ok=False)
    return folder_name
