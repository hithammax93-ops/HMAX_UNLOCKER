import React, { useRef } from 'react';
import { X, Printer, Check, Smartphone, Calendar, DollarSign, ShieldCheck, QrCode } from 'lucide-react';

export interface ReceiptData {
  ticketId: string;
  clientName: string;
  clientPhone: string;
  deviceModel: string;
  issue: string;
  price: string;
  date: string;
  status: string;
}

interface CustomerReceiptModalProps {
  receipt: ReceiptData;
  onClose: () => void;
}

export const CustomerReceiptModal: React.FC<CustomerReceiptModalProps> = ({ receipt, onClose }) => {
  const receiptRef = useRef<HTMLDivElement>(null);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl flex flex-col max-h-[92vh]">
        {/* Modal Header (Hidden in Print) */}
        <div className="print:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-slate-950/70">
          <div className="flex items-center gap-2">
            <Printer className="w-5 h-5 text-[#00b4ff]" />
            <h3 className="text-sm font-black text-white">معاينة وطباعة وصل استلام الجهاز</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* The Printable Thermal Receipt Container */}
        <div className="overflow-y-auto p-4 sm:p-6 bg-slate-900">
          <div
            ref={receiptRef}
            id="printable-receipt"
            className="bg-white text-black p-5 rounded-2xl shadow-inner font-mono text-xs border border-slate-200 print:border-none print:shadow-none print:m-0 print:p-2"
            style={{ width: '100%', maxWidth: '320px', margin: '0 auto' }}
          >
            {/* Thermal Slip Header */}
            <div className="text-center pb-3 border-b border-dashed border-black/40">
              <h2 className="text-base font-black tracking-tight">HMAX SERVICE CENTER</h2>
              <p className="text-[10px] text-gray-700 font-sans mt-0.5">مركز هيثم ماكس لبرمجة وصيانة الهواتف</p>
              <p className="text-[9px] text-gray-500 font-sans mt-0.5">صنعاء - اليمن • واتساب: 772773388</p>
            </div>

            {/* Ticket Identifier */}
            <div className="py-2.5 border-b border-dashed border-black/40 space-y-1">
              <div className="flex justify-between items-center text-[11px]">
                <span className="font-bold">رقم الفاتورة:</span>
                <span className="font-bold font-sans">#{receipt.ticketId.slice(-6)}</span>
              </div>
              <div className="flex justify-between items-center text-[10px] text-gray-600">
                <span>تاريخ الاستلام:</span>
                <span>{receipt.date}</span>
              </div>
            </div>

            {/* Device & Client Details */}
            <div className="py-3 border-b border-dashed border-black/40 space-y-2">
              <div>
                <span className="text-[9px] text-gray-500 block">اسم العميل:</span>
                <span className="font-bold text-[11px] font-sans block">{receipt.clientName}</span>
                {receipt.clientPhone && (
                  <span className="text-[10px] text-gray-700 font-mono block" dir="ltr">{receipt.clientPhone}</span>
                )}
              </div>

              <div>
                <span className="text-[9px] text-gray-500 block">موديل الجهاز:</span>
                <span className="font-bold text-[11px] font-sans block text-blue-900">{receipt.deviceModel}</span>
              </div>

              <div>
                <span className="text-[9px] text-gray-500 block">العطل المسجل:</span>
                <span className="font-sans text-[10px] block leading-tight text-gray-800">{receipt.issue}</span>
              </div>
            </div>

            {/* Cost & Total */}
            <div className="py-3 border-b border-dashed border-black/40">
              <div className="flex justify-between items-center text-sm font-black">
                <span>المبلغ المتفق عليه:</span>
                <span className="text-emerald-800">{receipt.price}</span>
              </div>
              <div className="flex justify-between items-center text-[10px] text-gray-600 mt-1">
                <span>حالة الجهاز:</span>
                <span className="font-bold font-sans">
                  {receipt.status === 'ready' ? 'جاهز للتسليم' : receipt.status === 'delivered' ? 'مستلم' : 'قيد الصيانة والبرمجة'}
                </span>
              </div>
            </div>

            {/* Simulated Barcode */}
            <div className="pt-3 text-center space-y-1.5">
              <div className="inline-block px-3 py-1 bg-black text-white text-[9px] font-bold tracking-widest rounded">
                *HMAX-{receipt.ticketId.slice(-6)}*
              </div>
              <p className="text-[8px] text-gray-500 font-sans leading-relaxed">
                * تنبيه: المركز غير مسؤول عن الأجهزة التي لا يستلمها أصحابها بعد مرور 30 يوماً من تاريخ الإبلاغ.
              </p>
              <p className="text-[9px] font-bold text-gray-800 font-sans">شكراً لثقتكم بخدماتنا!</p>
            </div>
          </div>
        </div>

        {/* Modal Actions Footer (Hidden in Print) */}
        <div className="print:hidden flex items-center justify-between p-4 border-t border-slate-800 bg-slate-950/70 gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition"
          >
            إغلاق
          </button>
          <button
            onClick={handlePrint}
            className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-black text-xs flex items-center gap-1.5 transition shadow-lg"
          >
            <Printer className="w-4 h-4" />
            <span>طباعة الوصل الحراري (80mm)</span>
          </button>
        </div>
      </div>
    </div>
  );
};
