# ChatPGT 

A Flask web application that utilizes the Groq API and Huggingface API to generate human-like responses to user input.

## Description

This project uses the Groq API to power a conversational chatbot. The Groq API allows us to generate text based on a given prompt or question, while also providing a wide range of pre-trained models to choose from. Additionally, this project utilizes the Huggingface API to access additional models and fine-tune our responses.

## Requirements

Python 3.8+
Flask (pip install flask)
Groq API (install with pip install groq)
Huggingface API (install with pip install transformers)
You can install the dependencies using pip:

``` python
pip install -r requirements.txt
The requirements.txt file contains the following dependencies:
```

- Flask
- Groq
- Transformers

## Setup

Clone the repository: git clone https://github.com/your-username/groq-chatbot.git
Copy .env.example to a .env and fill the variables
Run the application: python app.py

## Usage

Open a web browser and navigate to http://localhost:5000/
Select a model from the dropdown menu
Enter your question or prompt in the text field
Click "Ask Question" to generate a response

## Models

The following models are currently available:

- Meta-llama3 (llama3-8b-8192)
- Gemma 2 9B (gemma2-9b-it)
- GPT2 (openai-community/gpt2)
- Zephyr-7B (HuggingFaceH4/zephyr-7b-beta)
- Gemma-7B (google/gemma-7b)
- DialoGPT (microsoft/DialoGPT-medium)

## Contributing
Pull requests are welcome! Please fork the repository and submit a pull request with your changes.

# License
This project is licensed under the MIT License. See LICENSE for details.

