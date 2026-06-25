import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import SideNavBar from "@/components/SideNavBar";
import TopAppBar from "@/components/TopAppBar";
import BottomNavBar from "@/components/BottomNavBar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PCOS Copilot - Hormonal Intelligence",
  description: "Empathetic care and clinical-grade hormonal intelligence in your pocket.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="min-h-full bg-background text-on-surface">
        <div className="min-h-screen flex flex-col relative">
          {/* Desktop Navigation */}
          <SideNavBar />

          {/* Mobile Top App Bar */}
          <TopAppBar />

          {/* Main App Content Area */}
          {/* Offset: pl-64 on desktop (SideNavBar width), pt-16 on mobile (TopAppBar height), pb-16 on mobile (BottomNavBar height) */}
          <div className="flex-grow md:pl-64 pt-16 md:pt-0 pb-16 md:pb-0 min-h-screen">
            {children}
          </div>

          {/* Mobile Bottom Navigation */}
          <BottomNavBar />
        </div>
      </body>
    </html>
  );
}
