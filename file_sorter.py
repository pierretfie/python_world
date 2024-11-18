import os 

def sort_by_name(dir):
    files = os.listdir(dir)
    file_list = []
    for file in files:
        file_list.append(file)
    sorted_files = sorted(file_list)
    for file in sorted_files:
        #os.rename(os.path.join(dir, file), os.path.join(dir, file))
        print(file)
sort_by_name("C:/Users/user/Downloads/")
    
