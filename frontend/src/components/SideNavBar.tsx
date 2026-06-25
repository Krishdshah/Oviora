"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function SideNavBar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Dashboard", href: "/", icon: "dashboard" },
    { name: "Symptoms", href: "/symptoms", icon: "monitor_heart" },
    { name: "Cycle", href: "/cycle", icon: "calendar_today" },
    { name: "Insights", href: "/insights", icon: "query_stats" },
    { name: "Lab Analyzer", href: "/lab-analyzer", icon: "description" },
    { name: "AI Coach", href: "/ai-coach", icon: "smart_toy", fill: true },
    { name: "Doctor Summary", href: "/doctor-summary", icon: "clinical_notes" },
    { name: "Profile", href: "/profile", icon: "person" },
  ];

  return (
    <aside className="h-screen w-64 fixed left-0 top-0 hidden md:flex flex-col bg-surface shadow-sm p-md gap-base z-50 border-r border-outline-variant/10">
      {/* Branding Logo */}
      <div className="flex items-center gap-sm mb-lg px-xs">
        <div className="w-10 h-10 rounded-xl ai-orb-gradient flex items-center justify-center shadow-md">
          <span className="material-symbols-outlined text-[24px] text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
            health_and_safety
          </span>
        </div>
        <div>
          <h1 className="font-display-hero text-title-card text-primary leading-none font-bold">PCOS Copilot</h1>
          <p className="text-[10px] font-label-caps text-on-surface-variant opacity-75 uppercase tracking-widest mt-0.5">
            Hormonal Intelligence
          </p>
        </div>
      </div>

      {/* Nav Menu */}
      <nav className="flex flex-col gap-xs flex-grow">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-md p-md rounded-xl font-label-caps text-label-caps transition-all active:scale-[0.98] ${
                isActive
                  ? "bg-secondary-container text-on-secondary-container font-bold shadow-sm"
                  : "text-on-surface-variant hover:bg-surface-variant/50 hover:text-primary"
              }`}
            >
              <span
                className="material-symbols-outlined"
                style={{
                  fontVariationSettings: isActive || item.fill ? "'FILL' 1" : "'FILL' 0",
                }}
              >
                {item.icon}
              </span>
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Premium Upgrade & Footer links */}
      <div className="mt-auto pt-lg border-t border-outline-variant/30 flex flex-col gap-xs">
        <div className="bg-primary-container/10 p-md rounded-2xl mb-xs border border-primary-container/20">
          <p className="font-label-caps text-[10px] text-primary font-bold mb-xs">PREMIUM ACCESS</p>
          <p className="text-[11px] text-on-surface-variant mb-md leading-tight">Unlock full hormonal insights & personalized meal protocols.</p>
          <button className="w-full bg-primary hover:bg-primary/95 text-on-primary font-bold py-sm px-md rounded-xl text-label-caps text-[11px] transition-transform active:scale-[0.98] shadow-sm">
            Upgrade to Premium
          </button>
        </div>
        <Link
          href="/support"
          className="text-on-surface-variant hover:bg-surface-variant/50 hover:text-primary rounded-xl p-sm flex items-center gap-sm text-label-caps transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">help</span>
          <span>Support</span>
        </Link>
        <Link
          href="/logout"
          className="text-on-surface-variant hover:bg-surface-variant/50 hover:text-error rounded-xl p-sm flex items-center gap-sm text-label-caps transition-colors"
        >
          <span className="material-symbols-outlined text-[18px]">logout</span>
          <span>Log Out</span>
        </Link>
      </div>
    </aside>
  );
}
