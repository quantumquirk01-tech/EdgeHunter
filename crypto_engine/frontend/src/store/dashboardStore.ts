import { create } from 'zustand';
import { Analytics, ApiStatus, HeatmapCell, Signal, SystemStatus } from '../types/trading';
import { initialAnalytics, initialHeatmap, initialSignals } from '../lib/mockData';

type DashboardState = {
  signals: Signal[];
  analytics: Analytics;
  heatmap: HeatmapCell[];
  systemStatus: SystemStatus;
  apiStatus: ApiStatus;
  focusedSignalId: string | null;
  selectedSignal: Signal | null;
  setFocusedSignalId: (id: string | null) => void;
  setSelectedSignal: (signal: Signal | null) => void;
  setApiStatus: (status: ApiStatus) => void;
  setSystemStatus: (status: SystemStatus) => void;
  upsertSignal: (signal: Signal) => void;
  tick: () => void;
};

const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));
const mockEnabled = process.env.NEXT_PUBLIC_ENABLE_MOCK_SIGNALS === 'true';

export const useDashboardStore = create<DashboardState>((set) => ({
  signals: mockEnabled ? initialSignals : [],
  analytics: initialAnalytics,
  heatmap: initialHeatmap,
  systemStatus: mockEnabled ? 'LIVE' : 'DELAYED',
  apiStatus: mockEnabled ? 'CONNECTED' : 'DISCONNECTED',
  focusedSignalId: null,
  selectedSignal: null,
  setFocusedSignalId: (id) => set({ focusedSignalId: id }),
  setSelectedSignal: (signal) => set({ selectedSignal: signal }),
  setApiStatus: (status) => set({ apiStatus: status }),
  setSystemStatus: (status) => set({ systemStatus: status }),
  upsertSignal: (signal) =>
    set((state) => {
      if (signal.eventType !== 'Launchpool') {
        return state;
      }
      const exists = state.signals.some((item) => item.id === signal.id);
      const updated = exists
        ? state.signals.map((item) => (item.id === signal.id ? signal : item))
        : [signal, ...state.signals].slice(0, 4);
      return { signals: updated };
    }),
  tick: () =>
    set((state) => {
      const nextSignals: Signal[] = state.signals.map((signal) => {
        const delta = (Math.random() - 0.5) * 0.45;
        const nextScore = clamp(signal.score + delta, 0, 10);
        const nextLiquidity = Math.max(12000, signal.liquidityUsd * (1 + (Math.random() - 0.5) * 0.06));
        const nextSlippage = clamp(signal.slippage + (Math.random() - 0.5) * 0.12, 0.12, 3.8);
        const nextSpark = [...signal.sparkline.slice(1), clamp(nextScore, 0, 10)];
        const decision: Signal['decision'] = nextScore >= 8 ? 'ENTER' : nextScore >= 5 ? 'WATCH' : 'IGNORE';
        return {
          ...signal,
          score: Number(nextScore.toFixed(2)),
          liquidityUsd: Math.round(nextLiquidity),
          slippage: Number(nextSlippage.toFixed(2)),
          sparkline: nextSpark,
          decision,
          momentum: clamp(signal.momentum + (Math.random() - 0.5) * 0.08, 0, 1),
          isNew: false
        };
      });

      const top = nextSignals[0];
      const nextAnalytics = {
        ...state.analytics,
        winRate: clamp(state.analytics.winRate + (Math.random() - 0.5) * 0.35, 50, 92),
        roi: clamp(state.analytics.roi + (Math.random() - 0.5) * 0.25, -10, 80),
        drawdown: clamp(state.analytics.drawdown + (Math.random() - 0.5) * 0.22, 0.8, 15),
        usedCapital: clamp(state.analytics.usedCapital + (Math.random() - 0.5) * 120, 1200, state.analytics.capital)
      };

      const nextHeatmap = state.heatmap.map((cell) => ({
        ...cell,
        intensity: clamp(cell.intensity + (Math.random() - 0.5) * 0.09, 0.08, 1),
        momentum: clamp(cell.momentum + (Math.random() - 0.5) * 0.07, 0.05, 1)
      }));

      return {
        signals: nextSignals.sort((a, b) => b.score - a.score),
        analytics: nextAnalytics,
        heatmap: nextHeatmap,
        selectedSignal: state.selectedSignal ? nextSignals.find((s) => s.id === state.selectedSignal?.id) ?? null : top ?? null
      };
    })
}));
