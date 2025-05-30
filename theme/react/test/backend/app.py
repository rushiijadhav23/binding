from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_model import GeminiModel

app = Flask(__name__)
CORS(app)

model = GeminiModel()

@app.route('/enrich', methods=['POST'])
def enrich_product():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Missing input data"}), 400

        query = data.get("query", "")
        image = data.get("image", None)  # Expecting base64 image string

        metadata = model.generate_metadata(query=query, image_data=image)

        return jsonify({"metadata": metadata}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
