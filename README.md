# elabs / CosyVoice 2 TTS

Zero-shot voice cloning text-to-speech using Alibaba's CosyVoice 2. Clone any voice from a 3-10 second audio sample.

[![Docker Build](https://github.com/ELABS-AI/cosyvoice-2-runpod-worker/actions/workflows/build.yml/badge.svg)](https://github.com/ELABS-AI/cosyvoice-2-runpod-worker/actions/workflows/build.yml)

---

## Quick Start

Deploy this worker on [RunPod Serverless](https://www.runpod.io/serverless) using the **Deploy on RunPod** button in the Hub, or manually with the Docker image:

```
ghcr.io/elabs-ai/cosyvoice-2-runpod-worker:latest
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_ID` | `iic/CosyVoice2-0.5B` | HuggingFace model ID for CosyVoice 2 |
| `HF_HOME` | `/runpod-volume/models/huggingface` | HuggingFace cache directory |
| `HUGGINGFACE_HUB_CACHE` | `/runpod-volume/models/huggingface/hub` | HuggingFace hub cache |
| `PYTORCH_CUDA_ALLOC_CONF` | `expandable_segments:True` | CUDA memory allocator config |

> **Note:** `HF_HOME` and `HUGGINGFACE_HUB_CACHE` should point to a RunPod Network Volume mount path for model caching between runs.

---

## API Reference

### Input

```json
{"input": {"text": "Hello world!", "reference_audio_b64": "<base64 WAV/MP3 3-10s>"}}
```

### Output

```json
{"audio_b64": "<base64 WAV>", "wall_time_s": 3.2}
```

---

## Usage Examples

### Python (runpod SDK)

```python
import runpod
import base64

client = runpod.AsyncioEndpointClient("cosyvoice-2-runpod-worker")
result = await client.run({"input": {"text": "Hello world!", "reference_audio_b64": "<base64 WAV/MP3 3-10s>"}})
print(result)
```

### cURL

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Hello world!", "reference_audio_b64": "<base64 WAV/MP3 3-10s>"}}'

```

---

## GPU Requirements

RTX 3090+ (24GB VRAM) | ~3-8s per utterance | Apache 2.0 license

---

## License

Apache 2.0 — See [LICENSE](LICENSE)

---

## Built by [E-Labs AI](https://www.elabsai.com)

Part of the E-Labs AI Studio serverless model fleet. Visit [elabsai.com](https://www.elabsai.com) to use these models in a hosted UI.
