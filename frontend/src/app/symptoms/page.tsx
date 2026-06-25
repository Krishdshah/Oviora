"use client";

import { useState } from "react";
import { apiService } from "@/services/api";

interface SymptomConfig {
  id: string;
  name: string;
  desc: string;
  emoji: string;
}

export default function Symptoms() {
  const symptoms: SymptomConfig[] = [
    { id: "acne", name: "Acne", desc: "Skin clarity & breakouts", emoji: "😊" },
    { id: "mood", name: "Mood", desc: "Emotional stability & focus", emoji: "😴" },
    { id: "hairLoss", name: "Hair Loss", desc: "Thinning or shedding", emoji: "🍫" },
    { id: "energy", name: "Energy", desc: "Fatigue & activity levels", emoji: "✨" },
    { id: "cravings", name: "Cravings", desc: "Sugar or carb intensity", emoji: "🍫" },
    { id: "sleep", name: "Sleep", desc: "Restfulness & duration", emoji: "😴" },
  ];

  const [severities, setSeverities] = useState<Record<string, string>>({
    acne: "None",
    mood: "Good",
    hairLoss: "None",
    energy: "Medium",
    cravings: "None",
    sleep: "Medium",
  });

  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  const selectSeverity = (symptomId: string, value: string) => {
    setSeverities((prev) => ({
      ...prev,
      [symptomId]: value,
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    setSuccess(false);
    try {
      // Map severities to the schema expected by apiService.logSymptom
      await apiService.logSymptom({
        acne: severities.acne,
        fatigue: severities.energy,
        bloating: severities.sleep,
        cramps: severities.hairLoss,
        mood: severities.mood,
        cravings: severities.cravings,
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to save symptoms", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="px-lg py-xl max-w-5xl mx-auto flex flex-col gap-lg">
      {/* Page Hero */}
      <section className="mb-sm">
        <div className="mb-xs">
          <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
            DAILY CHECK-IN
          </span>
        </div>
        <h1 className="font-display-hero text-[32px] md:text-[40px] text-on-surface font-bold tracking-tight mb-xs">
          How are you feeling today?
        </h1>
        <p className="font-body-main text-on-surface-variant max-w-2xl leading-relaxed">
          Tracking your daily symptoms helps our AI identify patterns, align daily tasks, and provide personalized hormonal insights.
        </p>
      </section>

      {/* Symptom Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-md">
        {symptoms.map((symptom) => {
          const currentVal = severities[symptom.id];
          // Define levels based on whether they are general/numerical or mood/cravings
          let options = ["Low", "Medium", "High"];
          if (symptom.id === "mood") options = ["Good", "Anxious", "Irritable"];
          if (symptom.id === "cravings") options = ["None", "Sweet", "Carbs"];
          if (symptom.id === "acne" || symptom.id === "hairLoss") options = ["None", "Mild", "Severe"];

          return (
            <div
              key={symptom.id}
              className="bg-white p-lg rounded-[24px] border border-outline-variant/20 hover:border-primary/30 flex flex-col justify-between gap-md transition-all duration-300 shadow-sm hover:shadow-md"
            >
              <div className="flex justify-between items-start">
                <div className="w-12 h-12 rounded-xl bg-surface-container-low flex items-center justify-center text-xl">
                  {symptom.emoji}
                </div>
                <span className="material-symbols-outlined text-outline-variant cursor-pointer hover:text-primary">
                  info
                </span>
              </div>
              
              <div>
                <h3 className="font-title-card text-title-card font-semibold text-on-surface">
                  {symptom.name}
                </h3>
                <p className="text-[12px] text-on-surface-variant mt-0.5">{symptom.desc}</p>
              </div>

              <div className="flex gap-xs mt-sm">
                {options.map((opt) => {
                  const isSelected = currentVal === opt;
                  return (
                    <button
                      key={opt}
                      onClick={() => selectSeverity(symptom.id, opt)}
                      className={`flex-1 border px-sm py-sm rounded-full font-label-caps text-[10px] text-center transition-all ${
                        isSelected
                          ? "bg-primary-container text-on-primary-container font-bold border-primary-container shadow-sm"
                          : "border-outline-variant text-on-surface-variant hover:border-primary"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </section>

      {/* Submit Section */}
      <section className="mt-md">
        <div className="flex flex-col md:flex-row items-center justify-between gap-lg bg-surface-container-low/50 border border-outline-variant/20 p-xl rounded-[24px]">
          <div className="flex gap-md items-center">
            <div className="w-12 h-12 rounded-full bg-primary-container/15 flex items-center justify-center text-primary shrink-0">
              <span className="material-symbols-outlined text-2xl">psychiatry</span>
            </div>
            <div>
              <h4 className="font-title-card text-title-card font-semibold text-on-surface">
                Daily Reflection Summary
              </h4>
              <p className="text-[12px] text-on-surface-variant mt-0.5">
                {success ? "Check-in logged successfully!" : "Your checks help refine your tomorrow cycle forecast."}
              </p>
            </div>
          </div>
          
          <button
            onClick={handleSave}
            disabled={saving}
            className={`bg-primary hover:bg-primary/95 text-on-primary font-bold px-xl py-md rounded-xl text-label-caps text-[13px] transition-transform active:scale-[0.98] shadow-md ${
              saving ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            {saving ? "Saving..." : success ? "Saved ✓" : "Save Daily Check-in"}
          </button>
        </div>
      </section>

      {/* Success Toast */}
      {success && (
        <div className="fixed bottom-20 right-4 z-50 bg-inverse-surface text-inverse-on-surface px-lg py-md rounded-xl shadow-lg flex items-center gap-sm animate-bounce">
          <span className="material-symbols-outlined text-primary-container">check_circle</span>
          <span className="text-[13px] font-medium">Daily symptom logs updated successfully!</span>
        </div>
      )}
    </div>
  );
}
