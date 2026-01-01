import sqlite3
from datetime import datetime, timezone

# DB_FILENAME = "expt.sqlite"


def create_table(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_moves (
            game_step INTEGER,
            move INTEGER,
            is_white INTEGER,
            is_legal_move INTEGER,
            engine TEXT,
            move_attempt INTEGER,
            move_was_rnd_choice INTEGER,
            uci_move TEXT,
            move_time DATETIME
        )
    """)
    conn.commit()
    conn.close()


def write_row(
    db_filename: str,
    game_step: int,
    move: int,
    is_white: bool,
    is_legal_move: bool,
    engine: str,
    move_attempt: int,
    move_was_rnd_choice: bool,
    uci_move: str,
):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO game_moves (game_step, move, is_white, is_legal_move,
                                engine, move_attempt, move_was_rnd_choice, uci_move, move_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            game_step,
            move,
            int(is_white),
            int(is_legal_move),
            engine,
            move_attempt,
            int(move_was_rnd_choice),
            uci_move,
            datetime.now(timezone.utc).replace(tzinfo=None),
        ),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_filename = "/tmp/chess_db.sqlite"
    create_table(db_filename)
    print(db_filename)
    write_row(db_filename, 1, 1, True, True, "stockfish", 1, False, "e2e4")
    write_row(db_filename, 1, 2, False, True, "gpt-4", 1, False, "e7e5")
    write_row(db_filename, 2, 3, True, False, "stockfish", 2, True, "d2d4")
