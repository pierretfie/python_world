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
        temperature=0.5,
        top_p=0.9,
        top_k=10,
        do_sample=True
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


