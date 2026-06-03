"""
RunPod serverless handler for CosyVoice 2 TTS — text → audio generation with
voice cloning and emotion control.

Architecture:
  - CosyVoice 2 next-gen TTS model
  - Supports multi-speaker synthesis, emotion control, voice cloning
  - 24kHz output with natural prosody
  - Requires >=8GB VRAM

Environment:
  - RUNPOD_POD_ID       — auto
  - RUNPOD_AI_API_KEY   — auto

Input schema (via RunPod serverless job):
  {
    "input": {
      "text": "Hello world!",                   // REQUIRED — text to synthesize
      "voice": "default",                        // optional — speaker/voice ID
      "emotion": "neutral",                      // optional — emotion style
      "reference_audio": null                    // optional — URL for voice cloning
    }
  }

Output:
  {
    "audio_base64": "<base64-encoded WAV>",
    "text": "Hello world!",
    "voice": "default",
    "wall_time_s": 1.2
  }
"""

import base64
import os
import time
import traceback
from io import BytesIO

# ── Environment setup ─────────────────────────────────────────────────────────
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import torch

# Disable flash/mem-efficient SDPA for broad GPU compatibility
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_math_sdp(True)

# ── Model path (baked into image at BUILD TIME) ──────────────────────────────
MODEL_ID = "/models/cosyvoice"

# ── Global pipeline (loaded once, reused across jobs) ─────────────────────────
_pipe = None
_device = None
_emotion_pipe = None


def load_pipeline():
    """Load CosyVoice 2 model once and cache globally."""
    global _pipe, _device, _emotion_pipe
    if _pipe is not None:
        return _pipe, _device

    print("[Cold Start] Loading CosyVoice 2 model...", flush=True)
    t0 = time.time()

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    print(f"  Device: {_device}, dtype: {dtype}", flush=True)

    # Import CosyVoice
    from cosyvoice.cli.cosyvoice import CosyVoice2
    from cosyvoice.utils.common import upload_audio_to_url

    # Load the model from local path
    pipe = CosyVoice2(
        model_dir=MODEL_ID,
        device=str(_device),
        dtype=dtype,
    )

    print(f"[Cold Start] Pipeline ready in {time.time() - t0:.1f}s", flush=True)

    _pipe = pipe
    return _pipe, _device


def audio_to_wav_b64(audio_array, sample_rate: int = 24000) -> str:
    """Convert numpy audio array to base64 WAV string."""
    import numpy as np
    from scipy.io import wavfile

    buf = BytesIO()
    audio_int16 = np.clip(audio_array * 32767, -32768, 32767).astype(np.int16)
    wavfile.write(buf, sample_rate, audio_int16)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def download_audio(url: str) -> bytes:
    """Download audio file from URL and return raw bytes."""
    import httpx

    response = httpx.get(url, timeout=30.0, follow_redirects=True)
    response.raise_for_status()
    return response.content


def run_inference(
    text: str,
    voice: str = "default",
    emotion: str = "neutral",
    reference_audio: str | None = None,
) -> tuple:
    """
    Run CosyVoice 2 inference.
    Returns (audio_base64, actual_voice, wall_time_s).
    """
    pipe, device = load_pipeline()

    print(f"[Inference] Synthesizing: text='{text[:80]}'", flush=True)
    print(f"  voice={voice}, emotion={emotion}", flush=True)

    t_start = time.time()

    # Run inference
    with torch.inference_mode():
        if voice == "clone" and reference_audio:
            print(f"  Voice cloning mode — downloading reference audio...", flush=True)
            audio_bytes = download_audio(reference_audio)
            import numpy as np
            import soundfile as sf
            from io import BytesIO as BufIO

            ref_audio, sr = sf.read(BufIO(audio_bytes))
            if ref_audio.ndim > 1:
                ref_audio = ref_audio.mean(axis=1)

            # Voice cloning inference
            result = pipe.inference(
                text=text,
                prompt_speech_16k=ref_audio,
                emotion=emotion,
            )
        else:
            # Standard TTS with selected voice
            result = pipe.inference(
                text=text,
                spk_id=voice,
                emotion=emotion,
            )

        audio_out = result["audio"]
        if audio_out is None:
            raise RuntimeError("CosyVoice returned empty audio")

    wall_time = time.time() - t_start
    print(f"[Done] Synthesis took {wall_time:.2f}s", flush=True)

    # Convert to base64 WAV
    audio_b64 = audio_to_wav_b64(audio_out)

    return audio_b64, voice, wall_time


# ═══════════════════════════════════════════════════════════════════════════════
# RunPod Serverless Handler
# ═══════════════════════════════════════════════════════════════════════════════


def handler(job):
    """
    RunPod serverless handler: text → base64 WAV audio.

    Called once per job. The pipeline stays loaded across jobs (global).
    """
    job_input = job.get("input", {})
    text = job_input.get("text", "")

    if not text:
        return {"error": "Missing required field: text"}

    voice = str(job_input.get("voice", "default"))
    emotion = str(job_input.get("emotion", "neutral"))
    reference_audio = job_input.get("reference_audio", None)

    # Validate emotion
    valid_emotions = ["neutral", "happy", "sad", "angry", "surprise", "fearful"]
    if emotion not in valid_emotions:
        emotion = "neutral"

    try:
        # Run inference
        audio_b64, actual_voice, wall_time = run_inference(
            text=text,
            voice=voice,
            emotion=emotion,
            reference_audio=reference_audio,
        )

        return {
            "audio_base64": audio_b64,
            "text": text,
            "voice": actual_voice,
            "wall_time_s": round(wall_time, 2),
        }

    except Exception as exc:
        traceback.print_exc()
        return {
            "error": f"CosyVoice inference failed: {str(exc)}",
            "traceback": traceback.format_exc(),
        }


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import runpod

    runpod.serverless.start({"handler": handler})
