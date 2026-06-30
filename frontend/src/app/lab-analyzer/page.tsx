"use client";

import { useEffect, useState } from "react";
import { apiService, LabMarker } from "@/services/api";

import { LabAnalyzerHeader } from "@/components/lab-analyzer/LabAnalyzerHeader";
import { LabAnalyzerUploadZone } from "@/components/lab-analyzer/LabAnalyzerUploadZone";
import { LabAnalyzerResults } from "@/components/lab-analyzer/LabAnalyzerResults";

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-md">
          <span className="material-symbols-outlined text-[48px] text-primary animate-spin">
            progress_activity
          </span>
          <p className="font-label-caps text-on-surface-variant">
            Calibrating Diagnostic Baselines...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-lg py-xl max-w-6xl mx-auto flex flex-col gap-lg">
      <LabAnalyzerHeader />
      
      <LabAnalyzerUploadZone 
        uploading={uploading} 
        fileName={fileName} 
        onFileUpload={handleFileUpload} 
      />

      {parsed && !uploading && (
        <LabAnalyzerResults markers={markers} />
      )}
    </div>
  );
}
