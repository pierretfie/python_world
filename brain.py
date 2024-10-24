from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset
from os import path

# Load GPT-2 tokenizer and model
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the pad_token to eos_token to avoid padding issues
tokenizer.pad_token = tokenizer.eos_token

model = GPT2LMHeadModel.from_pretrained(model_name)

# Dataset for fine-tuning
data = {
    'text': [
        "User: Hello!\nBot: Hi there! How can I assist you?",
        "User: Hey!\nBot: Hello! How can I help you today?",
        "User: Hi\nBot: Hey! How are you?"
    ]
}

dataset = Dataset.from_dict(data)

# Tokenize the data
def tokenize_function(example):
    return tokenizer(example['text'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Fine-tuning GPT-2
# Define training arguments
training_args = TrainingArguments(
    output_dir=path.expanduser('~/Documents/brain'),  # where to save the model
    num_train_epochs=3,  # number of training epochs
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,  # only keep the latest two models
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets
)

# Train the model
trainer.train()

# Test the fine-tuned model
input_text = "User: Hello!\nBot:"
inputs = tokenizer.encode(input_text, return_tensors='pt')

# Generate a response
outputs = model.generate(inputs, max_length=50, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
