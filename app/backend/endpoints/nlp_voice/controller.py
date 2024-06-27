import base64
import io
import pydub
import speech_recognition as sr

def process_base64_audio(encoded_audio, language_code):
    recognizer = sr.Recognizer()

    # Decode base64 string to get the binary content
    binary_content = base64.b64decode(encoded_audio)

    # Convert base64 to BytesIO
    bytes_io = io.BytesIO(binary_content)

    try:
        # Use pydub to load the audio and convert to standard WAV format
        audio = pydub.AudioSegment.from_file(bytes_io)
        wav_data = audio.raw_data
        sample_width = audio.sample_width
        sample_rate = audio.frame_rate

        # Use sr.AudioData to handle the recognition
        audio_data_obj = sr.AudioData(wav_data, sample_rate, sample_width)
        text = recognizer.recognize_google(audio_data_obj, language=language_code)

        print(f"nlp_voice: Recognized text: {text}")

        return text
    except sr.UnknownValueError:
        print("nlp_voice: Google Speech Recognition could not understand audio")
        return "nlp_voice: Google Speech Recognition could not understand audio"
    except sr.RequestError:
        print("nlp_voice: Could not request results from Google Speech Recognition service")
        return "nlp_voice: Could not request results from Google Speech Recognition service"

