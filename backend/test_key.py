import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the .env file
load_dotenv()
print("Attempting to load API key from .env file...")

try:
    # Initialize the client (this will fail if the key is wrong)
    client = OpenAI()
    print("API key loaded successfully.")

    # Make a very simple API call
    print("Making a test API call...")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
      ]
    )
    print("API call successful!")
    print("Response:", completion.choices[0].message.content)

except Exception as e:
    print("\n--- AN ERROR OCCURRED ---")
    print(f"Error: {e}")
    print("\nTroubleshooting:")
    print("1. Is your .env file named correctly and in the same folder?")
    print("2. Is the variable name OPENAI_API_KEY?")
    print("3. Is the key itself valid and do you have credits on your OpenAI account?")