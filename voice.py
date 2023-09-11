import speech_recognition as sr
import openai
from gtts import gTTS
import pygame


openai.api_key = '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'


def transcribe_from_microphone():
    recognizer = sr.Recognizer()


    with sr.Microphone() as source:
        print("Please speak into the microphone.")
        audio_data = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio_data, language='hi-IN')
            return text

        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio."
        except sr.RequestError as e:
            return "Could not request results from Google Web Speech API; {0}".format(e)


def get_response_from_openai(text):
    # Use the completion endpoint to get a response from GPT-4
    response = openai.Completion.create(engine="text-davinci-003", prompt=text, max_tokens=150)
    return response.choices[0].text.strip()


def text_to_speech(text, language='hi'):
    tts = gTTS(text=text, lang=language, slow=False)
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


if __name__ == '__main__':
    transcribed_text = transcribe_from_microphone()
    print("Transcribed Text: ", transcribed_text)

    response = get_response_from_openai(transcribed_text)
    print("OpenAI Response: ", response)

    text_to_speech(response)
