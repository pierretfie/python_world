import numpy as np
from deepface import DeepFace

# Function for identifying a single person
def ID_single_person(img_path, embeddings_db, threshold=0.6):
    # Generate embedding for the input image
    result = DeepFace.represent(img_path=img_path, model_name='VGG-Face', enforce_detection=False)
    embedding = np.array(result[0]["embedding"])  # Ensure embedding is a numeric array

    # Compare embedding to embeddings in the database
    for person, embeddings in embeddings_db.items():
        for ref_embedding in embeddings:
            ref_embedding = np.array(ref_embedding)  # Ensure ref_embedding is also a numeric array
            distance = np.linalg.norm(ref_embedding - embedding)
            if distance < threshold:
                return person  # Match found
    
    return "Unknown, no match found"


# Example usage
new_image_path = '/content/drive/MyDrive/reference_images/Peter/DSC_0299~2.JPG'
identified_person = ID_single_person(new_image_path, embeddings_db)
print(f'Person identified as {identified_person}')
