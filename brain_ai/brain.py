from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset, load_dataset, concatenate_datasets
from os import path
from transformers import AdamW

# Load GPT-2 tokenizer and model
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model_path = '/content/python_world/brain_ai'


dailydialog = load_dataset("daily_dialog", split="train", trust_remote_code= True)
personachat = load_dataset("bavard/personachat_truecased", split="train", trust_remote_code=True)
empathetic_dialogues = load_dataset("empathetic_dialogues", split="train", trust_remote_code=True)
# Function to format DailyDialog conversations
#print(empathetic_dialogues.column_names)

def format_dailydialog(example):
    conversation = ""
    for i, turn in enumerate(example['dialog']):
        speaker = "User" if i % 2 == 0 else "Bot"
        conversation += f"{speaker}: {turn}\n"
    return {'text': conversation.strip()}
def format_personachat(example):
    conversation = ""
    # Access the 'history' key instead of 'utterances'
    for i, turn in enumerate(example['history']):
        speaker = "User" if i % 2 == 0 else "Bot"
        conversation += f"{speaker}: {turn}\n"
    return {'text': conversation.strip()}
def format_empathetic(example):
    # Format as User-Bot conversation using context and utterance fields
    conversation = f"User: {example['context']}\nBot: {example['utterance']}"
    return {'text': conversation.strip()}

# Apply formatting function to each conversation in DailyDialog
formatted_dailydialog = dailydialog.map(format_dailydialog)
formatted_personachat = personachat.map(format_personachat)
formatted_empathetic = empathetic_dialogues.map(format_empathetic)

# Simplify datasets to retain only the 'text' column
formatted_dailydialog = formatted_dailydialog.remove_columns([col for col in formatted_dailydialog.column_names if col != 'text'])
formatted_personachat = formatted_personachat.remove_columns([col for col in formatted_personachat.column_names if col != 'text'])
formatted_empathetic = formatted_empathetic.remove_columns([col for col in formatted_empathetic.column_names if col != 'text'])

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

original_dataset = Dataset.from_dict(data)

# Combine DailyDialog and original datasets
combined_dataset = concatenate_datasets([original_dataset, formatted_dailydialog,formatted_personachat, formatted_empathetic])

# Tokenize the data with labels
def tokenize_function(example):
    tokenized = tokenizer(example['text'], padding='max_length', truncation=True, max_length=60)
    tokenized['labels'] = tokenized['input_ids'].copy()
    return tokenized

tokenized_datasets = combined_dataset.map(tokenize_function, batched=True)

# Split into training and evaluation sets for better learning
split_datasets = tokenized_datasets.train_test_split(test_size=0.2)
train_dataset = split_datasets['train']
eval_dataset = split_datasets['test']

# Training arguments with gradient accumulation and more epochs
training_args = TrainingArguments(

    output_dir=path.expanduser(model_path),
    num_train_epochs=3,
    per_device_train_batch_size=128,
    gradient_accumulation_steps=1,  # Effective batch size of 4
    save_steps=10000,
    save_total_limit=2,
    gradient_checkpointing=True,
    dataloader_num_workers=4,
  
    #lr_scheduler_type="linear",            # Linear scheduler with warm-up
    warmup_steps=500,
    logging_steps=1000,
    eval_steps=2000,
    fp16=True,
    evaluation_strategy="epoch"
)

# Initialize Trainer with eval_dataset
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)
optimizer = AdamW(model.parameters(), lr=5e-6, betas=(0.9, 0.98)),
num_training_steps = len

# Train the model
trainer.train()


import torch

# Ensure the model is on the GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Prepare inputs
input_text = "User: how many colors do you know?\nBot:"
inputs = tokenizer.encode(input_text, return_tensors='pt', padding='longest', truncation=True)

# Transfer inputs to the same device as the model
inputs = inputs.to(device)

# Create an attention mask to handle padding tokens correctly
attention_mask = (inputs != tokenizer.pad_token_id).long()
# Adjusting generation parameters
outputs = model.generate(
    inputs,
    attention_mask=attention_mask,
    max_new_tokens=50,         # Allow the bot more tokens to complete its response
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.5,           # Reduced temperature for more deterministic output
    top_p=0.9,
    top_k=10,                  # Reduced top_k for more probable completions
    do_sample=True
)


# Decode the generated response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# Extract only the bot's first response
bot_response = response.split("Bot:")[-1].strip().split("\n")[0].split(".")[0]
print("Bot:", bot_response)

