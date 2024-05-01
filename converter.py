import codecs
import zlib


class Converter:
    def __init__(self, file_name, duration):
        self.file_name = file_name
        self.duration = duration
        self.hex_values = ['', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        self.frequency_dictionary = {
            '0': 100,
            '1': 200,
            '2': 300,
            '3': 400,
            '4': 500,
            '5': 600,
            '6': 700,
            '7': 800,
            '8': 900,
            '9': 1000,
            'a': 1100,
            'b': 1200,
            'c': 1300,
            'd': 1400,
            'e': 1500,
            'f': 1600,
        }
        self.generate_frequency_dictionary(self.hex_values, 50)
        self.inverse_frequency_dictionary = {v: k for k, v in self.frequency_dictionary.items()}

    def generate_frequency_dictionary(self, hex_values, step):
        frequency = 50
        dictionary = {}
        for i in range(len(hex_values)):
            for j in range(len(hex_values)):
                value = hex_values[i] + hex_values[j]
                dictionary[value] = frequency
                frequency += step
        self.frequency_dictionary = dictionary
        print(self.frequency_dictionary)

    def get_frequency_list(self):
        frequency_dict = self.inverse_frequency_dictionary
        return frequency_dict.keys()

    def convert_file_to_frequency_list(self):
        text = self.read_file(self.file_name)
        hex_val = self.convert_string_to_hex_string(text)

        frequency_list = []
        first = 0
        previous = 0
        for i in range(len(hex_val)):
            j = hex_val[first:previous + 2]
            first += 2
            previous += 2
            if j == "":
                break
            print(j)

            frequency_list.append((self.frequency_dictionary[j], self.duration))
        print(
            f"Initial text - {text}\nHex value - {hex_val}\nFrequency list - {frequency_list}")
        return frequency_list

    def convert_frequency_list_to_file(self, frequency_list):
        final_file = ''
        for i in range(len(frequency_list)):
            final_file += self.inverse_frequency_dictionary[frequency_list[i]]
        print(f"final file - {final_file}")
        string_val = self.convert_hex_string_to_string(final_file)
        self.write_file("Decoded file.txt", string_val)

    def convert_string_to_hex_string(self, text) -> str:
        return text.hex()
        # return "".join("{:02x}".format(ord(c)) for c in text)

    def convert_hex_string_to_string(self, text):
        return bytes.fromhex(text)
        # return ''.join([chr(int(text[i:i + 2], 16)) for i in range(0, len(text), 2)])

    def read_file(self, file_name: str):
        with open(file_name, "rb") as f:
            file_read = f.read()
        print(file_read)
        file_read = zlib.compress(file_read)
        return file_read

    def write_file(self, file_name: str, text):
        text = zlib.decompress(text)
        with open(file_name, "wb") as f:
            f.write(text)
        print('break')
