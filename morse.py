
#inbuilt function lacks some characters
# custom Morse code dictionary
custom_morse_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    "'": '.----.', '-': '-....-', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '!': '-.-.--', '@': '.--.-.'
}

# Functions to encode and decode using custom Morse dictionary
# Define custom encode function
def custom_encode(message):
    encoded_message = []
    for char in message.upper():
        if char in custom_morse_dict:
            encoded_message.append(custom_morse_dict[char])
            print(char)
    return ' '.join(encoded_message)

# Define custom decode function
def custom_decode(morse_code):
    reverse_dict = {v: k for k, v in custom_morse_dict.items()}
    decoded_message = []
    for symbol in morse_code.split():
        if symbol in reverse_dict:
            decoded_message.append(reverse_dict[symbol])
    return ''.join(decoded_message)

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
