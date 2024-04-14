import json
import httpx
import requests
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


# ChatWoot config
chatwoot_url = os.getenv('CHATWOOT_URL')
chatwoot_bot_token = os.getenv('CHATWOOT_BOT_TOKEN')


async def send_to_chatwoot(account, conversation, message):
    data = {
        'content': message
    }
    url = f"{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation}/messages"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}

    r = requests.post(url, json=data, headers=headers)
    
    print("dentro do send_to_chatwoot", r.json())

    return r.json()


def send_private_message_human_handoff(account, conversation, message):
    data = {
        'content': message,
        "message_type": "outgoing",
        'private': True
    }
    url = f"{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation}/messages"
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}

    try:
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            print("dentro do send_to_chatwoot", r.json())
            return r.json()
    except requests.RequestException as e:
        print(f"Error during API call: {e}")
        return None  # or handle the error in a way that makes sense for your application


def hand_over_human(account, conversation_id):
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print("&&&& ENTREI no hand_over_human &&&&")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    data = {
        "status": "open"
    }

    url = f"{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation_id}/toggle_status"

    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}
    
    r = requests.post(url, json=data, headers=headers)
    
    send_private_message_human_handoff(account, conversation_id, "Cliente quer conversar com humano")

    print("Handed to Human", r.json())

    return r.json()


def toggle_status(account, conversation_id, new_status):
    data = {
        "status": new_status
    }

    url = f"{chatwoot_url}/api/v1/accounts/{account}/conversations/{conversation_id}/toggle_status"

    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "api_access_token": f"{chatwoot_bot_token}"}

    r = requests.post(url, json=data, headers=headers)

    print(f"Changed status to {new_status}", r.json())

    return r.json()


# async def make_chatwoot_request(method, endpoint, data=None):
#     url = f"{chatwoot_url}/api/v1/{endpoint}"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "api_access_token": f"{chatwoot_bot_token}"
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.request(method, url, json=data, headers=headers)
#         response.raise_for_status()
#         return response.json()


async def make_chatwoot_request(method, endpoint, data=None):
    # Ensure method is uppercase
    method = method.upper()

    # Construct the URL
    url = f"{chatwoot_url}/api/v1/{endpoint}"

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api_access_token": f"{chatwoot_bot_token}"
    }

    try:
        # Make the asynchronous request
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()

    except httpx.RequestError as req_err:
        # Handle network-related errors
        error_message = f"Network error while making the request: {req_err}"
        print(error_message)
        raise

    except httpx.HTTPError as http_err:
        # Handle HTTP errors (4xx and 5xx status codes)
        error_message = f"HTTP error ({http_err.response.status_code}): {http_err}"
        print(error_message)
        raise

    except Exception as ex:
        # Handle other unexpected errors
        error_message = f"An unexpected error occurred: {ex}"
        print(error_message)
        raise
