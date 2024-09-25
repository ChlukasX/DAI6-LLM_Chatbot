from dotenv import load_dotenv
import os
from groq import Groq
import requests
import json

# Load environment variables
load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

# List of models
models = [
    ["Meta-llama3", "llama3-8b-8192"],
    ["Gemma 2 9B", "gemma2-9b-it"],
    ["GPT2", "openai-community/gpt2"],
    ["Zephyr-7b", "HuggingFaceH4/zephyr-7b-beta"],
    ["Gemma-7b", "google/gemma-7b"],
    ["DialoGPT", "microsoft/DialoGPT-medium"],
]

# Initialize Groq client
client = Groq(api_key=os.environ.get("API_KEY"))

def query(payload, api_url, headers):
    """Send query to the API."""
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return {}
    except Exception as err:
        print(f"Error occurred: {err}")
        return {}

def ask_question_huggingface(model_url, question):
    """Send a question to Huggingface API."""
    API_URL = "https://api-inference.huggingface.co/models/" + model_url
    headers = {"Authorization": f"Bearer {huggingface_token}"}
    
    output = query({"inputs": question}, API_URL, headers)
    
    print(f"\nAI ({model_url}):\n")

    if 'error' in output:
        print(f"Error: {output['error']}")
    else:
        for item in output:
            if 'generated_text' in item:
                print(f"{item['generated_text']}\n")

def ask_question_groq(question, model):
    """Send a question to Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": question}],
            model=model,
        )
        print(f"\nAI ({model}):\n")
        print(chat_completion.choices[0].message.content + "\n")
    except Exception as e:
        print(f"Error communicating with Groq API: {e}")

def main():
    """Main loop for user interaction."""
    while True:
        # Display model list
        print("\nAvailable models:")
        print("0. Exit")
        for idx, model in enumerate(models, 1):
            print(f"{idx}. {model[0]}")

        # Input validation for model choice
        user_input = input("\nChoose a model (type the number or '0' to exit): ").strip()
        if user_input == "0":
            print("Goodbye!")
            break

        try:
            selected_model = models[int(user_input) - 1]
        except (IndexError, ValueError):
            print("Invalid selection. Please choose a valid model number.")
            continue

        # Ask the question
        user_question = input("You: ").strip()
        if user_question.lower() == "quit":
            print("Goodbye!")
            break

        # Display the user question as if in a chat format
        print(f"\nUser:\n{user_question}\n")

        # Determine the API to use based on the model URL format
        model_name, model_url = selected_model

        if "/" in model_url:
            print("\nUsing Huggingface API")
            ask_question_huggingface(model_url, user_question)
        else:
            print("\nUsing Groq API")
            ask_question_groq(user_question, model_url)

if __name__ == "__main__":
    main()