"use client";

import { useEffect, useState } from "react";
import { apiService } from "@/services/api";
import Link from "next/link";

interface DashboardData {
  profileName: string;
  cycle: {
    currentDay: number;
    totalDays: number;
    phase: string;
    phaseRemainingDays: number;
    estrogen: number;
    progesterone: number;
    lh: number;
    fsh: number;
  };
  recentSymptomStatus: string;
  todayFocus: string;
  tasks: Array<{ id: string; text: string; completed: boolean }>;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await apiService.getDashboardData();
        setData(res);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const toggleTask = (taskId: string) => {
    if (!data) return;
    setData({
      ...data,
      tasks: data.tasks.map((t) =>
        t.id === taskId ? { ...t, completed: !t.completed } : t
      ),
    });
    // TODO: Connect this to apiService.toggleDashboardTask(taskId) to save in backend
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-md">
          <span className="material-symbols-outlined text-[48px] text-primary animate-spin">
            progress_activity
          </span>
          <p className="font-label-caps text-on-surface-variant">Loading Hormonal Intelligence...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <p className="text-on-surface-variant">Failed to load data. Please refresh.</p>
      </div>
    );
  }

  const score = 78;
  const progressCircumference = 540;
  const strokeDashoffset = progressCircumference * (1 - score / 100);

  return (
    <div className="px-lg py-xl max-w-7xl mx-auto flex flex-col gap-lg">
      
      {/* Welcome Hero Banner */}
      <section className="relative overflow-hidden hero-gradient rounded-[32px] p-xl flex flex-col md:flex-row items-center justify-between gap-xl border border-outline-variant/20 shadow-sm transition-all hover:shadow-md">
        <div className="absolute top-[-20%] right-[-10%] w-[300px] h-[300px] bg-primary-fixed/20 blur-[80px] rounded-full -z-10"></div>
        <div className="relative z-10 flex-1">
          <h2 className="font-display-hero text-[32px] md:text-[38px] text-primary font-bold mb-xs">
            Good Morning, {data.profileName.split(" ")[0]}
          </h2>
          <p className="font-body-main text-on-surface-variant text-lg max-w-2xl leading-relaxed">
            Your health is improving this month. We noticed your sleep quality stabilized your cortisol levels and {data.todayFocus.toLowerCase()}
          </p>
          <div className="mt-lg flex gap-sm flex-wrap">
            <span className="bg-white/60 backdrop-blur-sm border border-outline-variant/20 px-md py-base rounded-full text-primary font-label-caps text-[11px] flex items-center gap-xs shadow-sm">
              <span className="material-symbols-outlined text-[14px]">trending_up</span>
              Improvement Streak: 12 Days
            </span>
            <span className="bg-white/60 backdrop-blur-sm border border-outline-variant/20 px-md py-base rounded-full text-on-surface-variant font-label-caps text-[11px] flex items-center gap-xs shadow-sm">
              <span className="material-symbols-outlined text-[14px]">water_drop</span>
              Phase: {data.cycle.phase} (Day {data.cycle.currentDay})
            </span>
          </div>
        </div>
        <div className="w-full md:w-[260px] h-[180px] relative flex justify-center shrink-0">
          <div className="w-40 h-40 rounded-full bg-primary-container/20 absolute -z-10 blur-xl"></div>
          {/* Abstract wellness design representation using CSS instead of broken image URLs */}
          <div className="flex items-center justify-center gap-sm">
            <div className="w-20 h-28 rounded-full bg-primary-container/40 blur-[2px] transform -rotate-12 animate-pulse"></div>
            <div className="w-24 h-24 rounded-full bg-secondary-container/50 blur-[2px] transform rotate-12 -ml-8"></div>
            <div className="w-16 h-28 rounded-full bg-tertiary-container/30 blur-[2px] transform -rotate-45 -ml-8"></div>
          </div>
        </div>
      </section>

      {/* Bento Grid Layout */}
      <div className="bento-grid">
        
        {/* Card 1: PCOS Health Score */}
        <div className="col-span-12 lg:col-span-4 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col items-center text-center transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div className="w-full flex justify-between items-center mb-md">
            <h3 className="font-title-card text-title-card text-on-surface font-semibold">Health Score</h3>
            <span className="material-symbols-outlined text-primary cursor-pointer hover:opacity-80">info</span>
          </div>
          
          <div className="relative w-44 h-44 mb-lg">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                className="text-surface-container-low"
                cx="88"
                cy="88"
                fill="transparent"
                r="78"
                stroke="currentColor"
                strokeWidth="10"
              />
              <circle
                className="text-primary"
                cx="88"
                cy="88"
                fill="transparent"
                r="78"
                stroke="url(#scoreGradient)"
                strokeDasharray={progressCircumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                strokeWidth="10"
                style={{ transition: "stroke-dashoffset 1s ease-in-out" }}
              />
              <defs>
                <linearGradient id="scoreGradient" x1="0%" x2="100%" y1="0%" y2="100%">
                  <stop offset="0%" stopColor="#F28C52" />
                  <stop offset="100%" stopColor="#FFD6BF" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold text-primary">{score}</span>
              <span className="text-[11px] font-label-caps text-on-surface-variant/70 uppercase">/100</span>
            </div>
          </div>

          <div className="bg-surface-container-low px-md py-sm rounded-full flex items-center gap-sm">
            <span className="w-2.5 h-2.5 rounded-full bg-primary-container animate-pulse"></span>
            <span className="font-label-caps text-[11px] text-primary font-bold">Status: Improving</span>
          </div>
        </div>

        {/* Card 2: Cycle Intelligence Progress */}
        <div className="col-span-12 lg:col-span-8 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col justify-between transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div className="flex justify-between items-start mb-lg gap-md">
            <div>
              <h3 className="font-title-card text-title-card text-on-surface font-semibold">Cycle Intelligence</h3>
              <p className="text-text-secondary text-on-surface-variant mt-0.5">{data.cycle.phase} Phase</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-primary">Day {data.cycle.currentDay} of {data.cycle.totalDays}</div>
              <p className="text-[12px] text-on-surface-variant mt-0.5">
                Ovulation Predicted: <span className="text-primary font-bold">in 8 days</span>
              </p>
            </div>
          </div>

          {/* Timeline Visualizer */}
          <div className="my-md">
            <div className="flex justify-between mb-2 px-1">
              <span className="text-[10px] font-label-caps text-on-surface-variant">Menstrual</span>
              <span className="text-[10px] font-label-caps text-primary font-bold">Follicular (Active)</span>
              <span className="text-[10px] font-label-caps text-on-surface-variant">Luteal</span>
            </div>
            <div className="h-4 w-full bg-surface-container-low rounded-full overflow-hidden flex border border-outline-variant/15 p-0.5">
              <div className="h-full bg-primary-fixed-dim/40 rounded-full" style={{ width: "18%" }}></div>
              <div className="h-full bg-primary-container rounded-full relative ml-1" style={{ width: "35%" }}>
                <div className="absolute top-0 right-1 w-2.5 h-2.5 bg-white rounded-full animate-ping"></div>
                <div className="absolute top-0.5 right-1.5 w-1.5 h-1.5 bg-white rounded-full"></div>
              </div>
              <div className="h-full bg-surface-container-low rounded-full ml-1" style={{ width: "47%" }}></div>
            </div>
            <div className="flex justify-between mt-1 px-1">
              <span className="text-[10px] text-on-surface-variant/60">Days 1-5</span>
              <span className="text-[10px] text-primary font-bold">Today: Day {data.cycle.currentDay}</span>
              <span className="text-[10px] text-on-surface-variant/60">Days 12-28</span>
            </div>
          </div>

          <div className="p-md bg-surface-container-low rounded-2xl flex items-start gap-md mt-sm border border-outline-variant/10">
            <span className="material-symbols-outlined text-primary mt-0.5">flare</span>
            <p className="text-[13px] text-on-surface-variant leading-relaxed">
              Your estrogen is rising. This stabilizes energy and mood. Consider scheduling high-energy tasks, resistance training, and complex discussions.
            </p>
          </div>
        </div>

        {/* Card 3: Hormonal Status Bento Column */}
        <div className="col-span-12 md:col-span-6 lg:col-span-7 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col gap-md transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div className="flex justify-between items-center mb-xs">
            <h3 className="font-title-card text-title-card text-on-surface font-semibold">Today's Hormonal Status</h3>
            <Link href="/lab-analyzer" className="text-primary hover:underline text-[12px] font-bold font-label-caps flex items-center gap-xs">
              View Labs <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
            </Link>
          </div>
          
          <div className="grid grid-cols-2 gap-sm">
            <div className="p-md bg-surface-container-low/40 rounded-xl border border-outline-variant/10 flex flex-col justify-between">
              <span className="text-[11px] font-label-caps text-on-surface-variant/70">ESTROGEN</span>
              <div className="flex items-baseline gap-xs mt-xs">
                <span className="text-2xl font-bold text-on-surface">{data.cycle.estrogen}</span>
                <span className="text-[11px] text-on-surface-variant">pg/mL</span>
              </div>
              <span className="text-[10px] text-primary font-bold mt-sm flex items-center gap-xs">
                <span className="material-symbols-outlined text-[12px]">trending_up</span> Rising
              </span>
            </div>
            
            <div className="p-md bg-surface-container-low/40 rounded-xl border border-outline-variant/10 flex flex-col justify-between">
              <span className="text-[11px] font-label-caps text-on-surface-variant/70">PROGESTERONE</span>
              <div className="flex items-baseline gap-xs mt-xs">
                <span className="text-2xl font-bold text-on-surface">{data.cycle.progesterone}</span>
                <span className="text-[11px] text-on-surface-variant">ng/mL</span>
              </div>
              <span className="text-[10px] text-on-surface-variant/60 mt-sm flex items-center gap-xs">
                <span className="material-symbols-outlined text-[12px]">horizontal_rule</span> Baseline Low
              </span>
            </div>

            <div className="p-md bg-surface-container-low/40 rounded-xl border border-outline-variant/10 flex flex-col justify-between">
              <span className="text-[11px] font-label-caps text-on-surface-variant/70">LH LEVELS</span>
              <div className="flex items-baseline gap-xs mt-xs">
                <span className="text-2xl font-bold text-on-surface">{data.cycle.lh}</span>
                <span className="text-[11px] text-on-surface-variant">mIU/mL</span>
              </div>
              <span className="text-[10px] text-on-surface-variant/60 mt-sm flex items-center gap-xs">
                <span className="material-symbols-outlined text-[12px]">check_circle</span> Normal Baseline
              </span>
            </div>

            <div className="p-md bg-surface-container-low/40 rounded-xl border border-outline-variant/10 flex flex-col justify-between">
              <span className="text-[11px] font-label-caps text-on-surface-variant/70">FSH LEVELS</span>
              <div className="flex items-baseline gap-xs mt-xs">
                <span className="text-2xl font-bold text-on-surface">{data.cycle.fsh}</span>
                <span className="text-[11px] text-on-surface-variant">mIU/mL</span>
              </div>
              <span className="text-[10px] text-on-surface-variant/60 mt-sm flex items-center gap-xs">
                <span className="material-symbols-outlined text-[12px]">check_circle</span> Normal Baseline
              </span>
            </div>
          </div>
        </div>

        {/* Card 4: Daily Copilot Checklist */}
        <div className="col-span-12 md:col-span-6 lg:col-span-5 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col justify-between transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div>
            <h3 className="font-title-card text-title-card text-on-surface font-semibold mb-xs">Daily Copilot Tasks</h3>
            <p className="text-text-secondary text-on-surface-variant mb-md">Your personalized hormonal actions for today.</p>
            
            <div className="flex flex-col gap-sm">
              {data.tasks.map((task) => (
                <div
                  key={task.id}
                  onClick={() => toggleTask(task.id)}
                  className="flex items-center gap-md p-md rounded-2xl bg-surface-container-low/40 hover:bg-surface-container-low border border-outline-variant/10 cursor-pointer transition-all active:scale-[0.99]"
                >
                  <span className={`material-symbols-outlined transition-colors ${
                    task.completed ? "text-primary fill-icon" : "text-outline"
                  }`}>
                    {task.completed ? "check_box" : "check_box_outline_blank"}
                  </span>
                  <span className={`text-[13px] leading-snug transition-all ${
                    task.completed ? "line-through text-on-surface-variant/50 font-medium" : "text-on-surface font-medium"
                  }`}>
                    {task.text}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-md pt-md border-t border-outline-variant/10 flex justify-between items-center">
            <span className="text-[11px] text-on-surface-variant/80 font-medium font-label-caps">
              {data.tasks.filter(t => t.completed).length} of {data.tasks.length} Completed
            </span>
            <Link href="/symptoms" className="text-primary hover:underline text-[11px] font-bold font-label-caps flex items-center gap-xs">
              Log Symptoms <span className="material-symbols-outlined text-[14px]">edit</span>
            </Link>
          </div>
        </div>

        {/* Card 5: AI Insights Summary */}
        <div className="col-span-12 md:col-span-7 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col justify-between transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div className="flex flex-col gap-sm">
            <div className="flex items-center gap-sm">
              <div className="w-8 h-8 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary">
                <span className="material-symbols-outlined text-[18px]">smart_toy</span>
              </div>
              <h3 className="font-title-card text-title-card text-on-surface font-semibold">AI Insights Summary</h3>
            </div>
            <p className="text-body-main text-on-surface-variant leading-relaxed text-[14px]">
              "Your LH levels show a normal follicular baseline. Based on your estrogen curve, ovulation is predicted in 8 days. Consider scheduling high-energy tasks for early next week. Your acne and bloating symptoms have decreased by 15% compared to this day last cycle."
            </p>
          </div>
          <div className="mt-lg flex gap-sm items-center">
            <Link href="/ai-coach" className="bg-primary hover:bg-primary/95 text-on-primary font-bold px-lg py-sm rounded-xl text-label-caps text-[11px] transition-transform active:scale-[0.98] shadow-sm">
              Chat with AI Coach
            </Link>
            <Link href="/insights" className="text-primary border border-primary/20 hover:bg-primary/5 font-bold px-lg py-sm rounded-xl text-label-caps text-[11px] transition-all">
              Detailed Trends
            </Link>
          </div>
        </div>

        {/* Card 6: Quick Actions Bento Column */}
        <div className="col-span-12 md:col-span-5 bg-white border border-outline-variant/20 rounded-[24px] shadow-sm p-lg flex flex-col justify-between transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
          <div>
            <h3 className="font-title-card text-title-card text-on-surface font-semibold mb-md">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-sm">
              <Link href="/symptoms" className="flex flex-col items-center justify-center p-md bg-surface-container-low/40 hover:bg-secondary-container/20 border border-outline-variant/10 rounded-2xl text-center transition-all group">
                <span className="material-symbols-outlined text-primary mb-xs group-hover:scale-110 transition-transform">edit_note</span>
                <span className="text-[12px] font-bold text-on-surface">Log Symptoms</span>
              </Link>
              
              <Link href="/ai-coach" className="flex flex-col items-center justify-center p-md bg-surface-container-low/40 hover:bg-secondary-container/20 border border-outline-variant/10 rounded-2xl text-center transition-all group">
                <span className="material-symbols-outlined text-primary mb-xs group-hover:scale-110 transition-transform">chat</span>
                <span className="text-[12px] font-bold text-on-surface">AI Coach Chat</span>
              </Link>

              <Link href="/lab-analyzer" className="flex flex-col items-center justify-center p-md bg-surface-container-low/40 hover:bg-secondary-container/20 border border-outline-variant/10 rounded-2xl text-center transition-all group">
                <span className="material-symbols-outlined text-primary mb-xs group-hover:scale-110 transition-transform">upload_file</span>
                <span className="text-[12px] font-bold text-on-surface">Lab Analyzer</span>
              </Link>

              <Link href="/doctor-summary" className="flex flex-col items-center justify-center p-md bg-surface-container-low/40 hover:bg-secondary-container/20 border border-outline-variant/10 rounded-2xl text-center transition-all group">
                <span className="material-symbols-outlined text-primary mb-xs group-hover:scale-110 transition-transform">picture_as_pdf</span>
                <span className="text-[12px] font-bold text-on-surface">Export Summary</span>
              </Link>
            </div>
          </div>
        </div>

      </div>
      
      {/* Recent Doctor Summary Export Row */}
      <section className="bg-primary text-on-primary rounded-[32px] p-xl flex flex-col md:flex-row justify-between items-center gap-lg shadow-lg border border-primary-container/20">
        <div className="flex items-center gap-md">
          <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
            <span className="material-symbols-outlined text-[26px]">clinical_notes</span>
          </div>
          <div>
            <h4 className="font-title-section text-title-card font-semibold mb-0.5">Clinical Share Export Ready</h4>
            <p className="opacity-80 text-[13px] leading-tight">Generate a HIPAA-compliant medical-grade trend export for your gynecologist.</p>
          </div>
        </div>
        <Link href="/doctor-summary" className="bg-white text-primary hover:bg-surface-container-low font-bold px-xl py-md rounded-xl text-label-caps text-[12px] transition-transform active:scale-[0.98] shadow-md shrink-0">
          Generate PCOS Clinical Export
        </Link>
      </section>

    </div>
  );
}
