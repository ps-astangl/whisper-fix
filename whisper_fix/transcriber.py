import logging
from queue import Queue, Empty
from typing import Tuple, List

import keyboard
import numpy as np
import pyautogui
import sounddevice as sd
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from whisper_fix.whisper_app import WhisperApp


class WhisperTranscriber:
    def __init__(self, model_path: str, hotkey: str, app: WhisperApp, device: str = 'cuda') -> None:
        self.device: str = device
        try:
            self.processor: WhisperProcessor = WhisperProcessor.from_pretrained(model_path)
            self.model: WhisperForConditionalGeneration = WhisperForConditionalGeneration.from_pretrained(model_path).to(self.device)
            self.logger: logging.Logger = logging.getLogger(__name__)
            self.logger.info(f":: Model and processor loaded from {model_path}.")
        except Exception as e:
            raise RuntimeError(f":: Failed to load model or processor from {model_path}: {str(e)}")

        self.hotkey: str = hotkey
        self.app: WhisperApp = app

    def transcribe(self, audio_array: np.ndarray, sampling_rate: int, language: str = 'en') -> str:
        try:
            self.app.set_state('transcribing')
            input_features = self.processor(audio_array, sampling_rate=sampling_rate, return_tensors="pt").input_features.to(self.device)
            self.logger.debug(":: Input features generated from audio data.")
            predicted_ids = self.model.generate(input_features, language=language)
            self.logger.debug(":: Predicted IDs generated from model.")
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
            self.logger.debug(":: Transcription completed.")
            raw_transcription: str = transcription[0]
            pyautogui.write(raw_transcription)
            return raw_transcription
        except Exception as e:
            self.logger.error(f":: Failed to transcribe audio: {str(e)}")
            return ""
        finally:
            self.app.set_state('idle')

    def record_audio(self, sample_rate: int = 16000) -> Tuple[np.ndarray, int]:
        self.app.set_state('recording')
        self.logger.info(":: Starting audio recording.")
        audio_queue: Queue[np.ndarray] = Queue()
        audio_data: List[np.ndarray] = []

        def callback(indata: np.ndarray, frames: int, time, status) -> None:
            audio_queue.put(indata.copy())

        try:
            with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback, dtype='float32'):
                while keyboard.is_pressed(self.hotkey):
                    try:
                        data = audio_queue.get(timeout=0.1)  # Use a small timeout to prevent infinite wait
                        audio_data.append(data)
                    except Empty:
                        continue

            if audio_data:  # Check if audio_data is not empty
                # noinspection PyTypeChecker
                # (audio_data is guaranteed to be non-empty at this point)
                audio_data = np.concatenate(audio_data, axis=0)
                self.logger.info("Recording complete.")

                # noinspection PyUnresolvedReferences
                # (audio_data is guaranteed to be non-empty at this point)
                return audio_data.squeeze(), sample_rate
            else:
                self.logger.warning("No audio data was recorded.")
                return np.array([]), sample_rate
        except Exception as e:
            self.logger.error(f"Failed to record audio: {str(e)}")
            return np.array([]), sample_rate

    def transcribe_from_mic(self, sample_rate: int = 16000, language: str = 'en') -> str:
        self.app.set_state('recording')
        try:
            audio_array, sr = self.record_audio(sample_rate)
            if audio_array.size == 0:
                return ""
            return self.transcribe(audio_array, sr, language=language)
        finally:
            self.app.set_state('idle')
