from google.cloud import speech


def speech_to_text(audio_bytes: bytes):
    """
    Convert microphone audio bytes to text.
    Supports English, Hindi, Spanish (auto-detect).
    """

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code="en-US",
        alternative_language_codes=["hi-IN", "es-ES"],
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return "", "unknown"

    result = response.results[0]
    transcript = result.alternatives[0].transcript

    detected_language = (
        result.language_code if hasattr(result, "language_code") else "unknown"
    )

    return transcript, detected_language
