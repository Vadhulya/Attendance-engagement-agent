import pyaudio
import numpy as np

class AudioMonitor:
    def __init__(self, rate=16000, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def get_rms(self):
        try:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            rms = np.sqrt(np.mean(np.square(audio_data)))
            return float(rms)
        except Exception:
            return 0.0

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()