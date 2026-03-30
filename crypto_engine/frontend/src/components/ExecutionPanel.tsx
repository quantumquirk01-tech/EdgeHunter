import { useMemo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Signal } from '../types/trading';

type ExecutionPanelProps = {
  signal: Signal | null;
  capital: number;
  onClose: () => void;
};

export function ExecutionPanel({ signal, capital, onClose }: ExecutionPanelProps) {
  const [orderType, setOrderType] = useState<'MARKET' | 'LIMIT'>('LIMIT');
  const [amountPct, setAmountPct] = useState(24);

  const amount = useMemo(() => (capital * amountPct) / 100, [amountPct, capital]);
  const projectedSlippage = useMemo(() => {
    if (!signal) {
      return 0;
    }
    return Number((signal.slippage * (orderType === 'MARKET' ? 1.35 : 0.78)).toFixed(2));
  }, [signal, orderType]);

  return (
    <AnimatePresence>
      {signal && (
        <motion.aside
          initial={{ opacity: 0, x: 26 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 26 }}
          transition={{ duration: 0.2 }}
          className="glass sticky top-4 h-fit space-y-4 rounded-2xl p-4"
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Execution Panel</p>
              <h3 className="text-lg font-bold text-white" style={{ fontFamily: 'var(--font-space)' }}>
                {signal.token} · {signal.exchange}
              </h3>
            </div>
            <button type="button" onClick={onClose} className="text-sm text-zinc-400 hover:text-white">
              Close
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 rounded-xl bg-black/35 p-2">
            <button
              type="button"
              onClick={() => setOrderType('LIMIT')}
              className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${orderType === 'LIMIT' ? 'bg-electric text-black' : 'bg-zinc-800 text-zinc-300'}`}
            >
              Limit
            </button>
            <button
              type="button"
              onClick={() => setOrderType('MARKET')}
              className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${orderType === 'MARKET' ? 'bg-warning text-black' : 'bg-zinc-800 text-zinc-300'}`}
            >
              Market
            </button>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs text-zinc-400">
              <span>Amount Allocation</span>
              <span>{amountPct}%</span>
            </div>
            <input
              type="range"
              min={2}
              max={100}
              value={amountPct}
              onChange={(event) => setAmountPct(Number(event.target.value))}
              className="h-2 w-full cursor-pointer appearance-none rounded-full bg-zinc-800 accent-accent"
            />
            <p className="text-sm font-semibold text-white">${amount.toFixed(0)}</p>
          </div>

          <div className="rounded-xl bg-black/35 p-3">
            <p className="text-xs text-zinc-400">Slippage Preview</p>
            <p className={`text-lg font-bold ${projectedSlippage > 1.2 ? 'text-warning' : 'text-accent'}`}>
              {projectedSlippage}%
            </p>
          </div>

          <button
            type="button"
            className="w-full rounded-xl bg-accent py-3 text-base font-bold text-black shadow-neon transition duration-150 hover:brightness-110"
          >
            Confirm {orderType} Order
          </button>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
