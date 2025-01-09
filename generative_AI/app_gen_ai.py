from flask import Flask, request, jsonify
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
from py_eureka_client.eureka_client import EurekaClient 
import time
import requests
import threading

# Initialize Flask app
app = Flask(__name__)

# Set the device to CPU
device = torch.device("cpu")
print(f"Using device: {device}")

# Load the model and tokenizer
MODEL_NAME = "Mohammedbendahrass/threat-detection-gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
model.to(device)  # Move the model to CPU

######################################
EUREKA_SERVER = "http://localhost:8761/eureka/"
SERVICE_NAME = "generative_ai_app_flak"
SERVICE_PORT = 5001
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"


def register_with_eureka():
    """Registers the Flask app with Eureka."""
    registration_data = {
        "instance": {
            "instanceId": INSTANCE_ID,
            "hostName": "localhost",
            "app": SERVICE_NAME.upper(),
            "ipAddr": "127.0.0.1",
            "status": "UP",
            "port": {"$": SERVICE_PORT, "@enabled": "true"},
            "dataCenterInfo": {
                "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
                "name": "MyOwn"
            }
        }
    }

    while True:
        try:
            response = requests.post(
                f"{EUREKA_SERVER}apps/{SERVICE_NAME}",
                json=registration_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 204:
                print("Successfully registered with Eureka")
                break
            else:
                print(f"Failed to register with Eureka: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error registering with Eureka: {e}")
        time.sleep(5)  # Retry after 5 seconds




######################################


# Define the /td/detection endpoint
@app.route('/ai/detection', methods=['POST'])
def threat_detection():
    # Get the input prompt from the request
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "Please provide a 'prompt' in the request body"}), 400

    test_prompt = data['prompt']

    # Tokenize the input prompt
    inputs = tokenizer(test_prompt, return_tensors="pt").to(device)

    # Generate text
    max_length = len(inputs.input_ids[0]) + 512
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        num_beams=5,
        temperature=0.6,
        no_repeat_ngram_size=2,
        early_stopping=True
    )

    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Return the generated text as a JSON response
    return jsonify({"generated_text": generated_text})

# Run the Flask app
if __name__ == '__main__':
    threading.Thread(target=register_with_eureka).start()
    app.run(port=SERVICE_PORT)