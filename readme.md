Sure thing, Captain. Here's the updated README for you to copy and paste:

### README.md

# Whisper Fix

Whisper Fix is a simple implementation of a transcription service using the Whisper model from Hugging Face Transformers. This project records audio, transcribes it, and automatically types the transcription using PyAutoGUI.

## Features

- Record audio using `sounddevice`
- Transcribe audio using Hugging Face's Whisper model
- Automatically type the transcription using `PyAutoGUI`
- Hotkey listener to start transcription

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/whisper-fix.git
cd whisper-fix
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Download the Whisper Large model from Hugging Face into the repo directory:

```bash
git lfs install
git clone https://huggingface.co/openai/whisper-large whisper_fix/whisper-large
```

4. Copy `.env.template` to `.env` and update the values as needed:

```bash
cp .env.template .env
```

Make sure the model path in your `.env` file matches the path where you cloned the Whisper Large model (`whisper_fix/whisper-large`).

## Usage

1. Run the main script:

```bash
python main.py
```

2. Press `Ctrl+Shift+Alt` to start recording audio. Release the keys to stop recording and get the transcription.

## File Structure

- `whisper_fix/`
  - `__init__.py`: Initialization file for the package
  - `whisper_transcriber.py`: Contains the `WhisperTranscriber` class for audio recording and transcription
  - `whisper-large/`: Directory where the Whisper Large model is cloned
  - `main.py`: Main script to run the hotkey listener and transcriber
- `.env`: Environment variable file
- `.env.template`: Template for environment variable file
- `requirements.txt`: List of dependencies
- `setup.py`: Setup script for the package

## Requirements

- Python 3.8+
- `transformers`
- `torch`
- `keyboard`
- `numpy`
- `pyautogui`
- `sounddevice`
- `python-dotenv`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
