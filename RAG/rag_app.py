from flask import Flask, request, jsonify
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function
from py_eureka_client.eureka_client import EurekaClient 
import threading
import time
from flask import request
import requests
app = Flask(__name__)

EUREKA_SERVER = "http://localhost:8761/eureka/"
SERVICE_NAME = "flask-RAG"
SERVICE_PORT = 5002
INSTANCE_ID = f"{SERVICE_NAME}:{SERVICE_PORT}"
CHROMA_PATH = "chroma"

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




PROMPT_TEMPLATE = """
You are a cybersecurity expert. Answer only questions related to the cybersecurity domain:

{context}

---

Answer the question based on the above context: {question}
"""

@app.route('/rag/generate', methods=['POST'])
def query_rag():
    
    data = request.json
    query_text = data.get('query_text')

    if not query_text:
        return jsonify({"error": "query_text is required"}), 400

    
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    
    results = db.similarity_search_with_score(query_text, k=5)

    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    
    model = Ollama(model="llama3.2:1b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = {
        "response": response_text,
        "sources": sources
    }

    return jsonify(formatted_response), 200

if __name__ == "__main__":

    threading.Thread(target=register_with_eureka).start()
    
    app.run(port=SERVICE_PORT)