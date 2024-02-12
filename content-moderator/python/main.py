import os 
from dotenv import load_dotenv
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient 
from azure.core.credentials import AzureKeyCredential
from pprint import pprint

def main():
  try:
    # Obtain environment variables
    load_dotenv()
    endpoint = os.environ["API_ENDPOINT"]
    key = os.environ["API_KEY"]

    # Initiate client using Azure SDK
    content_safety_client = ContentModeratorClient(endpoint=endpoint, credentials=AzureKeyCredential(key))

    # Run content moderation examples

  except Exception as ex:
    print(ex)

def analyze_text(client, text):
  client.text_moderation.screen_text()
