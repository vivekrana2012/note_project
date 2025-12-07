# Myro - YouTube Video Summarization Platform

A comprehensive full-stack application that automatically downloads YouTube videos, transcribes them, generates structured summaries using local LLMs, and presents them through a modern Angular web interface.

## 🎯 Overview

Myro automates the entire process of converting YouTube videos into structured, entity-based summaries with preserved numeric details. The system includes an RSS feed puller for automated processing, a Python backend with Prefect orchestration, and an Angular frontend for browsing summaries.

### Key Features

- **📺 RSS Feed Automation**: Automatically pulls new videos from YouTube channels
- **🎵 Audio Extraction**: Downloads audio from YouTube videos using `pytubefix`
- **🗣️ Speech-to-Text**: Transcribes audio using Faster Whisper (small model)
- **🤖 AI Summarization**: Uses Ollama (llama3.2:3b) to create entity-based summaries
- **🔢 Number Preservation**: Extracts and preserves ALL numeric information exactly as stated
- **🏢 Entity Organization**: Groups information by entities (companies, industries, regulatory bodies)
- **📝 Smart Formatting**: Cleans and structures summaries using additional LLM passes
- **🌐 Web Interface**: Modern Angular frontend to browse and view summaries
- **⚙️ Workflow Orchestration**: Managed by Prefect for reliable execution and monitoring
- **💾 Database Storage**: SQLite database for video metadata and tracking
- **🔄 Scheduled Execution**: Cron-based automation with caffeinate support

## 🏗️ Architecture

### System Overview

```
RSS Feed → Prefect Pipeline → Database → FastAPI → Angular Frontend
                ↓
        [Audio → Transcript → Summary → Formatted JSON]
```

### Pipeline Components

```
1. RSS Puller (rss_puller.py)
   ↓ Fetches latest videos from YouTube channels
   
2. Download Audio (yt_to_audio.py)
   ↓ Extracts audio + metadata, stores in DB
   
3. Transcription (audio_to_text.py)
   ↓ Converts speech to text using Whisper
   
4. Summarization (summarizer.py)
   ↓ Generates entity-based summaries with chunking
   
5. Formatting (summary_formatter.py)
   ↓ Cleans and structures summary using LLM
   
6. FastAPI Backend (api.py)
   ↓ Serves summaries and metadata
   
7. Angular Frontend
   ↓ Displays summaries in modern UI
```

## 📋 Prerequisites

### Backend
- Python 3.8+
- Ollama installed locally with `llama3.2:3b` model
- Prefect server (optional, for UI monitoring)
- SQLite3

### Frontend
- Node.js 18+
- Angular CLI 17+

### System
- macOS (for caffeinate support in cron)

## 🚀 Installation

### 1. Backend Setup

```bash
# Clone the repository
git clone <repository-url>
cd note_project

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python init.py
```

### 2. Install & Configure Ollama

```bash
# macOS
brew install ollama

# Start Ollama
ollama serve

# Pull required model
ollama pull llama3.2:3b
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on http://localhost:4200

### 4. Start Backend API

```bash
# From project root
uvicorn api:app --reload
```

API will run on http://localhost:8000

## 📦 Project Structure

```
note_project/
├── Backend (Python)
│   ├── pipeline.py              # Main Prefect flow orchestration
│   ├── yt_to_audio.py          # YouTube audio download + DB storage
│   ├── audio_to_text.py        # Whisper transcription
│   ├── summarizer.py           # LLM-based summarization with chunking
│   ├── summary_formatter.py    # LLM-based summary cleaning
│   ├── rss_puller.py           # RSS feed fetcher
│   ├── api.py                  # FastAPI backend
│   ├── utils.py                # Helper functions
│   ├── prompts.py              # LLM prompts storage
│   ├── init.py                 # Database initialization
│   ├── init.sql                # Database schema
│   ├── startup_script.py       # Cron job entry point
│   ├── setup_cron.sh           # Cron setup helper
│   ├── batch_format_summaries.py  # Batch formatting utility
│   ├── delete_youtube_video.py    # Video deletion utility
│   └── view_youtube_db.py         # Database viewer
│
├── Frontend (Angular)
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.*        # Root component with header
│   │   │   ├── app.routes.ts         # Routing configuration
│   │   │   ├── video.service.ts      # API service
│   │   │   ├── video-list/           # Video grid page
│   │   │   └── video-summary/        # Summary detail page
│   │   ├── assets/                   # Static assets (logo)
│   │   ├── index.html
│   │   ├── main.ts
│   │   ├── styles.css
│   │   └── proxy.conf.json          # API proxy config
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── resources/                   # Generated files & database
│   ├── youtube.db              # SQLite database
│   └── {video_id}/            # Per-video directories
│       ├── audio__{video_id}.*
│       ├── metadata__{video_id}.txt
│       ├── transcript__{video_id}.txt
│       ├── chunk_summaries__{video_id}.txt
│       ├── final_summary__{video_id}.txt
│       └── formatted_summary__{video_id}.json
│
├── logs/                       # Cron job logs
├── requirements.txt
├── prefect.yaml
├── .gitignore
└── README.md
```

## 🎮 Usage

### Manual Pipeline Execution

```python
from pipeline import yt_pipeline

