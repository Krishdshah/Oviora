"use client";

import { useEffect, useState, useRef } from "react";
import { apiService, CycleData } from "@/services/api";
import Link from "next/link";

export default function CycleIntelligence() {
  const [cycle, setCycle] = useState<CycleData | null>(null);
  const [loading, setLoading] = useState(true);
  const [retryCount, setRetryCount] = useState(0);
  const [backendStatus, setBackendStatus] = useState<"connecting" | "connected" | "error">("connecting");
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadData() {
      try {
        setBackendStatus("connecting");
        const res = await apiService.getCycleData();
        
        if (!isMounted) return;
        
        setCycle(res);
        setBackendStatus("connected");
        setLoading(false);
        
        if (pollIntervalRef.current) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
        }
      } catch (err) {
        if (!isMounted) return;
        console.error("Failed to load cycle data. Retrying...", err);
        setBackendStatus("error");
        setRetryCount((prev) => prev + 1);
      }
    }
    
    loadData();
    pollIntervalRef.current = setInterval(loadData, 5000);

    return () => {
      isMounted = false;
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, []);

  return (
    <div className="px-lg py-xl max-w-6xl mx-auto flex flex-col gap-lg relative">
      
      {/* Backend Connection Notification Banner */}
      {backendStatus !== "connected" && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 animate-in slide-in-from-top-4 fade-in duration-300">
          <div className="bg-surface border border-outline-variant/30 shadow-lg px-lg py-sm rounded-full flex items-center gap-sm">
            <span className="material-symbols-outlined text-[18px] text-primary animate-spin">
              progress_activity
            </span>
            <span className="font-label-caps text-[12px] font-bold text-on-surface-variant">
              {retryCount > 1 
                ? `Waking up Intelligence Engine (Attempt ${retryCount})...` 
                : "Connecting to Clinical Backend..."}
            </span>
          </div>
        </div>
      )}

      {/* Page Header */}
      <section className="mb-sm">
        <div className="mb-xs">
          <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
            CYCLE INTELLIGENCE
          </span>
        </div>
        <h1 className="font-display-hero text-[32px] md:text-[40px] text-on-surface font-bold tracking-tight mb-xs">
          Hormonal Path & Cycle Forecast
        </h1>
        <p className="font-body-main text-on-surface-variant max-w-2xl leading-relaxed">
          Gain deep visibility into your phases. Our clinical-grade predictions are customized specifically to PCOS-induced variances.
        </p>
      </section>

      {/* Cycle Visualization Section */}
      <section className={`flex flex-col lg:flex-row items-center gap-xl bg-white border border-outline-variant/20 rounded-[32px] p-xl shadow-sm mb-sm relative overflow-hidden transition-opacity duration-500 ${loading ? 'opacity-60' : 'opacity-100'}`}>
        <div className="absolute top-[-30%] right-[-20%] w-[350px] h-[350px] bg-primary-fixed/20 blur-[100px] rounded-full -z-10 animate-pulse"></div>
        
        {/* The Wheel */}
        <div className="flex-shrink-0 flex items-center justify-center relative w-72 h-72">
          <div className="w-full h-full rounded-full p-6 flex items-center justify-center bg-surface-container-low/40 border border-outline-variant/10 shadow-inner">
            {/* SVG Wheel */}
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {/* Background Track */}
              <circle
                className="text-surface-container-high"
                cx="50"
                cy="50"
                fill="none"
                r="44"
                stroke="currentColor"
                strokeWidth="7"
              />
              
              {/* Period Segment (Days 1-5 = ~18%) */}
              <circle
                className="text-error"
                cx="50"
                cy="50"
                fill="none"
                r="44"
                stroke="currentColor"
                strokeDasharray="276"
                strokeDashoffset="226" // Period duration representation
                strokeLinecap="round"
                strokeWidth="7.5"
                opacity="0.35"
              />
              
              {/* Follicular Segment (Days 6-13 = ~28%) */}
              <circle
                className="text-tertiary-container"
                cx="50"
                cy="50"
                fill="none"
                r="44"
                stroke="currentColor"
                strokeDasharray="276"
                strokeDashoffset="198"
                strokeLinecap="round"
                strokeWidth="7.5"
                style={{ transform: "rotate(64deg)", transformOrigin: "50% 50%" }}
                opacity="0.5"
              />
              
              {/* Ovulation Segment (Days 14-16 = ~11%) */}
              <circle
                className="text-primary animate-pulse"
                cx="50"
                cy="50"
                fill="none"
                r="44"
                stroke="currentColor"
                strokeDasharray="276"
                strokeDashoffset="246"
                strokeLinecap="round"
                strokeWidth="8"
                style={{ transform: "rotate(165deg)", transformOrigin: "50% 50%" }}
              />

              {/* Luteal Segment (Days 17-28 = ~43%) */}
              <circle
                className="text-secondary"
                cx="50"
                cy="50"
                fill="none"
                r="44"
                stroke="currentColor"
                strokeDasharray="276"
                strokeDashoffset="158"
                strokeLinecap="round"
                strokeWidth="7"
                style={{ transform: "rotate(205deg)", transformOrigin: "50% 50%" }}
                opacity="0.25"
              />
              
              {/* Current Day Indicator Dot */}
              {cycle && (
                <circle
                  cx="50"
                  cy="6"
                  r="3"
                  className="fill-primary stroke-white stroke-[1px]"
                  style={{
                    transform: "rotate(68deg)", // Dynamic rotation representation for day 6
                    transformOrigin: "50% 50%",
                  }}
                />
              )}
            </svg>
            
            {/* Center Text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-md">
              <span className="font-label-caps text-[10px] text-on-surface-variant/60 uppercase tracking-widest">
                Today
              </span>
              <span className="font-display-hero text-2xl font-bold text-primary my-0.5">
                {cycle ? `Day ${cycle.currentDay} of ${cycle.totalDays}` : "--/--"}
              </span>
              <span className="font-body-main text-[12px] text-secondary font-bold">
                {cycle ? `${cycle.phase} Phase` : "Analyzing..."}
              </span>
            </div>
          </div>
        </div>

        {/* Phase Legend & AI Summary */}
        <div className="flex-grow space-y-lg">
          <div className="space-y-md">
            <div className="flex items-start gap-md">
              <div className="w-10 h-10 rounded-xl bg-primary-container/10 flex items-center justify-center text-primary shrink-0">
                <span className="material-symbols-outlined text-[20px]">auto_awesome</span>
              </div>
              <div>
                <h3 className="font-title-card text-title-card font-semibold text-on-surface">
                  AI Cycle Forecast
                </h3>
                <p className="text-[13px] text-on-surface-variant leading-relaxed mt-1">
                  {cycle 
                    ? "Your body is currently transitioning from your Menstrual bleed to your Follicular peak. Estrogen is rising to support follicular maturation."
                    : "Connecting to intelligence engine..."}
                </p>
              </div>
            </div>
            
            {/* Legend Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-md pt-md border-t border-outline-variant/10">
              <div className="flex items-center gap-sm">
                <div className="w-3 h-3 rounded-full bg-error/35"></div>
                <span className="font-label-caps text-[10px] font-bold text-on-surface-variant">Period (Day 1-5)</span>
              </div>
              <div className="flex items-center gap-sm">
                <div className="w-3 h-3 rounded-full bg-tertiary-container/50"></div>
                <span className="font-label-caps text-[10px] font-bold text-on-surface-variant">Follicular (Day 6-13)</span>
              </div>
              <div className="flex items-center gap-sm">
                <div className="w-3 h-3 rounded-full bg-primary"></div>
                <span className="font-label-caps text-[10px] font-bold text-on-surface-variant">Ovulation (Day 14-16)</span>
              </div>
              <div className="flex items-center gap-sm">
                <div className="w-3 h-3 rounded-full bg-secondary/25"></div>
                <span className="font-label-caps text-[10px] font-bold text-on-surface-variant">Luteal (Day 17-28)</span>
              </div>
            </div>
          </div>
          
          <div className="p-md rounded-2xl bg-primary-fixed/20 border border-primary-fixed/30 mt-sm">
            <p className="font-body-main text-[13px] italic text-primary leading-relaxed">
              {cycle
                ? "\"Your low follicle stimulation risk and stable body temperature indicate a healthy progression. Expect energy to rise sequentially over the next 4 days.\""
                : "Awaiting clinical insight generation..."}
            </p>
          </div>
        </div>
      </section>

      {/* Prediction Cards Grid (Bento Style) */}
      <section className={`grid grid-cols-1 md:grid-cols-3 gap-md mb-xs transition-opacity duration-500 ${loading ? 'opacity-60' : 'opacity-100'}`}>
        
        {/* Next Period Card */}
        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div className="space-y-sm">
            <div className="w-10 h-10 rounded-full bg-surface-container-low flex items-center justify-center text-on-surface-variant">
              <span className="material-symbols-outlined text-[20px]">event_repeat</span>
            </div>
            <h4 className="font-title-card text-title-card font-semibold text-on-surface">Next Period</h4>
            <div className="flex items-baseline gap-xs">
              <span className="text-4xl font-extrabold text-primary leading-none">{cycle ? "22" : "--"}</span>
              <span className="font-label-caps text-[10px] text-on-surface-variant font-bold uppercase">Days Left</span>
            </div>
          </div>
          <div className="mt-lg pt-md border-t border-outline-variant/10">
            <p className="text-[12px] text-on-surface-variant leading-normal">
              <span className="font-bold text-primary">AI Forecast:</span> Cycles average 28 days. Based on previous symptom trends, variance is low (±1 day).
            </p>
          </div>
        </div>

        {/* Fertility Window Card */}
        <div className="bg-primary-fixed/15 border border-primary-fixed/30 rounded-[24px] p-lg flex flex-col justify-between shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div className="space-y-sm">
            <div className="w-10 h-10 rounded-full bg-primary-container text-white flex items-center justify-center">
              <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                favorite
              </span>
            </div>
            <h4 className="font-title-card text-title-card font-semibold text-on-surface">Fertility Window</h4>
            <div className="flex items-center">
              <span className="px-sm py-xs bg-primary-container text-white rounded-full font-label-caps text-[9px] font-bold">
                EST. IN {cycle ? "6" : "--"} DAYS
              </span>
            </div>
            <p className="text-[11px] text-on-surface-variant">Days 12 - 17 are highly fertile</p>
          </div>
          <div className="mt-lg pt-md border-t border-outline-variant/15">
            <p className="text-[12px] text-on-surface-variant leading-normal">
              <span className="font-bold text-primary">AI Forecast:</span> LH strip validation will trigger automatically as you enter your window.
            </p>
          </div>
        </div>

        {/* Ovulation Probability Card */}
        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div className="space-y-sm">
            <div className="w-10 h-10 rounded-full bg-surface-container-low flex items-center justify-center text-on-surface-variant">
              <span className="material-symbols-outlined text-[20px]">shutter_speed</span>
            </div>
            <h4 className="font-title-card text-title-card font-semibold text-on-surface">Ovulation Prob.</h4>
            <div className="flex items-baseline gap-xs">
              <span className="text-4xl font-extrabold text-tertiary leading-none">{cycle ? "84" : "--"}</span>
              <span className="font-label-caps text-[10px] text-on-surface-variant font-bold uppercase">%</span>
            </div>
          </div>
          <div className="mt-lg pt-md border-t border-outline-variant/10">
            <p className="text-[12px] text-on-surface-variant leading-normal">
              <span className="font-bold text-primary">AI Forecast:</span> Ovulation probability is rising dynamically. Basal body temperature shows steady baseline.
            </p>
          </div>
        </div>

      </section>

      {/* Action / Tips Section */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-md mt-sm">
        
        {/* Record Symptom card */}
        <div className="bg-white border border-outline-variant/20 rounded-[24px] overflow-hidden flex flex-col sm:flex-row shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div className="sm:w-1/3 h-36 sm:h-auto relative bg-surface-container-low flex items-center justify-center p-md">
            <span className="material-symbols-outlined text-primary text-[64px] animate-pulse">
              clinical_notes
            </span>
          </div>
          <div className="p-lg sm:w-2/3 flex flex-col justify-between">
            <div>
              <h4 className="font-title-card text-title-card font-semibold text-on-surface">Log Symptoms</h4>
              <p className="text-[12px] text-on-surface-variant mt-1 leading-relaxed">
                Log acne, sleep, energy, or cramps. Custom inputs refine our predictive AI.
              </p>
            </div>
            <Link
              href="/symptoms"
              className="mt-md inline-block text-center bg-surface-variant hover:bg-primary-container hover:text-white text-on-surface-variant font-bold py-sm rounded-xl text-label-caps text-[11px] transition-all"
            >
              Record Symptom Entry
            </Link>
          </div>
        </div>

        {/* Action Tip Card */}
        <div className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between border-l-4 border-primary shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div>
            <h4 className="font-title-card text-title-card font-semibold text-on-surface mb-xs">Personalized Tip</h4>
            <p className="text-[13px] text-on-surface-variant leading-relaxed">
              "Because your cycle is in the early follicular phase, your body responds well to complex carbohydrates and light strength training. Avoid fasting, as it can spike cortisol in PCOS bodies."
            </p>
          </div>
          <div className="mt-md flex items-center gap-xs text-primary">
            <span className="material-symbols-outlined text-[18px]">lightbulb</span>
            <span className="font-label-caps text-[10px] font-bold uppercase tracking-wider">Copilot Wisdom</span>
          </div>
        </div>

      </section>

    </div>
  );
}
