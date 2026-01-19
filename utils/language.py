def normalize_language(language_code: str) -> str:
    """
    Map detected language to TTS-compatible language codes.
    """

    if language_code.startswith("hi"):
        return "hi-IN"
    if language_code.startswith("es"):
        return "es-ES"

    return "en-US"
