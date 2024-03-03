import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

app = Flask(__name__)

load_dotenv()
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
search_index = os.getenv("SEARCH_INDEX")

def search_query(search_text, filter_by=None, sort_order=None):
  try:
    azure_credentials = AzureKeyCredential(search_key)
    search_client = SearchClient(search_endpoint, search_index, azure_credentials)

    results = search_client.search(search_text,
                                   search_mode="all",
                                   filter=filter_by,
                                   order_by=sort_order,
                                   facets='metadata_author',
                                   highlight_fields='merged_content-3,imageCaption-3',
                                   select="url,metadata_storage_name,metadata_author,metadata_storage_size,metadata_storage_last_modified,language,sentiment,merged_content,keyphrases,locations,imageTags,imageCaption")

    return results
  except Exception as e:
    raise e
  
@app.route("/")
def home():
  return render_template("default.html")

@app.route("/search", methods=['GET'])
def search():
  try: 
    search_text = request.args["search"]

    filter_expression = None
    if 'facet' in request.args:
      filter_expression = "metadata_author eq '{0}'".format(request.args["facet"])

    sort_expression = "search.score()"
    sort_field = "relevance"
    if 'sort' in request.args:
      sort_field = request.args["sort"]
      if sort_field == 'file_name':
        sort_expression = 'metadata_storage_name asc'
      elif sort_field == 'size':
        sort_expression = 'metadata_storage_size desc'
      elif sort_field == 'date':
        sort_expression = 'metadata_storage_last_modified desc'
      elif sort_field == 'sentiment':
        sort_expression = 'sentiment desc'
    results = search_query(search_text, filter_expression, sort_expression)
    for result in results: 
      print(result)
    return render_template("search.html", search_results=results, search_terms=search_text)

  except Exception as e:
    return render_template("error.html", error_message=e)
  

if __name__ == "__main__":
  results = search_query("london hotel")
  for result in results:
    print(result)