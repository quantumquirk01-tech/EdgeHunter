import { Analytics, ApiStatus, SystemStatus } from '../types/trading';

type TopBarProps = {
  analytics: Analytics;
  systemStatus: SystemStatus;
  apiStatus: ApiStatus;
};

export function TopBar({ analytics, systemStatus, apiStatus }: TopBarProps) {
  const freeCapital = analytics.capital - analytics.usedCapital;
  const systemColor = systemStatus === 'LIVE' ? 'text-accent' : 'text-warning';
  const apiColor = apiStatus === 'CONNECTED' ? 'text-accent' : 'text-danger';

  return (
    <header className="glass relative overflow-hidden rounded-2xl px-5 py-4">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-electric to-transparent" />
      <div className="grid gap-4 md:grid-cols-3">
        <div className="space-y-1">
          <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">System Status</p>
          <p className={`text-lg font-bold ${systemColor}`} style={{ fontFamily: 'var(--font-space)' }}>
            {systemStatus}
          </p>
        </div>
        <div className="space-y-1">
          <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">API Connectivity</p>
          <p className={`text-lg font-bold ${apiColor}`} style={{ fontFamily: 'var(--font-space)' }}>
            {apiStatus}
          </p>
        </div>
        <div className="space-y-1 text-right">
          <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Capital Overview</p>
          <p className="text-lg font-bold text-white" style={{ fontFamily: 'var(--font-space)' }}>
            ${analytics.capital.toLocaleString()}
          </p>
          <p className="text-xs text-zinc-400">
            Used ${analytics.usedCapital.toLocaleString()} · Free ${freeCapital.toLocaleString()}
          </p>
        </div>
      </div>
    </header>
  );
}
