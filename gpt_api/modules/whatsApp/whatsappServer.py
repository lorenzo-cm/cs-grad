# import os
# import sys
# sys.path.append('../')
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import uvicorn

# from whatsApp.whatsappParser import *
# from flask import Flask, request, jsonify

# class WebhookServer:
#     def __init__(self, verify_token):
#         # self.app = Flask(__name__)
#         self.app = FastAPI()
#         self.verify_token = verify_token
#         # self.app.route('/webhook', methods=['POST', 'GET'])(self.webhook)
#         self.app.add_api_route("/webhook", self.verify_webhook, methods=["GET"])
#         self.app.add_api_route("/webhook", self.webhook, methods=["POST"])

#     async def verify_webhook(self, hub_mode: str, hub_verify_token: str, hub_challenge: str):
#         if hub_mode == 'subscribe' and hub_verify_token == self.verify_token:
#             return hub_challenge
#         else:
#             return 'Verification failed'

#     async def webhook(self, request: Request):
#         webhook_payload = await request.json()
#         print('Received webhook payload:', webhook_payload)
#         data = parse_webhook_payload(webhook_payload)

#         if data:
#             fromphone = data["phone_number_id"]
#             tophone = data['from_number']
#             message = data['message']
#             print('Received data[message]', message)
#             print('Received data[phone_number_id]', fromphone)
#             print('Received data[from_number]', tophone)
#             return JSONResponse(content={"message": message})

#         else:
#             return JSONResponse(content={}, status_code=404)       

#     def start(self, host='0.0.0.0', port=8080):
#         uvicorn.run(self.app, host=host, port=port)
#         # self.app.run(host=host, debug=True, port=port)
#         # return ""

#     # def verify_token(self, token):
#     #     return token == self.verify_token

#     # def webhook(self):
#     #     if request.method == 'GET':
#     #         token_valid = (request.args.get('hub.verify_token') == os.getenv('VERIFY_TOKEN'))

#     #         if request.args.get('hub.mode') == 'subscribe' and token_valid:
#     #             challenge = request.args.get('hub.challenge')
#     #             return challenge, 200
#     #         else:
#     #             return 'Verification failed', 403
#     #     elif request.method == 'POST':
#     #         webhook_payload = request.json # Get the JSON data from the POST request
#     #         print('Received webhook payload:', webhook_payload)  # Add this line to log the received JSON
#     #         data = parse_webhook_payload(webhook_payload)

        
#     #         if data:
#     #             fromphone = data["phone_number_id"]
#     #             tophone = data['from_number']
#     #             message = data['message']
#     #             print('Received data[message]',message)
#     #             print('Received data[phone_number_id]', fromphone)
#     #             print('Received data[from_number]', tophone)
#     #             # return jsonify(message), 200,  {'Content-Type': 'application/json'}
#     #             return message

#     #         else:
#     #             return '', 404        

# if __name__ == '__main__':
#     server = WebhookServer(verify_token=os.getenv('VERIFY_TOKEN'))
#     server.start()









import sys
import os
sys.path.append('..')
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from whatsApp.whatsappParser import parse_webhook_payload
import uvicorn


class WebhookServer:
    def __init__(self, verify_token):
        self.app = FastAPI()
        self.verify_token = verify_token

        self.app.add_api_route("/webhook", self.webhook, methods=["POST", "GET"])

    async def webhook(self, request: Request):
        if request.method == "GET":
            hub_mode = request.query_params.get("hub.mode")
            hub_verify_token = request.query_params.get("hub.verify_token")
            print("hub_verify_token", hub_verify_token)
            hub_challenge = request.query_params.get("hub.challenge")
            print("hub_challenge", hub_challenge)

            if hub_mode == "subscribe" and hub_verify_token == self.verify_token:
                print("Condições OK")
                response = Response(content=hub_challenge, status_code=200) #Chat para Caraca! Temnde incluir status code=200!
                return response
            else:
                raise HTTPException(status_code=403, detail="Verification failed")

        elif request.method == "POST":
            webhook_payload = await request.json()
            print('Received webhook payload:', webhook_payload)
            data = parse_webhook_payload(webhook_payload)

            if data:
                fromphone = data["phone_number_id"]
                tophone = data['from_number']
                message = data['message']
                print('Received data[message]', message)
                print('Received data[phone_number_id]', fromphone)
                print('Received data[from_number]', tophone)
                return JSONResponse(content={"message": message})

            else:
                return JSONResponse(content={}, status_code=404)       

    def start(self, host='0.0.0.0', port=8080):
        uvicorn.run(self.app, host=host, port=port)

# Create an instance of WebhookServer with your verify token
if __name__ == '__main__':
    verify_token = os.getenv('VERIFY_TOKEN')  # Replace with your actual verify token
    print("*****" + str(verify_token))
    server = WebhookServer(verify_token=verify_token)
    server.start()