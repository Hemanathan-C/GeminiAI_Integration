import asyncio
from dotenv import load_dotenv
import speech_recognition as sr
from openai import OpenAI

from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI

load_dotenv()  # Load environment variables from .env file 
client = OpenAI()

async_client = AsyncOpenAI()

async def text_to_speech(text: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        instruction="Always speak in a friendly and helpful tone.",
        input=text,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source)
        recognizer.threshold = 2  # Adjust the threshold for ambient noise
        
        SYSTEM_PROMPT = """
            you're an expert voice agent. You are given the transcript of what user has
            said using voice. 
            You need to output as if you are a voice agent and whatever you speak
            will be converted to voice and played back to the user.
        """
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        print("Say something...")
        while True:
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

            messages.append({"role": "user", "content": text})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            print("AI Response: ", response.choices[0].message.content)

            asyncio.run(text_to_speech(response.choices[0].message.content))

main()
