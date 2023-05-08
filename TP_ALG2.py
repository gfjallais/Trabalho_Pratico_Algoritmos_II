import sys
import struct
import math

class Node():
    
    def __init__(self, string, value):
        self.children = []
        self.string = string
        self.value = value
        self.end_of_word = False

    def is_char_in_children(self, char):
        temp_list = [ch.string for ch in self.children]
        if not char in temp_list:
            return False
        else:
            return self.children[temp_list.index(char)]
    
class Trie():

    def __init__(self):
        self.root = Node("", 0)
        self.root.children.append(Node("\n", 1))
        self.curr_code = 2

    def find(self, word):
        current_node = self.root
        for char in word:
            if not current_node.is_char_in_children(char):
                return False
            current_node = current_node.is_char_in_children(char)
        return current_node.end_of_word
            
    def insert(self, word):
        current_node = self.root
        for char in word:
            if not current_node.is_char_in_children(char):
                temp = Node(char, self.curr_code)
                current_node.children.append(temp)
                self.curr_code += 1
            current_node = current_node.is_char_in_children(char)
        current_node.end_of_word = True
    
    def encode(self, lines, output):
        len_file = len(lines)
        output.write(self.bytes_needed_code.to_bytes(1, byteorder='little'))
        output.write(self.bytes_needed_char.to_bytes(1, byteorder='little'))
        for i, text in enumerate(lines):
            string = ""
            org_text = text
            text = text.replace("\n", "")
            for char in text:
                if self.find(string + char):
                    string += char
                else:
                    self.insert(string + char)
                    code = f'{self.get_code(string):b}'.zfill(self.bytes_needed_code)
                    char_code = f'{ord(char):b}'.zfill(self.bytes_needed_char)
                    byte_code = int(code, 2)
                    byte_char = int(char_code, 2)
                    output.write(byte_code.to_bytes(self.bytes_needed_code, byteorder='little'))
                    output.write(byte_char.to_bytes(self.bytes_needed_char, byteorder='big'))
                    string = ""
            if string != "":
                self.insert(string)
                code = f'{self.get_code(string):b}'.zfill(self.bytes_needed_code)
                char_code = f'{0:b}'.zfill(self.bytes_needed_char)
                byte_code = int(code, 2)
                byte_char = int(char_code, 2)
                output.write(byte_code.to_bytes(self.bytes_needed_code, byteorder='little'))
                output.write(byte_char.to_bytes(self.bytes_needed_char, byteorder='big'))
            if i < len_file - 1 or (i == len_file - 1 and org_text[-1] == "\n"):
                trie.insert("\n")
                string = "\n"
                code = f'{trie.get_code(string):b}'.zfill(trie.bytes_needed_code)
                char_code = f'{0:b}'.zfill(trie.bytes_needed_char)
                byte_code = int(code, 2)
                byte_char = int(char_code, 2)
                output.write(byte_code.to_bytes(trie.bytes_needed_code, byteorder='little'))
                output.write(byte_char.to_bytes(trie.bytes_needed_char, byteorder='big'))
    
    def get_code(self, string):
        node = self.root
        while string != "":
            for child in node.children:
                if child.string == string[0]:
                    node = child
                    string = string[1:]
                    break
        return node.value

    def decode(self, input, output):
        dictionary = {0: "", 1: "\n"}
        count = 2
        bytes_data = input.read(2)
        self.bytes_needed_code = bytes_data[0]
        self.bytes_needed_char = bytes_data[1]
        size_tuple = self.bytes_needed_code + self.bytes_needed_char
        while True:
            bytes_data = input.read(size_tuple)

            if not bytes_data:
                break
            if self.bytes_needed_code == 1:
               int_data = struct.unpack('<B', bytes_data[:1])[0]
            elif self.bytes_needed_code == 2:
                int_data = struct.unpack('<H', bytes_data[:2])[0]
            elif self.bytes_needed_code == 3:
                int_data = struct.unpack('<I', bytes_data[:3] + b'\x00')[0]
            elif self.bytes_needed_code == 4:
                int_data = struct.unpack('<I', bytes_data[:4])[0]
            str_data = chr(int.from_bytes(bytes_data[self.bytes_needed_code:], byteorder='big', signed=False))

            if int_data == 1:
                output.write("\n")
                continue
            if str_data != "\x00":
                if dictionary[int_data] + str_data not in dictionary:
                    dictionary[count] = dictionary[int_data] + str_data
                    count += 1
                str_data = dictionary[int_data] + str_data
            else: str_data = dictionary[int_data]
            output.write(str_data)

    def number_of_bytes_needed(self, lines):
        string = ""
        diff_chars = []
        dictionary = {"": 0, "\n": 1}
        count = 2
        for text in lines:
            text = text.replace("\n", "")
            for char in text:
                if char not in diff_chars:
                    diff_chars.append(char)
                if (string + char) in dictionary:
                    string += char
                else:
                    dictionary[string+char] = count
                    count += 1 
                    string = ""
        bits_needed_code = count.bit_length()
        self.bytes_needed_code = math.ceil(bits_needed_code / 8)
        bits_needed_char = max([ord(ch) for ch in diff_chars]).bit_length()
        self.bytes_needed_char = math.ceil(bits_needed_char / 8)
        return self.bytes_needed_code, self.bytes_needed_char
        
if sys.argv[1] == '-c':
    with open(sys.argv[2]) as input:
        trie = Trie()
        if len(sys.argv) == 4:
            output = open(sys.argv[3], "wb")
        else:
            output = open(sys.argv[2][:-4] + '.z78', "wb+")
        lines = input.readlines()
        len_file = len(lines)

        trie.number_of_bytes_needed(lines)
        trie.encode(lines, output)

elif sys.argv[1] == '-x':
    with open(sys.argv[2], "rb") as input:
        trie = Trie()
        if len(sys.argv) == 4:
            output = open(sys.argv[3], "w")
        else:
            output = open(sys.argv[2][:-4] + '.txt', "w+")
        trie.decode(input, output)


