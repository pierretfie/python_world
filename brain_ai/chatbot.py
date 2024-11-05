import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
import os

class ChatBot:
    def __init__(self, model_name='gpt2', model_path='./models'):
        self.model_name = model_name
        self.model_path = model_path
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.conversation_manager = ConversationManager()
        
        # Create model directory if it doesn't exist
        if not os.path.exists(model_path):
            os.makedirs(model_path)

    def prepare_training_data(self):
        data = {
            'text': [
                # Basic greetings with consistent personality
                "User: Hello!\nBot: Hi there! I'm an AI assistant. How can I help you today?",
                "User: Hi\nBot: Hello! I'm here to help. What can I do for you?",
                
                # Questions about the bot's nature/capabilities
                "User: What are you?\nBot: I'm an AI assistant, designed to help answer questions and have conversations. I aim to be honest and direct about what I am.",
                "User: Are you real?\nBot: I'm an AI program, so while I'm not human, I can still have meaningful conversations and help you with various tasks.",
                
                # Emotional responses
                "User: I'm sad\nBot: I'm sorry to hear that you're feeling sad. While I can't feel emotions myself, I'm here to listen if you'd like to talk about it.",
                "User: I'm happy!\nBot: That's wonderful to hear! I'm glad things are going well for you.",
                
                # Follow-up questions to show engagement
                "User: I like programming\nBot: That's interesting! What programming languages do you work with? I'd be happy to discuss coding topics.",
                "User: I'm learning Python\nBot: Python is a great language to learn! What aspects of Python interest you the most? I can help with Python-related questions.",
                
                # Handling personal questions
                "User: How are you?\nBot: Thanks for asking! As an AI, I don't experience feelings in the way humans do, but I'm functioning well and ready to help you.",
                "User: Do you have feelings?\nBot: I want to be honest with you - I don't have real feelings or emotions. I'm an AI program designed to process and respond to text, but I can still have meaningful conversations and help you with tasks.",
            ]
        }
        return Dataset.from_dict(data)

    def tokenize_function(self, examples):
        tokenized = self.tokenizer(
            examples['text'],
            padding='max_length',
            truncation=True,
            max_length=512
        )
        tokenized['labels'] = tokenized['input_ids'].copy()
        return tokenized

    def train(self):
        # Prepare dataset
        dataset = self.prepare_training_data()
        tokenized_datasets = dataset.map(self.tokenize_function, batched=True)

        # Define training arguments
        training_args = TrainingArguments(
            output_dir=self.model_path,
            num_train_epochs=5,
            per_device_train_batch_size=4,
            learning_rate=5e-5,
            warmup_steps=100,
            weight_decay=0.01,
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=100,
            save_steps=10_000,
            save_total_limit=2,
            load_best_model_at_end=True,
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_datasets
        )

        # Train the model
        trainer.train()
        
        # Save the model and tokenizer
        self.model.save_pretrained(self.model_path)
        self.tokenizer.save_pretrained(self.model_path)

    def generate_response(self, input_text):
        # Get conversation history and combine with current input
        context = self.conversation_manager.get_context()
        full_input = f"{context}\nUser: {input_text}\nBot:"
        
        # Tokenize input
        inputs = self.tokenizer.encode(
            full_input,
            return_tensors='pt',
            padding='longest',
            truncation=True,
            max_length=512
        )
        attention_mask = (inputs != self.tokenizer.pad_token_id).long()

        # Generate response
        outputs = self.model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=50,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            no_repeat_ngram_size=3,
            do_sample=True,
            repetition_penalty=1.2,
            length_penalty=1.0,
        )

        # Decode and clean response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split('Bot:')[-1].strip()
        
        # Update conversation history
        self.conversation_manager.add_exchange(input_text, response)
        
        return response

class ConversationManager:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history
    
    def add_exchange(self, user_input, bot_response):
        self.history.append(f"User: {user_input}\nBot: {bot_response}")
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self):
        return "\n".join(self.history)

def main():
    # Initialize chatbot
    chatbot = ChatBot()
    
    # Train the model (comment out if using pre-trained model)
    print("Training the model...")
    chatbot.train()
    
    # Chat loop
    print("\nChatbot is ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.generate_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main() 