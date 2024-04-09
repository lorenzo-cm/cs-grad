# app.py
import sys
sys.path.append('../')
from flask import Flask, request, jsonify
from dispatcher import *


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Extract parameters from the query string
    business_id = request.args.get('business_id')
    prompt = request.args.get('prompt')
    id = request.args.get('id')
    conversation_id = request.args.get('conversation_id')
    
    # Call the dispatcher function with the parameters
    response = dispatcher(business_id, prompt, id, conversation_id)
    
    # Return the JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3003)
