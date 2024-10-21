from moviepy.editor import VideoFileClip


def convert_mp4_to_wav(input_filepath, output_filepath):
    """
    Converts an MP4 file to a WAV file.

    :param input_filepath: Path to the input MP4 file
    :param output_filepath: Path to save the output WAV file
    """
    # Load the video file
    video_clip = VideoFileClip(input_filepath)

    # Extract the audio as an AudioFileClip
    audio_clip = video_clip.audio

    # Write the audio clip to a WAV file
    audio_clip.write_audiofile(output_filepath, codec='pcm_s16le')

    # Close the clips to free resources
    audio_clip.close()
    video_clip.close()


if __name__ == '__main__':
    input_mp4 = "C:\\Users\\Alfred.Stangl\\OneDrive - CRISP Shared Services\\Desktop\\Recording 2024-08-15 103459.mp4"
    output_wav = 'output_audio.wav'
    convert_mp4_to_wav(input_mp4, output_wav)