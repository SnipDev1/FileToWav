import numpy as np
from scipy.io.wavfile import write


class GenerateAudio:
    def __init__(self, frequencies, file_name, duration_scale=1):
        self.volume = 1
        self.sample_rate = 44100 * 2
        self.frequencies = frequencies
        self.file_name = file_name
        self.duration_scale = duration_scale

    def generate_audio(self):
        total_samples = sum(int(self.sample_rate * duration * self.duration_scale) for frequency, duration in self.frequencies)
        samples = np.zeros(total_samples, dtype=np.float32)
        current_sample = 0
        for frequency, duration in self.frequencies:
            freq_samples = (np.sin(2 * np.pi * np.arange(int(self.sample_rate * duration * self.duration_scale))
                                   * frequency / self.sample_rate)).astype(np.float32)
            samples[current_sample:current_sample + len(freq_samples)] += freq_samples
            current_sample += len(freq_samples)
        write(self.file_name, self.sample_rate, samples)


if __name__ == '__main__':
    frequencies = [(400, 1), (600, 1), (400, 1), (400, 1)]  # List of tuples: (frequency, duration)
    GenerateAudio(frequencies, "test.wav", 1).generate_audio()
