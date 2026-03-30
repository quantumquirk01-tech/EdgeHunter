import { ScoreRing } from './ScoreRing';
import { Sparkline } from './Sparkline';
import { TimeDecayBar } from './TimeDecayBar';
import { Signal } from '../types/trading';

type SignalCardProps = {
  signal: Signal;
  focused: boolean;
  onFocus: () => void;
  onExecute: () => void;
};

const decisionStyles: Record<Signal['decision'], string> = {
  ENTER: 'bg-accent/15 text-accent border border-accent/45',
  WATCH: 'bg-warning/15 text-warning border border-warning/45',
  IGNORE: 'bg-zinc-800 text-zinc-400 border border-zinc-700'
};

export function SignalCard({ signal, focused, onFocus, onExecute }: SignalCardProps) {
  const ageSeconds = (Date.now() - signal.detectedAt) / 1000;
  const liquidityLabel = signal.liquidityUsd > 1_000_000 ? 'Ultra' : signal.liquidityUsd > 300_000 ? 'Strong' : 'Thin';
  const eventTime =
    Number.isFinite(signal.eventTimestamp) && signal.eventTimestamp > 0
      ? new Date(signal.eventTimestamp).toLocaleString()
      : 'N/A';

  return (
    <article
      onClick={onFocus}
      className={`glass relative isolate min-h-[380px] cursor-pointer overflow-hidden rounded-2xl p-4 ${focused ? 'border-accent/60 bg-accent/5' : 'border-white/10'}`}
    >
      <div className="relative space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-accent bg-accent/10 px-1.5 py-0.5 rounded">المنصة: {signal.exchange}</span>
            </div>
            <h3 className="mt-1 text-2xl font-black text-white" style={{ fontFamily: 'var(--font-space)' }}>
              {signal.token}
            </h3>
            <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-widest">{signal.eventType}</p>
          </div>
          <ScoreRing value={signal.score} />
        </div>

        <div className="space-y-3 rounded-xl border border-white/5 bg-black/40 p-4">
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">شرح الحدث</p>
            <p className="mt-1.5 text-xs leading-relaxed text-zinc-200">{signal.eventSummary}</p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 border-t border-white/5 pt-3">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">المنصة</p>
              <p className="mt-0.5 text-sm font-semibold text-white">{signal.exchange}</p>
            </div>
            <div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-zinc-500">التوقيت</p>
              <p className="mt-0.5 text-sm font-semibold text-white">{eventTime}</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-2">
          <div className="rounded-lg bg-black/35 p-2 border border-white/5">
            <p className="text-[10px] font-bold text-zinc-500 uppercase">Detected</p>
            <p className="text-sm font-bold text-white">{ageSeconds.toFixed(1)}s</p>
          </div>
          <div className="rounded-lg bg-black/35 p-2 border border-white/5">
            <p className="text-[10px] font-bold text-zinc-500 uppercase">Liquidity</p>
            <p className="text-sm font-bold text-white">{liquidityLabel}</p>
          </div>
          <div className="rounded-lg bg-black/35 p-2 border border-white/5">
            <p className="text-[10px] font-bold text-zinc-500 uppercase">Slippage</p>
            <p className="text-sm font-bold text-white">{signal.slippage.toFixed(2)}%</p>
          </div>
        </div>

        <div className="rounded-xl border border-white/5 bg-black/30 p-2">
          <Sparkline data={signal.sparkline} positive={signal.decision !== 'IGNORE'} />
        </div>

        <TimeDecayBar seconds={ageSeconds} />

        <div className="flex items-center justify-between gap-3 pt-2">
          <span className={`rounded-lg px-4 py-1.5 text-[11px] font-black uppercase tracking-tighter ${decisionStyles[signal.decision]}`}>
            {signal.decision}
          </span>
          <button
            type="button"
            onClick={(event) => {
              event.stopPropagation();
              onExecute();
            }}
            className="rounded-lg bg-accent px-5 py-2 text-xs font-black text-black hover:brightness-110 active:scale-95 transition-none"
          >
            EXECUTE
          </button>
        </div>
      </div>
    </article>
  );
}
