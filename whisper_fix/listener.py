import logging
import keyboard
from whisper_fix.transcriber import WhisperTranscriber
from whisper_fix.whisper_app import WhisperApp


class HotkeyListener:
    def __init__(self, transcriber: WhisperTranscriber, hotkey: str, app: WhisperApp) -> None:
        self.transcriber: WhisperTranscriber = transcriber
        self.hotkey: str = hotkey
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.app: WhisperApp = app

    def start_listening(self) -> None:
        self.app.set_state('transcribing')
        try:
            self.logger.info(f":: Starting hotkey listener for hotkey: {self.hotkey}")
            keyboard.add_hotkey(self.hotkey, self.trigger_transcription)
            keyboard.wait()
        except Exception as e:
            self.logger.error(f":: Failed to start hotkey listener: {str(e)}")
        finally:
            self.app.set_state('idle')

    def trigger_transcription(self) -> None:
        try:
            self.logger.info(f":: Hotkey pressed. Starting transcription.")
            transcription: str = self.transcriber.transcribe_from_mic()
            self.logger.info(f":: Transcription: {transcription}")
        except Exception as e:
            self.logger.error(f":: Failed to transcribe from mic: {str(e)}")
