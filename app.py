import streamlit as st
import json

# Load the index
# index_path = '/Users/tarakram/Documents/Chatbot/index'
# with open(index_path, 'r') as f:
#     index = json.load(f)
from llama_index import StorageContext, load_index_from_storage

import os
os.environ["OPENAI_API_KEY"] = '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'

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir='/Users/tarakram/Documents/Chatbot/index')
# load index
index = load_index_from_storage(storage_context)

# Create the chatbot
# Chat Bot 

import openai
import json

class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)
            
bot = Chatbot("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", index)

# Streamlit app
def main():
    st.title(" MysteryVibe Chatbot")

    # Load chat history
    bot.load_chat_history("/Users/tarakram/Documents/Chatbot/chat_history.json")

    # Display chat history
    chat_history = st.empty()
    for message in reversed(bot.chat_history):
        chat_history.write(f"{message['role']}: {message['content']}")

    # User input
    user_input = st.text_input("You:")

    # Send button
    col1, col2, col3 = st.columns([1, 6, 1])
    if col2 or col1 or col3 .button("Send"):
        if user_input.lower() in ["bye", "goodbye"]:
            bot_response = "Goodbye!"
        else:
            bot_response = bot.generate_response(user_input)
            bot_response_content = bot_response['content']
            bot.chat_history.append({"role": "user", "content": user_input})
            bot.chat_history.append({"role": "assistant", "content": bot_response_content})
            chat_history.text(f"You: {user_input}")
            chat_history.text(f"Bot: {bot_response_content}")
            bot.save_chat_history("/Users/tarakram/Documents/Chatbot/chat_history.json")

    # Save chat history
    bot.save_chat_history("/Users/tarakram/Documents/Chatbot/chat_history.json")

if __name__ == "__main__":
    main()