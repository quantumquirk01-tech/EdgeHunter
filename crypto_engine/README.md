
# Crypto Opportunity Detection & Execution Engine

This project is a fully automated system for detecting, evaluating, and executing early crypto opportunities like new exchange listings.

## Deployment Steps

### Prerequisites
- Docker and Docker Compose installed on your Ubuntu server.
- Git installed.
- A registered domain name (optional, for HTTPS with Nginx).

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd crypto_engine
```

### 2. Configure Environment Variables
Copy the example environment file and fill in your actual API keys and secrets.

```bash
cp .env.example .env
nano .env
```

**Important:** Fill in your `BINANCE_API_KEY`, `TELEGRAM_BOT_TOKEN`, etc. Also, change the `DATABASE_URL` to use the service name from `docker-compose.yml`:

```
# Example DATABASE_URL for Docker environment
DATABASE_URL="postgresql+asyncpg://crypto_user:strong_password@db/crypto_db"

# Example REDIS_URL for Docker environment
REDIS_URL="redis://redis:6379"
```

### 3. Build and Run with Docker Compose
This single command will build the Docker images for your services and start them in the background.

```bash
sudo docker-compose -f deployment/docker-compose.yml up --build -d
```

### 4. Verify the Services
Check if all containers are running correctly:

```bash
sudo docker-compose -f deployment/docker-compose.yml ps
```

You should see `backend`, `db`, and `redis` services with a status of `Up`.

Check the logs of the backend service to ensure all workers have started without errors:

```bash
sudo docker-compose -f deployment/docker-compose.yml logs -f backend
```

You should see log messages indicating that the Data Ingestion, Event Detection, and Signal Processing workers have started.

### 5. Accessing the API
The API will be available at `http://<your-server-ip>:8000`.

You can test the health check endpoint:

```bash
curl http://<your-server-ip>:8000/health
```

### 6. Running the Frontend
To run the Next.js frontend, navigate to the `frontend` directory and run:

```bash
cd ../frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`.

### 7. (Optional) Setup Nginx as a Reverse Proxy
For a production setup, it's recommended to use Nginx as a reverse proxy to handle incoming traffic and manage SSL certificates.

---

## Sample Run Scenario: New Listing on Binance

This scenario illustrates the end-to-end flow of the system when a new coin is announced.

**Hypothesis:** Binance announces they will list a new token called "HyperAI (HAI)".

**Step 1: Ingestion**
- The `data_ingestion_worker` scrapes the Binance announcements page and finds the new post: `Binance Will List HyperAI (HAI)`.
- It creates a raw data object and pushes it to the `raw_events` Redis queue.

**Step 2: Event Detection**
- The `event_detection_worker` pops the raw data from the queue.
- The `parse_raw_announcement` function analyzes the title, extracts the token symbol `HAI`, and classifies the event as a `New Listing` for the `binance` exchange.
- It creates a structured event object and pushes it to the `parsed_events` Redis queue.

**Step 3: Signal Generation (CORE ALPHA)**
- The `signal_processing_worker` pops the structured event.
- The `generate_signal_from_event` function is called:
  - It fetches live market context (simulated): low initial liquidity, high buy-side imbalance.
  - It calculates a score:
    - `+5` for Binance (major exchange).
    - `+3.8` for fast detection.
    - `+3` for low liquidity.
    - `+3` for order book imbalance.
    - **Total Score: 14.8**
  - Since 14.8 > `ENTER_THRESHOLD` (8.0), the decision is **ENTER**.

**Step 4: Notification**
- The `send_telegram_notification` function is called.
- A message is sent to your Telegram chat with the signal details: `🚀 New Opportunity ✅ ... Token: HAI, Exchange: Binance, Score: 14.8, Decision: ENTER`.

**Step 5: Risk Management**
- The `assess_risk_and_create_order` function validates the `ENTER` signal against the rules:
  - Max concurrent trades check: **Pass**.
  - Max daily loss check: **Pass**.
  - Market spread check: **Pass**.
- An order object is created with a position size of `$10.00`, a stop-loss at `-8%`, and take-profit targets.

**Step 6: Execution**
- The `execute_order` function receives the final order object.
- It selects the `Binance` client and calls its `execute_order` method.
- A `MARKET BUY` order for `$10.00` worth of `HAI` is sent to the Binance API.
- Upon successful execution, `manage_active_trade` is called to place the corresponding SL/TP orders.
- The trade details are saved to the PostgreSQL database.

**Step 7: Learning**
- Later, the trade is closed (e.g., hits Take-Profit 1).
- The `analyze_trade_outcome` function logs insights based on the profitable outcome, reinforcing that the combination of factors in the original signal was effective.
