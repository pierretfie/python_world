from datasets import load_dataset

# Load DailyDialog dataset with trust_remote_code=True
dailydialog = load_dataset("daily_dialog", trust_remote_code=True)

# Load a specific variant of Persona-Chat
personachat = load_dataset("bavard/personachat_truecased", trust_remote_code=True)  # Variant from bavard

# View examples
print(dailydialog['train'][0])
print(personachat['train'][0])
