import os
import wave
import numpy as np
from faster_whisper import WhisperModel
import pyaudio

MODEL = WhisperModel("Systran/faster-whisper-large-v3", device="cpu", compute_type="int8", num_workers=8)

def transcribe_chunk(model : WhisperModel, file_path):
    segments, info = model.transcribe(file_path, beam_size=5, language='fr', word_timestamps=True, suppress_blank=True)
    transcription = ' '.join (segment.text for segment in segments)
    return transcription

def record_chunk(p, stream, file_path, chunk_length=1):
    frames = []
    for _ in range(0, int (16000 / 1024 * chunk_length)):
        data = stream.read(1024, exception_on_overflow = False)
        frames. append (data)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels (1)
    wf.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    wf.setframerate (16000) 
    wf.writeframes(b''.join (frames))
    wf.close ( )

def main2():
    # Choose your model settings
   
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    accumulated_transcription = "" # Initialize an empty string to accumulate transcriptions
    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file)
            transcription = transcribe_chunk(MODEL, chunk_file)
            print(transcription )
            os.remove (chunk_file)
            # Append the new transcription to the accumulated transcription
            accumulated_transcription += transcription + " "
    except KeyboardInterrupt:
        print("Stopping...")
    # Write the accumulated transcription to the log file
    with open ("log. txt", "w") as log_file: 
       log_file.write(accumulated_transcription)

if __name__ == "__main__":
    # main2()
    # Start the transcription thread
    print("Starting transcription thread...")
