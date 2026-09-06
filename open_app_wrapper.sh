#!/bin/bash
# ==============================================================================
# WORLD SET: STANDALONE DESKTOP APPLICATION WRAPPER
# Launches http://localhost:8000/index.html in a dedicated, borderless app window
# ==============================================================================

PORT=8000
URL="http://localhost:${PORT}/index.html"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ensure local HTTP server is running
if ! lsof -i :${PORT} >/dev/null 2>&1; then
  echo "[Wrapper] Starting local background HTTP server on port ${PORT}..."
  nohup python3 -m http.server ${PORT} --directory "${PROJECT_DIR}" >/dev/null 2>&1 &
  sleep 1
fi

echo "[Wrapper] Launching World Set in dedicated standalone wrapper window..."

if [ -d "/Applications/Google Chrome.app" ]; then
  open -na "Google Chrome" --args --app="${URL}" --window-size=1440,900
  echo "[Wrapper] Launched successfully in Google Chrome App Mode."
elif [ -d "/Applications/Brave Browser.app" ]; then
  open -na "Brave Browser" --args --app="${URL}" --window-size=1440,900
  echo "[Wrapper] Launched successfully in Brave App Mode."
else
  open -a Safari "${URL}"
  echo "[Wrapper] Opened in Safari."
fi
