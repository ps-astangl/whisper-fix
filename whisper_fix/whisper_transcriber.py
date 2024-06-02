import logging
from queue import Queue, Empty
import keyboard
import numpy as np
import pyautogui
import sounddevice as sd
from transformers import WhisperProcessor, WhisperForConditionalGeneration

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class WhisperTranscriber:
    def __init__(self, model_path, hotkey, device='cuda'):
        self.device = device
        try:
            self.processor = WhisperProcessor.from_pretrained(model_path)
            self.model = WhisperForConditionalGeneration.from_pretrained(model_path).to(self.device)
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Model and processor loaded from {model_path}.")
        except Exception as e:
            raise RuntimeError(f"Failed to load model or processor from {model_path}: {str(e)}")

        self.hotkey = hotkey

    def transcribe(self, audio_array, sampling_rate, language='en'):
        try:
            input_features = self.processor(audio_array, sampling_rate=sampling_rate,
                                            return_tensors="pt").input_features.to(self.device)
            self.logger.debug("Input features generated from audio data.")
            predicted_ids = self.model.generate(input_features, language=language)
            self.logger.debug("Predicted IDs generated from model.")
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
            self.logger.debug("Transcription completed.")
            raw_transcription = transcription[0]
            pyautogui.write(raw_transcription)
            return raw_transcription
        except Exception as e:
            self.logger.error(f"Failed to transcribe audio: {str(e)}")
            return ""

    def record_audio(self, sample_rate=16000):
        self.logger.info("Starting audio recording.")
        audio_queue = Queue()
        audio_data = []

        def callback(indata, frames, time, status):
            audio_queue.put(indata.copy())

        try:
            with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback, dtype='float32'):
                while keyboard.is_pressed(self.hotkey):
                    try:
                        data = audio_queue.get(timeout=0.1)  # Use a small timeout to prevent infinite wait
                        audio_data.append(data)
                    except Empty:
                        continue

            audio_data = np.concatenate(audio_data, axis=0)
            self.logger.info("Recording complete.")
            return audio_data.squeeze(), sample_rate
        except Exception as e:
            self.logger.error(f"Failed to record audio: {str(e)}")
            return np.array([]), sample_rate

    def transcribe_from_mic(self, sample_rate=16000, language='en'):
        audio_array, sr = self.record_audio(sample_rate)
        if audio_array.size == 0:
            return ""
        return self.transcribe(audio_array, sr, language=language)


class HotkeyListener:
    def __init__(self, transcriber, hotkey):
        self.transcriber = transcriber
        self.hotkey = hotkey
        self.logger = logging.getLogger(__name__)

    def start_listening(self):
        try:
            self.logger.info(f"Starting hotkey listener for hotkey: {self.hotkey}")
            keyboard.add_hotkey(self.hotkey, self.trigger_transcription)
            keyboard.wait()
        except Exception as e:
            self.logger.error(f"Failed to start hotkey listener: {str(e)}")

    def trigger_transcription(self):
        try:
            self.logger.info("Hotkey pressed. Starting transcription.")
            transcription = self.transcriber.transcribe_from_mic()
            self.logger.info(f"Transcription: {transcription}")
        except Exception as e:
            self.logger.error(f"Failed to transcribe from mic: {str(e)}")
