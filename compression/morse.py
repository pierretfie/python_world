
#inbuilt function lacks some characters
# custom Morse code dictionary
custom_morse_dict = {
    'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010',
    'G': '110', 'H': '0000', 'I': '00', 'J': '0111', 'K': '101', 'L': '0100',
    'M': '11', 'N': '10', 'O': '111', 'P': '0110', 'Q': '1101', 'R': '010',
    'S': '000', 'T': '1', 'U': '001', 'V': '0001', 'W': '011', 'X': '1001',
    'Y': '1011', 'Z': '1100', '1': '01111', '2': '00111', '3': '00011', 
    '4': '00001', '5': '00000', '6': '10000', '7': '11000', '8': '11100', 
    '9': '11110', '0': '11111', ',': '110011', '.': '010101', '?': '001100',
    "'": '011110', '-': '100001', '/': '10010', '(': '10110', ')': '101101',
    '&': '01000', ':': '111000', ';': '101010', '=': '10001', '+': '01010',
    '_': '001101', '"': '010010', '$': '0001001', '!': '101011', '@': '011010'
}

# Functions to encode and decode using custom Morse dictionary
# Define custom encode function
def custom_encode(message):
    encoded_message = []
    for char in message.upper():
        if char == ' ':
            # Add three spaces to indicate a word boundary
            encoded_message.append('   ')
        elif char in custom_morse_dict:
            encoded_message.append(custom_morse_dict[char])
    return ' '.join(encoded_message)

# Define custom decode function
# Define custom decode function with spaces handling
def custom_decode(morse_code):
    reverse_dict = {v: k for k, v in custom_morse_dict.items()}
    decoded_message = []
    
    # Split the Morse code input into sections by two or more spaces
    words = morse_code.split('   ')  # Three spaces denote word breaks
    
    for word in words:
        letters = word.split()  # Separate Morse letters by single spaces
        decoded_word = ''.join(reverse_dict.get(symbol, '') for symbol in letters)
        decoded_message.append(decoded_word)
    
    return ' '.join(decoded_message)  # Join decoded words with single spaces

def morsecoder():
    while True:
        try:
            option = input('Enter 1 to ENCODE, 2 to DECODE, or any other key to EXIT:\n')
            if option not in ['1', '2']:
                print('EXITING Morse coder')
                break
            else:
                if option == '1':
                    message = input('Enter message to encrypt:\n')
                    encoded_message = custom_encode(message)
                    print(f"Encoded: {encoded_message}")
                else:
                    message = input('Enter Morse code to decrypt (separate symbols with spaces):\n')
                    decoded_message = custom_decode(message)
                    print(f"Decoded: {decoded_message}")
        except KeyboardInterrupt:
            print('Exiting due to KEYBOARD INTERRUPT')
            break

if __name__ == "__main__":
    morsecoder()
