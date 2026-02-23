#!/bin/bash
# =============================================================================
# F1 Race Predictor — Quick Start Setup Script
# =============================================================================
# Usage: bash setup.sh
#
# This script installs dependencies for both backend and frontend.
# It does NOT start the servers — see docs/LOCAL_SETUP.md for that.
# =============================================================================

set -e  # Exit immediately if any command fails

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo ""
echo "=============================================="
echo "   F1 Race Predictor — Setup Script"
echo "=============================================="
echo ""

# ── Prerequisite Checks ───────────────────────────────────────────────────────
log_info "Checking prerequisites..."

command -v python3 &>/dev/null || log_error "Python 3 not found. Install from https://python.org"
command -v node   &>/dev/null || log_error "Node.js not found. Install from https://nodejs.org"
command -v npm    &>/dev/null || log_error "npm not found. It should come bundled with Node.js."
command -v psql   &>/dev/null || log_warning "psql not found — PostgreSQL may not be on your PATH. See docs/LOCAL_SETUP.md#createdb-command-not-found"

log_info "Python:     $(python3 --version)"
log_info "Node.js:    $(node --version)"
log_info "npm:        $(npm --version)"

echo ""

# ── Backend Setup ─────────────────────────────────────────────────────────────
log_info "Setting up backend..."

cd Backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  log_info "Creating Python virtual environment..."
  python3 -m venv venv
else
  log_info "Virtual environment already exists, skipping creation."
fi

# Activate venv
log_info "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || log_error "Failed to activate virtual environment."

# Install Python dependencies
log_info "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    log_warning ".env file created from .env.example — please update it with your database credentials before starting the server."
  else
    log_warning "No .env or .env.example found in Backend/. You'll need to create Backend/.env manually. See docs/LOCAL_SETUP.md."
  fi
else
  log_info ".env already exists, skipping."
fi

deactivate
cd ..

log_info "Backend setup complete. ✅"
echo ""

# ── Frontend Setup ────────────────────────────────────────────────────────────
log_info "Setting up frontend..."

cd Frontend

# Install Node dependencies
log_info "Installing Node.js dependencies (this may take a moment)..."
npm install --silent

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    log_info ".env file created from .env.example."
  else
    log_warning "No .env.example found in Frontend/. Create Frontend/.env manually with: VITE_API_BASE_URL=http://localhost:8000/api"
  fi
else
  log_info ".env already exists, skipping."
fi

cd ..

log_info "Frontend setup complete. ✅"
echo ""

# ── Done ──────────────────────────────────────────────────────────────────────
echo "=============================================="
echo "   Setup complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "  1. Update Backend/.env with your database credentials"
echo "  2. Start PostgreSQL and create the database:"
echo "       createdb f1_predictor"
echo "  3. Run database migrations:"
echo "       cd Backend && source venv/bin/activate && alembic upgrade head"
echo "  4. Start the backend (Terminal 1):"
echo "       cd Backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"
echo "  5. Start the frontend (Terminal 2):"
echo "       cd Frontend && npm run dev"
echo ""
echo "  Full setup guide: docs/LOCAL_SETUP.md"
echo ""