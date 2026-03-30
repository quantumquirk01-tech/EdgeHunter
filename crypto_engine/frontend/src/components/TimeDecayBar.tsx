type TimeDecayBarProps = {
  seconds: number;
  maxSeconds?: number;
};

export function TimeDecayBar({ seconds, maxSeconds = 30 }: TimeDecayBarProps) {
  const remaining = Math.max(0, maxSeconds - seconds);
  const ratio = remaining / maxSeconds;
  const width = `${Math.max(4, ratio * 100)}%`;
  const color = ratio > 0.55 ? '#00FF9F' : ratio > 0.3 ? '#FF9F1C' : '#FF3B3B';

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-[11px] text-zinc-400">
        <span>Edge Decay</span>
        <span>{remaining.toFixed(0)}s</span>
      </div>
      <div className="h-2.5 overflow-hidden rounded-full bg-zinc-900">
        <div
          className="h-full rounded-full"
          style={{ background: color, width }}
        />
      </div>
    </div>
  );
}
