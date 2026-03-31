
'use client';

import { useEffect, useMemo, useState } from 'react';
import { useLiveSignals } from '../hooks/useLiveSignals';
import { useDashboardStore } from '../store/dashboardStore';
import { TopBar } from '../components/TopBar';
import { LiveSignalsFeed } from '../components/LiveSignalsFeed';
import { ExecutionPanel } from '../components/ExecutionPanel';
import { AnalyticsSection } from '../components/AnalyticsSection';
import { HeatmapSection } from '../components/HeatmapSection';
import { FocusMode } from '../components/FocusMode';
import { Signal } from '../types/trading';
import { ApiKeysFormValues, ApiKeysPanel } from '../components/ApiKeysPanel';

export default function DashboardPage() {
  useLiveSignals();

  const [mounted, setMounted] = useState(false);
  const signals = useDashboardStore((s) => s.signals);
  const analytics = useDashboardStore((s) => s.analytics);
  const heatmap = useDashboardStore((s) => s.heatmap);
  const systemStatus = useDashboardStore((s) => s.systemStatus);
  const apiStatus = useDashboardStore((s) => s.apiStatus);
  const focusedSignalId = useDashboardStore((s) => s.focusedSignalId);
  const selectedSignal = useDashboardStore((s) => s.selectedSignal);
  const setFocusedSignalId = useDashboardStore((s) => s.setFocusedSignalId);
  const setSelectedSignal = useDashboardStore((s) => s.setSelectedSignal);
  const [focusModeSignal, setFocusModeSignal] = useState<Signal | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const topSignal = useMemo(() => signals[0] ?? null, [signals]);

  const handleFocusSignal = (id: string) => {
    setFocusedSignalId(id);
    const next = signals.find((signal) => signal.id === id) ?? null;
    if (next) {
      setSelectedSignal(next);
    }
  };

  const handleExecute = (signal: Signal) => {
    setSelectedSignal(signal);
    setFocusModeSignal(signal);
  };

  const handleSaveApiKeys = async (values: ApiKeysFormValues) => {
    const filtered = Object.fromEntries(
      Object.entries(values).filter(([, value]) => value.trim().length > 0)
    );
    if (Object.keys(filtered).length === 0) {
      return;
    }
    const response = await fetch('/api/config/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_keys: filtered })
    });
    if (!response.ok) {
      throw new Error('تعذر حفظ مفاتيح API');
    }
  };

  if (!mounted) {
    return (
      <main className="min-h-screen bg-background px-4 py-4 text-white md:px-6">
        <div className="grid-overlay pointer-events-none fixed inset-0 opacity-[0.22]" />
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background px-4 py-4 text-white md:px-6">
      <div className="grid-overlay pointer-events-none fixed inset-0 opacity-[0.22]" />
      <div className="relative mx-auto max-w-[1480px] space-y-4">
        <TopBar analytics={analytics} systemStatus={systemStatus} apiStatus={apiStatus} />

        <div className="grid gap-4 xl:grid-cols-[1fr_330px]">
          <section className="space-y-4">
            <div className="glass relative overflow-hidden rounded-2xl p-4">
              <div className="absolute right-4 top-0 h-24 w-px bg-gradient-to-b from-accent/0 via-accent/90 to-accent/0" />
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Primary Opportunity</p>
              <div className="mt-2 flex items-end justify-between">
                <div>
                  <h1 className="text-3xl font-bold text-white md:text-4xl" style={{ fontFamily: 'var(--font-space)' }}>
                    {topSignal ? `${topSignal.token} · ${topSignal.decision}` : 'Monitoring Feed'}
                  </h1>
                  <p className="text-sm text-zinc-400">
                    {topSignal
                      ? `${topSignal.exchange} · Score ${topSignal.score.toFixed(1)} · ${topSignal.eventType}`
                      : 'Waiting for new live opportunities'}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => topSignal && handleExecute(topSignal)}
                  disabled={!topSignal}
                  className="rounded-xl bg-accent px-5 py-3 text-sm font-bold text-black shadow-neon transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Quick Execute
                </button>
              </div>
            </div>

            <LiveSignalsFeed
              signals={signals}
              focusedSignalId={focusedSignalId}
              onFocusSignal={handleFocusSignal}
              onExecute={handleExecute}
            />
          </section>

          <section className="space-y-4">
            <ExecutionPanel signal={selectedSignal ?? topSignal} capital={analytics.capital} onClose={() => setSelectedSignal(null)} />
            <ApiKeysPanel onSave={handleSaveApiKeys} />
            <AnalyticsSection analytics={analytics} />
            <HeatmapSection cells={heatmap} />
          </section>
        </div>
      </div>

      <FocusMode signal={focusModeSignal} onClose={() => setFocusModeSignal(null)} onExecute={() => setFocusModeSignal(null)} />
    </main>
  );
}
