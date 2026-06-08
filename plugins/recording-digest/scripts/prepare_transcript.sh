#!/usr/bin/env bash
# Prepare a plain-text transcript from a recording that lives on disk.
# Audio in  -> local whisper transcription (no network, no external API).
# Text in   -> passthrough.
# Prints exactly one machine-readable line on stdout: TRANSCRIPT=<path>
# Progress and errors go to stderr so stdout stays clean for the caller.
#
# Everything here is local. Privileged intake audio never leaves the machine.
set -uo pipefail

INPUT="${1:?usage: prepare_transcript.sh <audio-or-text-file> [out_dir]}"
OUT_DIR="${2:-$(dirname "$INPUT")}"
# Apple-Silicon MLX model (isolated via uvx, fast, no Homebrew Python deps).
MLX_MODEL="${MLX_WHISPER_MODEL:-mlx-community/whisper-small}"
# Fallback model name for the legacy openai-whisper CLI, if it is ever used.
WHISPER_MODEL="${WHISPER_MODEL:-small}"

[ -f "$INPUT" ] || { echo "ERROR: no such file: $INPUT" >&2; exit 1; }

ext="${INPUT##*.}"; ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
base="$(basename "${INPUT%.*}")"

is_audio=0
case "$ext" in
  m4a|mp3|wav|aac|aiff|caf|flac|ogg|mp4|mov) is_audio=1 ;;
  txt|md|markdown|text|vtt|srt)              is_audio=0 ;;
  *)
    # Unknown extension: probe for an audio stream rather than guessing.
    if command -v ffprobe >/dev/null 2>&1 && \
       ffprobe -v error -select_streams a -show_entries stream=codec_type \
               -of csv=p=0 "$INPUT" 2>/dev/null | grep -q audio; then
      is_audio=1
    fi
    ;;
esac

if [ "$is_audio" -eq 1 ]; then
  out="$OUT_DIR/$base.txt"
  if command -v uvx >/dev/null 2>&1; then
    # Preferred: MLX whisper in an ephemeral env. Avoids the Homebrew
    # torch/protobuf breakage and uses Apple Silicon acceleration.
    echo "Transcribing locally with mlx-whisper ($MLX_MODEL). First run downloads the model; long recordings take a few minutes..." >&2
    uvx --from mlx-whisper mlx_whisper "$INPUT" --model "$MLX_MODEL" \
        --output-dir "$OUT_DIR" --output-format txt 1>&2 || {
      echo "ERROR: mlx-whisper failed on $INPUT" >&2; exit 3; }
  elif command -v whisper >/dev/null 2>&1; then
    # Fallback: legacy openai-whisper CLI (may be broken by Homebrew deps).
    echo "Transcribing with openai-whisper ($WHISPER_MODEL)..." >&2
    whisper "$INPUT" --model "$WHISPER_MODEL" --output_format txt \
            --output_dir "$OUT_DIR" --language en 1>&2 || {
      echo "ERROR: whisper failed on $INPUT" >&2; exit 3; }
  else
    echo "ERROR: audio input but no transcriber found." >&2
    echo "Easiest fix: ensure uv is installed (you have it). The script uses 'uvx mlx-whisper' automatically." >&2
    exit 2
  fi
  [ -f "$out" ] || { echo "ERROR: transcription produced no $out" >&2; exit 3; }
  echo "TRANSCRIPT=$out"
else
  # Already text. Pass it straight through.
  echo "TRANSCRIPT=$INPUT"
fi
