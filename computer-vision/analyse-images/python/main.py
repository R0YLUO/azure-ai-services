from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
import os

def main():
  load_dotenv()
  client = ImageAnalysisClient(endpoint=os.getenv('API_ENDPOINT'), credential=AzureKeyCredential(os.getenv('API_KEY')))

  analyse_image(client)

def analyse_image(client):
  res = client.analyze(
    image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png", 
    visual_features=[VisualFeatures.PEOPLE]
  )
  print(res)

if __name__ == "__main__":
  main()