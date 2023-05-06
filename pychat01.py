import openai
import os
import sys
import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("Nie udało się odczytać wartości zmiennej środowiskowej OPENAI_API_KEY.")
    exit(1)

openai.api_key = api_key

def chat_gpt(prompt):
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=150,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    #
    # return response.choices[0].text.strip()
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.9,
        max_tokens=1060,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    # print("A: ", response.choices[0].text)

    return response.choices[0].text.strip()


if __name__ == "__main__":
    print("Witaj w CLI ChatGPT-4! Aby zakończyć, wpisz 'exit'.")
    while True:
        question = input("Pytanie: ")
        if question.lower() == "exit":
            sys.exit("Do zobaczenia!")
        else:
            response = chat_gpt(question)
            print(f">>>: {response}")

#%%
