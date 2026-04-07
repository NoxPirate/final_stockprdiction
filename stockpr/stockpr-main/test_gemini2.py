import os
from google import genai

api_key = os.environ.get('GOOGLE_API_KEY')

SYSTEM_INSTRUCTION = "You are Pulse."

try:
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.5-flash", config=dict(system_instruction=SYSTEM_INSTRUCTION))
    res = chat.send_message("hii")
    print("SUCCESS")
    print(res.text)
except Exception as e:
    import traceback
    traceback.print_exc()
