"""
Quick test script to verify Perplexity API key
Run this to check if your API key is valid
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_BASE_URL = 'https://api.perplexity.ai/chat/completions'

print("=" * 50)
print("PERPLEXITY API KEY TEST")
print("=" * 50)

if not PERPLEXITY_API_KEY or PERPLEXITY_API_KEY == 'your_perplexity_api_key_here':
    print("❌ ERROR: No valid API key found in .env file")
    print("\n📝 To fix:")
    print("1. Get API key from: https://www.perplexity.ai/settings/api")
    print("2. Update .env file: PERPLEXITY_API_KEY=your_actual_key")
    exit(1)

print(f"✓ API Key found: {PERPLEXITY_API_KEY[:10]}...{PERPLEXITY_API_KEY[-5:]}")
print("\n🔄 Testing API connection...")

headers = {
    'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
    'Content-Type': 'application/json'
}

data = {
    'model': 'sonar',
    'messages': [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Say "API test successful!" if you can read this.'}
    ],
    'max_tokens': 50
}

try:
    response = requests.post(PERPLEXITY_BASE_URL, headers=headers, json=data, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        print(f"\n✅ SUCCESS! API is working correctly!")
        print(f"Response: {ai_response}")
    elif response.status_code == 401:
        print(f"\n❌ ERROR: Invalid API key (401 Unauthorized)")
        print("Your API key is not valid or has expired.")
        print("\n📝 To fix:")
        print("1. Go to: https://www.perplexity.ai/settings/api")
        print("2. Generate a new API key")
        print("3. Update .env file with new key")
    else:
        print(f"\n❌ ERROR: API returned status code {response.status_code}")
        print(f"Response: {response.text[:300]}")
        
except requests.exceptions.Timeout:
    print("\n⏱️ ERROR: Request timeout - API took too long to respond")
except requests.exceptions.ConnectionError:
    print("\n🔌 ERROR: Connection error - Check your internet connection")
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")

print("\n" + "=" * 50)
