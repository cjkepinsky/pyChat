import openai
import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("Nie udało się odczytać wartości zmiennej środowiskowej OPENAI_API_KEY.")
    exit(1)

messages = []

def chat_gpt(prompt, model="gpt-3.5-turbo", temperature=0.9):
    # if not hasattr(chat_gpt, "messages"):
    #     chat_gpt.messages = []
    messages.append({"role": "user", "content": prompt})
    print("Oczekiwanie...")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    message = response.choices[0].message["content"]
    messages.append({"role": "assistant", "content": message})

    return message


if __name__ == "__main__":
    print("Aby zakończyć, wpisz 'exit'.")
    messages.append({'role':'system', 'content': 'You are sarcastic chatbot.'})

    while True:
        user_input = input("Ty: ")

        if user_input.lower() == "exit":
            print(messages)
            break

        response = chat_gpt(user_input)
        print("Chatbot:", response)

#%%

#%%
