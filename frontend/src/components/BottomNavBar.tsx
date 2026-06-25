"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function BottomNavBar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Home", href: "/", icon: "home" },
    { name: "Cycle", href: "/cycle", icon: "calendar_month" },
    { name: "Coach", href: "/ai-coach", icon: "chat_bubble", center: true },
    { name: "Insights", href: "/insights", icon: "analytics" },
    { name: "Profile", href: "/profile", icon: "account_circle" },
  ];

  return (
    <nav className="fixed bottom-0 w-full z-50 rounded-t-2xl md:hidden bg-surface/90 backdrop-blur-xl shadow-[0_-4px_20px_rgba(0,0,0,0.05)] border-t border-outline-variant/10 flex justify-around items-center h-16 px-md pb-safe">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        
        if (item.center) {
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex flex-col items-center justify-center rounded-full p-2 w-12 h-12 -mt-8 shadow-lg border-4 border-background transition-transform active:scale-95 ${
                isActive
                  ? "bg-primary text-on-primary"
                  : "bg-primary-container text-on-primary-container"
              }`}
            >
              <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                {item.icon}
              </span>
            </Link>
          );
        }

        return (
          <Link
            key={item.name}
            href={item.href}
            className={`flex flex-col items-center justify-center p-2 transition-colors ${
              isActive ? "text-primary font-semibold" : "text-on-surface-variant hover:text-primary"
            }`}
          >
            <span className="material-symbols-outlined text-[22px]" style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}>
              {item.icon}
            </span>
            <span className="font-label-caps text-[9px] uppercase mt-0.5 tracking-wider">{item.name}</span>
          </Link>
        );
      })}
    </nav>
  );
}
