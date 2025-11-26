# YouTube Video to Summary Pipeline

A comprehensive pipeline that downloads YouTube videos, transcribes them using Whisper, and generates structured summaries using local LLMs via Ollama. Built with Prefect for workflow orchestration.

## 🎯 Overview

This project automates the process of converting YouTube videos into structured, entity-based summaries with preserved numeric details. It's designed for extracting and organizing information from long-form content like podcasts, news shows, and educational videos.

### Key Features

- **Audio Extraction**: Downloads audio from YouTube videos using `pytubefix`
- **Speech-to-Text**: Transcribes audio using Faster Whisper (small model)
- **Intelligent Summarization**: Uses Ollama (llama3.2:3b) to create entity-based summaries
- **Number Preservation**: Extracts and preserves ALL numeric information exactly as stated
- **Entity Organization**: Groups information by entities (companies, industries, regulatory bodies)
- **Workflow Orchestration**: Managed by Prefect for reliable execution and monitoring
- **Chunking Strategy**: Processes large transcripts in overlapping chunks (500 words with 100-word overlap)

## 🏗️ Architecture

```
YouTube URL
    ↓
[yt_to_audio.py] → Downloads audio + metadata
    ↓
[audio_to_text.py] → Transcribes using Faster Whisper
    ↓
[summarizer.py] → Generates structured summary using Ollama
    ↓
Final Summary + Chunk Summaries
```

### Pipeline Flow

1. **Download Audio** (`yt_to_audio.py`)
   - Extracts audio stream from YouTube
   - Saves metadata (title, author, views, description, etc.)
   - Generates files: `audio_{video_id}.{ext}`, `metadata_{video_id}.txt`

2. **Transcription** (`audio_to_text.py`)
   - Uses Faster Whisper (small model)
   - Generates: `transcript_{video_id}.txt`

3. **Summarization** (`summarizer.py`)
   - Chunks transcript (500 words, 100-word overlap)
   - Summarizes each chunk preserving all numbers
   - Merges summaries into final entity-based structure
   - Generates: `chunk_summaries_{video_id}.txt`, `final_summary_{video_id}.txt`

## 📋 Prerequisites

- Python 3.8+
- Ollama installed locally with `llama3.2:3b` model
- Prefect server running (optional, for UI monitoring)

### Install Ollama

```bash
# macOS
brew install ollama

# Start Ollama
ollama serve

# Pull the model
ollama pull llama3.2:3b
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd note_project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify Ollama is running**
```bash
# Test Ollama connection
ollama list
```

## 📦 Project Structure

```
note_project/
├── pipeline.py              # Main Prefect flow orchestration
├── yt_to_audio.py          # YouTube audio download task
├── audio_to_text.py        # Whisper transcription task
├── summarizer.py           # LLM-based summarization task
├── utils.py                # Helper functions (videoId extraction)
├── prefect.yaml            # Prefect deployment configuration
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── notes.txt              # Prefect setup notes
└── testing/               # Sample outputs
    ├── transcript.txt
    ├── chunk_summaries.txt
    ├── final_summary.txt
    └── older_prompts.txt
```

## 🎮 Usage

### Option 1: Direct Python Execution

```python
from pipeline import yt_pipeline

# Run the pipeline
result = yt_pipeline(url="https://www.youtube.com/watch?v=VIDEO_ID")

print(f"Audio: {result['audio']}")
print(f"Transcript: {result['transcript']}")
print(f"Summary: {result['summary']}")
```

### Option 2: Using Prefect (Recommended)

#### 1. Start Prefect Server

```bash
prefect server start
```

Access UI at: http://127.0.0.1:4200

#### 2. Configure Prefect API

```bash
export PREFECT_API_URL=http://127.0.0.1:4200/api
```

#### 3. Create Worker Pool

Create a worker pool named `yt-pipeline` via the Prefect UI or CLI:

```bash
prefect work-pool create yt-pipeline --type process
```

#### 4. Start Worker

```bash
prefect worker start --pool "yt-pipeline"
```

#### 5. Deploy the Flow

```bash
prefect deploy
```

#### 6. Run the Pipeline

```bash
prefect deployment run 'YouTube Video to Summary Pipeline/yt_pipeline_deploy' \
  --params '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

Monitor execution in the Prefect UI at http://127.0.0.1:4200

## 📄 Output Files

For each processed video with ID `abc123`, the following files are generated:

| File | Description |
|------|-------------|
| `audio_abc123.mp3` | Downloaded audio file |
| `metadata_abc123.txt` | Video metadata (title, author, views, etc.) |
| `transcript_abc123.txt` | Full transcription |
| `chunk_summaries_abc123.txt` | Individual chunk summaries |
| `final_summary_abc123.txt` | Merged entity-based summary |

## 🧩 Core Components

### 1. Video ID Extraction (`utils.py`)

```python
def videoId(filepath):
    """Extracts video_id from '<scope>_<video_id>.<ext>' filenames."""
```

Utility function that extracts video IDs from generated filenames for consistent file naming.

### 2. Audio Download (`yt_to_audio.py`)

```python
@task
def download_audio(url):
    """Downloads audio and saves metadata from YouTube URL."""
```

- Uses `pytubefix` for robust YouTube downloading
- Extracts metadata (title, author, publish date, views, description, keywords)
- Returns path to downloaded audio file

