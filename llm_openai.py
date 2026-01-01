import json
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
# model = "meta-llama/llama-4-scout"


def make_prompt(colour, moves, fen, board_render):
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
    llm_input += f"First analyse the board state and provide brief commentary from your position as the {colour} player.\n"
    llm_input += "Choose your next move (using the 4 character UCI format) or write 'resign' inside triple-back-ticks like ``` on the following line:"
    return instructions, llm_input


def call_llm(colour, moves, fen=None, board_render=None, model_name=None):
    assert colour == "black"
    instructions, llm_input = make_prompt(colour, moves, fen, board_render)

    # instructions = "You are a chess master, you always pick the best correct move to improve your position."
    # examples = "Moves are described only by location eg a2a3, b1c3, h8h5\n"
    # llm_input = f"You are {colour}. {examples}. The moves to far are {', '.join(moves)}. Choose your next move, write just the next move and nothing else."

    print(llm_input)
    if model_name.startswith("meta-llama/llama-4-scout"):
        only_providers = ["deepinfra"]
    if model_name.startswith("deepseek/deepseek-v3.2-speciale"):
        only_providers = ["parasail"]
    if model_name.startswith("deepseek/deepseek-v3.1-terminus"):
        only_providers = ["atlas-cloud"]
    if model_name.startswith("z-ai/glm-4.7"):
        only_providers = ["z-ai"]
    if model_name.startswith("anthropic"):
        only_providers = None  # ["anthropic"] gives 521 and 520 errors intermittently
    if model_name.startswith("openai"):
        only_providers = None
    extra_params = {"provider": {"allow_fallbacks": False, "only": only_providers}}
    print(f"LLM calling with {model_name}")
    # extra_params = {}
    while True:
        try:
            response = client.responses.create(
                model=model_name,
                instructions=instructions,
                input=llm_input,
                extra_body=extra_params,
            )
            break  # jump out if we're successful
        except json.JSONDecodeError:
            print("Oops, got a JSONDecodeError after calling LLM")

    print(f"Raw return from llm call:\n{response.output_text}")
    extracted = utils.extract_from_triple_backticks(response.output_text)
    print(f"Extracted answer:\n{extracted}")
    return extracted


# return response.output_text


if __name__ == "__main__":
    print(f"Openrouter API key: {os.getenv('OPENROUTER_API_KEY')}")
    moves = ["e2e4", "d7d5", "g1f3"]

    from stockfish import Stockfish

    from utils import SF_PATH, printable_clean_sf_visual

    # model_name = 'meta-llama/llama-4-scout' # fast
    model_name = "deepseek/deepseek-v3.1-terminus"  # fast
    model_name = "deepseek/deepseek-v3.2-speciale"  # non responsive
    model_name = "z-ai/glm-4.7"  # slow

    sf_params = {"Skill Level": 1}
    sfi = Stockfish(path=SF_PATH, parameters=sf_params)
    sfi.set_position(moves)
    fen = sfi.get_fen_position()
    visualiser_routine = printable_clean_sf_visual
    board_render = visualiser_routine(sfi)
    for n in range(5):
        mv = call_llm(
            "black", moves, fen=fen, board_render=board_render, model_name=model_name
        )
        print(mv)
