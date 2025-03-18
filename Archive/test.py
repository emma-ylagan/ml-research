import os

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY environment variable is NOT set.")
else:
    print(f"OPENAI_API_KEY is set: {api_key[:5]}...{api_key[-5:]}")
