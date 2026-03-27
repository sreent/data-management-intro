# Voice Reference — Narrator

Reference audio used by the TTS pipeline to clone the narrator's voice.

## File

| File | Format | Description |
|------|--------|-------------|
| `narrator-ref-24k-mono.wav` | PCM 16-bit, 24 kHz, mono | Production-ready reference clip (~10 s, calm lecture style) |

## Reference Transcript

> Hi. Good morning. Today we begin a new topic. I will talk in a calm way. I will read line by line. You can take a note. Thank you.

## Naming

| Original name | Renamed to |
|---------------|------------|
| `New Recording 31_training_ready_24k_mono_v3.wav` | `narrator-ref-24k-mono.wav` |

## Usage

The production-ready clip (`narrator-ref-24k-mono.wav`) is consumed by the TTS production spec (`specs/production/tts/tts_production_spec.md`) and passed to **Qwen3-TTS** as the `ref_audio` argument for zero-shot voice cloning.
