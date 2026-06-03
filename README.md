# elabs / CosyVoice 2 TTS

[![Run on RunPod](https://runpod.io/badge/runpod-hub)](https://runpod.io/console/hub)

Next-generation **text-to-speech** with natural prosody and voice cloning capabilities. Supports multi-speaker synthesis, emotion control, and voice cloning from short audio samples.

## Highlights

- **Natural prosody** — next-gen TTS with human-like intonation and rhythm
- **Voice cloning** — clone any voice from a short audio sample (~5 seconds)
- **Emotion control** — select from neutral, happy, sad, angry, surprise, fearful emotions
- **Multi-speaker** — built-in speaker presets plus custom voice cloning
- **High quality** — 24kHz output with natural pauses and emphasis

## API

### Input
```json
{
  "input": {
    "text": "Welcome to CosyVoice 2, the next generation of text-to-speech synthesis.",
    "voice": "default",
    "emotion": "neutral",
    "reference_audio": null
  }
}
```

### Output
```json
{
  "audio_base64": "<base64 WAV>",
  "text": "Welcome to CosyVoice 2, the next generation of text-to-speech synthesis.",
  "voice": "default",
  "wall_time_s": 1.2
}
```

### Parameters
| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | string | **required** | Input text to synthesize |
| `voice` | string | `"default"` | Speaker/voice ID or `"clone"` for voice cloning |
| `emotion` | string | `"neutral"` | Emotion style (`neutral`, `happy`, `sad`, `angry`, `surprise`, `fearful`) |
| `reference_audio` | string | `null` | URL to reference audio for voice cloning (used when `voice="clone"`) |

## GPU Requirements
- **Recommended**: RTX 4090 / RTX 6000 Ada / L40S / A5000+
- **Minimum**: Any GPU with ≥8GB VRAM
- **CUDA**: 12.0+

## Benchmark
| GPU | Text Length | Time |
|---|---|---|
| RTX 4090 | Short (30 chars) | ~0.5s |
| RTX 4090 | Medium (200 chars) | ~1.2s |
| RTX 4090 | Long (1000 chars) | ~3.5s |
| L40S | Medium (200 chars) | ~1.0s |

## License
Apache-2.0
