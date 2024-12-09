word = 'hello world'
print(word)
s = '*'

for i in word
    index = word.index(i)
    print (f'{i} {s*index}')

if 'e' in word:
    print("a letter 'e' found in the word")
else:
    print("demanded letter not found")