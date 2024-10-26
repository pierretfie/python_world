from transformers import GPT2Tokenizer, GPT2LMHeadModel
model_path = '~/Documents/brain'
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

#function to generate response
def  generate_response(user_input):
    input_text = f"User: {user_input}\nBot:"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length = 50, num_return_sequence=1, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_specia_tokens =True)
    bot_response = response.split("Bot:")[-1].strip()
    return bot_response
#conversation loop for multiple responses
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye!")
        break
    response = generate_response(user_input)
    print(f'Bot: {response}')


