import speech_recognition as sr 
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI   
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "cc72bdc5ffd4446090c1923ba366a28a"

# Function to speak using pyttsx3
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Function to speak using gTTS and play the audio
def speak(text):
    from gtts import gTTS
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the mixer module for audio playback
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the audio
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up resources
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    
# Handle AI-powered command processing through external API    
def aiProcess(command):
    base_url = "https://api.aimlapi.com/v1"
    api_key = "9300ccd36edc49d2960be4dff6146409"
    system_prompt = "You are a virtual assistant named FRIDAY, skilled in general tasks like Alexa and Google cloud. Give short responses"
    user_prompt = command

    api = OpenAI(api_key=api_key, base_url=base_url)
    try:
        completion = api.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=256,
        )

        # Extract response from the API completion
        response = completion.choices[0].message.content
        return response

    except Exception as e:
        return f"Error processing AI response: {e}"

# Process commands from the user and respond accordingly
def processCommand(c):    
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        # Fetch the music link from the music library and play it
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        # Fetch and read out the latest news using News API
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles:
                speak(article['title'])
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
    if output:
        speak(output)
    else:
        speak("Sorry, I couldn't process your request.")

if __name__ == "__main__":
    # Initial welcome message
    speak("Initializing FRIDAY..... ")
    while True:
        # Listen for the wake word FRIDAY 
        r = sr.Recognizer() 
        print("recognizing...")
        # Recognize speech using Google API
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "friday":
                speak("Yes")
                # Listen for command after activation
                with sr.Microphone() as source:
                    print("FRIDAY Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            # Handle exceptions gracefully and continue
            print("Error; {0}".format(e))