# Process a single video
result = yt_pipeline(url="https://www.youtube.com/watch?v=VIDEO_ID")
```

### RSS Feed Processing

```python
from rss_puller import pull

# Process all videos from configured channels
pull()
```

### Scheduled Automation

#### 1. Configure Cron Schedule

```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

This will display the cron command. The default schedule is:
- **12:00 PM IST daily** (6:30 AM UTC)
- Uses `caffeinate -dims` to prevent system sleep

#### 2. Add to Crontab

```bash
crontab -e

# Add the line shown by setup_cron.sh
30 6 * * * cd /path/to/project && /usr/bin/caffeinate -dims python startup_script.py >> logs/cron.log 2>&1
```

### Using Prefect (Optional)

#### 1. Start Prefect Server

```bash
prefect server start
```

Access UI at: http://127.0.0.1:4200

#### 2. Configure & Deploy

```bash
export PREFECT_API_URL=http://127.0.0.1:4200/api
prefect work-pool create yt-pipeline --type process
prefect worker start --pool "yt-pipeline"
prefect deploy
```

#### 3. Run Deployment

```bash
prefect deployment run 'YouTube Video to Summary Pipeline/yt_pipeline_deploy' \
  --params '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### Database Management

#### View All Videos

```bash
python view_youtube_db.py
```

#### Delete Specific Video

```bash
python delete_youtube_video.py VIDEO_ID
```

#### Delete All Videos

```bash
python delete_youtube_video.py --all
```

#### Batch Format Summaries

```bash
python batch_format_summaries.py
```

Processes all `final_summary__*.txt` files and generates formatted JSON output.

## 🌐 Web Interface

### Video List Page (`/`)

- Grid layout with 3 columns (4:3 aspect ratio cards)
- Video thumbnails with titles and publish dates
- Click card to view summary
- Click thumbnail to open YouTube video

### Summary Page (`/video/:id`)

- Sticky title that remains visible while scrolling
- Entity-based summary sections
- Bullet-pointed facts with preserved numbers
- Click title to open YouTube video in new tab

### Navigation

- Clicking logo/name in header returns to home page
- Browser back button supported via Angular routing

## 📄 Database Schema

```sql
CREATE TABLE youtube (
    video_id      TEXT PRIMARY KEY,
    url           TEXT,
    title         TEXT,
    publish_date  TEXT,
    thumbnail     TEXT,
    keywords      TEXT,              -- JSON array as string
    timestamp     TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### RSS Channels

Edit `rss_puller.py`:

```python
channel_ids = [
    "UCXbKJML9pVclFHLFzpvBgWw",  # Markets by Zerodha
    "ANOTHER_CHANNEL_ID",         # Add more channels
]
```

### LLM Model

Edit `summarizer.py` and `summary_formatter.py`:

```python
model = "llama3.2:3b"  # Change to any Ollama model
```

### Chunking Parameters

Edit `summarizer.py`:

```python
chunks = chunk_text(transcript, max_words=500, overlap_words=100)
```

### Whisper Model

Edit `audio_to_text.py`:

```python
model = WhisperModel("small")  # Options: tiny, base, small, medium, large
```

### Cron Schedule

Edit `setup_cron.sh`:

```bash
CRON_SCHEDULE="30 6 * * *"  # Change time (currently 12 PM IST)
```

## 🤖 AI Prompts

All LLM prompts are centralized in `prompts.py`:

- `CHUNK_SUMMARIZE_PROMPT`: Initial chunk summarization
- `MERGE_SUMMARIES_PROMPT`: Merging chunk summaries
- `ENTITY_NAME_CLEANER`: Cleaning entity names
- `SUMMARY_POINT_CLEANER`: Cleaning summary bullet points

## 📊 API Endpoints

### GET `/videos`

Returns list of videos with available summaries.

**Response:**
```json
[
  {
    "video_id": "abc123",
    "url": "https://youtube.com/watch?v=abc123",
    "title": "Video Title",
    "publish_date": "2024-01-15",
    "thumbnail": "https://...",
    "keywords": "[\"keyword1\", \"keyword2\"]",
    "timestamp": "2024-01-15T10:30:00",
    "file": "formatted_summary__abc123.json",
    "path": "abc123/formatted_summary__abc123.json"
  }
]
```

### GET `/videos/{video_id}`

Returns formatted summary for specific video.

**Response:**
```json
[
  {
    "entity": "Company Name",
    "summary": [
      "Fact 1 with numbers",
      "Fact 2 with numbers"
    ]
  }
]
```

## 🎨 Frontend Styling

### Color Scheme

- Primary: `#3498db` (blue)
- Text: `#2c3e50` (dark gray)
- Secondary Text: `#7f8c8d` (light gray)
- Error: `#e74c3c` (red)
- Background: `#f5f5f5` (light gray)

### Responsive Breakpoints

- Desktop: 3 columns (default)
- Tablet (<1024px): 2 columns
- Mobile (<768px): 2 columns
- Small Mobile (<480px): 1 column

## 🔍 Output Format Example

### Formatted Summary JSON

```json
[
  {
    "entity": "Ola Electric",
    "summary": [
      "Sold 52,666 vehicles in Q3 2024",
      "Recorded first positive EBITDA of 0.3%",
      "Secured PLI certification through 2028",
      "Filed PLI claim of Rs 380 crore for FY25"
    ]
  },
  {
    "entity": "India's Electric Two-Wheeler Industry",
    "summary": [
      "Became world's second-largest EV market in 2025",
      "Crossed 8% penetration rate",
      "Recorded 1.44 lakh e-scooter sales in October 2024"
    ]
  }
]
```

## ⚡ Performance

### Processing Times (30-minute video)

- Audio download: 10-30 seconds
- Transcription: 3-5 minutes
- Chunk summarization: 2-4 minutes per chunk
- Summary formatting: 1-2 minutes
- **Total: ~25-45 minutes**

### Resource Usage

- RAM: 4-8GB during transcription
- CPU: High during transcription and summarization
- Disk: ~5-10MB per minute of audio
- Database: Minimal (<1MB for metadata)

## 🐛 Troubleshooting

### Backend Issues

**Ollama connection failed**
```bash
ollama serve
ollama list
```

**Database not found**
```bash
python init.py
```

**Video already exists error**
```bash
# Delete and reprocess
python delete_youtube_video.py VIDEO_ID
```

### Frontend Issues

**Assets not loading (404 errors)**
```bash
# Ensure assets are in src/assets/
# Rebuild Angular app
cd frontend
ng serve
```

**API calls failing**
```bash
# Check proxy configuration
cat frontend/src/proxy.conf.json

# Ensure backend is running
uvicorn api:app --reload
```

**Routing not working**
```bash
# Check RouterModule imports in app.component.ts
# Ensure routes are defined in app.routes.ts
```

## 🔐 Privacy & Security

- All AI processing happens locally via Ollama
- No data sent to external APIs (except YouTube downloads)
- Database stored locally in `resources/youtube.db`
- Respect YouTube's Terms of Service
- For personal/research use only

## 🛠️ Future Enhancements

- [ ] GPU acceleration for Whisper
- [ ] Support for more video platforms
- [ ] Search functionality in frontend
- [ ] Tags and categories
- [ ] Export summaries to PDF/Markdown
- [ ] Integration with note-taking apps
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Timeline visualization

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

- **Faster Whisper**: Optimized Whisper implementation
- **Ollama**: Local LLM runtime
- **Prefect**: Workflow orchestration
- **PyTubeFix**: Reliable YouTube downloading
- **FastAPI**: Modern Python web framework
- **Angular**: Frontend framework

## 📧 Contact

vivekrana.2012@gmail.com

---

**Built with ❤️ using local AI - No cloud dependencies**
