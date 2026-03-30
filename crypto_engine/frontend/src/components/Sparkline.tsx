type SparklineProps = {
  data: number[];
  positive?: boolean;
};

export function Sparkline({ data, positive = true }: SparklineProps) {
  const width = 160;
  const height = 52;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const span = Math.max(max - min, 0.1);

  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * width;
      const y = height - ((value - min) / span) * height;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="h-14 w-full">
      <polyline
        points={points}
        fill="none"
        stroke={positive ? '#00C2FF' : '#FF3B3B'}
        strokeWidth="2.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
