import streamlit as st
import json
import os

# Load the index
# index_path = '/Users/tarakram/Documents/Chatbot/index'
# with open(index_path, 'r') as f:
#     index = json.load(f)
from llama_index import StorageContext, load_index_from_storage

os.environ["OPENAI_API_KEY"] = 'Add your API Key here '

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir='/Users/tarakram/Documents/Chatbot/index')
# load index
index = load_index_from_storage(storage_context)

# Create the chatbot
# Chat Bot 

import openai
import json

class Chatbot:
    def __init__(self, api_key, index, user_id):
        self.index = index
        openai.api_key = api_key
        self.user_id = user_id
        self.chat_history = []
        self.filename = f"{self.user_id}_chat_history.json"

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self):
        try:
            with open(self.filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self):
        with open(self.filename, 'w') as f:
            json.dump(self.chat_history, f)
            
# Streamlit app
def main():
    st.title("Chatbot")

    # User ID
    user_id = st.text_input("Your Name:")
    
    # Check if user ID is provided
    if user_id:
        # Create chatbot instance for the user
        bot = Chatbot("Add your API Key here ", index, user_id)

        # Load chat history
        bot.load_chat_history()

        # Display chat history
        for message in bot.chat_history[-6:]:
            st.write(f"{message['role']}: {message['content']}")

        # User input
        user_input = st.text_input("Type your questions here :) - ")

        # Generate response
        if user_input:
            if user_input.lower() in ["bye", "goodbye"]:
                bot_response = "Goodbye!"
            else:
                bot_response = bot.generate_response(user_input)
                bot_response_content = bot_response['content']
                st.write(f"{user_id}: {user_input}")
                st.write(f"Bot: {bot_response_content}")
                bot.save_chat_history()
                bot.chat_history.append({"role": "user", "content": user_input})
                bot.chat_history.append({"role": "assistant", "content": bot_response_content})

if __name__ == "__main__":
    main()
