from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration with your actual keys
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDw7pukbkHMBXQpDdM_n_TlC5tNy5dZqJM"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

def verify_api_keys():
    """Enhanced API verification with detailed diagnostics"""
    logger.info("\n" + "="*60)
    logger.info("API KEY VERIFICATION")
    logger.info("="*60)
    
    # Test Groq API key
    groq_status = False
    if GROQ_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            response = requests.get("https://api.groq.com/openai/v1/models", 
                                 headers=headers, 
                                 timeout=10)
            if response.status_code == 200:
                groq_status = True
                models = [m['id'] for m in response.json().get('data', [])]
                logger.info(f"✅ Groq API working. Available models: {models}")
            else:
                logger.error(f"❌ Groq API returned status {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"❌ Groq API test failed: {str(e)}")
    
    # Test Gemini API key with more detailed checks
    gemini_status = False
    if GEMINI_API_KEY:
        try:
            url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
            test_payload = {
                "contents": [{
                    "parts": [{
                        "text": "Hello"
                    }]
                }]
            }
            response = requests.post(url, json=test_payload, timeout=10)
            
            if response.status_code == 200:
                gemini_status = True
                logger.info("✅ Gemini API working")
            else:
                error_details = response.json().get('error', {}).get('message', 'Unknown error')
                logger.error(f"❌ Gemini API returned status {response.status_code}: {error_details}")
        except Exception as e:
            logger.error(f"❌ Gemini API test failed: {str(e)}")
    
    logger.info("="*60 + "\n")
    return groq_status, gemini_status

def create_bollywood_prompt(title, content):
    return f"""Transform this news article into a Bollywood musical:

ORIGINAL TITLE: {title}
CONTENT: {content[:1500]}...

Create:
1. A dramatic Bollywood movie title in English
2. A full song with verses and chorus telling this story

Requirements:
- Use typical Bollywood themes: drama, emotion, family
- Make it entertaining but keep the core message
- Include a catchy chorus
- Format with clear verse/chorus structure

Respond EXACTLY in this JSON format:
{{
    "movie_title": "Title Here",
    "song": "Verse 1:\\nLyrics...\\n\\nChorus:\\nLyrics...\\n\\nVerse 2:\\nLyrics..."
}}"""

def call_groq_api(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a Bollywood songwriter..."  # Keep your existing prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "llama3-70b-8192",  # Updated model
        "temperature": 0.7,
        "max_tokens": 1024,
        "response_format": {"type": "json_object"}
    }
    
    try:
        logger.info("Calling Groq API...")
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=30)
        
        logger.info(f"Groq API status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = response.json().get('error', {}).get('message', response.text)
            logger.error(f"Groq API error: {error_msg}")
            return None
            
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Enhanced JSON parsing
        try:
            if content.startswith('{'):
                parsed = json.loads(content)
            elif '```json' in content:
                json_part = content.split('```json')[1].split('```')[0]
                parsed = json.loads(json_part.strip())
            else:
                parsed = json.loads(content)
                
            # Validate response structure
            if not all(k in parsed for k in ['movie_title', 'song']):
                raise ValueError("Missing required fields in response")
                
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Groq response: {str(e)}")
            logger.debug(f"Raw response: {content}")
            return None
            
    except Exception as e:
        logger.error(f"Groq API request failed: {str(e)}")
        return None

def call_gemini_api(prompt):
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    
    data = {
        "contents": [{
            "parts": [{
                "text": f"{prompt}\n\nImportant: Respond STRICTLY with valid JSON in this exact format:\n{{\"movie_title\":\"...\",\"song\":\"...\"}}\nThe song must have verses and chorus."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        }
    }
    
    try:
        logger.info("Calling Gemini API...")
        response = requests.post(url, json=data, timeout=30)
        
        logger.info(f"Gemini API status: {response.status_code}")
        
        if response.status_code != 200:
            error_details = response.json().get('error', {}).get('message', response.text)
            logger.error(f"Gemini API error: {error_details}")
            return None
            
        result = response.json()
        content = result['candidates'][0]['content']['parts'][0]['text']
        
        # Enhanced JSON parsing with validation
        try:
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
                
            parsed = json.loads(content)
            
            if not all(k in parsed for k in ['movie_title', 'song']):
                raise ValueError("Missing required fields in response")
                
            return parsed
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse Gemini response: {str(e)}")
            logger.debug(f"Raw response: {content}")
            return None
            
    except Exception as e:
        logger.error(f"Gemini API request failed: {str(e)}")
        return None

def create_fallback_content(title, content):
    return {
        "movie_title": f"{title.split()[0]} - The Bollywood Story",
        "song": f"Verse 1:\nNews becomes song in Bollywood style\n{title[:50]}...\n\nChorus:\nDance and sing with all your might!\nBollywood magic day and night!"
    }

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "apis": {
            "groq": "active" if GROQ_API_KEY else "inactive",
            "gemini": "active" if GEMINI_API_KEY else "inactive"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/bollywoodify', methods=['POST'])
def bollywoodify():
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Missing title or content"}), 400
        
        title = data['title'].strip()
        content = data['content'].strip()
        
        logger.info(f"Processing: {title[:50]}...")
        prompt = create_bollywood_prompt(title, content)
        
        result = None
        source = None
        
        # Try Groq first
        if GROQ_API_KEY:
            result = call_groq_api(prompt)
            if result:
                source = "groq"
                logger.info("Successfully used Groq API")
        
        # Fallback to Gemini
        if not result and GEMINI_API_KEY:
            result = call_gemini_api(prompt)
            if result:
                source = "gemini"
                logger.info("Successfully used Gemini API")
        
        # Final fallback
        if not result:
            result = create_fallback_content(title, content)
            source = "fallback"
            logger.warning("Using fallback content")
        
        return jsonify({
            "movie_title": result.get('movie_title', 'Bollywood Story'),
            "song": result.get('song', 'Bollywood magic song...'),
            "source": source,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({
            "error": "Processing failed",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    groq_working, gemini_working = verify_api_keys()
    
    print("\n🎬 Bollywoodify API Server")
    print(f"🔑 Groq API: {'✅ Working' if groq_working else '❌ Not working'}")
    print(f"🔑 Gemini API: {'✅ Working' if gemini_working else '❌ Not working'}")
    print("🚀 Running on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)