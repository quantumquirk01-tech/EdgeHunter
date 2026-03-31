'use client';

import { useState } from 'react';
import { Signal } from '../types/trading';
import { ScoreRing } from './ScoreRing';
import { Sparkline } from './Sparkline';
import { TimeDecayBar } from './TimeDecayBar';

type LiveSignalsFeedProps = {
  signals: Signal[];
  focusedSignalId: string | null;
  onFocusSignal: (id: string) => void;
  onExecute: (signal: Signal) => void;
};

const decisionStyles: Record<Signal['decision'], string> = {
  ENTER: 'bg-accent/15 text-accent border border-accent/45',
  WATCH: 'bg-warning/15 text-warning border border-warning/45',
  IGNORE: 'bg-zinc-800 text-zinc-400 border border-zinc-700'
};

export function LiveSignalsFeed({ signals, focusedSignalId, onFocusSignal, onExecute }: LiveSignalsFeedProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  if (signals.length === 0) {
    return (
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-[0.28em] text-zinc-400">Launchpool Feed</h2>
          <p className="text-xs text-zinc-500">0 opportunities</p>
        </div>
        <div className="glass rounded-2xl p-8 text-center">
          <p className="text-zinc-500">لا توجد فرص حالياً. انتظر الإشارات الحية من السيرفر...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-[0.28em] text-zinc-400">Launchpool Feed</h2>
        <p className="text-xs text-zinc-500">{signals.length} فرصة</p>
      </div>
      <div className="space-y-2">
        {signals.map((signal) => {
          const isExpanded = expandedId === signal.id;
          const isFocused = focusedSignalId === signal.id;
          const ageSeconds = (Date.now() - signal.detectedAt) / 1000;
          const liquidityLabel = signal.liquidityUsd > 1_000_000 ? 'Ultra' : signal.liquidityUsd > 300_000 ? 'Strong' : 'Thin';

          return (
            <div
              key={signal.id}
              className={`glass rounded-xl border transition-all cursor-pointer ${
                isFocused ? 'border-accent/60 bg-accent/5' : 'border-white/10 hover:border-white/20'
              }`}
              onClick={() => {
                onFocusSignal(signal.id);
                toggleExpand(signal.id);
              }}
            >
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-4">
                  <ScoreRing value={signal.score} size={48} />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-lg font-bold text-white">{signal.token}</span>
                      <span className="text-xs text-zinc-500">{signal.exchange}</span>
                    </div>
                    <p className="text-xs text-zinc-400">{signal.eventType} · منذ {ageSeconds.toFixed(0)} ثانية</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`rounded-lg px-3 py-1 text-xs font-bold ${decisionStyles[signal.decision]}`}>
                    {signal.decision}
                  </span>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onExecute(signal);
                    }}
                    className="rounded-lg bg-accent px-4 py-2 text-xs font-bold text-black hover:brightness-110"
                  >
                    EXECUTE
                  </button>
                </div>
              </div>

              {isExpanded && (
                <div className="border-t border-white/5 p-4 space-y-4" onClick={(e) => e.stopPropagation()}>
                  <div>
                    <p className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-1">شرح الحدث</p>
                    <p className="text-sm text-zinc-200">{signal.eventSummary}</p>
                  </div>

                  <div className="grid grid-cols-3 gap-3">
                    <div className="rounded-lg bg-black/35 p-2 border border-white/5">
                      <p className="text-[10px] font-bold text-zinc-500 uppercase">Liquidity</p>
                      <p className="text-sm font-bold text-white">{liquidityLabel}</p>
                      <p className="text-xs text-zinc-400">${(signal.liquidityUsd / 1000).toFixed(0)}K</p>
                    </div>
                    <div className="rounded-lg bg-black/35 p-2 border border-white/5">
                      <p className="text-[10px] font-bold text-zinc-500 uppercase">Slippage</p>
                      <p className="text-sm font-bold text-white">{signal.slippage.toFixed(2)}%</p>
                    </div>
                    <div className="rounded-lg bg-black/35 p-2 border border-white/5">
                      <p className="text-[10px] font-bold text-zinc-500 uppercase">Momentum</p>
                      <p className="text-sm font-bold text-white">{(signal.momentum * 100).toFixed(0)}%</p>
                    </div>
                  </div>

                  <div className="rounded-xl border border-white/5 bg-black/30 p-2">
                    <Sparkline data={signal.sparkline} positive={signal.decision !== 'IGNORE'} />
                  </div>

                  <TimeDecayBar seconds={ageSeconds} />

                  <div className="flex items-center justify-between text-xs text-zinc-500">
                    <span>Score: {signal.score.toFixed(1)}</span>
                    <span>ID: {signal.id}</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}