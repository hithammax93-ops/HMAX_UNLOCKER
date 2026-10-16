import React, { useState } from 'react';
import { Calculator, DollarSign, TrendingUp, Clock, AlertCircle, Sparkles, Check } from 'lucide-react';
import { GSM_SERVICES_CATALOG, GsmServiceItem } from '../data/gsmPricingData';

interface GsmPricingCalculatorProps {
  onCopyToast: (msg: string) => void;
}

export const GsmPricingCalculator: React.FC<GsmPricingCalculatorProps> = ({ onCopyToast }) => {
  const [selectedServiceId, setSelectedServiceId] = useState<string>('srv-frp-samsung');
  const [customerPrice, setCustomerPrice] = useState<number>(15);
  const [serverCreditCost, setServerCreditCost] = useState<number>(0);
  const [currency, setCurrency] = useState<'USD' | 'YER' | 'SAR'>('USD');
  const [exchangeRateToYER, setExchangeRateToYER] = useState<number>(535); // 1 USD = 535 YER or custom

  const service = GSM_SERVICES_CATALOG.find((s) => s.id === selectedServiceId) || GSM_SERVICES_CATALOG[0];

  const handleSelectService = (id: string) => {
    setSelectedServiceId(id);
    const item = GSM_SERVICES_CATALOG.find((s) => s.id === id);
    if (item) {
      setCustomerPrice(item.suggestedCustomerPrice);
      setServerCreditCost(item.defaultCost);
    }
  };

  const netProfit = Math.max(0, customerPrice - serverCreditCost);
  const profitMargin = customerPrice > 0 ? Math.round((netProfit / customerPrice) * 100) : 0;

  const priceInYER = currency === 'USD' ? customerPrice * exchangeRateToYER : customerPrice;
  const profitInYER = currency === 'USD' ? netProfit * exchangeRateToYER : netProfit;

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="p-5 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/40 border border-slate-800 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold">
          <Calculator className="w-3.5 h-3.5" />
          <span>حاسبة تسعير خدمات السوفت وير والأرباح — GSM Profit & Pricing Estimator</span>
        </div>
        <h2 className="text-lg font-black text-white">
          تقدير السعر العادل للزبون وحساب التكاليف وصافي الأرباح لعمليات البرمجة
        </h2>
        <p className="text-xs text-slate-400 leading-relaxed max-w-3xl">
          أداة مالية صُممت خصيصاً لأصحاب محلات الصيانة وفنيي السوفت وير لحساب تكلفة رصيد السيرفرات (Credits / Tokens) ومقارنتها بسعر السوق المحلي وحساب صافي الأرباح بالدولار والريال اليمني أو السعودي.
        </p>
      </div>

      {/* Main Calculator Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Step 1: Select Service */}
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3 text-xs">
          <h3 className="font-bold text-white flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-slate-800 text-amber-400 flex items-center justify-center font-mono">1</span>
            <span>اختر نوع العملية البرمجية</span>
          </h3>

          <div className="space-y-1.5 max-h-72 overflow-y-auto pr-1">
            {GSM_SERVICES_CATALOG.map((item) => (
              <button
                key={item.id}
                onClick={() => handleSelectService(item.id)}
                className={`w-full text-right p-2.5 rounded-xl border transition flex flex-col justify-between ${
                  selectedServiceId === item.id
                    ? 'bg-amber-500/15 border-amber-500/50 text-white shadow-md'
                    : 'bg-slate-950 border-slate-800/80 text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <strong className="text-xs">{item.name}</strong>
                  <span className="text-[10px] text-amber-400 font-mono font-bold">${item.suggestedCustomerPrice}</span>
                </div>
                <span className="text-[10px] text-slate-500 mt-1 line-clamp-1">{item.notes}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Pricing Adjustments */}
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3 text-xs">
          <h3 className="font-bold text-white flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-slate-800 text-amber-400 flex items-center justify-center font-mono">2</span>
            <span>ضبط التكلفة والسعر للزبون</span>
          </h3>

          <div>
            <label className="text-slate-400 block mb-1">العملة الأساسية:</label>
            <div className="grid grid-cols-3 gap-1.5">
              {(['USD', 'YER', 'SAR'] as const).map((c) => (
                <button
                  key={c}
                  type="button"
                  onClick={() => setCurrency(c)}
                  className={`py-1.5 rounded-lg font-bold transition text-xs ${
                    currency === c ? 'bg-amber-400 text-black' : 'bg-slate-950 text-slate-400 border border-slate-800'
                  }`}
                >
                  {c === 'USD' ? 'دولار ($)' : c === 'YER' ? 'ريال يمني' : 'ريال سعودي'}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-slate-400 block mb-1">سعر الخدمة النهائي للزبون ({currency}):</label>
            <input
              type="number"
              value={customerPrice}
              onChange={(e) => setCustomerPrice(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-white font-mono text-base font-black focus:outline-none focus:border-amber-400"
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">تكلفة كريدت السيرفر / الفلاشة ({currency}):</label>
            <input
              type="number"
              value={serverCreditCost}
              onChange={(e) => setServerCreditCost(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 font-mono text-sm focus:outline-none focus:border-amber-400"
            />
            <span className="text-[10px] text-slate-500 mt-1 block">
              ضع 0 إذا كانت الأداة مجانية أو تملك تفعيلها سنوياً بدون كريدت.
            </span>
          </div>

          {currency === 'USD' && (
            <div>
              <label className="text-slate-400 block mb-1">سعر صرف الدولار بالريال اليمني:</label>
              <input
                type="number"
                value={exchangeRateToYER}
                onChange={(e) => setExchangeRateToYER(parseFloat(e.target.value) || 535)}
                className="w-full px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 font-mono text-xs focus:outline-none focus:border-amber-400"
              />
            </div>
          )}
        </div>

        {/* Step 3: Profit Output Breakdown */}
        <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-950 to-slate-900 border border-amber-500/30 space-y-4 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              ملخص الأرباح والجدوى
            </span>
            <h4 className="text-sm font-black text-white mt-2">{service.name}</h4>

            <div className="mt-4 space-y-3">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
                <span className="text-xs text-slate-400">صافي ربح المحل:</span>
                <span className="text-lg font-black text-emerald-400 font-mono">
                  {currency === 'USD' ? `$${netProfit.toFixed(2)}` : `${netProfit} ${currency}`}
                </span>
              </div>

              {currency === 'USD' && (
                <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 flex justify-between items-center text-xs">
                  <span className="text-slate-400">المعادل بالريال اليمني:</span>
                  <span className="text-white font-mono font-bold">
                    {profitInYER.toLocaleString()} ريال
                  </span>
                </div>
              )}

              <div className="flex justify-between items-center text-xs px-1 text-slate-400">
                <span>هامش الربح الصافي:</span>
                <span className="text-amber-400 font-bold font-mono text-sm">{profitMargin}%</span>
              </div>

              <div className="flex justify-between items-center text-xs px-1 text-slate-400">
                <span>الوقت التقديري للعملية:</span>
                <span className="text-slate-300 font-bold">
                  {service.durationMins >= 60 ? `${Math.round(service.durationMins / 60)} ساعة` : `${service.durationMins} دقيقة`}
                </span>
              </div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/20 text-[11px] text-slate-300">
            💡 نصيحة تسعير: {service.notes}
          </div>
        </div>
      </div>
    </div>
  );
};
