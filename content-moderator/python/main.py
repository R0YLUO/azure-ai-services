import os 
from dotenv import load_dotenv
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient 
from msrest.authentication import CognitiveServicesCredentials
from pprint import pprint

def main():
  try:
    # Obtain environment variables
    load_dotenv()
    endpoint = os.environ["API_ENDPOINT"]
    key = os.environ["API_KEY"]

    # Initiate client using Azure SDK
    content_safety_client = ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))

    # Run content moderation examples
    analyze_text(content_safety_client)
  except Exception as ex: 
    print(ex)

def analyze_text(client):
  with open("content.txt", "r") as file:
    screen = client.text_moderation.screen_text(
      text_content_type="text/plain",
      text_content=file,
      pii=True,
      classify=True
    )
    pprint(screen.as_dict())

if __name__ == "__main__":
  main()