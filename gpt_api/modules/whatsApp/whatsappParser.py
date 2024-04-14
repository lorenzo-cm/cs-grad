import os
import requests

def send_message(from_id, to, body):
    url = f'https://graph.facebook.com/v17.0/{from_id}/messages?access_token={os.getenv("WHATSAPP_TOKEN")}'

    print(url)
    try:
        response = requests.post(
           url,
           headers={'Content-Type': 'application/json'},
           json={'messaging_product': 'whatsapp',
               'to': to,
               'text': {
               'body': body
               },
          }
        )
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        print("Message sent successfully!")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the API request: {err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")



def parse_webhook_payload(body):
  # whatsapp sends payloads for various things, we just want to ignore
  # unless it's a message with text
  try:
    return {
      'phone_number_id':
      body['entry'][0]['changes'][0]['value']['metadata']['phone_number_id'],
      'from_number':
      body['entry'][0]['changes'][0]['value']['messages'][0]['from'],
      'message':
      body['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'],
      'timestamp':
       body['entry'][0]['changes'][0]['value']['messages'][0]['timestamp'],
       'waba':
      body['entry'][0]['id'],
    }
  except KeyError:
    return None