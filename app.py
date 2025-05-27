from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# 💥 This is key: allow ANY route and any method from your Netlify domain
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return "YouTube Shorts Generator Backend is live!"

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        # Handle CORS preflight manually
        response = jsonify({'message': 'CORS preflight OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

    # Main POST logic
    response = jsonify({"message": "Video generation endpoint reached!"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
