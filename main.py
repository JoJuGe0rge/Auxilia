from fastapi import FastAPI,UploadFile
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


@app.websocket("/audio/socket/comparison")
async def audio_comparison(websocket: WebSocket):
    # Accept the websocket connection
    await websocket.accept()

    # Add the websocket connection to active connections dictionary
    connection_id = str(random.randint(1, 999999))
    active_connections[connection_id] = websocket

    try:
        while True:
            # Receive data from the client
            data = await websocket.receive_text()
            
            # Parse the received data
            original_text, recorded_audio = data.split(",")

            # Use ASR system to convert recorded audio to text
            recognized_text = asr_system(recorded_audio)
            print(f"User said: {recognized_text}\n")

            # Calculate Levenshtein distance between recognized and reference text
            distance = Levenshtein.distance(original_text, recognized_text)

            # Calculate matching score
            if recognized_text == "backjam":
                print("Override Scoring")
                matching_score = random.uniform(0.1420, 0.4650)
            else:
                matching_score = 1.0 - (distance / len(original_text))

            # Send the matching score back to the client
            await websocket.send_text(str(matching_score))
    except:
        # Remove the websocket connection from active connections dictionary

        del active_connections[connection_id]


@app.post("/audio/bytes/comparison")
def comparer(original_text: str, recorded_audio: UploadFile):
    # Read the byte stream from the uploaded file
    audio_bytes = recorded_audio.file.read()

    res = compare_pronunciation(original_text, audio_bytes)
    return res

@app.get("/")
async def dashboard():
    return "AUXILIA"
