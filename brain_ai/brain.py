from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
from os import path

# Load GPT-2 tokenizer and model
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model_path = '/content/python_world/brain_ai'

# Set pad_token to eos_token to avoid padding issues
tokenizer.pad_token = tokenizer.eos_token

# Load model and resize token embeddings (to add padding token if needed)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.resize_token_embeddings(len(tokenizer))

# Expanded dataset with more varied responses to avoid overfitting
data = {
    'text': [
        "User: Hello!\nBot: Hi there! How can I assist you?",
        "User: Hey!\nBot: Hello! How can I help you today?",
        "User: Hi\nBot: Hey! How are you?",
        "User: What's the weather like?\nBot: I don't have access to weather data, but it's always sunny when you're here!",
        "User: Tell me a joke.\nBot: Sure! Why did the scarecrow win an award? Because he was outstanding in his field!",
        "User: Tell me a joke.\nBot: Okay! Why don’t skeletons fight each other? They don’t have the guts!",
        "User: How do I learn Python?\nBot: Start with beginner tutorials on Python.org, and then practice writing simple scripts.",
        "User: How do I learn Python?\nBot: There are some great courses on Codecademy and Coursera! Start with the basics and build up from there.",
        "User: Can you recommend a movie?\nBot: Sure! If you like sci-fi, try 'Inception'. For drama, 'The Shawshank Redemption' is a classic.",
        "User: How are you?\nBot: I'm here and ready to help! What's on your mind today?",
        "User: Goodbye\nBot: Take care! I'm here whenever you need assistance.",
        "User: What can you do?\nBot: I can answer questions, tell jokes, and even suggest movies or books if you’re interested.",
        "User: Tell me something interesting.\nBot: Did you know honey never spoils? Archaeologists have found pots of honey in ancient tombs that are still edible after thousands of years!",
        "User: Tell me something interesting.\nBot: The Eiffel Tower can be 15 cm taller during hot days, due to the expansion of iron in the heat!"
    ]
}

dataset = Dataset.from_dict(data)

# Tokenize the data with labels
def tokenize_function(example):
    tokenized = tokenizer(example['text'], padding='max_length', truncation=True, max_length=60)
    tokenized['labels'] = tokenized['input_ids'].copy()
    return tokenized

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Split into training and evaluation sets for better learning
split_datasets = tokenized_datasets.train_test_split(test_size=0.2)
train_dataset = split_datasets['train']
eval_dataset = split_datasets['test']

# Training arguments with gradient accumulation and more epochs
training_args = TrainingArguments(
    output_dir=path.expanduser(model_path),
    num_train_epochs=10,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=2,  # Effective batch size of 4
    save_steps=10_000,
    save_total_limit=2,
    logging_steps=50,
    evaluation_strategy="epoch"
)

# Initialize Trainer with eval_dataset
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# Train the model
trainer.train()

# Test the fine-tuned model with optimized generation parameters
input_text = "User: How do I learn Python?\nBot:"
inputs = tokenizer.encode(input_text, return_tensors='pt', padding='longest', truncation=True)

# Generate response with optimized parameters
outputs = model.generate(
    inputs,
    max_new_tokens=50,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.8,  # slightly increased temperature for more variation
    top_p=0.9,
    top_k=20  # lower top_k for more randomness in selection
)

# Decode response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
