

import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/whatsapp-webhook", methods=["POST"])
def whatsapp_webhook():
    user_message = request.values.get("Body", "")
    sender_number = request.values.get("From", "")

    if not user_message:
        return jsonify({"status": "error", "message": "No message received"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are VyapaarAI, a billing assistant for Indian shopkeepers. Convert raw spoken text into a clean, itemized list with quantities. Format your response as a professional, easy-to-read WhatsApp text message with emojis."
                },
                {"role": "user", "content": f"Shopkeeper said: '{user_message}'"}
            ]
        )
        final_bill = response.choices[0].message.content
        print(f"Sending Bill to {sender_number}:\n{final_bill}")
        return f"<Response><Message>{final_bill}</Message></Response>", 200, {'Content-Type': 'text/xml'}
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Failed to process AI request"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
