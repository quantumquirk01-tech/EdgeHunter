import { HeatmapCell } from '../types/trading';

type HeatmapSectionProps = {
  cells: HeatmapCell[];
};

export function HeatmapSection({ cells }: HeatmapSectionProps) {
  return (
    <section className="space-y-3">
      <h2 className="text-sm font-semibold uppercase tracking-[0.28em] text-zinc-400">Momentum Heatmap</h2>
      <div className="glass rounded-2xl p-3">
        <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
          {cells.map((cell) => {
            const alpha = 0.14 + cell.intensity * 0.75;
            const border = 0.2 + cell.momentum * 0.45;
            return (
              <div
                key={cell.symbol}
                className="rounded-lg px-2 py-2 text-center"
                style={{
                  background: `rgba(0, 255, 159, ${alpha})`,
                  border: `1px solid rgba(0, 194, 255, ${border})`
                }}
              >
                <p className="text-sm font-semibold text-black">{cell.symbol}</p>
                <p className="text-[11px] text-black/80">{Math.round(cell.momentum * 100)}%</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
