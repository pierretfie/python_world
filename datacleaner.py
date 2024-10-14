#this code adds words into a list
def add_to_list():
    list = []
    words = input('paste your words:\n')
    for word in words:
        word = word.strip()
        list.append(word)
        return list
    
output = add_to_list()
print(output)