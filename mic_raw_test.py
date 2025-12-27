import speech_recognition as sr

# Try the mic index that looks like your laptop mic first
MIC_INDEX = 1  # we'll change this if needed

r = sr.Recognizer()

with sr.Microphone(device_index=MIC_INDEX) as source:
    print(f"🎤 Using microphone index {MIC_INDEX}")
    print("Adjusting for noise...")
    r.adjust_for_ambient_noise(source, duration=0.5)

    print("🎧 Say something (the program will stop after you finish speaking)...")
    audio = r.listen(source)  # 👈 NO timeout here

print("✅ Captured audio from the mic.")
wav_data = audio.get_wav_data()
print("Audio byte length:", len(wav_data))
