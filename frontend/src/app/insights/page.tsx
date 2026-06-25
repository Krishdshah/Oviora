"use client";

import Link from "next/link";

export default function Insights() {
  return (
    <div className="px-lg py-xl max-w-6xl mx-auto flex flex-col gap-lg">
      
      {/* Page Header */}
      <section className="mb-sm">
        <div className="mb-xs">
          <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
            INTELLIGENCE INSIGHTS
          </span>
        </div>
        <h1 className="font-display-hero text-[32px] md:text-[40px] text-on-surface font-bold tracking-tight mb-xs">
          Hormonal Intelligence Trends
        </h1>
        <p className="font-body-main text-on-surface-variant max-w-2xl leading-relaxed">
          Detailed patterns of your hormonal health based on daily logging and physiological metrics. Your data suggests a stabilizing progesterone trend.
        </p>
      </section>

      {/* Insight Stats Row */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-md mb-sm">
        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between shadow-sm border-l-4 border-primary">
          <span className="font-label-caps text-[10px] font-bold text-primary uppercase">Cycle Phase</span>
          <div className="flex items-end justify-between mt-md">
            <span className="text-xl font-bold text-on-surface">Late Luteal</span>
            <span className="text-[12px] text-on-surface-variant">Day 24 of 28</span>
          </div>
        </div>
        
        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between shadow-sm border-l-4 border-tertiary">
          <span className="font-label-caps text-[10px] font-bold text-tertiary uppercase">Avg Symptom Intensity</span>
          <div className="flex items-end justify-between mt-md">
            <span className="text-xl font-bold text-on-surface">Moderate</span>
            <span className="text-error flex items-center gap-0.5 text-[12px] font-bold">
              <span className="material-symbols-outlined text-[14px]">trending_up</span> 12%
            </span>
          </div>
        </div>

        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between shadow-sm border-l-4 border-primary-container">
          <span className="font-label-caps text-[10px] font-bold text-primary-container uppercase">Metabolic Health</span>
          <div className="flex items-end justify-between mt-md">
            <span className="text-xl font-bold text-on-surface">Optimal</span>
            <span className="text-tertiary flex items-center gap-0.5 text-[12px] font-bold">
              <span className="material-symbols-outlined text-[14px]">check_circle</span> Stable
            </span>
          </div>
        </div>
      </section>

      {/* Bento Grid Trends */}
      <div className="bento-grid">
        
        {/* Hormone Trends (Large SVG line chart) */}
        <div className="col-span-12 lg:col-span-8 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <div className="flex flex-col sm:flex-row justify-between items-start gap-sm mb-lg">
              <div>
                <h3 className="font-title-card text-title-card font-semibold text-on-surface">Hormone Trends</h3>
                <p className="text-[12px] text-on-surface-variant mt-0.5">Progesterone vs Estrogen Ratio</p>
              </div>
              <div className="flex gap-xs">
                <span className="flex items-center gap-xs px-sm py-1 bg-primary/10 text-primary rounded-full text-[11px] font-bold">
                  <span className="w-2 h-2 rounded-full bg-primary"></span> Estrogen
                </span>
                <span className="flex items-center gap-xs px-sm py-1 bg-tertiary/10 text-tertiary rounded-full text-[11px] font-bold">
                  <span className="w-2 h-2 rounded-full bg-tertiary"></span> Progesterone
                </span>
              </div>
            </div>
            
            {/* SVG Line Chart */}
            <div className="relative h-56 w-full mt-md">
              <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 800 200">
                <defs>
                  <linearGradient id="estrogenGrad" x1="0%" x2="0%" y1="0%" y2="100%">
                    <stop offset="0%" stopColor="rgba(153, 71, 17, 0.15)" />
                    <stop offset="100%" stopColor="rgba(153, 71, 17, 0)" />
                  </linearGradient>
                </defs>
                {/* Grid Lines */}
                <line x1="0" y1="50" x2="800" y2="50" stroke="#f1dfd7" strokeWidth="1" strokeDasharray="4 4" />
                <line x1="0" y1="100" x2="800" y2="100" stroke="#f1dfd7" strokeWidth="1" strokeDasharray="4 4" />
                <line x1="0" y1="150" x2="800" y2="150" stroke="#f1dfd7" strokeWidth="1" strokeDasharray="4 4" />
                
                {/* Estrogen Curve (Orange) */}
                <path
                  d="M0,150 C50,140 100,160 150,140 S250,80 300,70 S400,110 450,120 S550,150 600,140 S750,120 800,130"
                  fill="none"
                  stroke="#994711"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                />
                <path
                  d="M0,150 C50,140 100,160 150,140 S250,80 300,70 S400,110 450,120 S550,150 600,140 S750,120 800,130 L800,200 L0,200 Z"
                  fill="url(#estrogenGrad)"
                />
                {/* Progesterone Curve (Teal Dashed) */}
                <path
                  d="M0,180 C100,185 200,170 300,150 S400,60 500,40 S650,20 800,30"
                  fill="none"
                  stroke="#00696c"
                  strokeDasharray="8 5"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                />
              </svg>
            </div>
          </div>
          
          <div className="w-full flex justify-between text-[9px] font-label-caps text-on-surface-variant/60 font-bold uppercase tracking-widest pt-sm border-t border-outline-variant/10 mt-md">
            <span>Week 1</span>
            <span>Week 2</span>
            <span>Week 3</span>
            <span>Week 4</span>
          </div>
        </div>

        {/* Weight Trends (Small SVG chart) */}
        <div className="col-span-12 lg:col-span-4 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <h3 className="font-title-card text-title-card font-semibold text-on-surface">Weight Trends</h3>
            <p className="text-[12px] text-on-surface-variant mt-0.5">Last 30 Days</p>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center my-md">
            <div className="text-4xl font-bold text-on-surface leading-none">
              -2.4<span className="text-lg font-medium text-on-surface-variant">kg</span>
            </div>
            <p className="text-tertiary font-bold flex items-center gap-xs mt-xs text-[11px] font-label-caps">
              <span className="material-symbols-outlined text-[16px]">check_circle</span> Trending Down
            </p>
          </div>
          
          <div className="h-16 w-full bg-surface-container-low/30 rounded-xl p-xs border border-outline-variant/10">
            <svg className="w-full h-full" viewBox="0 0 200 80">
              <path
                d="M0,50 L30,52 L60,45 L90,40 L120,46 L150,30 L200,22"
                fill="none"
                stroke="#f28c52"
                strokeWidth="3"
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>

        {/* Symptom Trends (Interactive lists/progress indicators) */}
        <div className="col-span-12 lg:col-span-5 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <div className="flex justify-between items-center mb-md">
              <h3 className="font-title-card text-title-card font-semibold text-on-surface">Symptom Intensity</h3>
              <Link href="/symptoms" className="text-primary text-[11px] font-bold font-label-caps hover:underline">
                Log New
              </Link>
            </div>
            
            <div className="space-y-sm">
              <div className="flex flex-col gap-base">
                <div className="flex justify-between text-[12px] text-on-surface-variant font-medium">
                  <span>Bloating</span>
                  <span className="text-primary font-bold">High (85%)</span>
                </div>
                <div className="w-full h-2 bg-surface-container-low rounded-full overflow-hidden border border-outline-variant/5">
                  <div className="h-full bg-primary w-[85%] rounded-full"></div>
                </div>
              </div>
              
              <div className="flex flex-col gap-base">
                <div className="flex justify-between text-[12px] text-on-surface-variant font-medium">
                  <span>Acne Flare-up</span>
                  <span className="text-primary-container font-bold">Moderate (45%)</span>
                </div>
                <div className="w-full h-2 bg-surface-container-low rounded-full overflow-hidden border border-outline-variant/5">
                  <div className="h-full bg-primary-container w-[45%] rounded-full"></div>
                </div>
              </div>

              <div className="flex flex-col gap-base">
                <div className="flex justify-between text-[12px] text-on-surface-variant font-medium">
                  <span>Energy Levels</span>
                  <span className="text-tertiary font-bold">Optimal (90%)</span>
                </div>
                <div className="w-full h-2 bg-surface-container-low rounded-full overflow-hidden border border-outline-variant/5">
                  <div className="h-full bg-tertiary w-[90%] rounded-full"></div>
                </div>
              </div>

              <div className="flex flex-col gap-base">
                <div className="flex justify-between text-[12px] text-on-surface-variant font-medium">
                  <span>Brain Fog</span>
                  <span className="text-tertiary-container font-bold">Low (15%)</span>
                </div>
                <div className="w-full h-2 bg-surface-container-low rounded-full overflow-hidden border border-outline-variant/5">
                  <div className="h-full bg-tertiary-container w-[15%] rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Cycle Prediction (Visual Ring + Metadata) */}
        <div className="col-span-12 lg:col-span-7 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300 relative overflow-hidden">
          <div className="relative z-10 flex flex-col justify-between h-full gap-md">
            <div>
              <h3 className="font-title-card text-title-card font-semibold text-on-surface">Cycle Insights</h3>
              <p className="text-[12px] text-on-surface-variant mt-0.5">Consistent 28-day cycle for 3 months.</p>
            </div>
            
            <div className="flex flex-col sm:flex-row items-center gap-lg">
              <div className="relative w-36 h-36 flex items-center justify-center shrink-0">
                <svg className="w-full h-full transform -rotate-90">
                  <circle
                    className="text-surface-container-low"
                    cx="72"
                    cy="72"
                    fill="transparent"
                    r="60"
                    stroke="currentColor"
                    strokeWidth="9"
                  />
                  <circle
                    className="text-primary"
                    cx="72"
                    cy="72"
                    fill="transparent"
                    r="60"
                    stroke="currentColor"
                    strokeDasharray="377"
                    strokeDashoffset="94" // ~75% complete
                    strokeLinecap="round"
                    strokeWidth="9"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-2xl font-bold text-on-surface">4</span>
                  <span className="text-[9px] font-label-caps text-on-surface-variant uppercase">Days Left</span>
                </div>
              </div>
              
              <div className="flex-grow grid grid-cols-2 gap-sm w-full">
                <div className="bg-surface-container-low/50 p-md rounded-xl border border-outline-variant/10">
                  <span className="text-[9px] uppercase font-bold text-on-surface-variant/70 block mb-0.5">Last Cycle</span>
                  <span className="font-bold text-on-surface text-sm">29 Days</span>
                </div>
                <div className="bg-surface-container-low/50 p-md rounded-xl border border-outline-variant/10">
                  <span className="text-[9px] uppercase font-bold text-on-surface-variant/70 block mb-0.5">Period Length</span>
                  <span className="font-bold text-on-surface text-sm">5 Days</span>
                </div>
                <div className="col-span-2 bg-primary-fixed/25 p-md rounded-xl border border-primary-fixed/30">
                  <p className="text-[12px] text-primary leading-snug">
                    <span className="font-bold">Pro Tip:</span> Based on your luteal phase trends, expect a slight dip in energy tomorrow. Plan rest accordingly.
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="absolute -bottom-6 -right-6 opacity-[0.08] transform rotate-12 pointer-events-none text-primary">
            <span className="material-symbols-outlined text-[130px]">calendar_month</span>
          </div>
        </div>

      </div>

      {/* Medical Intelligence Report */}
      <section className="mt-md bg-white border border-outline-variant/20 rounded-[32px] p-xl shadow-sm">
        <div className="flex flex-col md:flex-row gap-lg items-center justify-between">
          <div className="flex-grow max-w-3xl">
            <div className="flex items-center gap-xs mb-md">
              <span className="material-symbols-outlined text-tertiary">verified_user</span>
              <h2 className="font-title-section text-title-section font-semibold text-on-surface">
                Hormonal Analysis Report
              </h2>
            </div>
            
            <div className="space-y-md text-body-main text-on-surface-variant leading-relaxed text-[14px]">
              <p>
                Our AI Coach has analyzed your 90-day logged parameters. We noticed a 15% reduction in cycle length variance since starting your current supplement and spearmint tea regimen. Your Basal Body Temperature (BBT) spike consistently aligns with Day 14, confirming healthy ovulation patterns.
              </p>
              <div className="flex flex-wrap gap-xs pt-sm">
                <span className="px-md py-xs bg-tertiary-container/15 text-on-tertiary-container rounded-full text-[11px] font-bold border border-tertiary-container/20">
                  Stable Ovulation
                </span>
                <span className="px-md py-xs bg-primary-fixed/30 text-primary rounded-full text-[11px] font-bold border border-primary-fixed/40">
                  Insulin Sensitive
                </span>
                <span className="px-md py-xs bg-secondary-container/50 text-on-secondary-container rounded-full text-[11px] font-bold border border-secondary-container/60">
                  Low Cortisol Spike
                </span>
              </div>
            </div>
          </div>
          
          <div className="w-full md:w-72 bg-surface-container-low/40 border border-outline-variant/10 rounded-2xl p-lg flex flex-col items-center text-center shrink-0">
            <div className="w-16 h-16 bg-secondary-container/40 rounded-full flex items-center justify-center mb-md text-primary">
              <span className="material-symbols-outlined text-[32px]">smart_toy</span>
            </div>
            <h4 className="font-title-card text-title-card font-semibold text-on-surface mb-xs">Next Doctor Visit?</h4>
            <p className="text-[12px] text-on-surface-variant mb-lg leading-snug">
              Export a clinical summary of these insights to share with your endocrinologist.
            </p>
            <Link
              href="/doctor-summary"
              className="w-full py-md bg-on-surface text-surface hover:bg-on-surface/90 rounded-xl font-bold flex items-center justify-center gap-sm text-[12px] font-label-caps transition-all active:scale-[0.98] shadow-sm"
            >
              <span className="material-symbols-outlined text-[18px]">ios_share</span>
              Export Summary
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
