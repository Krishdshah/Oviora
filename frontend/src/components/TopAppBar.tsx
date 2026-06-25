import Link from "next/link";

export default function TopAppBar() {
  return (
    <header className="fixed top-0 w-full z-50 md:hidden bg-surface/85 backdrop-blur-xl flex justify-between items-center px-lg py-md border-b border-outline-variant/10 shadow-sm">
      <Link href="/" className="flex items-center gap-xs">
        <div className="w-8 h-8 rounded-lg ai-orb-gradient flex items-center justify-center">
          <span className="material-symbols-outlined text-[18px] text-white" style={{ fontVariationSettings: "'FILL' 1" }}>
            health_and_safety
          </span>
        </div>
        <span className="font-display-hero text-title-card text-primary font-bold tracking-tight">
          PCOS Copilot
        </span>
      </Link>
      
      <div className="flex gap-md text-primary">
        <button className="hover:opacity-85 active:scale-95 transition-all">
          <span className="material-symbols-outlined text-[20px]">notifications</span>
        </button>
        <Link href="/profile" className="hover:opacity-85 active:scale-95 transition-all flex items-center">
          <span className="material-symbols-outlined text-[20px]">settings</span>
        </Link>
      </div>
    </header>
  );
}
