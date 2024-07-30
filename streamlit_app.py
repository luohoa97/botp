from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import threading
import time

# Define the path to the database file
db_path = 'database.sqlite3'

# Create a new ChatBot instance
chatbot = ChatBot(
    'RoleplayBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation'
    ],
    database_uri=f'sqlite:///{db_path}'
)

# Define roleplay data with alternating roles
roleplay_data = [
    "User: Hello, how are you?",
    "Bot: I'm great, thanks! How can I assist you today?",
    "User: Can you tell me a joke?",
    "Bot: Sure! Why did the chicken join a band? Because it had the drumsticks!",
    "User: That's funny!",
    "Bot: Glad you liked it! What else can I do for you?"
]

# Function to train the ChatBot
def train_chatbot():
    trainer = ListTrainer(chatbot)
    trainer.train(roleplay_data)
    print("Training completed.")

# Function to auto-save the chatbot state
def auto_save():
    while True:
        print("Auto-saving...")
        chatbot.storage.drop()  # Ensure database integrity
        chatbot.storage.save()
        time.sleep(60)  # Save every 60 seconds

# Function to handle roleplay interaction
def roleplay_mode():
    print("Roleplay Mode. Alternating between roles...")
    for item in roleplay_data:
        role, text = item.split(": ")
        print(f"{role}: {text}")
        if role == "User":
            # Get bot's response
            response = chatbot.get_response(text)
            print("Bot:", response)

# Function to handle chat interaction
def chat_mode():
    print("Chat Mode. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        bot_response = chatbot.get_response(user_input)
        print("Bot:", bot_response)

# Main function to toggle between modes
def main():
    # Train the ChatBot
    train_chatbot()
    
    # Start auto-save in the background
    auto_save_thread = threading.Thread(target=auto_save)
    auto_save_thread.daemon = True
    auto_save_thread.start()
    
    # Toggle between roleplay mode and chat mode
    while True:
        mode = input("Enter 'roleplay' for roleplay mode, 'chat' for chat mode, or 'exit' to quit: ").strip().lower()
        if mode == 'roleplay':
            roleplay_mode()
        elif mode == 'chat':
            chat_mode()
        elif mode == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please enter 'roleplay', 'chat', or 'exit'.")

if __name__ == '__main__':
    main()
