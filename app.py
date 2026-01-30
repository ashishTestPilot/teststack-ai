import os
import pandas as pd
from slack_bolt import App as SlackApp
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from openai import OpenAI

# ---------------- SLACK BOLT APP ----------------
bolt_app = SlackApp(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

handler = SlackRequestHandler(bolt_app)

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ---------------- LOAD TEST CASE EXCEL ----------------
df = pd.read_excel("testcases.xlsx")

# ---------------- EVENT HANDLER (AI LOGIC) ----------------
@bolt_app.event("app_mention")
def handle_mention(event, say):
    user_query = event["text"]

    # Limit Excel context size
    context = df.head(50).to_string()

    system_prompt = """
You are TestStack AI, a QA assistant.

Rules:
1. If the question is about test cases, modules, test steps, IDs, or coverage — use the provided test case data.
2. If the question is general (concepts, explanations, how-to, tech knowledge) — answer normally using your knowledge.
3. Be clear, structured, and helpful.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Test Case Data:\n{context}\n\nUser Question: {user_query}"}
        ]
    )

    say(response.choices[0].message.content)

# ---------------- FLASK SERVER ----------------
app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
