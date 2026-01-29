from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Slack verification step
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    return "OK", 200

if __name__ == "__main__":
    app.run(port=3000)
