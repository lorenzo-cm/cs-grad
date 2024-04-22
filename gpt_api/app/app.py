import sys
sys.path.append('../')
from flask import Flask, jsonify, request
from dispatcher import *

app = Flask(__name__)

@app.route('/upload/<user_id>', methods=['POST'])
def upload_file(user_id):
    # Retrieve file from the request
    file = request.files['file']
    if file:
        # Create a directory for the user if it doesn't exist
        user_directory = f"../data/pdf/{user_id}"
        os.makedirs(user_directory, exist_ok=True)

        # Save the file in the user's directory
        file.save(os.path.join(user_directory, file.filename))
        return 'File uploaded successfully', 200
    return 'No file found', 400


@app.route('/api/prompt=<prompt>+username=<username>', methods=['GET'])
def api_call(prompt, username):
    # Call the dispatcher function with the URL parameters
    response = dispatcher(prompt, username)
    
    # Return the JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3003)
