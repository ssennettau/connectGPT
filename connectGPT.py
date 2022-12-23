import json
import openai
import boto3

client = boto3.client("secretsmanager")
openai.api_key = client.get_secret_value(SecretId="connectGPT/openAI")['SecretString']

def lambda_handler(event, context):
    # Passing the message to OpenAI
    query = openai.Completion.create(
        model="text-davinci-003",
        prompt=("The following is a casual conversation between two friends.\n\nFriend: " + event['inputTranscript'] + "\nAI: "),
        temperature=0.5,
        max_tokens=100,
        presence_penalty=0.6,
        stop=["Friend: ","AI: "]
    )
    content = query.choices[0].text
    
    # Printing the details for CloudWatch Logs
    print({
        "in": {
            "transcript": event['inputTranscript'],
            "confidence": event['transcriptions'][0]['transcriptionConfidence']
        },
        "out": {
            "message": content,
            "gptTokens": query.usage.total_tokens
        }
    })
    
    # Returning the object to be passed back to Lex
    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitIntent"
            },
            "intent": {
                "name": "CatchAll",
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": content
            }
        ]
    }