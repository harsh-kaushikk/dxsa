#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${ROOT}/KFA_Brochure.pdf"
HTML="${ROOT}/kfa-brochure.html"

# Chrome sometimes hangs after writing the PDF; bound the process.
timeout 45s google-chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --disable-dev-shm-usage \
  --no-pdf-header-footer \
  --print-to-pdf="${OUT}" \
  --virtual-time-budget=12000 \
  "file://${HTML}" \
  || true

if [[ ! -s "${OUT}" ]]; then
  echo "Failed to generate ${OUT}" >&2
  exit 1
fi

echo "Wrote ${OUT} ($(wc -c < "${OUT}") bytes)"
