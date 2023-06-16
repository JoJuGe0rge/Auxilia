import speech_recognition as sr
import pyttsx3, random
import Levenshtein

engine = pyttsx3.init()

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        # Perform speech recognition
        query = r.recognize_google(audio,language="en-US")

    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio.")
        query = "backjam"
    return query


def compare_pronunciation(original_text):
    # Use ASR system to convert recorded audio to text
    recognized_text = TakeCommand()
    print(f"User said: {recognized_text}\n")
    # Calculate Levenshtein distance between recognized and reference text
    distance = Levenshtein.distance(original_text, recognized_text)

    # Calculate matching score
    if recognized_text=="backjam":
        print("Override Scoring")
        matching_score= random.uniform(0.1420, 0.4650)
        return matching_score

    matching_score = 1.0 - (distance / len(original_text))
    return matching_score


##################################

original_text = "k"

matching_score = compare_pronunciation(original_text)
print(f"Pronunciation matching score: {matching_score}")
