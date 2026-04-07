import os
import google.generativeai as genai

api_key = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

SYSTEM_INSTRUCTION = "You are Pulse."

try:
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_INSTRUCTION)
    chat = model.start_chat(history=[])
    res = chat.send_message("hii")
    print("SUCCESS")
    print(res.text)
except Exception as e:
    import traceback
    traceback.print_exc()
