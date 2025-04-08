from flask import Flask, request, jsonify
from flask_cors import CORS

# initialize app and cors
app = Flask(__name__)
CORS(app)  

"""
Possible endpoints

- generate_readme(): 
    receives data and then returns the generated text
    creates the readme 

- health():
    check if the app is running 
"""

@app.route('/generate_readme', methods=["POST"])
def generate_read():
    data = request.get_json()
    # Here you would integrate your AI logic using the data from Node.js
    generated_text = "hello world"
    return jsonify({"message": generated_text})

@app.route('/health', methods=["GET"])
def health():
    return jsonify({"message": "App is running and health endpoint is good"})

if __name__ == "__main__":
    app.run(debug=True)
