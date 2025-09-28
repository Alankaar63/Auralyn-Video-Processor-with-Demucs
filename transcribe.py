import whisper
model = whisper.load_model("base")
def transcribe_whisper(audio_path:str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]
# if __name__ == "__main__":
#     test_file = "clean_audio.wav"
#     text = transcribe_whisper(test_file)
#     print("Transcription:",text)