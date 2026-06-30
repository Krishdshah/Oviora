import React from "react";
import Link from "next/link";
import { LabMarker } from "@/services/api";

interface LabAnalyzerResultsProps {
  markers: LabMarker[];
}

export function LabAnalyzerResults({ markers }: LabAnalyzerResultsProps) {
  return (
    <section className="flex flex-col gap-lg">
      <div className="flex items-center justify-between">
        <h3 className="font-title-section text-title-card font-semibold text-primary">
          Extracted Hormone Markers
        </h3>
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

          const fillPercent =
            marker.id === "lh" ? 85 : marker.id === "fsh" ? 40 : marker.id === "amh" ? 70 : marker.id === "testosterone" ? 90 : 65;

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
            <span
              className="material-symbols-outlined text-[32px] text-white"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              smart_toy
            </span>
          </div>
          <div className="flex-grow">
            <h4 className="font-title-section text-title-card font-semibold mb-xs">
              Ready for your AI Coach Analysis?
            </h4>
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
  );
}
