import math
import librosa
import numpy as np
import time


class ReadAudio:
    def __init__(self, audio_file, frequency_list, element_duration):
        self.audio_file = audio_file
        self.frequency_list = frequency_list
        self.element_duration = element_duration

    def main(self):
        audio_length = float(librosa.get_duration(path=self.audio_file))
        read_frequencies = []
        counter = 0
        percentage = -1
        i = 0
        start_time = time.time()  # Start timer
        elements_per_second = -1
        elements_per_second_loop = -1
        estimated_time_loop = -1
        last_update_time = start_time
        size_of_file = int(audio_length // self.element_duration)
        while counter < audio_length:
            start_time_loop = time.time()  # Start timer for this iteration
            start_time_period = round(0 + i * self.element_duration, 4)  # Start time in seconds
            end_time_period = round(self.element_duration + i * self.element_duration, 4)  # End time in seconds
            dominant_frequency = self.get_dominant_frequency_over_period(self.audio_file, start_time_period,
                                                                         end_time_period)
            read_frequencies.append(self.nearest_value(self.frequency_list, dominant_frequency))
            counter += self.element_duration
            i += 1
            end_time_loop = time.time()  # End timer for this iteration
            time_diff = end_time_loop - start_time_loop
            if time_diff != 0:
                elements_per_second_loop = 1 / time_diff  # Calculate elements per second for this iteration

            current_time = time.time()
            if current_time - last_update_time >= 1:
                elements_per_second = elements_per_second_loop
                last_update_time = current_time
            if round(counter / audio_length, 3) != percentage:
                percentage = round(counter / audio_length, 3)
                percentage *= 100

                estimated_time = (size_of_file - (counter // self.element_duration)) / elements_per_second
                print(
                    f"[{math.floor(percentage // 10) * '|'}{' ' * (10 - math.floor(percentage // 10))}] {round(percentage, 2)}%/100% ({int(counter // self.element_duration)}/{size_of_file} elements); Elements per second: {math.floor(elements_per_second)}; Estimated time: {math.floor(estimated_time) // 60} minutes {math.fabs(math.floor(estimated_time) // 60 * 60 - math.floor(estimated_time))} seconds      ",
                    end="\r")
        end_time = time.time()  # End timer
        total_elements_per_second = i / (end_time - start_time)  # Calculate total elements per second
        print(f"\nTotal elements per second: {total_elements_per_second:.2f}")
        return read_frequencies

    def nearest_value(self, values: list, one) -> int:
        return min(values, key=lambda n: (abs(one - n), n))

    def get_dominant_frequency_over_period(self, audio_file, start_time, end_time):
        # Load the audio file
        y, sr = librosa.load(audio_file, sr=None)

        # Calculate frame indices for start and end times
        start_frame = int(start_time * sr)
        end_frame = int(end_time * sr)

        # Extract the audio data for the specified period
        audio_period = y[start_frame:end_frame]

        # Calculate the short-time Fourier transform (STFT)
        stft = np.abs(librosa.stft(audio_period))

        # Calculate the frequency spectrum
        frequency_spectrum = np.mean(stft, axis=1)

        # Find the dominant frequency
        dominant_frequency_index = np.argmax(frequency_spectrum)

        # Convert the dominant frequency index to Hz
        frequency_in_hz = librosa.fft_frequencies(sr=sr)[dominant_frequency_index]

        return frequency_in_hz


if __name__ == '__main__':
    freq_list = []
    freq = 0
    for i in range(16):
        freq += 100
        freq_list.append(freq)
    ReadAudio('test.wav', freq_list, 0.005).main()
