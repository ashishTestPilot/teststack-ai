import os
import pandas as pd
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from openai import OpenAI

# Slack credentials from environment
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

handler = SlackRequestHandler(app)

# OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load Excel file
df = pd.read_excel("testcases.xlsx")

@app.event("app_mention")
def handle_mention(event, say):
    user_query = event["text"]

    # Filter example (improve later)
    context = df.head(50).to_string()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a QA assistant using test case data."},
            {"role": "user", "content": f"{context}\n\nQuestion: {user_query}"}
        ]
    )

    say(response.choices[0].message.content)

# Flask server
app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
if __name__ == "__main__":
    flask_app.run(port=3000)
