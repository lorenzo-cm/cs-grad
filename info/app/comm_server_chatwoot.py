# from dotenv import load_dotenv
import sys
sys.path.append('..')
from whatsApp.chatwootUtils import *
from dispatcher import *
from whatsApp.whatsappParser import *
from datetime import datetime, timedelta
import asyncio
from fastapi import FastAPI, Request, Response


# Define the FastAPI application
app = FastAPI()

# Define a route for the webhook post
@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()

    message_type = data.get('message_type')
    status = data.get('conversation', {}).get('status')

    # Check if the incoming message type is 'incoming'
    if message_type == "incoming" and status == "pending":
        print("Received POST and acknowledged with 200")
        print('Received webhook payload:', data)
        asyncio.create_task(process_webhook_payload(data))
        return Response(content="Webhook acknowledged successfully", status_code=200)
    else:
        print("O message_type é:", message_type)
        print("O Status está como:", status)


async def process_webhook_payload(data):
    message_type = data.get('message_type')
    message = data.get('content')
    conversation_id = data.get('conversation', {}).get('id')
    contact = data.get('sender', {}).get('phone_number')
    site_id = data.get('account', {}).get('id')
    status = data.get('conversation', {}).get('status')

    #If it is first message, briefly change status so Human Agent can follow Iara's conversation
    count = data.get('conversation', {}).get('unread_count')

    if count == 1 and status == "pending":
        # Briefly Send to Human and back only to have a Human in ChatWoot following what Alia is answering
        # Perform the API call to change the status to 'open'
        print("Only one brief status change:", count)
        await make_chatwoot_request('POST', f"accounts/{site_id}/conversations/{conversation_id}/toggle_status", {"status": "open"})
        # Perform the API call to change the status back to 'pending'
        await make_chatwoot_request('POST', f"accounts/{site_id}/conversations/{conversation_id}/toggle_status", {"status": "pending"})

    for key, value in data.items():
        print(key, value)

    print('Received data[message]', message)
    print('Received site_id', site_id)
    print('Received conversation', conversation_id)
    print('Received data[from_number]', contact)
    print('Received message_type', message_type)
    print('Message STATUS', status)

    # Perform the necessary processing based on your logic
    result, docs = dispatcher(site_id, message, str(contact), conversation_id)
    print("%%%%%%%%RESULT$$$$$$$", result)

    # Perform the API call to change the status back to 'pending'
    # await make_chatwoot_request('POST', f"accounts/{site_id}/conversations/{conversation_id}/toggle_status", {"status": "pending"})

    print("Status is: ", status)
    # if status == "pending":
    await send_to_chatwoot(site_id, conversation_id, result)

# Entry point to start the application
if __name__ == '__main__':
    from uvicorn import run
    run(app, host='0.0.0.0', port=8080)
