import json
import openai
import boto3

openai.api_key = boto3.client("secretsmanager").get_secret_value(SecretId="connectGPT/openAI")['SecretString']

def lambda_handler(event, context):
    query = openai.Completion.create(model="text-davinci-003",prompt=("The following is a casual conversation between two friends.\n\nFriend: " + event['inputTranscript'] + "\nAI: "),temperature=0.5,max_tokens=100,presence_penalty=0.6,stop=["Friend: ","AI: "])    
    print({"in": {"transcript": event['inputTranscript'],"confidence": event['transcriptions'][0]['transcriptionConfidence']},"out": {"message": (query.choices[0].text),"gptTokens": query.usage.total_tokens}})    
    return {"sessionState": {"dialogAction": {"type": "ElicitIntent"},"intent": {"name": "CatchAll","state": "Fulfilled"}},"messages": [{"contentType": "PlainText","content": (query.choices[0].text)}]}