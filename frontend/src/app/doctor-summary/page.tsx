"use client";

import { useState } from "react";
import Link from "next/link";

export default function DoctorSummary() {
  const [generating, setGenerating] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);

  const handleGeneratePDF = () => {
    setGenerating(true);
    setToastVisible(false);
    
    // Simulate compilation latency
    setTimeout(() => {
      setGenerating(false);
      setToastVisible(true);
      setTimeout(() => setToastVisible(false), 3000);
    }, 2000);
  };

  return (
    <div className="px-lg py-xl max-w-7xl mx-auto flex flex-col gap-lg relative">
      
      {/* Header */}
      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-md mb-sm">
        <div>
          <div className="mb-xs">
            <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
              HIPAA EXPORT
            </span>
          </div>
          <h2 className="font-display-hero text-[32px] md:text-[40px] text-primary font-bold mb-xs">
            Clinical Doctor Summary
          </h2>
          <p className="font-body-main text-on-surface-variant leading-relaxed">
            Validated clinical summary compiled for your next consultation with an endocrinologist or gynecologist.
          </p>
        </div>
        
        <button
          onClick={handleGeneratePDF}
          disabled={generating}
          className="flex items-center gap-xs bg-primary hover:bg-primary/95 text-on-primary px-xl py-md rounded-xl font-bold text-label-caps text-[12px] shadow-md transition-all active:scale-95 shrink-0"
        >
          <span className="material-symbols-outlined text-[18px]">
            {generating ? "progress_activity" : "picture_as_pdf"}
          </span>
          {generating ? "Compiling Report..." : "Generate Doctor PDF"}
        </button>
      </header>

      {/* Patient Overview Metadata Bar */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-wrap gap-lg items-center shadow-sm">
        <div className="flex-grow min-w-[180px]">
          <span className="font-label-caps text-[10px] font-bold text-primary uppercase block mb-xs">Reporting Period</span>
          <p className="font-title-card text-on-surface font-semibold">Oct 01, 2023 - Jan 01, 2024</p>
        </div>
        <div className="h-10 w-px bg-outline-variant/30 hidden md:block"></div>
        <div className="flex-grow min-w-[180px]">
          <span className="font-label-caps text-[10px] font-bold text-primary uppercase block mb-xs">Phenotype Analysis</span>
          <p className="font-title-card text-on-surface font-semibold">Type C (Ovulatory PCOS)</p>
        </div>
        <div className="h-10 w-px bg-outline-variant/30 hidden md:block"></div>
        <div className="flex-grow min-w-[180px]">
          <span className="font-label-caps text-[10px] font-bold text-primary uppercase block mb-xs">Last Lab Update</span>
          <p className="font-title-card text-on-surface font-semibold">Dec 14, 2023</p>
        </div>
      </section>

      {/* Bento Grid layout */}
      <div className="bento-grid">
        
        {/* Symptoms prevalence (Large Column) */}
        <section className="col-span-12 lg:col-span-8 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-lg flex items-center gap-xs">
              <span className="material-symbols-outlined text-primary">analytics</span>
              Symptom Prevalence & Severity
            </h3>
            
            <div className="space-y-md">
              <div className="p-md bg-surface-container-low/50 rounded-xl flex items-center justify-between border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <div className="w-10 h-10 rounded-full bg-secondary-container/30 flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined">face</span>
                  </div>
                  <div>
                    <p className="font-bold text-on-surface text-[14px]">Hirsutism / Acne</p>
                    <p className="text-[11px] text-on-surface-variant">Androgen sensitivity indicators</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-error font-bold text-[12px]">Severe (82%)</p>
                  <div className="w-28 h-1.5 bg-surface-container-high rounded-full mt-1 overflow-hidden">
                    <div className="bg-error h-full w-[82%]"></div>
                  </div>
                </div>
              </div>

              <div className="p-md bg-surface-container-low/50 rounded-xl flex items-center justify-between border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <div className="w-10 h-10 rounded-full bg-secondary-container/30 flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined">battery_very_low</span>
                  </div>
                  <div>
                    <p className="font-bold text-on-surface text-[14px]">Fatigue / Brain Fog</p>
                    <p className="text-[11px] text-on-surface-variant">Metabolic/Inflammatory link</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-primary font-bold text-[12px]">Moderate (45%)</p>
                  <div className="w-28 h-1.5 bg-surface-container-high rounded-full mt-1 overflow-hidden">
                    <div className="bg-primary h-full w-[45%]"></div>
                  </div>
                </div>
              </div>

              <div className="p-md bg-surface-container-low/50 rounded-xl flex items-center justify-between border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <div className="w-10 h-10 rounded-full bg-secondary-container/30 flex items-center justify-center text-primary">
                    <span className="material-symbols-outlined">psychology</span>
                  </div>
                  <div>
                    <p className="font-bold text-on-surface text-[14px]">Mood Swings / Anxiety</p>
                    <p className="text-[11px] text-on-surface-variant">Progesterone deficiency related</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-primary font-bold text-[12px]">Moderate (56%)</p>
                  <div className="w-28 h-1.5 bg-surface-container-high rounded-full mt-1 overflow-hidden">
                    <div className="bg-primary h-full w-[56%]"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Cycle History (Small Column) */}
        <section className="col-span-12 lg:col-span-4 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-lg flex items-center gap-xs">
              <span className="material-symbols-outlined text-primary">calendar_month</span>
              Cycle History
            </h3>
            
            <div className="space-y-sm flex-grow">
              <div className="flex items-center justify-between border-b border-outline-variant/10 pb-sm">
                <span className="text-[13px] text-on-surface-variant">Avg Cycle Length</span>
                <span className="font-bold text-on-surface text-[13px]">42 Days</span>
              </div>
              <div className="flex items-center justify-between border-b border-outline-variant/10 pb-sm">
                <span className="text-[13px] text-on-surface-variant">Period Variation</span>
                <span className="font-bold text-on-surface text-[13px]">+/- 8 Days</span>
              </div>
              <div className="flex items-center justify-between border-b border-outline-variant/10 pb-sm">
                <span className="text-[13px] text-on-surface-variant">Flow Intensity</span>
                <span className="font-bold text-primary text-[13px]">Heavy (Clotted)</span>
              </div>
            </div>
          </div>
          
          <div className="bg-primary-fixed/20 p-md rounded-xl mt-md border border-primary-fixed/30">
            <p className="text-[10px] font-bold text-primary flex items-center gap-xs">
              <span className="material-symbols-outlined text-[13px]">warning</span>
              CLINICAL ALERT
            </p>
            <p className="text-[12px] text-primary mt-1 leading-snug">
              Patient reports secondary amenorrhea lasting 55 days in current cycle.
            </p>
          </div>
        </section>

        {/* Hormones & Labs (Full Width) */}
        <section className="col-span-12 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm hover:-translate-y-1 transition-all duration-300">
          <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-md flex items-center gap-xs">
            <span className="material-symbols-outlined text-primary">biotech</span>
            Hormonal & Lab Markers
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-md">
            <div className="p-md border border-outline-variant/25 rounded-2xl bg-surface-container-low/20">
              <p className="font-label-caps text-[9px] font-bold text-on-surface-variant mb-xs">LH/FSH RATIO</p>
              <div className="flex items-baseline gap-xs">
                <span className="text-2xl font-bold text-on-surface">3.2:1</span>
                <span className="text-error text-[11px] font-bold">High</span>
              </div>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-tight">Indicates possible follicular recruitment issue</p>
            </div>
            
            <div className="p-md border border-outline-variant/25 rounded-2xl bg-surface-container-low/20">
              <p className="font-label-caps text-[9px] font-bold text-on-surface-variant mb-xs">TESTOSTERONE</p>
              <div className="flex items-baseline gap-xs">
                <span className="text-2xl font-bold text-on-surface">78 ng/dL</span>
                <span className="text-error text-[11px] font-bold">Elevated</span>
              </div>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-tight">Free Androgen Index: 9.4%</p>
            </div>

            <div className="p-md border border-outline-variant/25 rounded-2xl bg-surface-container-low/20">
              <p className="font-label-caps text-[9px] font-bold text-on-surface-variant mb-xs">FASTING INSULIN</p>
              <div className="flex items-baseline gap-xs">
                <span className="text-2xl font-bold text-on-surface">14.2 µU/mL</span>
                <span className="text-primary text-[11px] font-bold">Borderline</span>
              </div>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-tight">HOMA-IR: 3.1 (Resistance Likely)</p>
            </div>

            <div className="p-md border border-outline-variant/25 rounded-2xl bg-surface-container-low/20">
              <p className="font-label-caps text-[9px] font-bold text-on-surface-variant mb-xs">VITAMIN D3</p>
              <div className="flex items-baseline gap-xs">
                <span className="text-2xl font-bold text-on-surface">22 ng/mL</span>
                <span className="text-error text-[11px] font-bold">Low</span>
              </div>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-tight">Recommend 5000 IU/day titration</p>
            </div>
          </div>
        </section>

        {/* Weight Trend (Left Column) */}
        <section className="col-span-12 lg:col-span-6 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm hover:-translate-y-1 transition-all duration-300">
          <div className="flex justify-between items-center mb-md">
            <h3 className="font-title-card text-title-card font-semibold text-on-surface flex items-center gap-xs">
              <span className="material-symbols-outlined text-primary">show_chart</span>
              Weight & BMI Trend
            </h3>
            <span className="px-md py-xs bg-surface-container-low border border-outline-variant/10 rounded-full text-[10px] font-bold font-label-caps text-on-surface-variant">
              90 Days
            </span>
          </div>
          
          {/* Simple CSS-based bar chart */}
          <div className="w-full h-40 flex items-end justify-between gap-xs px-md border-b border-l border-outline-variant/15 pb-2">
            <div className="bg-primary/20 w-full rounded-t-sm" style={{ height: "60%" }}></div>
            <div className="bg-primary/30 w-full rounded-t-sm" style={{ height: "62%" }}></div>
            <div className="bg-primary/40 w-full rounded-t-sm" style={{ height: "65%" }}></div>
            <div className="bg-primary/50 w-full rounded-t-sm" style={{ height: "68%" }}></div>
            <div className="bg-primary/60 w-full rounded-t-sm" style={{ height: "64%" }}></div>
            <div className="bg-primary/70 w-full rounded-t-sm" style={{ height: "60%" }}></div>
            <div className="bg-primary w-full rounded-t-sm" style={{ height: "58%" }}></div>
          </div>
          
          <div className="mt-md flex justify-between gap-md">
            <div>
              <p className="text-[11px] text-on-surface-variant/70 font-label-caps">Current Weight</p>
              <p className="font-bold text-on-surface text-[15px]">
                74.2 kg <span className="text-tertiary text-xs">(-2.4kg)</span>
              </p>
            </div>
            <div className="text-right">
              <p className="text-[11px] text-on-surface-variant/70 font-label-caps">BMI Index</p>
              <p className="font-bold text-on-surface text-[15px]">
                26.4 <span className="text-primary text-xs font-bold">Overweight</span>
              </p>
            </div>
          </div>
        </section>

        {/* Recommendations (Right Column) */}
        <section className="col-span-12 lg:col-span-6 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm hover:-translate-y-1 transition-all duration-300">
          <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-lg flex items-center gap-xs">
            <span className="material-symbols-outlined text-primary">clinical_notes</span>
            Clinical Recommendations
          </h3>
          
          <ul className="space-y-md">
            <li className="flex gap-md items-start">
              <div className="mt-0.5 bg-tertiary-container/30 text-primary w-6 h-6 shrink-0 rounded-full flex items-center justify-center text-[12px] font-bold">
                1
              </div>
              <p className="text-[13px] text-on-surface-variant leading-relaxed">
                Consider Inositol (4g/day) or clinical titration to address HOMA-IR of 3.1 and borderline fasting insulin levels.
              </p>
            </li>
            <li className="flex gap-md items-start">
              <div className="mt-0.5 bg-tertiary-container/30 text-primary w-6 h-6 shrink-0 rounded-full flex items-center justify-center text-[12px] font-bold">
                2
              </div>
              <p className="text-[13px] text-on-surface-variant leading-relaxed">
                Pelvic Ultrasound is recommended to validate polycystic ovarian morphology given elevated LH/FSH ratio and oligomenorrhea.
              </p>
            </li>
            <li className="flex gap-md items-start">
              <div className="mt-0.5 bg-tertiary-container/30 text-primary w-6 h-6 shrink-0 rounded-full flex items-center justify-center text-[12px] font-bold">
                3
              </div>
              <p className="text-[13px] text-on-surface-variant leading-relaxed">
                Serum DHEAS and 17-OHP labs are suggested to rule out late-onset NCAH given clinical androgen symptoms.
              </p>
            </li>
          </ul>
        </section>

      </div>

      {/* HIPAA Compliance note footer */}
      <footer className="text-center text-[11px] text-on-surface-variant/50 max-w-2xl mx-auto mt-md">
        This document represents raw clinical intelligence generated dynamically by Oviora PCOS Copilot. All data is processed using secure, HIPAA-compliant methodologies.
      </footer>

      {/* Success Toast */}
      {toastVisible && (
        <div className="fixed bottom-20 right-4 z-50 bg-inverse-surface text-inverse-on-surface px-lg py-md rounded-xl shadow-lg flex items-center gap-sm animate-bounce">
          <span className="material-symbols-outlined text-primary-container">check_circle</span>
          <span className="text-[13px] font-medium">HIPAA-compliant Doctor PDF compiled & saved!</span>
        </div>
      )}

    </div>
  );
}
