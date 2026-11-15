# Speakee Feature Tour Video

A 2D animated feature-tour video for [Speakee](https://speakee.tnxbd.top/) built with [HyperFrames](https://hyperframes.heygen.com).

## Project Overview

- **Duration:** ~5 minutes (299.4s)
- **Resolution:** 1920×1080 @ 30fps
- **Language:** Bengali narration with on-screen Bengali/English text
- **Narrator:** Bengali "News Reader" voice (sonic-3.5, 1.08× speed)
- **Music:** CC0 Freesound "New theme 6" looped

## Features Covered

1. **Voice Library** — 874 voices, 42 languages
2. **Models** — sonic-3.6, sonic-3.5 (default), sonic-preview, sonic-3
3. **Studio Controls** — Speed (0.6–1.5×), Volume (0.5–2.0×), 58 emotions
4. **Smart Chunking** — Auto-split long text, merge to single MP3/WAV
5. **Recent Generations** — Local history, select & merge, playback speed
6. **Developer API** — JSON POST /api/tts, no API key needed
7. **TAS Skill** — Text⇄Speech CLI (TTS + STT, SRT/VTT, word timestamps)
8. **Use Cases** — Content, education, accessibility, dev tools

## Local Development

```bash
# Install dependencies
npm ci

# Preview in browser (foreground)
npm run dev

# Or background preview for agent use
npx hyperframes preview --background

# Lint + check
npm run check

# Snapshot key frames
npx hyperframes snapshot --at 10,50,100,150,200,250,299

# Render to MP4
npm run render -- --quality looks -o speakee-feature-tour.mp4
```

## GitHub Actions Rendering

This project includes a workflow (`.github/workflows/render.yml`) that renders the video on GitHub's runners:

1. **Trigger manually** from the Actions tab
2. **Choose quality**: `looks` (default), `fast`, or `lossless`
3. **Download artifact** from the workflow run summary

The workflow installs Chrome, ffmpeg, Bengali fonts, and HyperFrames, then renders the full 5-minute video (~50-60 minutes on GitHub runners).

## Project Structure

```
├── index.html                    # Root composition
├── compositions/                 # Sub-compositions
├── src/
│   ├── base.css                  # Shared styles
│   └── scenes/                   # 23 scene sources
├── build/
│   ├── build_scenes.py           # Builds index.html + compositions
│   ├── timing.json               # Absolute timings
│   ├── lines.json                # Narration/demo text
│   └── timeline_spec.json        # Scene order & gaps
├── assets/
│   ├── audio/                    # Voiceover + demo clips
│   ├── img/                      # Site screenshots + QR
│   └── subs/                     # SRT/VTT/JSON transcripts
├── .github/workflows/render.yml  # CI render workflow
└── hyperframes.json              # Project config
```

## Credits

- **Speakee API:** https://speakee.tnxbd.top/
- **HyperFrames:** https://hyperframes.heygen.com
- **TAS Skill:** Text & Speech CLI for OpenCode
- **Voices:** Cartesia Sonic models (sonic-3.6, 3.5, preview, 3)
- **Music:** "New theme 6" by Freesound user (CC0)

## License

MIT — Video content © 2026 Speakee. HyperFrames compositions are editable source.