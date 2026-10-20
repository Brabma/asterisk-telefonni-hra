"""Generate telephone prompts (8 kHz, mono, 16 bit) from game/story.json.

Uses the Windows OneCore voice through render_tts.ps1,
then resamples, trims silence and normalizes each prompt for Asterisk.
"""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RENDERER = HERE / "render_tts.ps1"
TARGET_RATE = 8000


def render(text: str, voice: str, rate: int) -> tuple[np.ndarray, int]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "prompt.wav"
        payload = json.dumps({"text": text, "voice": voice, "rate": rate, "pitch": 1, "path": str(path)})
        subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(RENDERER)],
            input=payload.encode("utf-8"), check=True,
        )
        with wave.open(io.BytesIO(path.read_bytes()), "rb") as source:
            channels, width, rate_hz = source.getnchannels(), source.getsampwidth(), source.getframerate()
            frames = source.readframes(source.getnframes())
    if width != 2:
        raise ValueError(f"Unexpected sample width {width}")
    samples = np.frombuffer(frames, dtype="<i2").astype(np.float64)
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    return samples, rate_hz


def shorten_pauses(samples: np.ndarray, max_pause_s: float = 0.25) -> np.ndarray:
    """Cut silences between sentences down to max_pause_s so the menu comes sooner."""
    frame = TARGET_RATE // 100  # 10 ms
    count = len(samples) // frame
    loud = np.abs(samples[: count * frame].reshape(count, frame)).max(axis=1) >= 220
    keep = np.ones(count, dtype=bool)
    limit = round(max_pause_s * 100)
    run = 0
    for index, is_loud in enumerate(loud):
        run = 0 if is_loud else run + 1
        if run > limit:
            keep[index] = False
    return np.concatenate([samples[: count * frame].reshape(count, frame)[keep].ravel(), samples[count * frame:]])


def to_telephone(samples: np.ndarray, rate_hz: int) -> np.ndarray:
    if rate_hz != TARGET_RATE:
        # windowed-sinc low-pass at 3.4 kHz, then linear resampling
        cutoff = 3400 / rate_hz
        taps = np.arange(-64, 65)
        kernel = 2 * cutoff * np.sinc(2 * cutoff * taps) * np.hamming(len(taps))
        samples = np.convolve(samples, kernel / kernel.sum(), mode="same")
        positions = np.arange(0, len(samples), rate_hz / TARGET_RATE)
        samples = np.interp(positions, np.arange(len(samples)), samples)
    audible = np.flatnonzero(np.abs(samples) >= 220)
    if audible.size:
        pad = round(TARGET_RATE * 0.06)
        samples = samples[max(0, audible[0] - pad): audible[-1] + pad + 1]
        samples = shorten_pauses(samples)
    peak = np.abs(samples).max() or 1
    samples = samples * min(3.0, 32767 * 0.78 / peak)
    return np.clip(np.round(samples), -32768, 32767).astype("<i2")


def write(path: Path, samples: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as target:
        target.setnchannels(1)
        target.setsampwidth(2)
        target.setframerate(TARGET_RATE)
        target.writeframes(samples.tobytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--story", type=Path, default=HERE.parent / "game" / "story.json")
    parser.add_argument("--out", type=Path, default=HERE.parent / "audio")
    parser.add_argument("--voice", default="Microsoft Jakub")
    parser.add_argument("--rate", type=int, default=-1)
    args = parser.parse_args()

    story = json.loads(args.story.read_text(encoding="utf-8"))
    prompts = {story["game"]["invalid_audio"]: story["game"]["invalid_text"]}
    prompts.update({node["audio"]: node["text"] for node in story["nodes"].values()})
    for name, text in prompts.items():
        samples, rate_hz = render(text, args.voice, args.rate)
        out = to_telephone(samples, rate_hz)
        write(args.out / f"{name}.wav", out)
        print(f"{name}.wav  {len(out) / TARGET_RATE:.1f} s  (zdroj {rate_hz} Hz)")
    print(f"Hotovo: {len(prompts)} souborů")


if __name__ == "__main__":
    sys.exit(main())
