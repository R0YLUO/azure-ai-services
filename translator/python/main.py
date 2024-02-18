from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem
from dotenv import load_dotenv
import os

def main():
  load_dotenv()
  
  credentials = TranslatorCredential(os.getenv("API_KEY"), os.getenv("API_REGION"))
  client = TextTranslationClient(credentials)

  translate(client)

def translate(client):
  translation_response = client.translate(content=[InputTextItem(text="hello world"), InputTextItem(text="what are you doing")], to=["ja", "lzh"])
  print(translation_response)


if __name__ == "__main__":
  main()