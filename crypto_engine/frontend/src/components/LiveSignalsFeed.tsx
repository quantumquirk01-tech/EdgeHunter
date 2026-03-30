import { Signal } from '../types/trading';
import { SignalCard } from './SignalCard';

type LiveSignalsFeedProps = {
  signals: Signal[];
  focusedSignalId: string | null;
  onFocusSignal: (id: string) => void;
  onExecute: (signal: Signal) => void;
};

export function LiveSignalsFeed({ signals, focusedSignalId, onFocusSignal, onExecute }: LiveSignalsFeedProps) {
  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-[0.28em] text-zinc-400">Launchpool Feed</h2>
        <p className="text-xs text-zinc-500">{signals.length} launchpool opportunities</p>
      </div>
      <div className="grid auto-rows-fr items-start gap-3 2xl:grid-cols-2">
        {signals.map((signal) => (
          <SignalCard
            key={signal.id}
            signal={signal}
            focused={focusedSignalId === signal.id}
            onFocus={() => onFocusSignal(signal.id)}
            onExecute={() => onExecute(signal)}
          />
        ))}
      </div>
    </section>
  );
}
