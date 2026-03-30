import { Analytics } from '../types/trading';

type AnalyticsSectionProps = {
  analytics: Analytics;
};

type Metric = {
  label: string;
  value: string;
  tone: string;
};

export function AnalyticsSection({ analytics }: AnalyticsSectionProps) {
  const metrics: Metric[] = [
    { label: 'Win Rate', value: `${analytics.winRate.toFixed(1)}%`, tone: 'text-accent' },
    { label: 'ROI', value: `${analytics.roi.toFixed(1)}%`, tone: 'text-electric' },
    { label: 'Active Trades', value: `${analytics.activeTrades}`, tone: 'text-white' },
    { label: 'Drawdown', value: `${analytics.drawdown.toFixed(1)}%`, tone: 'text-warning' }
  ];

  return (
    <section className="space-y-3">
      <h2 className="text-sm font-semibold uppercase tracking-[0.28em] text-zinc-400">Analytics</h2>
      <div className="grid gap-3 sm:grid-cols-2">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="glass rounded-xl p-3"
          >
            <p className="text-xs text-zinc-500">{metric.label}</p>
            <p className={`text-2xl font-bold ${metric.tone}`} style={{ fontFamily: 'var(--font-space)' }}>
              {metric.value}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
