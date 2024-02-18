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

  classify_text(client)

def classify_text(client): 
  operation = client.begin_single_label_classify(
    documents=["""Caleb Foster says Nicole Wagner recovering after car accident 'Fun Summer' Season 2: Everything We Know So Far About Relecloud's New Show
           To be continued. After Fun Summer became a fan favorite on Relecloud, it got a quick renewal — leaving audiences craving for more.
The series debuted in April 2021 and told a story over three years: 1993, 1994 and 1995. It followed Nicole Wagner, who was kidnapped and later rescued, and Caleb Foster, who was accused of knowing the whereabouts of the missing girl.
The timeline went back and forth exploring both perspectives without revealing the truth until the explosive season 1 finale. The story wrapped up with Nicole admitting that she was wrong about Caleb seeing her in her kidnapper's home. However, a shocking twist revealed that Caleb actually heard Nicole asking for help when she was held captive in 1994."],
               """],
    project_name="ai102democlassify",
    deployment_name="ai102"
  )

  result = operation.result()

  for doc in result: 
    print(doc)

if __name__ == "__main__":
  main()