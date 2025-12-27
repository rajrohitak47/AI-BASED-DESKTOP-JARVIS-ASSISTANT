import speech_recognition as sr

MIC_INDEX = 1  # same as in listen.py

r = sr.Recognizer()

with sr.Microphone(device_index=MIC_INDEX) as source:
    print(f"🎤 Using microphone index {MIC_INDEX}")
    print("Adjusting for noise...")
    r.adjust_for_ambient_noise(source, duration=0.5)

    r.dynamic_energy_threshold = False
    r.energy_threshold = 300

    print("🎧 Say something...")
    audio = r.listen(source, timeout=7, phrase_time_limit=5)

print("Got audio, recognizing...")

try:
    text = r.recognize_google(audio, language="en-IN")
    print("You said:", text)
except Exception as e:
    print("Error:", e)
