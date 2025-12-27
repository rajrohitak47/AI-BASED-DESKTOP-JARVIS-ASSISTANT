import datetime
import os
import webbrowser
import subprocess

import pywhatkit
import wikipedia
import pyjokes
import pyautogui
import pyperclip

from speech_engine import speak

# --------- CONFIG ---------
NOTES_FILE = "jarvis_notes.txt"
TODO_FILE = "jarvis_todo.txt"

# Change this to your city if you want
DEFAULT_CITY = "Mumbai"

# Base folders
USER_HOME = os.path.expanduser("~")
DOWNLOADS = os.path.join(USER_HOME, "Downloads")
DOCUMENTS = os.path.join(USER_HOME, "Documents")
DESKTOP = os.path.join(USER_HOME, "Desktop")

# Common apps (Edit paths if needed)
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vs code": r"C:\Users\Acer\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "visual studio code": r"C:\Users\Acer\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": "notepad",
    "command prompt": "cmd",
    "cmd": "cmd",
    "calculator": "calc",
}


# =============== BASIC INFO ===============

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")


def tell_date():
    today = datetime.date.today()
    speak(f"Today's date is {today.day} {today.strftime('%B')} {today.year}")


# =============== WEB + MEDIA ===============

def open_website(name):
    if "youtube" in name:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "google" in name:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "whatsapp" in name:
        speak("Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com")
    else:
        speak(f"Opening {name}.")
        webbrowser.open(f"https://{name}.com")


def google_search(query):
    speak(f"Searching Google for {query}")
    pywhatkit.search(query)


def play_on_youtube(query):
    speak(f"Playing {query} on YouTube.")
    pywhatkit.playonyt(query)


def show_weather(city=DEFAULT_CITY):
    speak(f"Showing weather for {city}.")
    url = f"https://www.google.com/search?q=weather+in+{city.replace(' ', '+')}"
    webbrowser.open(url)


def wiki_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except Exception:
        speak("Sorry, I could not find information about that.")


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


# =============== MEMORY / NOTES / TODO ===============

def remember_this(text):
    try:
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        speak("Okay, I will remember that.")
    except Exception:
        speak("Sorry, I could not save that.")


def recall_notes():
    if not os.path.exists(NOTES_FILE):
        speak("I don't have anything remembered yet.")
        return

    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = f.readlines()

        if not notes:
            speak("I don't have anything remembered yet.")
            return

        speak("Here is what I remember.")
        for line in notes:
            speak(line.strip())
    except Exception:
        speak("Sorry, I could not read my notes.")


def add_todo(task):
    try:
        with open(TODO_FILE, "a", encoding="utf-8") as f:
            f.write("- " + task + "\n")
        speak("Task added to your to-do list.")
    except Exception:
        speak("Sorry, I could not add that to your to-do list.")


def read_todo():
    if not os.path.exists(TODO_FILE):
        speak("Your to-do list is empty.")
        return

    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            tasks = f.readlines()

        if not tasks:
            speak("Your to-do list is empty.")
            return

        speak("Here is your to-do list.")
        for task in tasks:
            speak(task.strip())
    except Exception:
        speak("Sorry, I could not read your to-do list.")


# =============== PC AUTOMATION ===============

def open_app(app_name: str):
    app_name = app_name.lower().strip()
    # try exact mapping first
    if app_name in APP_PATHS:
        path = APP_PATHS[app_name]
        speak(f"Opening {app_name}.")
        try:
            # if it's a simple command like 'notepad' or 'calc'
            if "." not in path and " " not in path and "\\" not in path:
                subprocess.Popen(path)
            else:
                os.startfile(path)
        except Exception:
            speak("Sorry, I could not open that application.")
    else:
        speak(f"I don't know the path for {app_name}. You can add it in APP_PATHS.")


def open_folder(name: str):
    name = name.lower()
    if "download" in name:
        folder = DOWNLOADS
    elif "document" in name:
        folder = DOCUMENTS
    elif "desktop" in name:
        folder = DESKTOP
    else:
        speak("Which folder? I can open Downloads, Documents, or Desktop.")
        return

    if os.path.exists(folder):
        speak(f"Opening {name} folder.")
        os.startfile(folder)
    else:
        speak("Sorry, that folder does not seem to exist.")


