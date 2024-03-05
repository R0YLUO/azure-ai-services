using Azure.AI.OpenAI;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;
using Azure;

namespace nlp
{
  class Program
  {
    static void Main(string[] args)
    {
      IConfiguration config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.Development.json")
        .Build();
      string? endpoint = config["ApiEndpoint"];
      string? apiKey = config["ApiKey"];
      string? deploymentName = config["DeploymentName"]; 

      if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(endpoint) || string.IsNullOrEmpty(deploymentName))
      {
        Console.WriteLine("Please set API_KEY, API_ENDPOINT, and IMAGE_GEN_DEPLOYMENT_NAME environment variables.");
        return;
      }

      OpenAIClient client = new OpenAIClient(new Uri(endpoint), new AzureKeyCredential(apiKey));
      
      string text = args[0].Length > 0 ? args[0] : ""; 
      ChatCompletionsOptions chatCompletionsOptions = new ChatCompletionsOptions()
      {
        Messages = 
        {
          new ChatMessage(ChatRole.System, "You are a helpful assistant"),
          new ChatMessage(ChatRole.User, "Summarise the following text in 8 words or less:\n" + text)
        },
        MaxTokens = 120,
        Temperature = 0.7f,
        DeploymentName = deploymentName
      };

      ChatCompletions response = client.GetChatCompletions(chatCompletionsOptions);
      string completion = response.Choices[0].Message.Content;

      Console.WriteLine("Summary: " + completion + "\n");
    }
  }
}