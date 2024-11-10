import numpy as np

#function for ID

def ID_single_person(img_path,embeddings_db, threshold=0.6):
    embedding = Deepface.represent(image_path, model_name= 'VGG-Face')

    #compare embedding to embeddings in the database
    for person, embeddings in embeddings_db.items():
        for ref_embedding in embeddings:
            distance - np.linalg.norm(np.array(ref_embedding) - np.array(embedding))
            if distance < threshold:
                return person #match found
            
    return 'Unknown, no match found'


new_image_path = 'path/test_image_1.jpg'
identified_person = ID_single_person(new_image_path, embeddings_db)
print(f'person identified as {identified_person}')
