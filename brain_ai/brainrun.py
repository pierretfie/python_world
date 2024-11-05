from transformers import GPT2Tokenizer, GPT2LMHeadModel
from os import path
import torch

model_path = '~/Desktop/coding space/brainai'
model_path = path.expanduser(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

# Add device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

#function to generate response
def  generate_response(user_input):
    input_text = f"User: {user_input}\nBot:"
    inputs = tokenizer.encode(input_text, return_tensors="pt", padding='longest', truncation=True)
    inputs = inputs.to(device)
    
    attention_mask = (inputs != tokenizer.pad_token_id).long()
    
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,
        max_new_tokens=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        do_sample=True
        repetition_penalty=1.2, # Discourages repetition
        length_penalty=1.0,     # Encourages reasonable length responses

    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    bot_response = response.split("Bot:")[-1].strip().split("\n")[0].split(".")[0]
    return bot_response

#conversation loop for multiple responses
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye!")
        break
    response = generate_response(user_input)
    print(f'Bot: {response}')




#ADD THESE
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

# Usage example
conversation = ConversationManager()

def chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        context = conversation.get_context()
        response = generate_response(user_input, context)
        print(f"Bot: {response}")
        
        conversation.add_exchange(user_input, response)