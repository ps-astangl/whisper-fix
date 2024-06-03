# Whisper Fix

Whisper Fix is a speech-to-text application that uses the Whisper model for transcription. The application listens for a hotkey press to start recording audio from the microphone, transcribes the recorded audio, and displays the transcription.

## Features
- Hotkey-based audio recording
- Real-time transcription using the Whisper model
- State change indicator using Tkinter

## Requirements
- Python 3.7+
- torch
- transformers
- keyboard
- numpy
- pyautogui
- sounddevice
- python-dotenv
- tkinter

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/whisper-fix.git
    cd whisper-fix
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following content:
    ```sh
    WHISPER_MODEL_PATH=openai/whisper-small
    HOTKEY=your_hotkey
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Press the specified hotkey to start recording audio. Release the hotkey to stop recording and start transcription.

## File Structure

- `main.py`: Entry point of the application. Initializes the Tkinter GUI and starts the WhisperApp.
- `whisper_fix/listener.py`: Contains the `HotkeyListener` class that listens for the hotkey press and triggers transcription.
- `whisper_fix/state_change_indicator.py`: Contains the `StateChangeIndicator` class that updates the state label in the Tkinter GUI.
- `whisper_fix/transcriber.py`: Contains the `WhisperTranscriber` class that handles audio recording and transcription.
- `whisper_fix/whisper_app.py`: Contains the `WhisperApp` class that manages the overall application state and coordinates between components.
