import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import openai
from gtts import gTTS
from decouple import config

# Set OpenAI API key
openai.api_key = config('openai.api_key')

# Adjust these parameters as necessary
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'
FILENAME = 'output.wav'


def record_audio(duration):
    st.write("Recording...")
    audio = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE)
    sd.wait()
    st.write("Recording complete.")
    write(FILENAME, SAMPLE_RATE, audio)
    return FILENAME


def transcribe_audio_file(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            return text
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"


def get_response_from_openai(text):
    response = openai.Completion.create(engine="text-davinci-003", prompt=text, max_tokens=150)
    return response.choices[0].text.strip()


def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False)
    filename = "response.mp3"
    tts.save(filename)
    return filename


def main():
    st.title("BotGoTalk: Your Personal Voice Assistant")

    # Greeting message at the start
    if not st.session_state.get('greeted'):
        welcome_message = "Welcome to Botgo"
        st.write(welcome_message)
        welcome_audio_path = text_to_speech(welcome_message)
        st.audio(welcome_audio_path, format='audio/mp3')
        st.session_state['greeted'] = True

    duration = st.slider("Recording Duration (seconds)", min_value=1, max_value=10)

    if st.button("Start Recording"):
        filename = record_audio(duration)
        transcribed_text = transcribe_audio_file(filename)
        st.write("Transcribed Text: ", transcribed_text)

        response = get_response_from_openai(transcribed_text)
        st.write("Response: ", response)

        audio_file_path = text_to_speech(response)
        st.audio(audio_file_path, format='audio/mp3')


if __name__ == '__main__':
    main()
