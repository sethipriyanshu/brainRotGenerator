# Brain Rot Generator

Turn Reddit posts into short meme-style videos with AI voiceover, character overlays, and captions—all from a single Reddit URL.

---

## Screenshot


---

## What it does

1. **Paste a Reddit post URL** (e.g. from r/AmItheAsshole, r/confessions).
2. **Pick a character** (Trump, LeBron, Spongebob, or Griffin) for voice and on-screen images.
3. **Generate** — the app scrapes the post, turns the text into speech (Coqui xTTS), aligns words to audio (wav2vec2), then builds a video with a base clip + TTS audio + character images + **burned-in captions**.

Everything runs locally on your machine.

---

## Quick start

**One command (setup + start):**

```bash
./run.sh
```

Then open **http://127.0.0.1:5000** in your browser.

- First run: creates a virtualenv, installs dependencies, downloads NLTK data, then starts the server.
- Later runs: install/update deps and start the server.

**Manual setup (if you prefer):**

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('vader_lexicon')"
python server.py
```

**Requirements:** Python 3.9+, [FFmpeg](https://ffmpeg.org/) on your PATH. No GPU required (CPU is slower but works).

---

## Features

- **Web UI** — URL input, character selector, and video preview.
- **Four built-in characters** — Trump, LeBron, Spongebob, Griffin (voice + image set for each).
- **Captions** — Sentence-level captions burned into the video above the character overlay.
- **Custom assets** — Add your own character folders and `.mp3` voice samples under `assets/` and use them via the UI or by adding a new option in the app.

---

## How it works (high level)

| Step | What happens |
|------|----------------|
| **Scrape** | Fetches post title + body from Reddit’s public JSON API. |
| **TTS** | Coqui xTTS turns the text into speech (using the selected character’s voice sample). |
| **Forced alignment** | wav2vec2 aligns words to audio so we know when each word is spoken. |
| **Video** | FFmpeg muxes the base video (e.g. `assets/subway.mp4`) with the TTS audio. |
| **Overlay + captions** | MoviePy overlays character images per sentence and burns in captions. |

Output is written to `final/final.mp4`.

---

## Project structure

- `server.py` — Flask app and `/generate` endpoint.
- `main.py` — Pipeline: scrape → TTS → alignment → video → overlay + captions.
- `scraping.py` — Reddit JSON fetching.
- `audio.py` — Coqui TTS and audio conversion.
- `force_alignment.py` — wav2vec2 alignment and ASS timing.
- `video_generator.py` — FFmpeg video + audio mux.
- `image_overlay.py` — Character overlays and caption rendering.
- `run.sh` — One-command setup and start.

---

## Thanks

- [Motu Hira’s forced alignment tutorial](https://pytorch.org/audio/main/tutorials/forced_alignment_tutorial.html) (PyTorch/wav2vec2).
- [Coqui TTS](https://github.com/coqui-ai/TTS) for xTTS.

