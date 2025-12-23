import sqlite3

DB_FILENAME = "expt.sqlite"


def create_table():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_moves (
            game_step INTEGER,
            move INTEGER,
            is_white INTEGER,
            is_legal_move INTEGER,
            engine TEXT,
            move_attempt INTEGER,
            move_was_rnd_choice INTEGER
        )
    """)
    conn.commit()
    conn.close()


def write_row(
    game_step: int,
    move: int,
    is_white: bool,
    is_legal_move: bool,
    engine: str,
    move_attempt: int,
    move_was_rnd_choice: bool,
):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO game_moves (game_step, move, is_white, is_legal_move,
                                engine, move_attempt, move_was_rnd_choice)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            game_step,
            move,
            int(is_white),
            int(is_legal_move),
            engine,
            move_attempt,
            int(move_was_rnd_choice),
        ),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    write_row(1, 1, True, True, "stockfish", 1, False)
    write_row(1, 2, False, True, "gpt-4", 1, False)
    write_row(2, 3, True, False, "stockfish", 2, True)
