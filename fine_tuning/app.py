from flask import Flask, request, jsonify
from llama_cpp import Llama
from py_eureka_client.eureka_client import EurekaClient


# Initialize Flask App
app = Flask(__name__)

# Initialize Model
print("Initializing model...")
model = Llama.from_pretrained(
    repo_id="Joussef/unsloth-llama-3-q4_k_m",
    filename="unsloth.Q4_K_M.gguf",
    n_gpu_layers=0
)
print("Model initialized.")

eureka_client = EurekaClient(
     eureka_server="http://localhost:8761/eureka/apps",  
    app_name="flask-service",
    instance_port=5000,
    instance_ip="127.0.0.1"
)

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()
        if not data or "prompt" not in data:
            return jsonify({"error": "Prompt is required."}), 400

        prompt = data["prompt"]
        response_text = model.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )['choices'][0]['message']['content']

        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    eureka_client.start()
    app.run(host='0.0.0.0', port=5000)
