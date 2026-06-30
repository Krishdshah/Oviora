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
    document.getElementById("lab-file-input")?.click();
  };

  return (
    <>
      <section className="mb-10">
        <input
          id="lab-file-input"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          className="hidden"
          onChange={onFileUpload}
        />

        <div
          onClick={triggerUpload}
          className="
            relative
            w-full
            min-h-[500px]
            rounded-[32px]
            border-2
            border-dashed
            border-orange-300
            bg-white
            shadow-sm
            hover:shadow-lg
            hover:border-orange-500
            transition-all
            duration-300
            cursor-pointer
            overflow-hidden
            flex
            items-center
            justify-center
            px-8
            py-14
          "
        >
          <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-transparent via-orange-300 to-transparent opacity-0 hover:opacity-100 transition-opacity" />

          <div className="w-full max-w-2xl flex flex-col items-center text-center">

            {/* Upload Icon */}
            <div className="relative mb-8">
              <div className="w-28 h-28 rounded-full bg-orange-50 flex items-center justify-center">
                <span className="material-symbols-outlined text-[56px] text-orange-600">
                  upload_file
                </span>
              </div>

              <div className="absolute -top-1 -right-1 w-8 h-8 rounded-full bg-orange-600 flex items-center justify-center border-4 border-white">
                <span className="material-symbols-outlined text-white text-[16px]">
                  auto_awesome
                </span>
              </div>
            </div>

            {/* Heading */}
            <h2 className="text-4xl font-bold text-gray-900 mb-4 w-full">
              {uploading
                ? "Extracting Lab Metrics..."
                : fileName
                ? fileName
                : "Upload Your Blood Report"}
            </h2>

            {/* Description */}
            <p
              className="
                w-full
                max-w-xl
                mx-auto
                text-base
                leading-7
                text-gray-500
                mb-10
              "
            >
              {uploading
                ? "Our AI engine is securely extracting hormone markers from your report."
                : "Drag & drop your blood report here or choose a PDF, JPG or PNG file to begin AI-powered hormone analysis."}
            </p>

            {/* Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">

              <button
                type="button"
                className="
                  flex
                  items-center
                  gap-2
                  rounded-xl
                  bg-orange-600
                  px-7
                  py-3
                  text-white
                  font-semibold
                  hover:bg-orange-700
                  transition
                "
              >
                <span className="material-symbols-outlined">
                  picture_as_pdf
                </span>
                Choose File
              </button>

              <button
                type="button"
                className="
                  flex
                  items-center
                  gap-2
                  rounded-xl
                  border
                  border-gray-300
                  bg-gray-50
                  px-7
                  py-3
                  text-gray-700
                  font-semibold
                  hover:bg-gray-100
                  transition
                "
              >
                <span className="material-symbols-outlined">
                  photo_camera
                </span>
                Scan Document
              </button>

            </div>

            {/* Footer */}
            <div className="mt-8 flex items-center gap-2 text-sm text-gray-500">
              <span className="material-symbols-outlined text-base">
                lock
              </span>
              HIPAA Compliant • Secure • Private Data Processing
            </div>
          </div>
        </div>
      </section>

      {uploading && (
        <div className="rounded-2xl border border-orange-100 bg-orange-50 py-8 flex flex-col items-center gap-4">
          <span className="material-symbols-outlined text-4xl text-orange-600 animate-spin">
            progress_activity
          </span>

          <p className="text-orange-700 font-semibold">
            Reading endocrine panels and extracting biomarkers...
          </p>
        </div>
      )}
    </>
  );
}