def create_folder(folder_name: str, base: str = DESKTOP):
    folder_name = folder_name.strip()
    if not folder_name:
        speak("What should be the folder name?")
        return
    full_path = os.path.join(base, folder_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        speak(f"Folder {folder_name} created.")
        os.startfile(full_path)
    except Exception:
        speak("Sorry, I could not create that folder.")


def create_quick_note(text: str):
    if not text:
        speak("What should I write in the note?")
        return
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(DESKTOP, f"note_{now}.txt")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        speak("Note created on your desktop.")
        os.startfile(filename)
    except Exception:
        speak("Sorry, I could not create the note.")


def take_screenshot():
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(DESKTOP, f"screenshot_{now}.png")
        image = pyautogui.screenshot()
        image.save(filename)
        speak("Screenshot taken and saved on your desktop.")
    except Exception:
        speak("Sorry, I could not take a screenshot.")


def type_text(text: str):
    if not text:
        speak("What should I type?")
        return
    try:
        # copy to clipboard and paste (more reliable for unicode)
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        speak("Done.")
    except Exception:
        # fallback: direct typing
        try:
            pyautogui.typewrite(text, interval=0.03)
            speak("Done.")
        except Exception:
            speak("Sorry, I could not type right now.")


def control_volume(action: str):
    # Simple keyboard based volume control
    try:
        if "mute" in action:
            pyautogui.press("volumemute")
            speak("Volume muted.")
        elif "up" in action:
            for _ in range(5):
                pyautogui.press("volumeup")
            speak("Volume increased.")
        elif "down" in action or "low" in action:
            for _ in range(5):
                pyautogui.press("volumedown")
            speak("Volume decreased.")
        else:
            speak("Do you want volume up, down, or mute?")
    except Exception:
        speak("Sorry, I could not control the volume.")


def system_power(action: str):
    action = action.lower()
    if "shutdown" in action or "shut down" in action:
        speak("Shutting down your system. Goodbye.")
        os.system("shutdown /s /t 0")
    elif "restart" in action or "reboot" in action:
        speak("Restarting your system.")
        os.system("shutdown /r /t 0")
    elif "log out" in action or "sign out" in action:
        speak("Signing out.")
        os.system("shutdown /l")
    else:
        speak("What should I do? Shutdown, restart, or log out?")


# =============== MAIN ROUTER ===============

def run_jarvis(command: str):
    """
    Main router for Jarvis commands.
    You call this from main.py with the recognized speech.
    """
    command = command.lower()
    print(f"[DEBUG] Command received: {command}")

    # ---- Basic info ----
    if "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    # ---- Web / media ----
    elif "open youtube" in command:
        open_website("youtube")

    elif "open google" in command:
        open_website("google")

    elif "open whatsapp" in command:
        open_website("whatsapp")

    elif "play" in command and "youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        if query:
            play_on_youtube(query)
        else:
            speak("What should I play?")

    elif "search for" in command or "google" in command:
        query = command.replace("search for", "").replace("google", "").strip()
        if query:
            google_search(query)
        else:
            speak("What should I search for?")

    elif "weather" in command:
        words = command.split()
        city = DEFAULT_CITY
        if "in" in words:
            idx = words.index("in")
            if idx + 1 < len(words):
                city = " ".join(words[idx + 1:])
        show_weather(city)

    elif "joke" in command:
        tell_joke()

    # ---- Memory / notes / todo ----
    elif "remember that" in command or "remember this" in command:
        text = command.replace("remember that", "").replace("remember this", "").strip()
        remember_this(text)

    elif "what do you remember" in command or "what did you remember" in command \
            or "my notes" in command or "read my notes" in command:
        recall_notes()

    elif "add task" in command or "add to my list" in command or "todo" in command:
        # e.g. "add task submit assignment" or "add to my list pay fees"
        text = command.replace("add task", "").replace("add to my list", "").replace("todo", "").strip()
        add_todo(text)

    elif "read my list" in command or "show my tasks" in command \
            or "show my to do" in command:
        read_todo()

    elif "make a note" in command or "create a note" in command:
        # e.g. "make a note buy groceries"
        text = command.replace("make a note", "").replace("create a note", "").strip()
        create_quick_note(text)

    # ---- PC automation ----
    elif "open folder" in command:
        # e.g. "open folder downloads"
        if "downloads" in command:
            open_folder("downloads")
        elif "documents" in command:
            open_folder("documents")
        elif "desktop" in command:
            open_folder("desktop")
        else:
            open_folder("")  # will ask

    elif "open" in command and ("app" in command or "application" in command or "program" in command):
        # e.g. "open app chrome", "open application vs code"
        name = command.replace("open app", "").replace("open application", "").replace("open program", "").strip()
        open_app(name)

    elif "open" in command and any(app in command for app in ["chrome", "notepad", "vs code", "visual studio code", "command prompt", "cmd", "calculator"]):
        # e.g. "open chrome", "open notepad"
        for key in APP_PATHS.keys():
            if key in command:
                open_app(key)
                break

    elif "create folder" in command or "make folder" in command:
        # e.g. "create folder college notes", default on Desktop
        name = command.replace("create folder", "").replace("make folder", "").strip()
        create_folder(name, DESKTOP)

    elif "take screenshot" in command or "screenshot" in command:
        take_screenshot()

    elif "type" in command and "this" in command:
        # not very useful, but kept as pattern
        speak("What should I type?")
    elif "type" in command:
        # e.g. "type hello how are you"
        text = command.split("type", 1)[1].strip()
        type_text(text)

    elif "volume" in command:
        control_volume(command)

    elif "shutdown" in command or "shut down" in command or "restart" in command or "reboot" in command or "log out" in command:
        system_power(command)

    # ---- Wikipedia fallback ----
    elif "who is" in command or "what is" in command or "tell me about" in command:
        if "who is" in command:
            topic = command.split("who is", 1)[1].strip()
        elif "what is" in command:
            topic = command.split("what is", 1)[1].strip()
        else:
            topic = command.split("tell me about", 1)[1].strip()

        if topic:
            speak(f"Searching Wikipedia for {topic}.")
            wiki_summary(topic)
        else:
            speak("What should I search on Wikipedia?")

    # ---- Final fallback: Google any unknown command ----
    else:
        speak("I did not understand, but I can search that on Google.")
        google_search(command)
