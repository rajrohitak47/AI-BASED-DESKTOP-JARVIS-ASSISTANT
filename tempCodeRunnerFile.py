from speech_engine import speak
from listen import take_command
from tasks import run_jarvis

speak("Hello, I am multilingual Jarvis. How can I help you?")

while True:
    command = take_command()
    if 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        break
    run_jarvis(command)
