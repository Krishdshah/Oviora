import React from "react";

export function LabAnalyzerHeader() {
  return (
    <header className="flex flex-col sm:flex-row sm:items-end justify-between gap-md mb-sm">
      <div className="max-w-2xl">
        <div className="mb-xs">
          <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
            AI CLINICAL LABS
          </span>
        </div>
        <h2 className="font-display-hero text-[32px] md:text-[40px] text-primary font-bold mb-xs">
          Lab Report Analyzer
        </h2>
        <p className="font-body-main text-on-surface-variant leading-relaxed">
          Transform your complex medical blood reports into clear, actionable health insights. Our AI clinically validates markers against PCOS-specific healthy ranges.
        </p>
      </div>
      <button className="flex items-center justify-center gap-xs px-md py-sm bg-white text-primary border border-primary/25 rounded-full font-label-caps text-[11px] font-bold shadow-sm hover:bg-primary-fixed/20 transition-all shrink-0">
        <span className="material-symbols-outlined text-[16px]">history</span>
        Past Analysis Reports
      </button>
    </header>
  );
}
