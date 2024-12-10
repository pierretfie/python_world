# Generate all possible 4-digit combinations
for num in range(10000):  # Numbers from 0000 to 9999
    with open('digits.txt','a') as file:
        file.write(f'{num:04d}\n')

