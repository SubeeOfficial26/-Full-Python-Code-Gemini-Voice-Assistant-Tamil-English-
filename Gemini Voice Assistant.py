import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

# 🔑 Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

# 🗣 Setup text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')

# Choose a voice (optional: Tamil-English mix voice)
for voice in voices:
    if "english" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# 🎤 Speech recognition setup
r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print("🧑 You:", query)
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Could not request results. Please check your internet.")
            return ""

# 🤖 Main loop
speak("Hi, I'm Jarvis. How can I help you?")
while True:
    command = listen()
    if command.lower() in ["exit", "stop", "bye", "shutdown"]:
        speak("Goodbye! Have a great day.")
        break
    elif command:
        try:
            response = model.generate_content(command)
            speak(response.text)
        except Exception as e:
            speak("Sorry, I couldn't get a response. Check your API key or internet.")
            print("Error:", e)
