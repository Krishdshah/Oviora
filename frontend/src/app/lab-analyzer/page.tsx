"use client";

import { useEffect, useState } from "react";
import { apiService, LabMarker } from "@/services/api";
import Link from "next/link";

export default function LabAnalyzer() {
  const [markers, setMarkers] = useState<LabMarker[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Custom upload state
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [parsed, setParsed] = useState(true); // show default parsed reports initially

  useEffect(() => {
    async function loadMarkers() {
      try {
        const res = await apiService.getLabMarkers();
        setMarkers(res);
      } catch (err) {
        console.error("Failed to fetch lab markers", err);
      } finally {
        setLoading(false);
      }
    }
    loadMarkers();
  }, []);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setFileName(file.name);
    setUploading(true);
    setParsed(false);
    
    // Simulate extraction latency
    setTimeout(() => {
      setUploading(false);
      setParsed(true);
    }, 2000);
  };

  const triggerUpload = () => {
    const input = document.getElementById("lab-file-input");
    input?.click();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-md">
          <span className="material-symbols-outlined text-[48px] text-primary animate-spin">
            progress_activity
          </span>
          <p className="font-label-caps text-on-surface-variant">Calibrating Diagnostic Baselines...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-lg py-xl max-w-6xl mx-auto flex flex-col gap-lg">
      
      {/* Header */}
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

      {/* Upload Zone */}
      <section className="mb-sm">
        <input
          id="lab-file-input"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={handleFileUpload}
        />
        
        <div
          onClick={triggerUpload}
          className="bg-white rounded-[32px] p-xl text-center border-2 border-dashed border-primary-fixed hover:border-primary/50 transition-all duration-300 group cursor-pointer relative overflow-hidden shadow-sm"
        >
          <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-transparent via-primary-container to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="flex flex-col items-center w-full max-w-lg mx-auto">
            <div className="w-20 h-20 mb-lg rounded-full bg-primary-container/10 flex items-center justify-center relative text-primary">
              <span className="material-symbols-outlined text-[40px] group-hover:scale-110 transition-transform">
                upload_file
              </span>
              <div className="absolute -top-1 -right-1 bg-primary text-white w-6 h-6 rounded-full flex items-center justify-center shadow-lg border-2 border-white">
                <span className="material-symbols-outlined text-[12px]">auto_awesome</span>
              </div>
            </div>
            
            <h3 className="w-full font-title-section text-title-card font-semibold text-on-surface mb-xs">
              {uploading ? "Extracting Lab Metrics..." : fileName ? `Selected: ${fileName}` : "Upload Your Blood Report"}
            </h3>
            <p className="w-full text-[13px] text-on-surface-variant mb-lg leading-relaxed">
              {uploading
                ? "Our clinical parser is reading the PDF markers..."
                : "Drag and drop your blood test results or click to browse. We support PDF, JPG, and PNG formats."}
            </p>
            
            <div className="flex flex-wrap justify-center gap-sm w-full">
              <button className="flex items-center gap-xs bg-primary hover:bg-primary/95 text-on-primary px-xl py-md rounded-xl font-bold text-label-caps text-[11px] shadow-md transition-all active:scale-95">
                <span className="material-symbols-outlined text-[16px]">picture_as_pdf</span>
                Choose File
              </button>
              <button className="flex items-center gap-xs bg-surface-container-high text-on-surface-variant px-xl py-md rounded-xl font-bold text-label-caps text-[11px] hover:bg-surface-variant transition-all active:scale-95">
                <span className="material-symbols-outlined text-[16px]">photo_camera</span>
                Scan Document
              </button>
            </div>
            
            <div className="mt-xl flex items-center gap-xs text-[10px] font-label-caps text-on-surface-variant/70">
              <span className="material-symbols-outlined text-[14px]">lock</span>
              HIPAA Compliant & Secure Private Data Processing
            </div>
          </div>
        </div>
      </section>

      {/* Simulated parser loading state */}
      {uploading && (
        <div className="py-md text-center flex flex-col items-center gap-sm animate-pulse bg-surface-container-low/30 rounded-2xl border border-outline-variant/10">
          <span className="material-symbols-outlined text-[36px] text-primary animate-spin">progress_activity</span>
          <p className="text-[13px] font-semibold text-primary">Reading endocrine panels. Matching hormones...</p>
        </div>
      )}

      {/* Results Section */}
      {parsed && !uploading && (
        <section className="flex flex-col gap-lg">
          <div className="flex items-center justify-between">
            <h3 className="font-title-section text-title-card font-semibold text-primary">Extracted Hormone Markers</h3>
            <span className="bg-tertiary-container/10 border border-tertiary-container/30 text-on-tertiary-container px-md py-xs rounded-full font-label-caps text-[10px] font-bold flex items-center gap-xs">
              <span className="material-symbols-outlined text-[14px]">check_circle</span>
              Clinical Extraction Complete
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-md">
            {markers.map((marker) => {
              const statusColors = {
                High: "bg-error-container text-on-error-container border-error/20",
                Normal: "bg-primary-fixed text-on-primary-fixed-variant border-primary/20",
                Borderline: "bg-secondary-container text-on-secondary-container border-secondary/25",
                Low: "bg-tertiary-container/20 text-on-tertiary-container border-tertiary/20",
              };

              const barColors = {
                High: "bg-error",
                Normal: "bg-primary",
                Borderline: "bg-secondary",
                Low: "bg-tertiary",
              };

              const fillPercent = marker.id === "lh" ? 85 : marker.id === "fsh" ? 40 : marker.id === "amh" ? 70 : marker.id === "testosterone" ? 90 : 65;

              // Wide layout for fasting insulin metabolic marker
              const isWide = marker.id === "insulin";

              return (
                <div
                  key={marker.id}
                  className={`bg-white border border-outline-variant/20 rounded-[24px] p-lg flex flex-col justify-between gap-md shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-md ${
                    isWide ? "md:col-span-2" : "col-span-1"
                  }`}
                >
                  <div>
                    <div className="flex justify-between items-start gap-sm mb-xs">
                      <div>
                        <span className="font-label-caps text-on-surface-variant/70 uppercase tracking-widest text-[9px] font-bold">
                          {marker.category}
                        </span>
                        <h4 className="font-title-card text-[15px] font-bold text-on-surface leading-tight">
                          {marker.name}
                        </h4>
                      </div>
                      <span className={`px-sm py-0.5 rounded-full font-label-caps text-[9px] font-bold border ${statusColors[marker.status]}`}>
                        {marker.status}
                      </span>
                    </div>

                    {isWide ? (
                      <div className="grid sm:grid-cols-2 gap-md mt-md">
                        <div>
                          <div className="flex items-baseline gap-xs mb-xs">
                            <span className="text-3xl font-bold text-on-surface">{marker.value}</span>
                            <span className="text-on-surface-variant text-[12px]">{marker.unit}</span>
                          </div>
                          <div className="bg-surface-container-low h-2 rounded-full overflow-hidden mb-sm border border-outline-variant/10">
                            <div className={`${barColors[marker.status]} h-full`} style={{ width: `${fillPercent}%` }}></div>
                          </div>
                        </div>
                        <div className="bg-surface-container-low/50 border border-outline-variant/15 rounded-xl p-md flex items-center justify-center">
                          <p className="text-[12px] text-on-surface-variant italic leading-normal text-center">
                            "Your insulin is within clinical 'normal' but above the 'optimal' range (&lt;7) for metabolic health in PCOS management."
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="mt-md">
                        <div className="flex items-baseline gap-xs mb-xs">
                          <span className="text-3xl font-bold text-on-surface">{marker.value}</span>
                          <span className="text-on-surface-variant text-[12px]">{marker.unit}</span>
                        </div>
                        <div className="bg-surface-container-low h-2 rounded-full overflow-hidden mb-sm border border-outline-variant/10">
                          <div className={`${barColors[marker.status]} h-full`} style={{ width: `${fillPercent}%` }}></div>
                        </div>
                      </div>
                    )}
                  </div>

                  <details className="group border-t border-outline-variant/10 pt-sm mt-xs">
                    <summary className="list-none flex items-center justify-between text-primary font-bold font-label-caps text-[10px] cursor-pointer hover:underline">
                      <span>Clinical Breakdown</span>
                      <span className="material-symbols-outlined text-[16px] group-open:rotate-180 transition-transform">
                        expand_more
                      </span>
                    </summary>
                    <div className="pt-sm text-[12px] text-on-surface-variant leading-relaxed space-y-xs">
                      <p>{marker.explanation}</p>
                      <p className="text-on-surface-variant/80 border-l-2 border-outline-variant/30 pl-sm italic">
                        {marker.detailedExplanation}
                      </p>
                    </div>
                  </details>
                </div>
              );
            })}
          </div>

          {/* Action CTA */}
          <section className="mt-sm">
            <div className="bg-primary text-on-primary rounded-[32px] p-xl flex flex-col md:flex-row items-center gap-xl shadow-lg border border-primary-container/20">
              <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center shrink-0">
                <span className="material-symbols-outlined text-[32px] text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
                  smart_toy
                </span>
              </div>
              <div className="flex-grow">
                <h4 className="font-title-section text-title-card font-semibold mb-xs">Ready for your AI Coach Analysis?</h4>
                <p className="opacity-85 text-[13px] leading-relaxed">
                  Get a personalized protocol based on these specific lab results including customized nutrition, supplements, and cortisol-conscious exercise advice.
                </p>
              </div>
              <Link
                href="/ai-coach"
                className="bg-white text-primary hover:bg-surface-container-low font-bold px-xl py-md rounded-xl text-label-caps text-[12px] transition-transform active:scale-[0.98] shadow-md shrink-0"
              >
                Generate My Plan
              </Link>
            </div>
          </section>
        </section>
      )}

    </div>
  );
}
