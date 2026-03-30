import { FormEvent, useState } from 'react';

export type ApiKeysFormValues = {
  binance_api_key: string;
  binance_api_secret: string;
  bybit_api_key: string;
  bybit_api_secret: string;
  kucoin_api_key: string;
  kucoin_api_secret: string;
  kucoin_api_passphrase: string;
  gateio_api_key: string;
  gateio_api_secret: string;
  cmc_api_key: string;
  telegram_bot_token: string;
  telegram_chat_id: string;
};

type ApiKeysPanelProps = {
  onSave: (values: ApiKeysFormValues) => Promise<void>;
};

const defaultValues: ApiKeysFormValues = {
  binance_api_key: '',
  binance_api_secret: '',
  bybit_api_key: '',
  bybit_api_secret: '',
  kucoin_api_key: '',
  kucoin_api_secret: '',
  kucoin_api_passphrase: '',
  gateio_api_key: '',
  gateio_api_secret: '',
  cmc_api_key: '',
  telegram_bot_token: '',
  telegram_chat_id: ''
};

export function ApiKeysPanel({ onSave }: ApiKeysPanelProps) {
  const [values, setValues] = useState<ApiKeysFormValues>(defaultValues);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const updateValue = (key: keyof ApiKeysFormValues, value: string) => {
    setValues((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setStatus(null);
    try {
      await onSave(values);
      setStatus('تم حفظ المفاتيح بنجاح');
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'فشل حفظ المفاتيح');
    } finally {
      setLoading(false);
    }
  };

  const inputClass =
    'w-full rounded-lg border border-zinc-700 bg-zinc-900/80 px-3 py-2 text-xs text-white outline-none transition focus:border-accent';

  return (
    <section className="glass rounded-2xl p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-[0.24em] text-zinc-400">API Keys</h2>
      <form className="space-y-2" onSubmit={handleSubmit}>
        <input className={inputClass} type="password" placeholder="Binance API Key" value={values.binance_api_key} onChange={(e) => updateValue('binance_api_key', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Binance API Secret" value={values.binance_api_secret} onChange={(e) => updateValue('binance_api_secret', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Bybit API Key" value={values.bybit_api_key} onChange={(e) => updateValue('bybit_api_key', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Bybit API Secret" value={values.bybit_api_secret} onChange={(e) => updateValue('bybit_api_secret', e.target.value)} />
        <input className={inputClass} type="password" placeholder="KuCoin API Key" value={values.kucoin_api_key} onChange={(e) => updateValue('kucoin_api_key', e.target.value)} />
        <input className={inputClass} type="password" placeholder="KuCoin API Secret" value={values.kucoin_api_secret} onChange={(e) => updateValue('kucoin_api_secret', e.target.value)} />
        <input className={inputClass} type="password" placeholder="KuCoin Passphrase" value={values.kucoin_api_passphrase} onChange={(e) => updateValue('kucoin_api_passphrase', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Gate.io API Key" value={values.gateio_api_key} onChange={(e) => updateValue('gateio_api_key', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Gate.io API Secret" value={values.gateio_api_secret} onChange={(e) => updateValue('gateio_api_secret', e.target.value)} />
        <input className={inputClass} type="password" placeholder="CMC API Key" value={values.cmc_api_key} onChange={(e) => updateValue('cmc_api_key', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Telegram Bot Token" value={values.telegram_bot_token} onChange={(e) => updateValue('telegram_bot_token', e.target.value)} />
        <input className={inputClass} type="password" placeholder="Telegram Chat ID" value={values.telegram_chat_id} onChange={(e) => updateValue('telegram_chat_id', e.target.value)} />
        <button
          type="submit"
          disabled={loading}
          className="mt-2 w-full rounded-lg bg-electric py-2 text-sm font-bold text-black transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'جاري الحفظ...' : 'حفظ المفاتيح'}
        </button>
      </form>
      {status && <p className="mt-2 text-xs text-zinc-300">{status}</p>}
    </section>
  );
}
