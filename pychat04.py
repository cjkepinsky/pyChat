import openai
import os
import time
import json
import threading
import sys
import tiktoken
import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("Nie udało się odczytać wartości zmiennej środowiskowej OPENAI_API_KEY.")
    exit(1)

messages = []


def load_history(file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    else:
        return []


def save_history(file_name, history):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)
    with open(file_path, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def timed_input(prompt, timeout=60):
    result = []

    def on_input():
        result.append(input(prompt))

    thread = threading.Thread(target=on_input)
    thread.start()
    thread.join(timeout)

    return result[0] if result else None


class WaitingPrompt:
    def __init__(self, interval=1):
        self.interval = interval
        self.finished = False
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while not self.finished:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(self.interval)

    def start(self):
        self.finished = False
        self.thread.start()

    def stop(self):
        self.finished = True
        self.thread.join()


def count_tokens(text):
    # return len(text.split())
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))



def chat_gpt(prompt, model="gpt-3.5-turbo", temperature=0.9):
    # if not hasattr(chat_gpt, "messages"):
    #     chat_gpt.messages = []
    prompt_len = count_tokens(prompt)
    max_tokens = 3600 - prompt_len
    messages = load_history("history.json")
    messages.append({"role": "user", "content": prompt})

    tokens = sum([count_tokens(m["content"]) for m in messages]) + prompt_len
    # print("\ntokens1: ", tokens)
    # print("\nmax_tokens: ", max_tokens)
    # res = tokens >= max_tokens
    # print("\nres: ", res)
    while tokens >= max_tokens - prompt_len:
        removed_message = messages.pop(0)
        # print("\n--removed: ", removed_message["content"])
        tokens -= count_tokens(removed_message["content"])
        # print("\ntokens2: ", tokens)

    waiting_prompt = WaitingPrompt()
    waiting_prompt.start()

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=120
        )
    except openai.error.APIConnectionError:
        # prompt = "napisz o tym coś więcej"
        # messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=120
        )

    waiting_prompt.stop()

    message = response.choices[0].message["content"]
    messages.append({"role": "assistant", "content": message})
    save_history("history.json", messages)

    return message


if __name__ == "__main__":
    print("Aby zakończyć, wpisz 'exit'.")
    messages.append(
        {'role': 'system', 'content': 'cześć, mam na imię Krzysztof. Bądź jak Jarvis, ale nigdy nie przepraszaj.'}
        # , {'role':'assistant', 'content':'Jarvis jest fikcyjnym inteligentnym asystentem z uniwersum Marvela, który pomagał Tony\'emu Starkowi w jego codziennych zadaniach. Oczywiście, postaram się zrobić wszystko, co w mojej mocy, aby pomóc Ci w najbardziej przyjazny i skuteczny sposób, Krzysztofie.'},
    )

    while True:
        user_input = timed_input("/> ", timeout=120)

        if user_input is None or user_input == "":
            user_input = "napisz o tym coś więcej."

        if user_input.lower() == "exit":
            # print(messages)
            break

        response = chat_gpt(user_input)
        print("\nJarvis:", response)
        print("\n\r")
        # pyautogui.press('enter')
