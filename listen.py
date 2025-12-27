import speech_recognition as sr

# Create recognizer once (not every call)
recognizer = sr.Recognizer()

def take_command():
    """
    Listen from the default microphone and return the recognized text (lowercased).
    Returns "" if nothing was understood.
    """
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for background noise... (speak after this)")
            recognizer.adjust_for_ambient_noise(source, duration=0.8)

            print("🎧 Listening...")
            # timeout: how long to wait for you to start speaking
            # phrase_time_limit: max length of your speech
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
    except sr.WaitTimeoutError:
        print("⏱️ No speech detected (timeout).")
        return ""

    try:
        # Change language if you want: "en-IN" works better for Indian accent
        command = recognizer.recognize_google(audio, language="en-IN")
        print("✅ You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("🌐 API error while contacting Google Speech:", e)
        return ""
    except Exception as e:
        print("⚠️ Unexpected error while recognizing speech:", e)
        return ""
