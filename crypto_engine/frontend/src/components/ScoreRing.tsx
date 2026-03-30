type ScoreRingProps = {
  value: number;
  size?: number;
};

export function ScoreRing({ value, size = 84 }: ScoreRingProps) {
  const clamped = Math.max(0, Math.min(10, value));
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (clamped / 10) * circumference;
  const color = clamped >= 8 ? '#00FF9F' : clamped >= 5 ? '#FF9F1C' : '#8F8F8F';

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="#2B2B2B" strokeWidth="8" fill="none" />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth="8"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
        />
      </svg>
      <div className="absolute flex flex-col items-center leading-none">
        <span className="font-bold text-white" style={{ fontFamily: 'var(--font-space)' }}>
          {clamped.toFixed(1)}
        </span>
        <span className="text-[10px] text-zinc-400">SCORE</span>
      </div>
    </div>
  );
}
