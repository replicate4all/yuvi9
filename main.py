from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
gpt = [{"code": 6, "model": "gpt-3.5-turbo"}]

@app.route("/api", methods=["GET"])
def api():
    try:
        prompt = request.args.get("prompt")
        if not prompt:
            return jsonify({
                "status_code": 400,
                "message": "missing_prompt",
                "author": "aliestercrowly.com"
            }), 400

        selected_model = gpt[0]

        response = requests.post(
            'https://us-central1-aiseo-official.cloudfunctions.net/newApiFree',
            json={"type": "chatOpenAI", "data": {"prompt": prompt, "system": selected_model["model"]}, "cost": 0}
        )

        if response.status_code == 200 and response.json().get("success") and response.json().get("data"):
            return jsonify({
                "status_code": 200,  # Change the code to 500 for server error
                "message": response.json()["data"],
                "author": "aliestercrowly.com"
            }), 200

        return jsonify({
            "status_code": 500,  # Change the code to 500 for server error
            "message": "unexpected_error",
            "author": "aliestercrowly.com"
        }), 500

    except Exception as e:
        return jsonify({
            "status_code": 500,  # Change the code to 500 for server error
            "message": "unexpected_error",
            "author": "aliestercrowly.com"
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
