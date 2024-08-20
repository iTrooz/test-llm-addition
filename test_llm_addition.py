import random
import os
from openai import OpenAI
from tqdm import tqdm

NUM_ITER = 10
MAX_PAIR_RANGE = 100000

OPENAI_KEY=os.getenv("OPENAI_KEY")
OPENAI_CLIENT = OpenAI(api_key = OPENAI_KEY)

def make_llm_prompt(system: str, user: str) -> str:
    completion = OPENAI_CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
            ],
        stream=False,
    )
    return completion.choices[0].message.content

def make_llm_addition(a: int, b: int) -> int:
    resp = make_llm_prompt(
        "Tell me the result of this addition. Your response will be parsed as a number. ONLY RESPOND WITH A PARSABLE NUMBER",
        f"{a}+{b}"
    )
    return int(resp)

def test_random_pair():
    a = random.randint(1, MAX_PAIR_RANGE)
    b = random.randint(1, MAX_PAIR_RANGE)
    try:
        c = make_llm_addition(a, b)
    except Exception as e:
        print(f"Error: {e}")
        return None
    if c == a + b:
        return True
    else:
        print(f"Error: {a} + {b} = {a+b}, but LLM said {c}")
        return False
    

def main():
    good = 0
    bad = 0
    fails = 0
    for i in tqdm(range(NUM_ITER)):
        res = test_random_pair()
        if res == True:
            good += 1
        elif res == False:
            bad += 1
        elif res == None:
            fails += 1

    print("Results:")            
    print("NUM_ITER:", NUM_ITER)
    print("MAX_PAIR_RANGE:", MAX_PAIR_RANGE)
    print("Good:", good)
    print("Bad:", bad)
    print("Fails:", fails)


main()