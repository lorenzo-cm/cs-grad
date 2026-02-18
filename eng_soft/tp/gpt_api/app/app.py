import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS

# Assuming your dispatcher import is correctly configured
from dispatcher import *

app = Flask(__name__)
CORS(app)  # Enable CORS on the app, with default options which allow all origins

CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:5173"},
    r"/upload/*": {"origins": "http://localhost:5173"}
})

@app.route('/upload/<user_id>', methods=['POST'])
def upload_file(user_id):
    file = request.files['file']
    if file:
        user_directory = f"../data/pdf/{user_id}"
        os.makedirs(user_directory, exist_ok=True)
        
        # Define the new filename using the user_id
        new_filename = f"{user_id}.pdf"
        
        # Save the file with the new filename
        file.save(os.path.join(user_directory, new_filename))
        
        # Path to the .parquet file to be deleted
        parquet_file_path = f"../data/embeddings/{user_id}.parquet"
        
        # Check if the .parquet file exists and then delete it
        if os.path.exists(parquet_file_path):
            os.remove(parquet_file_path)
            return 'File uploaded and old embedding deleted successfully', 200
        else:
            return 'File uploaded but no old embedding found to delete', 200
    return 'No file found', 400


@app.route('/api/prompt=<prompt>+username=<username>', methods=['GET'])
def api_call(prompt, username):
    response = dispatcher(prompt, username)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=3003)