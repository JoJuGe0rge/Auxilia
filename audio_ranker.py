import Levenshtein, speech_recognition as sr
import random
import pyttsx3

def convert_text_to_audio(text, language, output_filename):
    engine = pyttsx3.init()
    
    # Set the language
    engine.setProperty('rate', 100)
    # engine.setProperty('volume', 3.0)
    engine.setProperty('voice', language)
        
    # Save audio to PCM WAV file
    engine.save_to_file(text, output_filename)
    engine.runAndWait()


def asr_system(audio_file):
    r = sr.Recognizer()

    # # Read the audio file
    # with sr.AudioFile(audio_file) as source:
    #     audio = r.record(source, duration=2.0)

    # Access the audio from the URL
    audio_data = sr.AudioFile(audio_file)
    with audio_data as source:
            audio = r.record(source)

    try:
        # Perform speech recognition
        recognized_text = r.recognize_google(audio,language="en-US")
        print("recognized_text:",recognized_text)
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio.")
        recognized_text = "backjam"

    return recognized_text


def compare_pronunciation(original_text, recorded_audio):
    # Use ASR system to convert recorded audio to text
    recognized_text = asr_system(recorded_audio)

    # Calculate Levenshtein distance between recognized and reference text
    distance = Levenshtein.distance(original_text, recognized_text)

    # Calculate matching score
    if recognized_text=="backjam":
        print("Override Scoring")
        matching_score= random.uniform(0.1420, 0.4650)
        return matching_score

    matching_score = 1.0 - (distance / len(original_text))
    return matching_score

# Usage example
original_text = "free"
recorded_audio = "https://fms-set.s3.ap-south-1.amazonaws.com/Audio+dataset/three.wav"



# # Usage example
# text = "8"
# language = "en-US"
# output_filename = "output.wav"

# convert_text_to_audio(text, language, output_filename)
# print("Audio file saved successfully.")


matching_score = compare_pronunciation(original_text, recorded_audio)
print(f"Pronunciation matching score: {matching_score}")
