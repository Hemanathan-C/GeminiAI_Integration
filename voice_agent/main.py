import speech_recognition as sr

def main():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source)
        recognizer.threshold = 2  # Adjust the threshold for ambient noise
        
        print("Say something...")
        
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

main()
