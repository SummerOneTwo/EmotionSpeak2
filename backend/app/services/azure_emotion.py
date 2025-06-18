from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from app.core.config import settings

def analyze_emotion(text: str):
    client = TextAnalyticsClient(
        endpoint=settings.AZURE_TEXT_ANALYTICS_ENDPOINT,
        credential=AzureKeyCredential(settings.AZURE_TEXT_ANALYTICS_KEY)
    )
    response = client.analyze_sentiment([text])[0]
    return {
        "sentiment": response.sentiment,
        "confidence_scores": {
            "positive": response.confidence_scores.positive,
            "negative": response.confidence_scores.negative,
            "neutral": response.confidence_scores.neutral
        }
    } 