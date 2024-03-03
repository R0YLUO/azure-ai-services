import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv
import os

def main(): 
  load_dotenv()

  speech_config = speech_sdk.SpeechConfig(os.getenv("API_KEY"), os.getenv("API_REGION"))
  translation_config = speech_sdk.translation.SpeechTranslationConfig(os.getenv("API_KEY"), os.getenv("API_REGION"))

  translate_speech(translation_config)

def process_speech(speech_config):
  # Configure speech recognition
  audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
  speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
  print('Speak now...')

  result = speech_recognizer.recognize_once_async().get()
  print(result.text)

def synthesise_speech(speech_config):
  speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
  speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
  speech_synthesizer.speak_text_async("hello world").get()

def translate_speech(translation_config):
  translation_config.speech_recognition_language = "en-US"
  translation_config.add_target_language("fr")
  translation_config.add_target_language("ja")

  audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
  translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
  print("Speak now...")
  result = translator.recognize_once_async().get()
  print("Translating ", result.text)
  print("Results: ")
  for key in result.translations:
    print(result.translations[key])

if __name__ == '__main__':
  main()

