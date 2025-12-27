from speech_engine import speak
from listen import take_command
from tasks import run_jarvis

wake_word = "jarvis"

speak("Hello, I am Jarvis. Say my name when you need help.")

while True:
    print("Waiting for command...")
    command = take_command()

    if not command:
        continue

    if "exit" in command or "stop" in command or "goodbye" in command:
        speak("Goodbye!")
        break

    if wake_word in command:
        command = command.replace(wake_word, "").strip()
        if command == "":
            speak("Yes, what can I do for you?")
        else:
            run_jarvis(command)
