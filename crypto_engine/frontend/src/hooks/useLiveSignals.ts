import { useEffect } from 'react';
import { useDashboardStore } from '../store/dashboardStore';
import { Signal } from '../types/trading';

const resolveWebSocketUrl = () => {
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL;
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  try {
    if (wsUrl) {
      const socketUrl = new URL(wsUrl);

      if (apiBaseUrl) {
        const apiUrl = new URL(apiBaseUrl);
        const apiPath = apiUrl.pathname.replace(/\/$/, '');

        if (socketUrl.pathname === '/ws' && apiPath) {
          socketUrl.pathname = `${apiPath}/ws`;
        }
      }

      return socketUrl.toString();
    }

    if (!apiBaseUrl) {
      return null;
    }

    const apiUrl = new URL(apiBaseUrl);
    apiUrl.protocol = apiUrl.protocol === 'https:' ? 'wss:' : 'ws:';
    apiUrl.pathname = `${apiUrl.pathname.replace(/\/$/, '')}/ws`;
    return apiUrl.toString();
  } catch {
    return null;
  }
};

const randomToken = () => {
  const list = ['VELO', 'ALT', 'NEXA', 'FLUX', 'ZRO', 'DYM', 'STRK', 'MAV', 'JUP', 'PYTH'];
  return list[Math.floor(Math.random() * list.length)];
};

const randomExchange = () => {
  const list = ['Binance', 'Bybit', 'KuCoin', 'Gate.io'];
  return list[Math.floor(Math.random() * list.length)];
};

const randomSummary = (token: string, exchange: string) =>
  `${exchange} Launchpool لـ ${token} مع نافذة دخول مبكرة وحجم اهتمام مرتفع خلال الدقائق الأولى.`;

export function useLiveSignals() {
  const tick = useDashboardStore((s) => s.tick);
  const upsertSignal = useDashboardStore((s) => s.upsertSignal);
  const setApiStatus = useDashboardStore((s) => s.setApiStatus);
  const setSystemStatus = useDashboardStore((s) => s.setSystemStatus);

  useEffect(() => {
    const mockEnabled = process.env.NEXT_PUBLIC_ENABLE_MOCK_SIGNALS === 'true';
    let socket: WebSocket | null = null;
    let reconnectTimeout: NodeJS.Timeout;
    let hasConnectedSocket = false;
    let fallbackMode = false;

    const connect = () => {
      if (fallbackMode) return;

      const wsUrl = resolveWebSocketUrl();
      if (!wsUrl) return;

      try {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => {
          hasConnectedSocket = true;
          setApiStatus('CONNECTED');
          setSystemStatus('LIVE');
          console.log('Connected to signals engine');
        };
        socket.onmessage = (event) => {
          try {
            const parsed = JSON.parse(event.data) as Signal;
            upsertSignal({ ...parsed, isNew: true });
          } catch (e) {
            console.error('Failed to parse signal:', e);
          }
        };
        socket.onclose = () => {
          if (fallbackMode) {
            return;
          }

          setApiStatus('DISCONNECTED');
          setSystemStatus('DELAYED');
          console.log('Disconnected. Retrying in 3s...');
          reconnectTimeout = setTimeout(connect, 3000);
        };
        socket.onerror = (err) => {
          console.error('WebSocket error:', err);
          socket?.close();
        };
      } catch (err) {
        console.error('Connection failed:', err);
        setApiStatus('DISCONNECTED');
        setSystemStatus('DELAYED');
      }
    };

    const fetchSignalsFallback = async () => {
      try {
        const res = await fetch('/api/proxy');
        if (res.ok) {
          const signals = await res.json();
          if (Array.isArray(signals)) {
            if (!hasConnectedSocket) {
              fallbackMode = true;
              clearTimeout(reconnectTimeout);
              if (socket) {
                socket.onclose = null;
                socket.close();
                socket = null;
              }
            }
            signals.forEach(upsertSignal);
            setApiStatus('CONNECTED');
            setSystemStatus('LIVE');
          }
        }
      } catch (e) {
        console.error('Fallback fetch failed:', e);
      }
    };

    const interval = mockEnabled ? window.setInterval(() => tick(), 450) : window.setInterval(fetchSignalsFallback, 5000);

    if (!mockEnabled) {
      connect();
      fetchSignalsFallback();
    }

    const inject = mockEnabled
      ? window.setInterval(() => {
          const score = Number((5 + Math.random() * 5).toFixed(2));
          const token = randomToken();
          const exchange = randomExchange();
          const eventTimestamp = Date.now() + (20 + Math.floor(Math.random() * 120)) * 60_000;
          const signal: Signal = {
            id: `${Date.now()}`,
            token,
            exchange,
            eventType: 'Launchpool',
            eventSummary: randomSummary(token, exchange),
            eventTimestamp,
            score,
            detectedAt: Date.now(),
            decision: score >= 8 ? 'ENTER' : score >= 5 ? 'WATCH' : 'IGNORE',
            liquidityUsd: Math.round(140000 + Math.random() * 950000),
            slippage: Number((0.18 + Math.random() * 1.65).toFixed(2)),
            sparkline: Array.from({ length: 8 }).map(() => Number((3 + Math.random() * 7).toFixed(2))),
            momentum: Number((0.55 + Math.random() * 0.4).toFixed(2)),
            isNew: true
          };
          upsertSignal(signal);
        }, 3800)
      : null;

    return () => {
      if (interval) window.clearInterval(interval);
      if (inject) window.clearInterval(inject);
      if (socket) {
        socket.onclose = null;
        socket.close();
      }
      clearTimeout(reconnectTimeout);
    };
  }, [setApiStatus, setSystemStatus, tick, upsertSignal]);
}
