#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: ./compress_video.sh INPUT_VIDEO OUTPUT_VIDEO [MAX_WIDTH]" >&2
  exit 1
fi

input="$1"
output="$2"
max_width="${3:-1280}"

mkdir -p "$(dirname "$output")"

ffmpeg -y \
  -i "$input" \
  -map 0:v:0 \
  -map 0:a? \
  -vf "scale='min(${max_width},iw)':-2" \
  -c:v libx264 \
  -preset slow \
  -crf 28 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac \
  -b:a 128k \
  "$output"
