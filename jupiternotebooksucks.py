from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from groq import Groq
import requests
import json

# Load environment variables
load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_API_KEY")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = Flask(__name__)

# List of models
models = [
    ["Meta-llama3", "llama3-8b-8192"],
    ["Gemma 2 9B", "gemma2-9b-it"],
    ["GPT2", "openai-community/gpt2"],
    ["Zephyr-7b", "HuggingFaceH4/zephyr-7b-beta"],
    ["Gemma-7b", "google/gemma-7b"],
    ["DialoGPT", "microsoft/DialoGPT-medium"],
]



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

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    selected_model = ""
    if request.method == "POST":
        selected_model = request.form["model"]
        user_question = request.form["question"]

        # Find the model URL
        model_name, model_url = next((name, url) for name, url in models if name == selected_model)

        if "/" in model_url:
            # Huggingface API
            response = ask_question_huggingface(model_url, user_question)
        else:
            # Groq API
            response = ask_question_groq(user_question, model_url)

    return render_template("screen/index.html", models=models, response=response, selected_model=selected_model)

if __name__ == "__main__":
    app.run(debug=True)