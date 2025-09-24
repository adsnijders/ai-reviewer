import os
import openai
import sys

# Retrieve the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Check if the key is set
if not api_key:
    print("❌ OPENAI_API_KEY not set.")
    sys.exit(1)

# Set the key
openai.api_key = api_key

try:
    # Simple test: list models (does not cost much)
    models = openai.Model.list()
    print(f"✅ OpenAI API key is valid! Found {len(models.data)} models.")
except Exception as e:
    print(f"❌ OpenAI API key validation failed: {e}")
    sys.exit(1)
