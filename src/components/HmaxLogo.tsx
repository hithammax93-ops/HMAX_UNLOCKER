import React from 'react';

interface HmaxLogoProps {
  className?: string;
  size?: number | string;
  showText?: boolean;
}

export const HmaxLogo: React.FC<HmaxLogoProps> = ({
  className = 'w-10 h-10',
  size,
  showText = false,
}) => {
  return (
    <div className={`relative flex items-center gap-2.5 ${showText ? '' : 'justify-center'}`}>
      <img
        src="/logo.svg"
        alt="HMAX-Unlocker Logo"
        width={size}
        height={size}
        className={`object-contain drop-shadow-[0_0_12px_rgba(0,180,255,0.4)] ${className}`}
        loading="eager"
      />
      {showText && (
        <div className="leading-tight select-none">
          <div className="text-sm font-black tracking-tight flex items-center gap-1">
            <span className="text-white">HMAX</span>
            <span className="text-[#00b4ff]">-</span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#ffd768] to-[#e6b83b]">Unlocker</span>
          </div>
          <span className="text-[10px] text-slate-400 font-medium block">متجر السوفت وير الشامل</span>
        </div>
      )}
    </div>
  );
};
