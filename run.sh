#!/usr/bin/env bash
# One-command setup and start for Brain Rot Generator.
# Usage: ./run.sh   (or: bash run.sh)

set -e
cd "$(dirname "$0")"

PROJECT_ROOT="$(pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

echo "Brain Rot Generator — setup and start"
echo "Project root: $PROJECT_ROOT"
echo ""

# 1. Create virtualenv if missing
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
  echo "Done."
else
  echo "Virtual environment found."
fi

# 2. Upgrade pip and install dependencies
echo "Installing/updating dependencies..."
"$VENV_PIP" install --upgrade pip -q
"$VENV_PIP" install -r requirements.txt -q
echo "Done."

# 3. Ensure NLTK VADER data exists
echo "Checking NLTK data..."
"$VENV_PYTHON" -c "
import nltk
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)
print('NLTK OK.')
"

# 4. Optional: create .env if missing (user can add GROQ_API_KEY later)
if [ ! -f "$PROJECT_ROOT/.env" ]; then
  touch "$PROJECT_ROOT/.env"
  echo "# Add GROQ_API_KEY=your_key if needed" >> "$PROJECT_ROOT/.env"
  echo "Created .env (add your keys there if needed)."
fi

# 5. Start the Flask server
echo ""
echo "Starting server at http://127.0.0.1:5000"
echo "Press Ctrl+C to stop."
echo ""
exec "$VENV_DIR/bin/python" server.py
