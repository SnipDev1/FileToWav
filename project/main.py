import converter
import generate_audio
import read_audio


class Main:
    def __init__(self, text_file_name, audio_file_name, element_duration):
        self.conv = None
        self.text_file_name = text_file_name
        self.audio_file_name = audio_file_name
        self.element_duration = element_duration
        self.frequency_list = []
        self.generate_frequency_list()

    def generate_frequency_list(self):
        freq_list = []
        freq = 0
        for i in range(16):
            freq += 25
            freq_list.append(freq)
        self.frequency_list = freq_list

    def main(self):
        self.conv = converter.Converter(self.text_file_name, self.element_duration)
        self.frequency_list = self.conv.get_frequency_list()
        self.encode_file_to_audio()
        self.decode_file_to_audio()

    def encode_file_to_audio(self):
        print("ENCODING")

        frequencies = self.conv.convert_file_to_frequency_list()
        generate_audio.GenerateAudio(frequencies, self.audio_file_name).generate_audio()

    def decode_file_to_audio(self):
        print("DECODING")
        frequencies = read_audio.ReadAudio(self.audio_file_name, self.frequency_list, self.element_duration).main()
        # print(frequencies)

        converter.Converter(self.text_file_name, self.element_duration).convert_frequency_list_to_file(frequencies)


if __name__ == '__main__':
    Main("extra_files/to_convert/image.png", 'extra_files\\image.wav', 0.005).main()
