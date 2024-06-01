import os
import signal
import sys
import threading

from dotenv import load_dotenv

from whisper_fix.whisper_transcriber import WhisperTranscriber, HotkeyListener


def signal_handler(sig, frame):
    print("Interrupted by user. Shutting down...")
    sys.exit(0)


if __name__ == '__main__':
    load_dotenv()
    # Register the signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)

    whisper_model_path = os.getenv('WHISPER_MODEL_PATH')
    transcriber = WhisperTranscriber(whisper_model_path, None)
    hotkey_listener = HotkeyListener(transcriber)

    listener_thread = threading.Thread(target=hotkey_listener.start_listening)
    listener_thread.start()

    try:
        while listener_thread.is_alive():
            listener_thread.join(timeout=1)  # Join with a timeout to allow checking for KeyboardInterrupt
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
        sys.exit(0)
