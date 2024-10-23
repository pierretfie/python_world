from transformers import GPT2Tokenizer, GPT2LMHeadModel
from datasets import Dataset
#loading GPT2 tokenizer and model
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

#dataset for fine tuning
data = {

    'text':[
        "User: Hello!\nBot: Hi there! how can i assist you?",
        "User: Hey!\nBot: Hello! How can I help you today?",
        "User: Hi\nBot: Hey! How are you?"
    ]
}

dataset = Dataset.from_dict(data)

#tokenize my data
def tokenize_function(example):
    return tokenizer(example['text'], padding='max_length', truncation=True)
tokenized_datasets = dataset.map(tokenize_function, batched=True)