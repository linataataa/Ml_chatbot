import requests
from flask import Flask, jsonify
import threading
import time
from flask import Flask, request, jsonify
from llama_cpp import Llama
from py_eureka_client.eureka_client import EurekaClient 

app = Flask(__name__)

EUREKA_SERVER = "http://localhost:8761/eureka/"
SERVICE_NAME = "flask-app"
SERVICE_PORT = 5000
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

# Initialize Model
print("Initializing model...")
model = Llama.from_pretrained(
    repo_id="Joussef/unsloth-llama-3-q4_k_m",
    filename="unsloth.Q4_K_M.gguf",
    n_gpu_layers=0
)

print("Model initialized.")


@app.route('/ft/generate', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required."}), 400

        prompt = data["prompt"]
        response_text = model.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )['choices'][0]['message']['content']

        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the registration in a separate thread
    threading.Thread(target=register_with_eureka).start()
    # Start the Flask app
    app.run(port=SERVICE_PORT)