from fastapi import FastAPI
import speech_recognition as sr
import random,requests,os
import Levenshtein
from fastapi import WebSocket

app = FastAPI()

# Dictionary to store active websocket connections
active_connections = {}

async def asr_system(audio_url):
    recognizer = sr.Recognizer()

    audio_file_path = "temp_audio.wav"
    response = requests.get(audio_url)
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(response.content)

    # Use the ASR system to convert audio to text
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        recognized_text = recognizer.recognize_google(audio)
        return recognized_text
    except sr.UnknownValueError:
        return "override"  # Return an empty string if speech cannot be recognized
    finally:
        os.remove(audio_file_path)  # Remove the temporary audio file


async def compare_pronunciation(original_text, recorded_audio):
    # Use ASR system to convert recorded audio to text

    recognized_text = await asr_system(recorded_audio)
    print(f"User said: {recognized_text}\n")

    # Calculate Levenshtein distance between recognized and reference text
    distance = Levenshtein.distance(original_text, recognized_text)

    # Calculate matching score
    if recognized_text == "override":
        print("Override Scoring")
        matching_score = random.uniform(0.14, 0.42)
        return [recognized_text,matching_score]

    matching_score = 1.0 - (distance / len(original_text))
    return [recognized_text,matching_score]

@app.get("/audio/comparison")
async def comparer(original_text: str, recorded_audio: str):
    print(recorded_audio)
    res = await compare_pronunciation(original_text, recorded_audio)
    return {
        "Recognized Text": res[0],
        "Matching Score": res[1]}

@app.get("/")
async def dashboard():
    return "AUXILIA"
