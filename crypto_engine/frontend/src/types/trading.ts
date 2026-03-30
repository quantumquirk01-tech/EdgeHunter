export type Decision = 'ENTER' | 'WATCH' | 'IGNORE';
export type EventType = 'Listing' | 'Launchpool' | 'Pre-market';
export type SystemStatus = 'LIVE' | 'DELAYED';
export type ApiStatus = 'CONNECTED' | 'DISCONNECTED';

export type Signal = {
  id: string;
  token: string;
  exchange: string;
  eventType: EventType;
  eventSummary: string;
  eventTimestamp: number;
  score: number;
  detectedAt: number;
  decision: Decision;
  liquidityUsd: number;
  slippage: number;
  sparkline: number[];
  momentum: number;
  isNew?: boolean;
};

export type Analytics = {
  winRate: number;
  roi: number;
  activeTrades: number;
  drawdown: number;
  capital: number;
  usedCapital: number;
};

export type HeatmapCell = {
  symbol: string;
  intensity: number;
  momentum: number;
};
