from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os 

def main():
  load_dotenv()

  client = TextAnalyticsClient(
    endpoint=os.getenv("API_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("API_KEY"))
  )

  extract_custom_entities(client)

def extract_custom_entities(client): 
  documents = [
    "I am selling my car for $10,000. Pick up at 123 Main Street, Anytown, USA.",
  ]

  operation = client.begin_recognize_custom_entities(
    documents,
    project_name="ai102extractcustom",
    deployment_name="ai102"
  )

  result = operation.result()

  for doc in result:
    print(doc)

if __name__ == "__main__":
  main()