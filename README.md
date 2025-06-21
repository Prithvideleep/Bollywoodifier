# 🎬 Bollywoodify Chrome Extension

Transform boring news articles into entertaining Bollywood-style songs and movie titles! This Chrome extension works with popular Indian news sites and uses AI to create magical Bollywood content.

## 🎯 What It Does

- **Detects** Indian news sites (TOI, Hindustan Times, NDTV, Indian Express, etc.)
- **Transforms** article headlines into Bollywood movie titles
- **Converts** article content into full Bollywood songs with verses and chorus
- **Beautiful UI** with gradients, animations, and Bollywood styling
- **Works offline** with fallback content if APIs are unavailable

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Your Free API Key
Choose **ONE** of these free options:

**Option A: Groq (Recommended)**
1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up/login and create a new API key
3. Copy the key

**Option B: Google Gemini**
1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign up/login and create an API key
3. Copy the key

### Step 2: Setup Backend
```bash
# Clone or create these files in a folder called 'bollywoodify-backend'
mkdir bollywoodify-backend
cd bollywoodify-backend

# Create the .env file with your API key
echo "GROQ_API_KEY=your_actual_api_key_here" > .env
# OR if using Gemini:
# echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The server will start on `http://localhost:5000` 🎉

### Step 3: Install Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the folder containing your extension files (manifest.json, content.js, etc.)
5. The extension should appear with a 🎬 icon

## 📁 File Structure
```
bollywoodify-backend/
├── app.py              # Flask API server
├── requirements.txt    # Python dependencies
├── .env               # Your API keys
└── README.md

bollywoodify-extension/
├── manifest.json      # Extension configuration
├── content.js         # Main extension logic
├── background.js      # Service worker
├── popup.html         # Extension popup UI
└── icons/            # Extension icons (optional)
```

## 🎮 How to Use

1. **Open any Indian news site** (Times of India, Hindustan Times, etc.)
2. **Visit an article page**
3. **Wait 2 seconds** - the extension auto-transforms the page!
4. **Or click the 🎬 extension icon** and hit "Transform This Article"

## 🎨 Features

### ✨ What You'll See
- **Original headline** → **Bollywood movie title**
- **Article content** → **Full Bollywood song** with:
  - Dramatic verses
  - Catchy chorus
  - Emotional bridges
  - Beautiful formatting with emojis and styling

### 🎭 Supported Sites
- Times of India (timesofindia.com)
- Hindustan Times (hindustantimes.com)
- NDTV (ndtv.com)
- Indian Express (indianexpress.com)
- India Times (indiatimes.com)

### 🛡️ Fallback System
- If APIs fail → Uses creative fallback content
- If site unsupported → Shows helpful message
- Always works, even offline!

## 🔧 Technical Details

### Backend (Flask API)
- **Endpoint**: `POST /bollywoodify`
- **Input**: `{"title": "...", "content": "..."}`
- **Output**: `{"movie_title": "...", "song": "..."}`
- **CORS enabled** for Chrome extension
- **Multiple AI providers** (Groq, Gemini)
- **Error handling** with fallbacks

### Frontend (Chrome Extension)
- **Manifest V3** compliant
- **Site-specific selectors** for content extraction
- **Beautiful styling** with CSS animations
- **Auto-transformation** + manual trigger
- **Local storage** for stats and settings

## 🚨 Troubleshooting

### Extension not working?
1. Check if you're on a supported news site
2. Open Developer Tools (F12) and check Console for errors
3. Ensure backend server is running on `http://localhost:5000`
4. Try clicking the extension icon and manually triggering

### Backend errors?
1. Check your API key in `.env` file
2. Test the endpoint: `curl http://localhost:5000/health`
3. Check server logs for detailed error messages

### API rate limits?
- Groq: 30 requests/minute (free tier)
- Gemini: 15 requests/minute (free tier)
- Extension includes rate limiting protection

## 🎬 Example Transformation

**Original**: "India's GDP Growth Reaches 7% in Q3"

**Becomes**:
- **Movie Title**: "The Golden Quarter: A Growth Story"
- **Song**:
```
🎵 Verse 1:
In the land of dreams and endless hope
Where numbers dance and spirits soar
Seven percent growth, our nation's pride
Through every challenge, we rise and stride!

🎵 Chorus:
Growth ki yeh kahani, dil mein basi hai
Hindustan ki shaan, sabko dikhaani hai
Rise up, rise up, let the world see
India's golden destiny! 🎵
```

## 🔮 Future Features (Easy to Add)

1. **More news sites** - Just add selectors to `siteSelectors`
2. **Language options** - Hindi/Tamil songs
3. **Fine-tuned models** - Backend is modular for custom AI
4. **Social sharing** - Share your Bollywood transformations
5. **Audio generation** - Text-to-speech for songs

## 📝 API Documentation

### POST /bollywoodify
Transform news into Bollywood content

**Request**:
```json
{
  "title": "Article headline here",
  "content": "Article content here..."
}
```

**Response**:
```json
{
  "movie_title": "Dramatic Bollywood Title",
  "song": "Verse 1:\n...\n\nChorus:\n...",
  "status": "success",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET /health
Check API status
```json
{
  "status": "healthy",
  "groq_configured": true,
  "gemini_configured": false,
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🎪 Demo Video Script

1. Open Times of India article
2. Show original boring headline and content
3. Extension auto-transforms in 2 seconds
4. Reveal beautiful Bollywood movie title
5. Scroll through formatted song with verses/chorus
6. Show popup interface and manual trigger
7. Test on different news sites

## 🚀 Deployment Options

### Local Development
```bash
python app.py  # Runs on localhost:5000
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t bollywoodify-api .
docker run -p 5000:5000 bollywoodify-api
```

### Cloud Deployment
- **Heroku**: Just push with Procfile
- **Railway**: Connect GitHub repo
- **Render**: Auto-deploy from Git
- **Vercel**: Serverless functions

## 🎊 Credits

Built with ❤️ for the hiring challenge using:
- **Flask** - Lightweight Python web framework
- **Groq API** - Fast LLM inference
- **Chrome Extensions API** - Browser integration
- **Bollywood Magic** - The secret ingredient! 🎬

---

**Ready to make news fun again? Let's Bollywoodify the world! 🎵✨**