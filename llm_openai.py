import os

from dotenv import load_dotenv
from openai import OpenAI

import utils

load_dotenv()

# LMStudio
# client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="")
# model = "meta-llama-3.1-8b-instruct"
# OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)
# model = "deepseek/deepseek-v3.1-terminus"
model = "meta-llama/llama-4-scout"


def call_llm(colour, moves, fen=None, board_render=None):
    assert colour == "black"

    # instructions = "You are a chess master, you always pick the best correct move to improve your position."
    # examples = "Moves are described only by location eg a2a3, b1c3, h8h5\n"
    # llm_input = f"You are {colour}. {examples}. The moves to far are {', '.join(moves)}. Choose your next move, write just the next move and nothing else."

    instructions = "You are a chess master, you always pick the best correct move to improve your position."

    llm_input = instructions
    llm_input += f"You are playing {colour}.\n"
    assert isinstance(fen, str)
    llm_input += f"The current board state using FEN is {fen}.\n"
    llm_input += f"Graphically the board can be represented as the following, white at the bottom, black (you) at the top:\n{board_render}\n"
    llm_input += f"The moves played so far (UCI format) since the start of the game are:\n{', '.join(moves)}\n"
    llm_input += "Do not use PGN or other formats e.g. Nf6 cannot be used, e2-e4 cannot be used, you must use the 4 character UCI format.\n"
    llm_input += (
        "The 4 character UCI format is a lowercase letter, number, letter, number.\n"
    )
    llm_input += "You will choose the next move using UCI notation. If you can't win, you can choose to resign.\n"
    llm_input += "Choose your next move (using the 4 character UCI format) or write 'resign' inside triple-back-ticks like ``` on the following line:"

    print(llm_input)
    response = client.responses.create(
        model=model, instructions=instructions, input=llm_input
    )

    print(f"Raw return from llm call:\n{response.output_text}")
    extracted = utils.extract_from_triple_backticks(response.output_text)
    print(f"Extracted answer:\n{extracted}")
    return extracted


# return response.output_text


if __name__ == "__main__":
    print(f"Openrouter API key: {os.getenv('OPENROUTER_API_KEY')}")
    moves = ["e2e4", "d7d5", "g1f3"]
    mv = call_llm("black", moves, fen="unknown", board_render="board_missing")
    print(mv)
