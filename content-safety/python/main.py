import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory, AnalyzeImageOptions, ImageData, ImageCategory

def main():
  try:
    load_dotenv()
    endpoint = os.environ["API_ENDPOINT"]
    key = os.environ["API_KEY"]
    credential = AzureKeyCredential(key)

    content_safety_client = ContentSafetyClient(endpoint, credential)

    analyze_text(content_safety_client, "You are an idiot")
    analyze_image(content_safety_client, os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "./images/man-holding-gun.jpg")))

  except Exception as ex:
    print(ex)


def analyze_text(client, text):
  request = AnalyzeTextOptions(text=text)
  
  try:
    response = client.analyze_text(request)
  except Exception as ex:
    print(ex)
  
  print(f"Text: {text}")
  hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
  self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
  sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
  violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

  if hate_result:
      print(f"Hate severity: {hate_result.severity}")
  if self_harm_result:
      print(f"SelfHarm severity: {self_harm_result.severity}")
  if sexual_result:
      print(f"Sexual severity: {sexual_result.severity}")
  if violence_result:
      print(f"Violence severity: {violence_result.severity}")


def analyze_image(client, image_path):
  with open(image_path, "rb") as file:
     request = AnalyzeImageOptions(image=ImageData(content=file.read()))
    
  try:
    response = client.analyze_image(request)
  except Exception as ex:
    print(ex)
  
  print("")
  print("Image analysis")
  hate_result = next(item for item in response.categories_analysis if item.category == ImageCategory.HATE)
  self_harm_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SELF_HARM)
  sexual_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SEXUAL)
  violence_result = next(item for item in response.categories_analysis if item.category == ImageCategory.VIOLENCE)

  if hate_result:
      print(f"Hate severity: {hate_result.severity}")
  if self_harm_result:
      print(f"SelfHarm severity: {self_harm_result.severity}")
  if sexual_result:
      print(f"Sexual severity: {sexual_result.severity}")
  if violence_result:
      print(f"Violence severity: {violence_result.severity}")

if __name__ == "__main__":
  main()