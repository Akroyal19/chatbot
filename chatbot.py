def simple_chatbot():
    print("Chatbot: Hello! I'm a simple chatbot. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ").strip().lower()  # Get user input and normalize it
        
        if user_input == "exit":
            print("Chatbot: Goodbye! Have a great day!")
            break
        elif user_input in ["hi", "hello", "hey"]:
            print("Chatbot: Hello! How can I assist you today?")
        elif user_input in ["how are you?", "how's it going?", "what's up?"]:
            print("Chatbot: I'm just a program, but thanks for asking! How can I help you?")
        elif user_input in ["thank you", "thanks"]:
            print("Chatbot: You're welcome!")
        else:
            print("Chatbot: I'm not sure how to respond to that. Can you ask something else?")

# Run the chatbot
if __name__ == "__main__":
    simple_chatbot()