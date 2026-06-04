# elabs / CosyVoice 2 TTS

[![Deploy on RunPod](https://img.shields.io/badge/RunPod-Deploy-orange?logo=runpod)](https://console.runpod.io/hub)
[![CUDA 12.4](https://img.shields.io/badge/CUDA-12.4-green)](https://developer.nvidia.com/cuda-toolkit)
[![Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://opensource.org/licenses/Apache-2.0)

**Next-generation TTS with zero-shot voice cloning** using CosyVoice 2. Clone any voice from a 3-10 second reference audio sample. Natural prosody, emotion control, multi-language support.

![CosyVoice 2](https://pub-796a08821c1c483aaf5e274e0d03e350.r2.dev/hub-icons/cosyvoice.svg)

## Highlights

- Zero-shot voice cloning -- clone any voice from 3-10s audio
- Natural prosody -- human-like rhythm and intonation
- Emotion control -- neutral, happy, sad, angry, surprised
- Multi-speaker -- multiple built-in voices included
- Apache-2.0 -- commercial use permitted

## Quick Start

```bash
# Built-in voice
curl -X POST https://api.runpod.ai/v2/{ENDPOINT_ID}/run \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Hello, this is CosyVoice 2.", "voice": "default"}}'
```

## API

### Input (built-in voice)

```json
{
  "input": {
    "text": "Hello, this is CosyVoice 2 text-to-speech.",
    "voice": "default",
    "emotion": "neutral",
    "speed": 1.0
  }
}
```

### Input (voice cloning)

```json
{
  "input": {
    "text": "This text will be spoken in the cloned voice.",
    "reference_audio": "<base64 WAV, 3-10 seconds>",
    "reference_text": "Exact transcription of the reference audio."
  }
}
```

### Output

```json
{
  "audio_base64": "<base64 WAV>",
  "text": "Hello, this is CosyVoice 2 text-to-speech.",
  "voice": "default",
  "emotion": "neutral",
  "wall_time_s": 1.2
}
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | string | required | Text to synthesize (max 5000 chars) |
| `voice` | string | `"default"` | Built-in voice ID |
| `reference_audio` | string | optional | Base64 WAV for voice cloning |
| `reference_text` | string | optional | Transcription of reference audio |
| `emotion` | string | `"neutral"` | "neutral", "happy", "sad", "angry", "surprised" |
| `speed` | float | `1.0` | Speaking rate (0.5-2.0) |

## Voice Cloning Tips

1. Use 3-10 seconds of clean audio (no background noise)
2. Provide the exact transcription of the reference audio
3. WAV format, 16kHz mono recommended
4. Reference audio should match target language for best results

## GPU Requirements

- Minimum: >=8GB VRAM
- Recommended: RTX 4090, L40S, A5000 (>=16GB)
- CUDA: 12.4+

## License

Apache-2.0. Based on [FunAudioLLM/CosyVoice2-0.5B](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B).
