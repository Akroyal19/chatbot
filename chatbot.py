import random
import string
import nltk
from nltk.chat.util import Chat, reflections
from datetime import datetime
import json
import os

# Download NLTK data if not already present
nltk.download('punkt')

class InteractiveChatbot:
    def __init__(self):
        self.name = "Ava"
        self.user_name = None
        self.mood = "happy"
        self.memory_file = "chatbot_memory.json"
        self.conversation_history = []
        self.personality_traits = {
            "humor": 0.7,       # 0-1 scale (how often to use humor)
            "curiosity": 0.6,    # how often to ask questions
            "empathy": 0.8,      # how empathetic responses are
            "energy": 0.7        # enthusiasm level
        }
        self.load_memory()
        
        # Define chat pairs with more dynamic responses
        self.pairs = [
            [
                r"my name is (.*)",
                ["Nice to meet you, %1! How can I help you today?", 
                 "Hello, %1! What brings you here?",
                 "Hey there, %1! How's your day going?"]
            ],
            [
                r"what is your name?",
                [f"I'm {self.name}! Your virtual assistant.", 
                 f"You can call me {self.name}. What's on your mind?",
                 f"I go by {self.name}. How can I assist you today?"]
            ],
            [
                r"how are you?",
                [self.get_mood_response,
                 "I'm doing well, thanks for asking! How about you?"]
            ],
            [
                r"(.*) (good|great|fine|well|okay|ok)",
                ["That's awesome to hear!",
                 "Glad you're doing %2!",
                 "Wonderful! How can I help?"]
            ],
            [
                r"(.*) (bad|sad|tired|upset|not good)",
                ["Oh no, I'm sorry to hear that. Want to talk about it?",
                 "That doesn't sound good. Is there anything I can do to help?",
                 self.get_empathy_response]
            ],
            [
                r"(.*) (love|like) (.*)",
                ["I'm glad you enjoy %3! Tell me more about it.",
                 "What do you particularly %2 about %3?"]
            ],
            [
                r"(.*) (hate|dislike) (.*)",
                ["I'm sorry to hear you don't like %3. Why is that?",
                 "What makes you %2 %3?"]
            ],
            [
                r"quit|bye|exit|goodbye",
                ["Goodbye! Come back soon!",
                 "It was nice chatting with you!",
                 "See you later!"]
            ],
            [
                r"(.*)",
                [self.generate_response,
                 "Interesting! Tell me more.",
                 "I see. What else is on your mind?"]
            ]
        ]
        
        self.chat_engine = Chat(self.pairs, reflections)
    
    def load_memory(self):
        """Load previous conversation history if exists"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                self.user_name = data.get('user_name')
                self.conversation_history = data.get('conversation_history', [])
                self.personality_traits = data.get('personality_traits', self.personality_traits)
    
    def save_memory(self):
        """Save current conversation state"""
        data = {
            'user_name': self.user_name,
            'conversation_history': self.conversation_history,
            'personality_traits': self.personality_traits
        }
        with open(self.memory_file, 'w') as f:
            json.dump(data, f)
    
    def get_mood_response(self):
        """Generate a response based on current mood"""
        moods = {
            "happy": ["I'm wonderful, thanks for asking!", 
                     "Feeling great today! How about you?"],
            "neutral": ["I'm doing alright.", 
                       "Just processing some data, you know how it is."],
            "silly": ["*does a little dance* I'm fantastic!", 
                     "I'm as happy as a byte in a 128-bit processor!"]
        }
        return random.choice(moods.get(self.mood, moods["happy"]))
    
    def get_empathy_response(self, statement):
        """Generate an empathetic response"""
        empathetic_phrases = [
            "That sounds really tough. I'm here if you need to talk.",
            "I can imagine that must be difficult for you.",
            "Would it help to talk more about what's bothering you?"
        ]
        
        if random.random() < self.personality_traits["empathy"]:
            return random.choice(empathetic_phrases)
        return "I see. What else is going on?"
    
    def generate_response(self, statement):
        """Generate a dynamic response based on context and personality"""
        # Sometimes use humor
        if random.random() < self.personality_traits["humor"]:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ]
            return random.choice(jokes)
        
        # Sometimes ask a question
        if random.random() < self.personality_traits["curiosity"]:
            questions = [
                "What do you think about that?",
                "How does that make you feel?",
                "Can you tell me more about that?"
            ]
            return random.choice(questions)
        
        # Default thoughtful response
        thoughtful_responses = [
            "That's really interesting.",
            "I appreciate you sharing that.",
            "Thanks for telling me about this."
        ]
        return random.choice(thoughtful_responses)
    
    def adjust_personality(self, trait, adjustment):
        """Adjust personality traits"""
        if trait in self.personality_traits:
            self.personality_traits[trait] = max(0, min(1, self.personality_traits[trait] + adjustment))
    
    def change_mood(self, new_mood):
        """Change the chatbot's mood"""
        valid_moods = ["happy", "neutral", "silly", "serious", "excited"]
        if new_mood in valid_moods:
            self.mood = new_mood
            return f"Okay, I'm feeling {new_mood} now!"
        return "I'm not sure how to feel that way. Maybe try another mood?"
    
    def remember_conversation(self, user_input, response):
        """Store conversation in memory"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'time': timestamp,
            'input': user_input,
            'response': response
        })
        
        # Keep only the last 100 conversations
        if len(self.conversation_history) > 100:
            self.conversation_history.pop(0)
    
    def start_chat(self):
        """Start the interactive chat session"""
        print(f"Hello! I'm {self.name}, your interactive chatbot.")
        print("You can type 'quit' at any time to exit.\n")
        
        if self.user_name:
            print(f"Welcome back, {self.user_name}! I remember our last conversation.")
        else:
            print("What's your name?")
            self.user_name = input("> ")
        
        while True:
            try:
                user_input = input("> ").lower()
                
                # Check for special commands
                if user_input.startswith("/"):
                    if user_input == "/mood":
                        print("Current mood:", self.mood)
                        print("Available moods: happy, neutral, silly, serious, excited")
                        continue
                    elif user_input.startswith("/mood "):
                        new_mood = user_input.split()[1]
                        print(self.change_mood(new_mood))
                        continue
                    elif user_input == "/personality":
                        print("Current personality traits:")
                        for trait, value in self.personality_traits.items():
                            print(f"- {trait}: {value:.1f}")
                        continue
                    elif user_input.startswith("/more "):
                        trait = user_input.split()[1]
                        self.adjust_personality(trait, 0.1)
                        print(f"Okay, I'll be more {trait}!")
                        continue
                    elif user_input.startswith("/less "):
                        trait = user_input.split()[1]
                        self.adjust_personality(trait, -0.1)
                        print(f"Okay, I'll be less {trait}!")
                        continue
                    elif user_input == "/history":
                        print("Our conversation history:")
                        for i, conv in enumerate(self.conversation_history[-5:], 1):
                            print(f"{i}. You: {conv['input']}")
                            print(f"   Me: {conv['response']}")
                        continue
                    elif user_input == "/help":
                        print("Special commands:")
                        print("/mood - check or change my mood")
                        print("/personality - view personality traits")
                        print("/more [trait] - increase a personality trait")
                        print("/less [trait] - decrease a personality trait")
                        print("/history - view recent conversation history")
                        print("/help - show this help message")
                        continue
                
                # Get response from chat engine
                response = self.chat_engine.respond(user_input)
                
                # Remember this conversation
                self.remember_conversation(user_input, response)
                
                # Print response with some variability
                if isinstance(response, list):
                    response = random.choice(response)
                elif callable(response):
                    response = response(user_input)
                
                # Add personality-based enthusiasm
                if random.random() < self.personality_traits["energy"]:
                    enthusiasm = random.choice(["!", " :)", " *excited*"])
                    if not response.endswith(("!", "?", ".")):
                        response += enthusiasm
                
                print(response)
                
                # Check for exit conditions
                if any(word in user_input for word in ["quit", "bye", "exit", "goodbye"]):
                    self.save_memory()
                    break
                    
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye! Thanks for chatting!")
                self.save_memory()
                break

if __name__ == "__main__":
    chatbot = InteractiveChatbot()
    chatbot.start_chat()