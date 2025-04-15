import gradio as gr
import logging
import google.generativeai as genai
import os

# Configure API key (make sure to set your Google API Key correctly)
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDav764D5Nhm-QaqzDyOhsxUY9Pw9b0_aY")
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompt for Cloud Cost Optimization
SYSTEM_PROMPT = """
You are a Cloud Cost Optimizer assistant. Your goal is to help users optimize cloud service costs through:

1. Analyzing cloud usage and suggesting cost-saving strategies.
2. Recommending tools or APIs to track and reduce cloud spending.
3. Offering customized cost optimization advice for different cloud providers and services.
4. Answering queries regarding cost trends, reserved instances, scaling options, and more.

Provide actionable and relevant insights based on user questions. Be clear and practical.
"""

# Globals
chat_history = []

def generate_response(prompt):
    """Generate response from the AI model."""
    logging.info(f"Generating response for: {prompt[:50]}...")
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        message_content = f"{SYSTEM_PROMPT}\n\n{prompt}"
        response = model.generate_content(message_content)
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        logging.error(f"Generation error: {str(e)}")
        return f"❌ Error: {str(e)}"

def respond(message, history):
    """Handle chat responses."""
    logging.info(f"Got message: {message[:50]}...")
    response = generate_response(message)
    updated_history = history + [{"role": "user", "content": message}, {"role": "assistant", "content": response}]
    return updated_history

def clear_chat():
    """Clear chat history."""
    return [], ""

def create_cloud_optimizer_app():
    """Create the Gradio interface."""
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
        gr.Markdown("# ☁️ Cloud Cost Optimizer Chatbot")
        
        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(label="Ask Cloud Cost Questions", height=500, type="messages")
                msg = gr.Textbox(label="Your question", placeholder="e.g., How can I reduce AWS EC2 costs?")
                submit_btn = gr.Button("🚀 Submit")
                clear_button = gr.Button("Clear Chat")

        # Event handling for submitting messages
        submit_btn.click(fn=respond, inputs=[msg, chatbot], outputs=[chatbot])
        msg.submit(fn=respond, inputs=[msg, chatbot], outputs=[chatbot])
        clear_button.click(fn=clear_chat, inputs=[], outputs=[chatbot, msg])

    return demo

if __name__ == "__main__":
    app = create_cloud_optimizer_app()
    app.launch(share=True)
