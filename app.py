import os
from flask import Flask, request, jsonify
from ChatGPT import ChatGPTbotapi

# Flask application
app = Flask(__name__)

def initialize_bot_api():
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key not provided in environment variable")
    try:
        return ChatGPTbotapi(openai_api_key)
    except Exception as e:
        raise RuntimeError("Failed to initialize ChatGPTbotapi instance: " + str(e))

bot_api = None  # Global variable to store the ChatGPTbotapi instance

@app.route('/initialize', methods=['GET'])
def initialize():
    global bot_api
    try:
        bot_api = initialize_bot_api()
        return jsonify({"message": "OpenAI API initialized"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to initialize OpenAI API", "error": str(e)}), 500


@app.route('/create_prompt', methods=['POST'])
def create_prompt():
    try:
        if not bot_api:
            raise RuntimeError("OpenAI API not initialized")
        prompt = request.json.get('prompt')
        if not prompt:
            raise ValueError("Invalid JSON input: 'prompt' field is missing")
        prompt_id = bot_api.create_prompt(prompt)
        return jsonify({"message": "Prompt created", "prompt_id": prompt_id}), 201
    except Exception as e:
        return jsonify({"message": "Error creating prompt", "error": str(e)}), 500


@app.route('/get_response/<int:prompt_id>', methods=['GET'])
def get_response(prompt_id):
    try:
        if not bot_api:
            raise RuntimeError("OpenAI API not initialized")
        response = bot_api.get_response(prompt_id)
        if response is not None:
            return jsonify({"message": "Response fetched", "response": response}), 200
        else:
            return jsonify({"message": "Invalid prompt ID"}), 400
    except Exception as e:
        return jsonify({"message": "Error fetching response", "error": str(e)}), 500


@app.route('/update_prompt/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    try:
        if not bot_api:
            raise RuntimeError("OpenAI API not initialized")
        new_prompt = request.json.get('prompt')
        if not new_prompt:
            raise ValueError("Invalid JSON input: 'prompt' field is missing")
        bot_api.update_prompt(prompt_id, new_prompt)
        return jsonify({"message": "Prompt updated"}), 200
    except Exception as e:
        return jsonify({"message": "Error updating prompt", "error": str(e)}), 500


@app.route('/delete_prompt/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    try:
        if not bot_api:
            raise RuntimeError("OpenAI API not initialized")
        if bot_api.delete_prompt(prompt_id):
            return jsonify({"message": "Prompt deleted"}), 200
        else:
            return jsonify({"message": "Invalid prompt ID"}), 400
    except Exception as e:
        return jsonify({"message": "Error deleting prompt", "error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
