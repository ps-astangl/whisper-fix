import os
import signal
import sys
import tkinter as tk
import threading
from dotenv import load_dotenv

from whisper_fix.state_change_indicator import StateChangeIndicator
from whisper_fix.whisper_app import WhisperApp

stop_event = threading.Event()


def signal_handler(sig, frame):
    print("Interrupted by user. Shutting down...")
    stop_event.set()
    # Allow the Tkinter mainloop to exit
    root.quit()


def start_app(app, stop_event):
    app.start(stop_event)


if __name__ == '__main__':
    load_dotenv()

    signal.signal(signal.SIGINT, signal_handler)

    whisper_model_path: str = os.getenv('WHISPER_MODEL_PATH', "")
    hotkey: str = os.getenv('HOTKEY', "")

    root = tk.Tk()

    # Display a message when the app starts
    start_message = tk.Label(root, text="Speach To Text", font=("Arial", 14))
    start_message.pack(pady=20)  # Add some padding for better layout

    label = tk.Label(root, text="Idle", font=("Arial", 12))
    label.pack()

    state_change_indicator = StateChangeIndicator(label)

    app = WhisperApp(whisper_model_path, hotkey, state_change_indicator)

    # Start the WhisperApp in a separate thread
    app_thread = threading.Thread(target=start_app, args=(app, stop_event))
    app_thread.start()

    # Start the Tkinter event loop in the main thread
    root.mainloop()

    # Wait for the app thread to finish
    app_thread.join()
