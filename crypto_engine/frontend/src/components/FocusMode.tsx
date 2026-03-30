import { AnimatePresence, motion } from 'framer-motion';
import { MouseEvent } from 'react';
import { Signal } from '../types/trading';
import { ScoreRing } from './ScoreRing';
import { Sparkline } from './Sparkline';
import { TimeDecayBar } from './TimeDecayBar';

type FocusModeProps = {
  signal: Signal | null;
  onClose: () => void;
  onExecute: () => void;
};

export function FocusMode({ signal, onClose, onExecute }: FocusModeProps) {
  return (
    <AnimatePresence>
      {signal && (
        <motion.div
          className="fixed inset-0 z-40 flex items-center justify-center bg-black/75 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          onClick={onClose}
        >
          <motion.div
            className="glass w-full max-w-2xl rounded-2xl p-5"
            initial={{ scale: 0.95, y: 16 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.95, y: 10 }}
            transition={{ duration: 0.2 }}
            onClick={(event: MouseEvent<HTMLDivElement>) => event.stopPropagation()}
          >
            <div className="mb-4 flex items-start justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.22em] text-zinc-400">Focus Mode</p>
                <h3 className="text-2xl font-bold text-white" style={{ fontFamily: 'var(--font-space)' }}>
                  {signal.token} · {signal.exchange}
                </h3>
                <p className="text-sm text-zinc-400">{signal.eventType}</p>
              </div>
              <ScoreRing value={signal.score} size={96} />
            </div>

            <div className="mb-3 rounded-xl border border-white/5 bg-black/30 p-2">
              <Sparkline data={signal.sparkline} positive={signal.decision !== 'IGNORE'} />
            </div>

            <div className="mb-4 grid grid-cols-3 gap-2">
              <div className="rounded-lg bg-black/35 p-2">
                <p className="text-xs text-zinc-500">Decision</p>
                <p className="text-sm font-semibold text-accent">{signal.decision}</p>
              </div>
              <div className="rounded-lg bg-black/35 p-2">
                <p className="text-xs text-zinc-500">Liquidity</p>
                <p className="text-sm font-semibold text-white">${signal.liquidityUsd.toLocaleString()}</p>
              </div>
              <div className="rounded-lg bg-black/35 p-2">
                <p className="text-xs text-zinc-500">Slippage</p>
                <p className="text-sm font-semibold text-white">{signal.slippage.toFixed(2)}%</p>
              </div>
            </div>

            <TimeDecayBar seconds={(Date.now() - signal.detectedAt) / 1000} />

            <div className="mt-4 flex gap-2">
              <button
                type="button"
                onClick={onExecute}
                className="flex-1 rounded-lg bg-accent py-3 text-sm font-bold text-black transition hover:brightness-110"
              >
                Execute Now
              </button>
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg border border-zinc-700 px-4 py-3 text-sm font-semibold text-zinc-300"
              >
                Close
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
