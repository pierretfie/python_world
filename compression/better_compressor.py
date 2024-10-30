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
def compress_image_lzw(image):
    img_data = np.array(image)
    flat_data = img_data.flatten().astype(str).tolist()
    lzw = LZW()
    encoded_data = lzw.encode(''.join(flat_data))
    return encoded_data

def compress_image_huffman(image):
    img_data = np.array(image)
    flat_data = img_data.flatten().astype(str).tolist()
    huffman = HuffmanCoding()
    encoded_data = huffman.encode(''.join(flat_data))
    return encoded_data

def get_image_size(image_path):
    return os.path.getsize(image_path)

def calculate_compression_ratios(image_path, lzw_compressed_data, huffman_compressed_data):
    original_size = get_image_size(image_path)
    lzw_size = len(lzw_compressed_data) * 8  # Assume each code is represented by 8 bits
    huffman_size = len(huffman_compressed_data)  # Each character is represented as a bit string

    lzw_compression_ratio = original_size / lzw_size
    huffman_compression_ratio = original_size / huffman_size

    return lzw_compression_ratio, huffman_compression_ratio

def save_compressed_data(filename, data):
    with open(filename, 'wb') as f:
        f.write(bytearray(data))

def decompress_image_lzw(encoded_data, original_shape):
    lzw = LZW()
    decompressed_data = lzw.decode(encoded_data)
    return np.array(list(map(int, decompressed_data))).reshape(original_shape)

def decompress_image_huffman(encoded_data, original_shape):
    huffman = HuffmanCoding()
    decompressed_data = huffman.decode(encoded_data)
    return np.array(list(map(int, decompressed_data))).reshape(original_shape)

def quantize_image(image_path, num_colors=256):
    img = Image.open(image_path).convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    return img

# Main Execution
if __name__ == "__main__":
    image_path = os.path.expanduser("~/Pictures/portrait.png")
    quantized_image = quantize_image(image_path)
    
    # Perform compression
    lzw_compressed_data = compress_image_lzw(quantized_image)
    huffman_compressed_data = compress_image_huffman(quantized_image)

    # Calculate compression ratios
    lzw_ratio, huffman_ratio = calculate_compression_ratios(image_path, lzw_compressed_data, huffman_compressed_data)

    print("LZW Compressed Data Length:", len(lzw_compressed_data))
    print("Huffman Compressed Data Length:", len(huffman_compressed_data))
    print("LZW Compression Ratio:", lzw_ratio)
    print("Huffman Compression Ratio:", huffman_ratio)

    # Decompression
    original_size = np.array(quantized_image).shape
    decompressed_lzw_data = decompress_image_lzw(lzw_compressed_data, original_size)
    decompressed_huffman_data = decompress_image_huffman(huffman_compressed_data, original_size)

    # Save the compressed data
    save_compressed_data("lzw_compressed.lzw", lzw_compressed_data)
    save_compressed_data("huffman_compressed.huff", huffman_compressed_data)

    # Display results
    Image.fromarray(decompressed_lzw_data).show(title='Decompressed LZW Image')
    Image.fromarray(decompressed_huffman_data).show(title='Decompressed Huffman Image')
