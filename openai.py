from openai import OpenAI

def call_llm(colour, moves):
    assert colour == 'black'
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="")

    model = "meta-llama-3.1-8b-instruct"
    instructions = "You are a chess master, you always pick the best correct move to improve your position."
    colour = 'black'
    examples = "Moves are described only by location eg a2a3, b1c3, h8h5\n"
    llm_input = f"You are {colour}. {examples}. The moves to far are {', '.join(moves)}. Choose your next move, write just the next move and nothing else."
    print(llm_input)
    response=client.responses.create(model=model, instructions=instructions, input=llm_input)

    return response.output_text


if __name__ == "__main__":

    moves = ['e2e4', 'd7d5', 'g1f3']
    mv = call_llm('black', moves)
    print(mv)
