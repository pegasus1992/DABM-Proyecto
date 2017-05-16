import pyaudio
import wave

'''FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print ("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()'''


class GuardarAudio():
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 3
        self.WAVE_OUTPUT_FILENAME = "audio.wav"
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.stream = None


    def iniciarGrabacion(self):
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,rate=self.RATE, input=True,frames_per_buffer=self.CHUNK)
        print ("recording...")

    def grabar(self):
        data =  self.stream.read(self.CHUNK)
        self.frames.append(data)

    def guardarGrabacion(self):
        print ("finished recording")
        # stop Recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        waveFile = wave.open( self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels( self.CHANNELS)
        waveFile.setsampwidth( self.audio.get_sample_size( self.FORMAT))
        waveFile.setframerate( self.RATE)
        waveFile.writeframes(b''.join( self.frames))
        waveFile.close()











