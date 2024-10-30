import heapq
from collections import defaultdict
from PIL import Image
import numpy as np
import os

# LZW Class
class LZW:
    def __init__(self):
        self.max_table_size = 256

    def encode(self, input_string):
        dictionary = {chr(i): i for i in range(self.max_table_size)}
        result = []
        w = ''
        code = self.max_table_size

        for c in input_string:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = code
                code += 1
                w = c

        if w:
            result.append(dictionary[w])

        return result

    def decode(self, encoded):
        dictionary = {i: chr(i) for i in range(self.max_table_size)}
        w = chr(encoded[0])
        result = [w]
        code = self.max_table_size

        for k in encoded[1:]:
            if k in dictionary:
                entry = dictionary[k]
            elif k == code:
                entry = w + w[0]
            else:
                raise ValueError("Invalid LZW code.")
            result.append(entry)
            dictionary[code] = w + entry[0]
            code += 1
            w = entry

        return ''.join(result)


# Huffman Coding Class
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency

    def make_heap(self, frequency):
        heap = []
        for key in frequency:
            node = Node(key, frequency[key])
            heapq.heappush(heap, node)
        return heap

    def merge_nodes(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self, heap):
        root = heapq.heappop(heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def encode(self, text):
        frequency = self.make_frequency_dict(text)
        heap = self.make_heap(frequency)
        self.merge_nodes(heap)
        self.make_codes(heap)
        encoded_text = ''.join(self.codes[char] for char in text)
        return encoded_text

    def decode(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""
        return decoded_text


# Image Compression Functions
def compress_image_lzw(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_data = np.array(img)
    flat_data = img_data.flatten().astype(str).tolist()
    lzw = LZW()
    encoded_data = lzw.encode(''.join(flat_data))
    return encoded_data, img.size  # Return encoded data and original image size



def compress_image_huffman(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_data = np.array(img)
    flat_data = img_data.flatten().astype(str).tolist()
    huffman = HuffmanCoding()
    encoded_data = huffman.encode(''.join(flat_data))
    return list(encoded_data)  # Return a list of bits as strings
def decompress_image_lzw(compressed_data, original_size):
    lzw = LZW()
    decompressed_data = lzw.decode(compressed_data)
    
    # Convert the decompressed data back to an array and reshape
    # Ensure we convert back to integers
    decompressed_array = np.array(list(map(int, decompressed_data)))
    
    # Check the size of the decompressed array
    if decompressed_array.size != original_size[0] * original_size[1]:
        raise ValueError(f"Decompressed data size {decompressed_array.size} does not match original size {original_size}")

    return decompressed_array.reshape(original_size)

def decompress_image_huffman(compressed_data):
    huffman = HuffmanCoding()
    decoded_text = huffman.decode(compressed_data)
    return np.array(list(map(int, decoded_text))).reshape(-1, -1)

def save_compressed_data(filename, data, method='lzw'):
    with open(filename, 'wb') as f:
        if method == 'lzw':
            # Convert LZW integer data to bytes
            byte_array = bytearray()
            for num in data:
                byte_array.append(num % 256)  # Using modulo 256 to ensure values are in range
            f.write(byte_array)
        elif method == 'huffman':
            # Convert Huffman encoded data (string of bits) to bytes
            byte_array = bytearray()
            bit_string = ''.join(data)  # Join the list of strings into a single string
            for i in range(0, len(bit_string), 8):  # Process in chunks of 8 bits
                byte = bit_string[i:i+8]
                if len(byte) < 8:
                    byte = byte.ljust(8, '0')  # Pad with zeros if less than 8 bits
                byte_array.append(int(byte, 2))  # Convert binary string to an integer
            f.write(byte_array)

def get_image_size(image_path):
    return os.path.getsize(image_path)

def calculate_compression_ratios(image_path, lzw_compressed_data, huffman_compressed_data):
    original_size = get_image_size(image_path)
    lzw_size = len(lzw_compressed_data) * 8  # Assume each code is represented by 8 bits
    huffman_size = len(huffman_compressed_data)  # Each character is represented as a bit string

    lzw_compression_ratio = original_size / lzw_size
    huffman_compression_ratio = original_size / huffman_size

    return lzw_compression_ratio, huffman_compression_ratio

# Main Execution
if __name__ == "__main__":
    image_path = os.path.expanduser("~/Pictures/portrait.png")
    print(f"Using image path: {image_path}")

    # Compress images
    lzw_compressed_data, original_size = compress_image_lzw(image_path)
    huffman_compressed_data = compress_image_huffman(image_path)

    # Calculate compression ratios
    lzw_ratio, huffman_ratio = calculate_compression_ratios(image_path, lzw_compressed_data, huffman_compressed_data)

    print("LZW Compressed Data Length:", len(lzw_compressed_data))
    print("Huffman Compressed Data Length:", len(huffman_compressed_data))
    print("LZW Compression Ratio:", lzw_ratio)
    print("Huffman Compression Ratio:", huffman_ratio)

    # Save compressed data
    save_compressed_data("lzw_compressed.lzw", lzw_compressed_data, method='lzw')
    save_compressed_data("huffman_compressed.huff", huffman_compressed_data, method='huffman')

    # Decompress images
    try:
        decompressed_lzw_data = decompress_image_lzw(lzw_compressed_data, original_size)
        # You can implement Huffman decompression similarly if needed

        # Save decompressed images
        Image.fromarray(decompressed_lzw_data.astype(np.uint8)).save("decompressed_lzw.png")
        
        # Display results
        decompressed_lzw_image = Image.open("decompressed_lzw.png")
        decompressed_lzw_image.show()

        # Check file sizes of decompressed images
        lzw_decompressed_size = os.path.getsize("decompressed_lzw.png")
        print("Decompressed LZW Image Size:", lzw_decompressed_size)
        print("Original Image Size:", get_image_size(image_path))

    except ValueError as e:
        print(e)