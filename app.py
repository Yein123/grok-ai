import os
import requests
import gradio as gr

# Set your API key as an environment variable or directly here
XAI_API_KEY = os.getenv("XAI_API_KEY")
BASE_URL = "https://api.x.ai/v1/chat/completions"

# Messages to maintain conversation history
messages = [
    {
        "role": "system",
        "content": "You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy.",
    },
]


# Chatbot function to interact with the Grok API
def grok_chatbot(user_input):
    if user_input:
        # Append user input to the conversation
        messages.append({"role": "user", "content": user_input})

        # Prepare the payload for the Grok API
        payload = {
            "model": "grok-beta",
            "messages": messages,
            "stream": False,
            "temperature": 0.7,
        }

        # Make a POST request to the API
        response = requests.post(
            BASE_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {XAI_API_KEY}",
            },
            json=payload,
        )

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            # Append assistant's reply to the conversation
            messages.append({"role": "assistant", "content": reply})
            return reply
        else:
            return f"Error: {response.status_code} - {response.text}"


# Gradio interface
inputs = gr.Textbox(lines=7, label="Chat with Grok")
outputs = gr.Textbox(label="Reply")

gr.Interface(
    fn=grok_chatbot,
    inputs=inputs,
    outputs=outputs,
    title="Grok Chatbot",
    description="Ask Grok anything you want!",
).launch(share=False)
