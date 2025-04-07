import os
import wave
import numpy as np
from faster_whisper import WhisperModel
import pyaudio
import torch
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time 

N_CHUNK = 30
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MODEL = WhisperModel("Systran/faster-whisper-large-v3", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="int8", num_workers=8)



def transcribe_chunk(model : WhisperModel, file_path):
    segments, info = model.transcribe(file_path, beam_size=5, language='fr', word_timestamps=True, suppress_blank=True)
    transcription = ' '.join (segment.text for segment in segments)
    return transcription



def simulate_audio_stream_n_fixe(file_path):
    with wave.open(file_path, 'rb') as input_wf:
        # Get audio parameters from the input file
        channels = input_wf.getnchannels()
        sample_width = input_wf.getsampwidth()
        frame_rate = input_wf.getframerate()

        number_of_frames = input_wf.getnframes()

        print(f"Number of frames: {number_of_frames}")

        number_of_frames = number_of_frames // N_CHUNK

        print(f"Number of chunks: {number_of_frames}")
        chunk_index = 0
        while chunk_index < N_CHUNK:
            # Open the output WAV file with the same parameters
            chunk_file = f"temp_chunks/chunk_{chunk_index}.wav".format(chunk_index =chunk_index)
            with wave.open(chunk_file, 'wb') as output_wf:
                output_wf.setnchannels(channels)
                output_wf.setsampwidth(sample_width)
                output_wf.setframerate(frame_rate)
                index = number_of_frames

                print("Reading and writing audio...")
                while index > 0:
                    # Read a chunk of audio data
                    chunk = input_wf.readframes(CHUNK)
                    if not chunk:
                        break

                    # Process the audio chunk
                    processed_chunk = chunk

                    # Write the processed chunk to the output file
                    output_wf.writeframes(processed_chunk)
                    index -= CHUNK
            transciped = transcribe_chunk(MODEL, chunk_file)
            print(transciped)
            chunk_index += 1

    print("Audio processing complete.")
        # Transcribe the chunk
        # transcription = transcribe_chunk(MODEL, chunk_file)
        # print(transcription)

        # Append the new transcription to the accumulated transcription
        # accumulated_transcription += transcription + " "

        # Remove the temporary chunk file
        # os.remove(chunk_file)

def main2():
    # Choose your model settings
    print(torch.cuda.is_available())

    start = time.time()
    # print(transcribe_chunk(MODEL, "./wavFiles/Stade Jean Bouin.wav"))
    print("Transcription time: ", time.time() - start)
    # Simulate the audio stream with fixed chunks
    # simulate_audio_stream_n_fixe("./wavFiles/Stade Jean Bouin.wav")
    # Simulate the audio stream with silence detection
    # simulate_audio_stream_with_cutted_silence("./wavFiles/Stade Jean Bouin.wav")
if __name__ == "__main__":
    # Start the transcription thread
    print("Starting transcription thread...")
    main2()
