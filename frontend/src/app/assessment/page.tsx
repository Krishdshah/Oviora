"use client";

import { useState, useEffect } from "react";
import { apiService } from "@/services/api";

const INITIAL_STATE = {
  " Age (yrs)": 25,
  "Weight (Kg)": 65,
  "Height(Cm) ": 165,
  "BMI": 23.8,
  "Blood Group": 11,
  "Pulse rate(bpm) ": 72,
  "RR (breaths/min)": 18,
  "Hb(g/dl)": 12.0,
  "Cycle(R/I)": 2,
  "Cycle length(days)": 28,
  "Marraige Status (Yrs)": 0,
  "Pregnant(Y/N)": 0,
  "No. of aborptions": 0,
  "  I   beta-HCG(mIU/mL)": 1.99,
  "II    beta-HCG(mIU/mL)": 1.99,
  "FSH(mIU/mL)": 5.0,
  "LH(mIU/mL)": 5.0,
  "FSH/LH": 1.0,
  "Hip(inch)": 38,
  "Waist(inch)": 32,
  "Waist:Hip Ratio": 0.84,
  "TSH (mIU/L)": 2.5,
  "AMH(ng/mL)": 3.0,
  "PRL(ng/mL)": 15.0,
  "Vit D3 (ng/mL)": 30.0,
  "PRG(ng/mL)": 0.5,
  "RBS(mg/dl)": 95.0,
  "Weight gain(Y/N)": 0,
  "hair growth(Y/N)": 0,
  "Skin darkening (Y/N)": 0,
  "Hair loss(Y/N)": 0,
  "Pimples(Y/N)": 0,
  "Fast food (Y/N)": 0,
  "Reg.Exercise(Y/N)": 0,
  "BP _Systolic (mmHg)": 120,
  "BP _Diastolic (mmHg)": 80,
  "Follicle No. (L)": 5,
  "Follicle No. (R)": 5,
  "Avg. F size (L) (mm)": 12.0,
  "Avg. F size (R) (mm)": 12.0,
  "Endometrium (mm)": 8.0,
  "Total Follicles": 10,
  "Average Follicle Size": 12.0,
  "LH/FSH Ratio": 1.0,
  "Waist Height Ratio": 0.49
};

