import React from "react";

interface LabAnalyzerUploadZoneProps {
  uploading: boolean;
  fileName: string | null;
  onFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function LabAnalyzerUploadZone({
  uploading,
  fileName,
  onFileUpload,
}: LabAnalyzerUploadZoneProps) {
  const triggerUpload = () => {
    const input = document.getElementById("lab-file-input");
    input?.click();
  };

  return (
    <>
      <section className="mb-sm">
        <input
          id="lab-file-input"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={onFileUpload}
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
              {uploading
                ? "Extracting Lab Metrics..."
                : fileName
                ? `Selected: ${fileName}`
                : "Upload Your Blood Report"}
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
          <span className="material-symbols-outlined text-[36px] text-primary animate-spin">
            progress_activity
          </span>
          <p className="text-[13px] font-semibold text-primary">
            Reading endocrine panels. Matching hormones...
          </p>
        </div>
      )}
    </>
  );
}
