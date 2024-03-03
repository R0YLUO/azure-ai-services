using Microsoft.DotNet.Interactive;
using Microsoft.DotNet.Interactive.AIUtilities;
using Azure;
using Azure.AI.OpenAI;
using SkiaSharp;
using System.Net.Http;
using System.IO;

namespace dalle3
{
  class Program
  {
    static async Task Main(string[] args)
    {
      DotNetEnv.Env.Load("../../.env");
      var apiKey = Environment.GetEnvironmentVariable("API_KEY");
      var apiEndpoint = Environment.GetEnvironmentVariable("API_ENDPOINT");
      var deploymentName = Environment.GetEnvironmentVariable("IMAGE_GEN_DEPLOYMENT_NAME");

      if (string.IsNullOrEmpty(apiKey) || string.IsNullOrEmpty(apiEndpoint) || string.IsNullOrEmpty(deploymentName))
      {
        Console.WriteLine("Please set API_KEY, API_ENDPOINT, and IMAGE_GEN_DEPLOYMENT_NAME environment variables.");
        return;
      }

      OpenAIClient client = new OpenAIClient(new Uri(apiEndpoint), new AzureKeyCredential(apiKey));

      var imageGenerations = await client.GetImageGenerationsAsync(
        new ImageGenerationOptions()
        {
          Prompt = args.Length > 0 ? args[0] : "A painting of a sunset over the ocean.",
          Size = ImageSize.Size1024x1024,
          DeploymentName = deploymentName,
        }); 
      
      var imageUri = imageGenerations.Value.Data[0].Url;
      var surface = await ShowImage(imageUri.ToString(), 1024, 1024);
      using (var stream = new FileStream("image.png", FileMode.Create))
      {
        surface.Snapshot().Encode().SaveTo(stream);
      }
    }

    static async Task<SKSurface> ShowImage(string url, int width, int height)
    {
      SKImageInfo info = new SKImageInfo(width, height);
      SKSurface surface = SKSurface.Create(info);
      SKCanvas canvas = surface.Canvas;
      canvas.Clear(SKColors.White);
      var httpClient = new HttpClient();
      using (Stream stream = await httpClient.GetStreamAsync(url))
      using (MemoryStream memStream = new MemoryStream())
      {
        await stream.CopyToAsync(memStream);
        memStream.Seek(0, SeekOrigin.Begin);
        SKBitmap webBitmap = SKBitmap.Decode(memStream);
        canvas.DrawBitmap(webBitmap, 0, 0, null);
        surface.Draw(canvas, 0, 0, null);
      }
      return surface;
    }
  }
}