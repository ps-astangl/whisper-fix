import logging
import threading

from whisper_fix.state_change_indicator import StateChangeIndicator

class WhisperApp:
    def __init__(self, whisper_model_path: str, hotkey: str, state_change_indicator: StateChangeIndicator):
        self.state = 'idle'
        self.whisper_model_path = whisper_model_path
        self.hotkey = hotkey
        self.transcriber = None
        self.listener = None
        self.logger = logging.getLogger(__name__)
        self.state_change_indicator = state_change_indicator

    def start(self, stop_event):
        # Delay import to avoid circular import issues
        from whisper_fix.listener import HotkeyListener
        from whisper_fix.transcriber import WhisperTranscriber

        self.transcriber = WhisperTranscriber(self.whisper_model_path, self.hotkey, self)
        self.listener = HotkeyListener(self.transcriber, self.hotkey, self)

        listener_thread = threading.Thread(target=self.listener.start_listening)
        listener_thread.start()

        try:
            while listener_thread.is_alive() and not stop_event.is_set():
                listener_thread.join(timeout=1)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user. Shutting down...")

    def set_state(self, state: str):
        self.state = state
        self.state_change_indicator.display_state_change(state)

    def get_state(self):
        return self.state