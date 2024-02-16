from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os 

def main():
  load_dotenv()

  client = TextAnalyticsClient(
    endpoint=os.getenv("API_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("API_KEY"))
  )

  extract_linked_entities(client)
  
def detect_language(client):
  documents = ["This is written in English.", "Este es un documento escrito en Español.", "这是用中文写的。"]
  response = client.detect_language(documents)

  for document in response:
    print("Language detected: ", document.primary_language.name)


def analyze_sentiment(client):
  documents = ["The food and service were unacceptable. The concierge was nice, however."]
  response = client.analyze_sentiment(documents)

  for document in response:
    print("Overall sentiment: ", document.sentiment)
    for sentence in document.sentences:
      print("Sentence: ", sentence.text)
      print("Sentence sentiment: ", sentence.sentiment)
      print("Sentence confidence scores: ", sentence.confidence_scores)

def key_phase_extraction(client):
  documents = ["Dr. Smith has a very modern medical office, and she has great staff."]
  response = client.extract_key_phrases(documents)

  for document in response:
    print("Key phrases: ", document.key_phrases)

def extract_entities(client):
  documents = [
    "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975.",
    "I built a house in London last year.",
    "I woke up at 9am this morning"
  ]
  response = client.recognize_entities(documents)

  for document in response:
    for entity in document.entities:
      print("Entity: ", entity.text, "Type: ", entity.category, "Sub-type: ", entity.subcategory, "Confidence score: ", entity.confidence_score)

def extract_linked_entities(client):
  documents = [
    "Old Faithful is a geyser at Yellowstone Park.",
    "The Great Wall of China is a world heritage site.",
    "The Great Barrier Reef is the world's largest coral reef system."
  ]
  response = client.recognize_linked_entities(documents)
  print(response)
  for document in response:
    for entity in document.entities:
      print("Entity: ", entity.name, "ID: ", entity.data_source_entity_id, "URL: ", entity.url, "Data source: ", entity.data_source)

if __name__ == "__main__":
  main()