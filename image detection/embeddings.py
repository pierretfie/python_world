from  deepface import Deepface
import os

#dict to store embeddings

embeddings_db = {}

#loop through reference images
for person in os.lidtdir("reference_images"):
    person_folder = os.path.join('reference_folder', person)
    embeddings_db[person] = []
    
    
    for img_file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, img_file)

        #generate embeddings for the image
        embedding = Deepface.represent(img_path=img_path, model_name='VGG-Face')
        embeddings_db[person].append(embedding)
