import os
import pickle
from deepface import DeepFace
import numpy as np

# Path to save/load the embeddings database
embeddings_path = "/content/drive/MyDrive/embeddings_db.pkl"

# Step 1: Load existing embeddings_db if it exists, otherwise initialize an empty dictionary
if os.path.exists(embeddings_path):
    with open(embeddings_path, "rb") as f:
        embeddings_db = pickle.load(f)
else:
    embeddings_db = {}

# Reference folder with new people’s images
reference_folder = '/content/drive/MyDrive/reference_images'

# Step 2: Add new embeddings to embeddings_db
for person in os.listdir(reference_folder):
    person_folder = os.path.join(reference_folder, person)
    
    # Ensure the person key exists in the dictionary
    if person not in embeddings_db:
        embeddings_db[person] = []

    # Loop through images in the person's folder
    for img_file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_file)
        
        # Generate embedding for the image
        result = DeepFace.represent(img_path=img_path, model_name="VGG-Face", enforce_detection=False)
        embedding = result[0]["embedding"]  # Extract only the embedding array

        # Check if the embedding already exists to avoid duplicates
        if not any(np.allclose(np.array(e), embedding) for e in embeddings_db[person]):
            embeddings_db[person].append(embedding)

# Step 3: Save the updated embeddings_db back to the file
with open(embeddings_path, "wb") as f:
    pickle.dump(embeddings_db, f)

print("Embeddings database updated successfully.")
