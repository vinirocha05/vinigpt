import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4.1-mini"


def list_models():
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{BASE_URL}/models", headers=headers)
        response.raise_for_status()
        models = response.json()
        print("------------")
        print("Modelos disponíveis")
        for modelo in models["data"]:
            print(f"{modelo['id']}")

    except requests.RequestException as e:
        print("Ocorreu um erro na chamada da API: ", e)


def chat_with_model(model):
    conversation_history = [
        {
            "role": "system",
            "content": "Você é um assistente atencioso e animado! Sempre me ajudando a estudar Data Science, explicando cada detalhe do código e me incentivando a constitunar os estudos",
        }
    ]

    print("Bem vindo ao Vini GPT, você está usando o modelo ", model)
    print("Digite sair para encerrar a conversa")

    while True:
        user_input = input("\nUsuário: ")

        if user_input.lower() == "sair":
            print("Obrigado por conversar comigo. Até a próxima!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            data = {"model": model, "messages": conversation_history}

            response = requests.post(
                f"{BASE_URL}/chat/completions", headers=headers, json=data
            )
            response.raise_for_status()
            resposta_assistente = response.json()["choices"][0]["message"]["content"]

            print(f"\nVini GPT: {resposta_assistente}")

            conversation_history.append(
                {"role": "assistant", "content": resposta_assistente}
            )
        except requests.RequestException as e:
            print("Ocorreu um erro na chamada da API: ", e)


def main():
    # Lista modelos
    list_models()

    # Escolhe modelo
    modelo_escolhido = input("Escolha um modelo: ")

    if not modelo_escolhido:
        modelo_escolhido = DEFAULT_MODEL
        print("Seguiremos com o ", DEFAULT_MODEL)

    chat_with_model(modelo_escolhido)


if __name__ == "__main__":
    main()
