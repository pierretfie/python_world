# Custom Morse code dictionary with binary strings as provided
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

# Calculate Morse code lengths for each character
morse_code_lengths = {char: len(code) for char, code in custom_morse_dict.items()}

# Updated letter frequencies in percentages
letter_frequencies_percent = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
    'S': 6.28, 'R': 6.02, 'H': 5.92, 'D': 4.32, 'L': 3.98, 'U': 2.88,
    'C': 2.71, 'M': 2.61, 'F': 2.30, 'Y': 2.11, 'W': 2.09, 'G': 2.03,
    'P': 1.82, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'Q': 0.11,
    'J': 0.10, 'Z': 0.07
}

# Calculate the weighted average Morse code length using percentages
average_morse_length = sum(
    letter_frequencies_percent[letter] * morse_code_lengths[letter] for letter in letter_frequencies_percent
)

# Ideal binary encoding length (in bits)
ideal_binary_length = 4.7

# Efficiency calculation
efficiency = ideal_binary_length / average_morse_length

# Output the average Morse code length and efficiency
print("Average Morse Code Length:", average_morse_length)
print("Efficiency (η):", efficiency)