export default function AssessmentPage() {
  const [formData, setFormData] = useState<Record<string, any>>(INITIAL_STATE);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<{ risk_score: number, risk_level: string, factors: string[] } | null>(null);

  // Auto-calculate derived fields
  useEffect(() => {
    setFormData(prev => {
      const heightM = prev["Height(Cm) "] / 100;
      const bmi = heightM > 0 ? (prev["Weight (Kg)"] / (heightM * heightM)).toFixed(2) : 0;
      
      const lh = prev["LH(mIU/mL)"];
      const fsh = prev["FSH(mIU/mL)"];
      const fshLh = lh > 0 ? (fsh / lh).toFixed(2) : 0;
      const lhFsh = fsh > 0 ? (lh / fsh).toFixed(2) : 0;
      
      const waist = prev["Waist(inch)"];
      const hip = prev["Hip(inch)"];
      const heightInches = prev["Height(Cm) "] / 2.54;
      const waistHip = hip > 0 ? (waist / hip).toFixed(2) : 0;
      const waistHeight = heightInches > 0 ? (waist / heightInches).toFixed(2) : 0;
      
      const totalFoll = Number(prev["Follicle No. (L)"]) + Number(prev["Follicle No. (R)"]);
      const avgFollSize = (Number(prev["Avg. F size (L) (mm)"]) + Number(prev["Avg. F size (R) (mm)"])) / 2;

      return {
        ...prev,
        "BMI": Number(bmi),
        "FSH/LH": Number(fshLh),
        "LH/FSH Ratio": Number(lhFsh),
        "Waist:Hip Ratio": Number(waistHip),
        "Waist Height Ratio": Number(waistHeight),
        "Total Follicles": totalFoll,
        "Average Follicle Size": avgFollSize
      };
    });
  }, [
    formData["Weight (Kg)"], formData["Height(Cm) "], 
    formData["LH(mIU/mL)"], formData["FSH(mIU/mL)"],
    formData["Waist(inch)"], formData["Hip(inch)"],
    formData["Follicle No. (L)"], formData["Follicle No. (R)"],
    formData["Avg. F size (L) (mm)"], formData["Avg. F size (R) (mm)"]
  ]);

  const handleChange = (key: string, value: string | number) => {
    setFormData(prev => ({ ...prev, [key]: Number(value) }));
  };

  const handleAnalyze = async () => {
    setAnalyzing(true);
    setResult(null);
    try {
      const response = await apiService.predictClinicalRisk({ features: formData });
      setResult(response);
    } catch (error) {
      console.error(error);
      alert("Failed to connect to AI engine. Make sure the backend is running.");
    } finally {
      setAnalyzing(false);
    }
  };

  const renderInput = (key: string, label: string, isBinary: boolean = false) => {
    if (isBinary) {
      return (
        <div key={key} className="flex flex-col gap-1">
          <label className="text-[12px] font-bold text-on-surface-variant font-label-caps">{label}</label>
          <select 
            value={formData[key]} 
            onChange={e => handleChange(key, e.target.value)}
            className="p-md rounded-xl border border-outline-variant/30 bg-surface focus:outline-none focus:border-primary font-body-main text-[14px]"
          >
            <option value={0}>No (0)</option>
            <option value={1}>Yes (1)</option>
          </select>
        </div>
      );
    }

    return (
      <div key={key} className="flex flex-col gap-1">
        <label className="text-[12px] font-bold text-on-surface-variant font-label-caps">{label}</label>
        <input 
          type="number"
          step="any"
          value={formData[key]}
          onChange={e => handleChange(key, e.target.value)}
          className="p-md rounded-xl border border-outline-variant/30 bg-surface focus:outline-none focus:border-primary font-body-main text-[14px]"
        />
      </div>
    );
  };

  return (
    <div className="px-lg py-xl max-w-5xl mx-auto flex flex-col gap-lg pb-32">
      <header className="mb-sm">
        <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold mb-xs inline-block">
          AI CLINICAL ASSESSMENT
        </span>
        <h1 className="font-display-hero text-[32px] md:text-[40px] text-primary font-bold mb-xs">
          Clinical Risk Engine
        </h1>
        <p className="font-body-main text-on-surface-variant leading-relaxed">
          Enter patient parameters to generate a predictive risk assessment for PCOS using the CRE-v1.0 model.
        </p>
      </header>

      {/* Vitals */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm">
        <h3 className="font-title-card text-[18px] font-semibold text-on-surface mb-md">Physical & Vitals</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-md">
          {renderInput(" Age (yrs)", "Age (yrs)")}
          {renderInput("Weight (Kg)", "Weight (Kg)")}
          {renderInput("Height(Cm) ", "Height (Cm)")}
          {renderInput("BMI", "BMI")}
          {renderInput("Blood Group", "Blood Group (Code)")}
          {renderInput("Pulse rate(bpm) ", "Pulse Rate (bpm)")}
          {renderInput("RR (breaths/min)", "RR (breaths/min)")}
          {renderInput("BP _Systolic (mmHg)", "BP Systolic")}
          {renderInput("BP _Diastolic (mmHg)", "BP Diastolic")}
          {renderInput("Hip(inch)", "Hip (inch)")}
          {renderInput("Waist(inch)", "Waist (inch)")}
        </div>
      </section>

      {/* Cycle & Pregnancy */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm">
        <h3 className="font-title-card text-[18px] font-semibold text-on-surface mb-md">Cycle & History</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-md">
          {renderInput("Cycle(R/I)", "Cycle (2=Reg, 4=Irreg)")}
          {renderInput("Cycle length(days)", "Cycle Length (Days)")}
          {renderInput("Marraige Status (Yrs)", "Marriage (Yrs)")}
          {renderInput("Pregnant(Y/N)", "Pregnant", true)}
          {renderInput("No. of aborptions", "Abortions")}
        </div>
      </section>

      {/* Labs */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm">
        <h3 className="font-title-card text-[18px] font-semibold text-on-surface mb-md">Hormonal & Lab Markers</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-md">
          {renderInput("Hb(g/dl)", "Hb (g/dl)")}
          {renderInput("  I   beta-HCG(mIU/mL)", "I beta-HCG")}
          {renderInput("II    beta-HCG(mIU/mL)", "II beta-HCG")}
          {renderInput("FSH(mIU/mL)", "FSH")}
          {renderInput("LH(mIU/mL)", "LH")}
          {renderInput("FSH/LH", "FSH/LH")}
          {renderInput("TSH (mIU/L)", "TSH")}
          {renderInput("AMH(ng/mL)", "AMH")}
          {renderInput("PRL(ng/mL)", "PRL")}
          {renderInput("Vit D3 (ng/mL)", "Vit D3")}
          {renderInput("PRG(ng/mL)", "PRG")}
          {renderInput("RBS(mg/dl)", "RBS")}
        </div>
      </section>

      {/* Ultrasound */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm">
        <h3 className="font-title-card text-[18px] font-semibold text-on-surface mb-md">Pelvic Ultrasound</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-md">
          {renderInput("Follicle No. (L)", "Follicle No. (L)")}
          {renderInput("Follicle No. (R)", "Follicle No. (R)")}
          {renderInput("Avg. F size (L) (mm)", "Avg F Size L (mm)")}
          {renderInput("Avg. F size (R) (mm)", "Avg F Size R (mm)")}
          {renderInput("Endometrium (mm)", "Endometrium (mm)")}
          {renderInput("Total Follicles", "Total Follicles")}
        </div>
      </section>

      {/* Symptoms */}
      <section className="bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm">
        <h3 className="font-title-card text-[18px] font-semibold text-on-surface mb-md">Clinical Symptoms</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-md">
          {renderInput("Weight gain(Y/N)", "Weight Gain", true)}
          {renderInput("hair growth(Y/N)", "Hair Growth", true)}
          {renderInput("Skin darkening (Y/N)", "Skin Darkening", true)}
          {renderInput("Hair loss(Y/N)", "Hair Loss", true)}
          {renderInput("Pimples(Y/N)", "Pimples", true)}
          {renderInput("Fast food (Y/N)", "Fast Food", true)}
          {renderInput("Reg.Exercise(Y/N)", "Reg. Exercise", true)}
        </div>
      </section>

      <div className="flex justify-center mt-md">
        <button 
          onClick={handleAnalyze}
          disabled={analyzing}
          className="bg-primary text-on-primary font-bold px-3xl py-lg rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all active:scale-95 text-[16px] flex items-center gap-sm disabled:opacity-50"
        >
          <span className="material-symbols-outlined text-[24px]">
            {analyzing ? "progress_activity" : "psychology"}
          </span>
          {analyzing ? "Running AI Engine..." : "Analyze Clinical Risk"}
        </button>
      </div>

      {result && (
        <div className="fixed inset-0 z-50 bg-scrim/40 backdrop-blur-sm flex items-center justify-center p-md animate-in fade-in">
          <div className="bg-surface rounded-[32px] p-xl w-[90%] sm:w-[450px] min-w-[320px] shadow-2xl border border-outline-variant/20 relative animate-in zoom-in-95">
            <button 
              onClick={() => setResult(null)}
              className="absolute top-md right-md w-10 h-10 rounded-full bg-surface-container hover:bg-surface-container-high flex items-center justify-center text-on-surface transition-colors"
            >
              <span className="material-symbols-outlined">close</span>
            </button>
            
            <div className="text-center mt-sm">
              <div className={`w-24 h-24 rounded-full mx-auto flex items-center justify-center mb-md ${result.risk_level === 'High' ? 'bg-error-container text-error' : 'bg-primary-container text-primary'}`}>
                <span className="material-symbols-outlined text-[48px]">
                  {result.risk_level === 'High' ? 'warning' : 'verified_user'}
                </span>
              </div>
              
              <h2 className="font-display-hero text-[32px] font-bold text-on-surface mb-xs">
                {result.risk_level} Risk
              </h2>
              <p className="font-body-main text-on-surface-variant mb-lg">
                CRE-v1.0 AI Analysis Complete
              </p>
              
              <div className="bg-surface-container-low rounded-2xl p-lg border border-outline-variant/20 mb-lg">
                <span className="font-label-caps text-[10px] font-bold text-on-surface-variant">CONFIDENCE SCORE</span>
                <p className="font-display-hero text-[40px] font-bold text-on-surface">
                  {(result.risk_score * 100).toFixed(1)}%
                </p>
              </div>
              
              <button 
                onClick={() => setResult(null)}
                className="w-full bg-primary text-on-primary py-md rounded-xl font-bold transition-all active:scale-95"
              >
                Close Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
