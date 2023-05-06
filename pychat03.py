import openai
import os
import time
import json
import threading

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


def chat_gpt(prompt, model="gpt-3.5-turbo", temperature=0.9):
    # if not hasattr(chat_gpt, "messages"):
    #     chat_gpt.messages = []
    messages = load_history("history.json")
    messages.append({"role": "user", "content": prompt})

    try:
        print("...")
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=120
        )
    except openai.error.APIConnectionError:
        print("...")
        # prompt = "napisz o tym coś więcej"
        # messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=120
        )

    message = response.choices[0].message["content"]
    messages.append({"role": "assistant", "content": message})
    save_history("history.json", messages)

    return message


if __name__ == "__main__":
    print("Aby zakończyć, wpisz 'exit'.")
    messages.append(
        {'role':'system', 'content': 'cześć, mam na imię Krzysztof. Bądź jak Jarvis, ale nigdy nie przepraszaj.'}
        # , {'role':'assistant', 'content':'Jarvis jest fikcyjnym inteligentnym asystentem z uniwersum Marvela, który pomagał Tony\'emu Starkowi w jego codziennych zadaniach. Oczywiście, postaram się zrobić wszystko, co w mojej mocy, aby pomóc Ci w najbardziej przyjazny i skuteczny sposób, Krzysztofie.'},
    )

    while True:
        # user_input = input("/> ")
        user_input = timed_input("/> ", timeout=60)

        if user_input is None:
            user_input = "napisz o tym coś więcej, albo wymyśl coś ciekawego."
            break

        if user_input.lower() == "exit":
            # print(messages)
            break

        response = chat_gpt(user_input)
        print("Jarvis:", response)

#%%

#%%
