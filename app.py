from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "YouTube Shorts Generator Backend is live!"

@app.route("/generate", methods=["POST"])
def generate():
    # Placeholder logic
    return jsonify({"message": "Video generation endpoint reached!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