### 3. Transcription (`audio_to_text.py`)

```python
@task
def transcript(filename):
    """Transcribes audio using Faster Whisper."""
```

- Uses `faster-whisper` with "small" model
- Optimized for speed vs accuracy balance
- Segments are written line-by-line

### 4. Summarization (`summarizer.py`)

The most complex component with three main functions:

#### a. Text Chunking with Overlap

```python
def chunk_text(text, max_words=500, overlap_words=100):
    """Splits text into overlapping chunks for context preservation."""
```

- Prevents loss of context at chunk boundaries
- Default: 500 words per chunk, 100-word overlap

#### b. Chunk Summarization

For each chunk:
- Identifies entities (companies, industries, regulatory bodies)
- Extracts all numeric information
- Structures output by entity with preserved numbers

#### c. Summary Merging

```python
def merge_all_chunk_summaries(model, chunk_summaries):
    """Iteratively merges chunk summaries into final summary."""
```

- Merges summaries pairwise
- Deduplicates entity information
- Preserves ALL numeric details

### Output Format

```markdown
### ENTITY NAME
- Bullet point summary describing facts for this entity.

-- Key Numbers --
- Bullet list of every number related to this entity, with context.
```

## ⚙️ Configuration

### Model Configuration

Edit `summarizer.py` to change the LLM model:

```python
model = "llama3.2:3b"  # Change to any Ollama model
```

Available alternatives:
- `llama3.2:1b` (faster, less accurate)
- `llama3.1:8b` (slower, more accurate)
- `mistral:7b`

### Chunking Configuration

Adjust chunk size in `summarizer.py`:

```python
chunks = chunk_text(transcript, max_words=500, overlap_words=100)
```

Larger chunks = more context but slower processing.

### Whisper Model Size

Change model in `audio_to_text.py`:

```python
model = WhisperModel("small")  # Options: tiny, base, small, medium, large
```

| Model | Speed | Accuracy | VRAM |
|-------|-------|----------|------|
| tiny | Very Fast | Lower | ~1GB |
| small | Fast | Good | ~2GB |
| medium | Moderate | Better | ~5GB |
| large | Slow | Best | ~10GB |

## 🔍 Example Output

### Input Video
"The Daily Brief" - Episode on India's EV market and QCOs

### Generated Summary Structure

```markdown
### Entity Name: Ola Electric
- Sold 52,666 vehicles in Q3 2024
- Recorded first positive EBITDA of 0.3%
- Secured PLI certification through 2028

-- Key Numbers --
- 52,666: Vehicles sold in Q3 2024
- 0.3%: Positive EBITDA margin
- Rs 380 crore: PLI claim filed for FY25
- Rs 3000 crore: Eligible FY25 sales

### Entity Name: India's Electric Two-Wheeler Industry
- Became world's second-largest EV market in 2025
- Crossed 8% penetration rate

-- Key Numbers --
- 2020: Year market barely existed
- 2025: Year became second-largest market
- 8%: EV penetration rate
- 1.44 lakh: E-scooter sales in October 2024
```

## 🐛 Troubleshooting

### Common Issues

**1. "Ollama connection refused"**
```bash
# Ensure Ollama is running
ollama serve

# Test connection
ollama list
```

**2. "Model not found"**
```bash
# Pull the required model
ollama pull llama3.2:3b
```

**3. "Out of memory during transcription"**
```python
# Use a smaller Whisper model
model = WhisperModel("tiny")  # or "base"
```

**4. "Prefect worker not picking up jobs"**
```bash
# Verify worker is running
prefect worker ls

# Check worker pool configuration
prefect work-pool inspect yt-pipeline

# Restart worker
prefect worker start --pool "yt-pipeline"
```

**5. "YouTube download fails"**
- Video may be age-restricted or private
- Check if `pytubefix` needs updating: `pip install --upgrade pytubefix`

## 📊 Performance Notes

### Processing Times (approximate)

For a 30-minute video:
- Audio download: 10-30 seconds
- Transcription (small model): 3-5 minutes
- Summarization (10 chunks): 2-4 minutes per chunk
- **Total: ~25-45 minutes**

### Resource Usage

- RAM: 4-8GB during transcription
- CPU: High during transcription and summarization
- Disk: ~5-10MB per minute of audio

## 🔐 Privacy & Ethics

- Downloads are for personal use only
- Respect YouTube's Terms of Service
- Do not redistribute copyrighted content
- Be mindful of creator rights

## 🛠️ Future Enhancements

Potential improvements:
- [ ] GPU acceleration for Whisper
- [ ] Custom entity type definitions
- [ ] Export to structured formats (JSON, CSV)
- [ ] Web UI for easier access
- [ ] Integration with note-taking apps (Notion, Obsidian)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better prompt engineering
- Alternative chunking strategies
- Output formatting options
- Error handling
- Testing suite

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

- **Faster Whisper**: OpenAI's Whisper optimized for speed
- **Ollama**: Local LLM runtime
- **Prefect**: Workflow orchestration
- **PyTubeFix**: Reliable YouTube downloading

## 📧 Contact

vivekrana.2012@gmail.com

---

**Note**: This pipeline runs entirely locally and does not send data to external APIs (except for YouTube downloads). All AI processing happens on your machine via Ollama.
