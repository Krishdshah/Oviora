"use client";

import { useState } from "react";
import Link from "next/link";

export default function Profile() {
  const [goals, setGoals] = useState({
    weightLoss: true,
    fertility: true,
    regularCycles: true,
    betterSkin: false,
  });

  const [connectedDevices, setConnectedDevices] = useState({
    appleHealth: true,
    fitbit: false,
    garmin: false,
  });

  const toggleGoal = (goalKey: keyof typeof goals) => {
    setGoals((prev) => ({
      ...prev,
      [goalKey]: !prev[goalKey],
    }));
  };

  const toggleDevice = (deviceKey: keyof typeof connectedDevices) => {
    setConnectedDevices((prev) => ({
      ...prev,
      [deviceKey]: !prev[deviceKey],
    }));
  };

  return (
    <div className="px-lg py-xl max-w-6xl mx-auto flex flex-col gap-lg">
      
      {/* Profile Welcome Header */}
      <section className="flex flex-col md:flex-row md:items-end justify-between gap-lg mb-sm">
        <div>
          <div className="mb-xs">
            <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[10px] font-bold">
              PERSONALIZED PROFILE
            </span>
          </div>
          <h2 className="font-display-hero text-[32px] md:text-[40px] text-on-surface font-bold tracking-tight mb-xs">
            Sarah Thompson
          </h2>
          <p className="font-body-main text-on-surface-variant max-w-xl leading-relaxed">
            Managing PCOS with intelligent data since Jan 2024. Your personalized wellness recommendations align to your goals below.
          </p>
        </div>
        
        <div className="flex items-center gap-md shrink-0">
          <div className="w-16 h-16 rounded-full border-4 border-primary-container overflow-hidden shadow-md flex items-center justify-center bg-surface-container-low">
            <span className="material-symbols-outlined text-primary text-[32px]">person</span>
          </div>
          <button className="bg-surface-container-low hover:bg-primary-fixed/20 text-primary border border-primary/15 px-lg py-md rounded-xl font-bold text-label-caps text-[11px] transition-all active:scale-95">
            Edit Photo
          </button>
        </div>
      </section>

      {/* Bento Grid */}
      <div className="bento-grid">
        
        {/* Health Profile Goals (Large Card) */}
        <div className="col-span-12 lg:col-span-7 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <div className="flex justify-between items-center mb-lg">
              <h3 className="font-title-card text-title-card font-semibold text-on-surface flex items-center gap-xs">
                <span className="material-symbols-outlined text-primary" style={{ fontVariationSettings: "'FILL' 1" }}>
                  track_changes
                </span>
                Health Profile Goals
              </h3>
              <span className="text-[10px] font-label-caps text-on-surface-variant/60 font-bold uppercase">
                Tap to Toggle
              </span>
            </div>
            
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-sm">
              <button
                onClick={() => toggleGoal("weightLoss")}
                className={`p-md rounded-2xl flex flex-col items-center gap-sm border transition-colors cursor-pointer text-center ${
                  goals.weightLoss
                    ? "bg-primary-fixed/30 border-primary/30"
                    : "bg-surface-container-low border-outline-variant/20 hover:border-primary/20"
                }`}
              >
                <div className="w-10 h-10 rounded-full bg-primary-container/10 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined">scale</span>
                </div>
                <span className="font-label-caps text-[10px] text-on-surface-variant font-bold">
                  Weight Loss
                </span>
              </button>

              <button
                onClick={() => toggleGoal("fertility")}
                className={`p-md rounded-2xl flex flex-col items-center gap-sm border transition-colors cursor-pointer text-center ${
                  goals.fertility
                    ? "bg-primary-fixed/30 border-primary/30"
                    : "bg-surface-container-low border-outline-variant/20 hover:border-primary/20"
                }`}
              >
                <div className="w-10 h-10 rounded-full bg-primary-container/10 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined">baby_changing_station</span>
                </div>
                <span className="font-label-caps text-[10px] text-on-surface-variant font-bold">
                  Fertility
                </span>
              </button>

              <button
                onClick={() => toggleGoal("regularCycles")}
                className={`p-md rounded-2xl flex flex-col items-center gap-sm border transition-colors cursor-pointer text-center ${
                  goals.regularCycles
                    ? "bg-primary-fixed/30 border-primary/30"
                    : "bg-surface-container-low border-outline-variant/20 hover:border-primary/20"
                }`}
              >
                <div className="w-10 h-10 rounded-full bg-primary-container/10 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined">event_repeat</span>
                </div>
                <span className="font-label-caps text-[10px] text-on-surface-variant font-bold">
                  Regular Cycles
                </span>
              </button>

              <button
                onClick={() => toggleGoal("betterSkin")}
                className={`p-md rounded-2xl flex flex-col items-center gap-sm border transition-colors cursor-pointer text-center ${
                  goals.betterSkin
                    ? "bg-primary-fixed/30 border-primary/30"
                    : "bg-surface-container-low border-outline-variant/20 hover:border-primary/20"
                }`}
              >
                <div className="w-10 h-10 rounded-full bg-primary-container/10 text-primary flex items-center justify-center">
                  <span className="material-symbols-outlined">face_retouching_natural</span>
                </div>
                <span className="font-label-caps text-[10px] text-on-surface-variant font-bold">
                  Better Skin
                </span>
              </button>
            </div>
          </div>
          
          <div className="mt-lg p-md bg-primary-fixed/20 rounded-xl flex items-center gap-md border border-primary-fixed/30">
            <span className="material-symbols-outlined text-primary">auto_awesome</span>
            <p className="text-[12px] text-primary italic leading-tight">
              "We've prioritized regular cycles & insulin-balancing metrics in your AI recommendations today."
            </p>
          </div>
        </div>

        {/* Connected Wearables Card */}
        <div className="col-span-12 lg:col-span-5 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm flex flex-col justify-between hover:-translate-y-1 transition-all duration-300">
          <div>
            <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-lg flex items-center gap-xs">
              <span className="material-symbols-outlined text-primary">devices</span>
              Connected Devices
            </h3>
            
            <div className="space-y-sm">
              <div className="flex items-center justify-between p-md bg-surface-container-low/30 rounded-xl border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <span className="material-symbols-outlined text-[#FA2D48]">health_metrics</span>
                  <div>
                    <p className="font-bold text-on-surface text-[13px]">Apple Health</p>
                    <p className="text-[10px] text-on-surface-variant">Last synced: 2 mins ago</p>
                  </div>
                </div>
                <button
                  onClick={() => toggleDevice("appleHealth")}
                  className={`material-symbols-outlined transition-colors ${
                    connectedDevices.appleHealth ? "text-tertiary" : "text-outline-variant"
                  }`}
                  style={{ fontVariationSettings: "'FILL' 1" }}
                >
                  check_circle
                </button>
              </div>

              <div className="flex items-center justify-between p-md bg-surface-container-low/30 rounded-xl border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <span className="material-symbols-outlined text-primary">watch</span>
                  <div>
                    <p className="font-bold text-on-surface text-[13px]">Fitbit</p>
                    <p className="text-[10px] text-on-surface-variant">
                      {connectedDevices.fitbit ? "Synced just now" : "Not connected"}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => toggleDevice("fitbit")}
                  className="text-primary font-bold text-[11px] font-label-caps hover:underline"
                >
                  {connectedDevices.fitbit ? "Disconnect" : "Connect"}
                </button>
              </div>

              <div className="flex items-center justify-between p-md bg-surface-container-low/30 rounded-xl border border-outline-variant/10">
                <div className="flex items-center gap-md">
                  <span className="material-symbols-outlined text-blue-600">directions_run</span>
                  <div>
                    <p className="font-bold text-on-surface text-[13px]">Garmin</p>
                    <p className="text-[10px] text-on-surface-variant">
                      {connectedDevices.garmin ? "Synced just now" : "Not connected"}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => toggleDevice("garmin")}
                  className="text-primary font-bold text-[11px] font-label-caps hover:underline"
                >
                  {connectedDevices.garmin ? "Disconnect" : "Connect"}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Configuration settings (Full Width) */}
        <div className="col-span-12 bg-white border border-outline-variant/20 rounded-[24px] p-lg shadow-sm hover:-translate-y-1 transition-all duration-300 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full -mr-32 -mt-32 blur-3xl"></div>
          
          <h3 className="font-title-card text-title-card font-semibold text-on-surface mb-lg flex items-center gap-xs relative z-10">
            <span className="material-symbols-outlined text-primary">settings</span>
            Account Settings
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-md relative z-10">
            <div className="p-md rounded-2xl bg-surface-container-low/40 hover:bg-surface-container-low border border-outline-variant/10 transition-colors group cursor-pointer">
              <div className="flex items-center justify-between mb-md">
                <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center group-hover:scale-105 transition-transform text-primary">
                  <span className="material-symbols-outlined">notifications_active</span>
                </div>
                <span className="material-symbols-outlined text-outline text-[18px]">chevron_right</span>
              </div>
              <h4 className="font-bold text-on-surface text-[14px]">Notifications</h4>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-normal">
                Manage notifications for ovulation spikes, logging check-ins, and diet insights.
              </p>
            </div>

            <div className="p-md rounded-2xl bg-surface-container-low/40 hover:bg-surface-container-low border border-outline-variant/10 transition-colors group cursor-pointer">
              <div className="flex items-center justify-between mb-md">
                <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center group-hover:scale-105 transition-transform text-primary">
                  <span className="material-symbols-outlined">shield_person</span>
                </div>
                <span className="material-symbols-outlined text-outline text-[18px]">chevron_right</span>
              </div>
              <h4 className="font-bold text-on-surface text-[14px]">Privacy & Security</h4>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-normal">
                Biometric locks, HIPAA sharing configurations, and medical data deletion keys.
              </p>
            </div>

            <div className="p-md rounded-2xl bg-surface-container-low/40 hover:bg-surface-container-low border border-outline-variant/10 transition-colors group cursor-pointer">
              <div className="flex items-center justify-between mb-md">
                <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center group-hover:scale-105 transition-transform text-primary">
                  <span className="material-symbols-outlined">folder_managed</span>
                </div>
                <span className="material-symbols-outlined text-outline text-[18px]">chevron_right</span>
              </div>
              <h4 className="font-bold text-on-surface text-[14px]">Medical Records</h4>
              <p className="text-[11px] text-on-surface-variant mt-1 leading-normal">
                Securely store past blood reports, ultrasounds, and lab analyzer extractions.
              </p>
            </div>
          </div>
        </div>

      </div>

      {/* Quick stats bottom row */}
      <section className="flex flex-wrap gap-md justify-center mt-md">
        <div className="flex items-center gap-md px-lg py-md bg-white border border-outline-variant/10 rounded-2xl shadow-sm">
          <span className="text-xl font-bold text-primary">124</span>
          <span className="text-[10px] font-label-caps font-bold text-on-surface-variant uppercase">Days Tracked</span>
        </div>
        <div className="flex items-center gap-md px-lg py-md bg-white border border-outline-variant/10 rounded-2xl shadow-sm">
          <span className="text-xl font-bold text-primary">8</span>
          <span className="text-[10px] font-label-caps font-bold text-on-surface-variant uppercase">Insights Compiled</span>
        </div>
        <div className="flex items-center gap-md px-lg py-md bg-white border border-outline-variant/10 rounded-2xl shadow-sm">
          <span className="text-xl font-bold text-primary">98%</span>
          <span className="text-[10px] font-label-caps font-bold text-on-surface-variant uppercase">Data Fidelity</span>
        </div>
      </section>

    </div>
  );
}
