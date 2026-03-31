#!/bin/bash
set -e

echo "============================================"
echo "EdgeHunter Backend Setup for Ubuntu"
echo "============================================"

# Update system
echo "[1/6] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "[2/6] Installing Docker..."
sudo apt install -y docker.io docker-compose-v2

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Create project directory
echo "[3/6] Creating project directory..."
mkdir -p ~/edgehunter
cd ~/edgehunter

# Clone repository (replace with your repo URL)
# git clone https://github.com/quantumquirk01-tech/EdgeHunter.git .

# Create .env file
echo "[4/6] Creating .env file..."
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql+asyncpg://crypto_user:strong_password@db:5432/crypto_db
REDIS_URL=redis://redis:6379

# API Keys (REPLACE WITH REAL KEYS!)
CMC_API_KEY=YOUR_COINMARKETCAP_API_KEY
BINANCE_API_KEY=YOUR_BINANCE_API_KEY
BINANCE_API_SECRET=YOUR_BINANCE_API_SECRET
BYBIT_API_KEY=YOUR_BYBIT_API_KEY
BYBIT_API_SECRET=YOUR_BYBIT_API_SECRET
KUCOIN_API_KEY=YOUR_KUCOIN_API_KEY
KUCOIN_API_SECRET=YOUR_KUCOIN_API_SECRET
KUCOIN_API_PASSPHRASE=YOUR_KUCOIN_API_PASSPHRASE
GATEIO_API_KEY=YOUR_GATEIO_API_KEY
GATEIO_API_SECRET=YOUR_GATEIO_API_SECRET

# Telegram
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID

# Security
SECRET_KEY=change_this_to_a_very_strong_random_secret_key

# CORS
CORS_ORIGINS=http://localhost:3000,https://edgehunter.vercel.app
EOF

# Create docker-compose file for production
echo "[5/6] Creating production Docker Compose..."
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: ./crypto_engine
      dockerfile: ./backend/Dockerfile
    ports:
      - "8001:8000"
    volumes:
      - ./crypto_engine/backend/app:/app/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - crypto-net
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

  db:
    image: postgres:14-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=crypto_user
      - POSTGRES_PASSWORD=strong_password
      - POSTGRES_DB=crypto_db
    restart: unless-stopped
    networks:
      - crypto-net

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - crypto-net

networks:
  crypto-net:
    driver: bridge

volumes:
  postgres_data:
EOF

# Build and start containers
echo "[6/6] Building and starting containers..."
sudo docker compose -f docker-compose.prod.yml up -d --build

# Check status
echo ""
echo "============================================"
echo "Setup complete!"
echo "============================================"
echo ""
echo "Backend API: http://YOUR_SERVER_IP:8001"
echo "API Docs:    http://YOUR_SERVER_IP:8001/docs"
echo "Health:      http://YOUR_SERVER_IP:8001/health"
echo ""
echo "Check logs with: sudo docker compose -f docker-compose.prod.yml logs -f"
echo "Stop with:       sudo docker compose -f docker-compose.prod.yml down"
echo ""
