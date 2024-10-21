

import logging
import os
from typing import Optional

import numpy as np
import torch
from moviepy.editor import VideoFileClip
from scipy.io import wavfile
from tqdm import tqdm
from transformers import WhisperProcessor, WhisperForConditionalGeneration


class VideoTranscriber:
    def __init__(self, model_path: str, device: str = torch.cuda.is_available() and 'cuda' or 'cpu'):
        self.device = device
        self.processor: WhisperProcessor = WhisperProcessor.from_pretrained(model_path)
        self.model: WhisperForConditionalGeneration = WhisperForConditionalGeneration.from_pretrained(model_path).to(
            self.device)
        self.logger = logging.getLogger(__name__)

    def transcribe_video(self, path: str, language: str = 'en') -> Optional[str]:
        try:
            self.logger.info(f":: Loading video file from {path}.")
            video = VideoFileClip(path)
            audio = video.audio
            if audio is None:
                self.logger.error(":: No audio found in the video file.")
                return None

            audio_path = "temporary_audio.wav"
            self.logger.info(f":: Writing temporary audio file to {audio_path}.")

            self.logger.info(":: Extracting and transcribing audio on-the-fly.")
            fps = 16000

            buffers = []
            frame_chunk_size = int(fps * 60)  # Process every 15 seconds of audio
            frame_count = 0

            total_frames = int(audio.fps * audio.duration)
            transcription = []

            for frame in tqdm(audio.iter_frames(fps=fps, dtype='float32'), total=total_frames, desc="Processing audio frames"):
                frame_buffer = (frame.mean(axis=1) if frame.ndim == 2 else frame).astype(np.float32)
                buffers.append(frame_buffer)
                frame_count += 1

                if frame_count % frame_chunk_size == 0:
                    audio_chunk = np.concatenate(buffers)
                    buffers = []
                    transcribed_chunk = self.transcribe(audio_chunk, fps, language=language)
                    transcription.append(transcribed_chunk)
                    self.logger.debug(f":: Transcribed chunk: {transcribed_chunk}")

            # Process any remaining buffers
            if buffers:
                audio_chunk = np.concatenate(buffers)
                transcribed_chunk = self.transcribe(audio_chunk, fps, language=language)
                transcription.append(transcribed_chunk)
                self.logger.debug(f":: Transcribed final chunk: {transcribed_chunk}")

            out_transcription = ' '.join(transcription)
            self.logger.info(":: Transcription complete.")

            return out_transcription

        except Exception as e:
            self.logger.error(f":: Failed to transcribe video: {str(e)}")
            return None

    def transcribe(self, audio_array: np.ndarray, sampling_rate: int, language: str = 'en') -> str:
        try:
            input_features = self.processor(audio_array, sampling_rate=sampling_rate,
                                            return_tensors="pt").input_features.to(self.device)
            self.logger.debug(":: Input features generated from audio data.")
            predicted_ids = self.model.generate(input_features, language=language)
            self.logger.debug(":: Predicted IDs generated from model.")
            output_transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
            self.logger.debug(":: Transcription completed.")
            raw_transcription: str = output_transcription[0]
            return raw_transcription
        except Exception as e:
            self.logger.error(f":: Failed to transcribe audio: {str(e)}")
            return ""


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    video_path = "C:\\Users\\Alfred.Stangl\\OneDrive - CRISP Shared Services\\Desktop\\Recording 2024-08-15 103459.mp4"
    model_path = "openai/whisper-small"
    video_transcriber = VideoTranscriber(model_path)
    transcription = video_transcriber.transcribe_video(video_path)
    print(transcription)
