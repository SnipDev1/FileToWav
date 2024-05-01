import codecs
import math
import time
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
        self.key_for_filename = 'filename_key'
        self.default_path_for_reconverted = "extra_files\\reconverted\\"
        self.default_filename = self.default_path_for_reconverted + "Decoded file"
        self.save_filename = True

    def generate_frequency_dictionary(self, hex_values, step):
        frequency = 50
        dictionary = {}
        for i in range(len(hex_values)):
            for j in range(len(hex_values)):
                value = hex_values[i] + hex_values[j]
                dictionary[value] = frequency
                frequency += step
        self.frequency_dictionary = dictionary
        # print(self.frequency_dictionary)

    def get_frequency_list(self):
        frequency_dict = self.inverse_frequency_dictionary
        return frequency_dict.keys()

    def convert_file_to_frequency_list(self):
        text = self.read_file(self.file_name)
        hex_val = self.convert_string_to_hex_string(text)

        frequency_list = []
        first = 0
        previous = 0
        counter = 0
        percentage = -1
        i = 0
        hex_val_len = len(hex_val)
        start_time = time.time()  # Start timer
        elements_per_second = -1
        elements_per_second_loop = -1
        total_spent_time = 0
        estimated_time_loop = -1
        last_update_time = start_time
        size_of_file = int(hex_val_len // 2)

        for i in range(hex_val_len):
            j = hex_val[first:previous + 2]
            first += 2
            previous += 2
            # started trash

            start_time_loop = time.time()  # Start timer for this iteration
            start_time_period = round(0 + i * 2, 4)  # Start time in seconds
            end_time_period = round(2 + i * 2, 4)  # End time in seconds
            counter += 2
            i += 1
            end_time_loop = time.time()  # End timer for this iteration
            time_diff = end_time_loop - start_time_loop
            if time_diff != 0:
                elements_per_second_loop = 1 / time_diff  # Calculate elements per second for this iteration

            current_time = time.time()
            if current_time - last_update_time >= 1:
                elements_per_second = elements_per_second_loop
                last_update_time = current_time
                total_spent_time += 1
            if round(counter / hex_val_len, 3) != percentage:
                percentage = round(counter / hex_val_len, 3)
                percentage *= 100

                estimated_time = (size_of_file - (counter // 2)) / elements_per_second
                print(
                    f"[{math.floor(percentage // 10) * '|'}{' ' * (10 - math.floor(percentage // 10))}] {math.floor(percentage)}%/100% ({int(counter // 2)}/{size_of_file} elements); Elements per second: {math.floor(elements_per_second)}; Estimated time: {math.floor(estimated_time) // 60} minutes {math.fabs(math.floor(estimated_time) // 60 * 60 - math.floor(estimated_time))} seconds      ",
                    end="\r")

            if j == "":
                break

            frequency_list.append((self.frequency_dictionary[j], self.duration))
        end_time = time.time()  # End timer
        total_elements_per_second = i / (end_time - start_time)  # Calculate total elements per second
        print(f"\nTotal elements per second: {total_elements_per_second:.2f}")
        print(f"Total spent time: {total_spent_time // 60} minutes {total_spent_time} seconds")
        return frequency_list

    def convert_frequency_list_to_file(self, frequency_list):
        final_file = ''
        for i in range(len(frequency_list)):
            final_file += self.inverse_frequency_dictionary[frequency_list[i]]
        # Detecting filename and key for filename

        string_val = self.convert_hex_string_to_string(final_file)

        self.write_file(string_val)
        print('File was successfully written\n')

    def convert_string_to_hex_string(self, text) -> str:
        return text.hex()
        # return "".join("{:02x}".format(ord(c)) for c in text)

    def convert_hex_string_to_string(self, text):
        return bytes.fromhex(text)
        # return ''.join([chr(int(text[i:i + 2], 16)) for i in range(0, len(text), 2)])

    def read_file(self, file_name: str):
        with open(file_name, "rb") as f:
            file_read = f.read()
        meta_data = bytes(file_name + self.key_for_filename, "utf-8")
        file_read = zlib.compress(meta_data + file_read)
        return file_read

    def write_file(self, text):
        text = zlib.decompress(text)
        file_name = self.default_filename
        if text.__contains__(bytes(self.key_for_filename, "utf8")):
            file_name = text.split(bytes(self.key_for_filename, "utf8"))[0]
            text = text.replace(bytes(self.key_for_filename, "utf8"), b'')
            text = text.replace(file_name, b'')
            file_name = file_name.decode()
        if not self.save_filename:
            file_name = self.default_filename + '.' + file_name.split('.')[1]
        else:
            if file_name.__contains__('/'):
                file_name = file_name.split('/')[-1]
            else:
                if file_name.__contains__('\\'):
                    file_name = file_name.split('\\')[-1]
            file_name = self.default_path_for_reconverted + file_name

        with open(file_name, "wb") as f:
            f.write(text)
