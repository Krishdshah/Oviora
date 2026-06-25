"use client";

import { useEffect, useRef, useState } from "react";
import { apiService, CoachMessage } from "@/services/api";

export default function AICoach() {
  const [messages, setMessages] = useState<CoachMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    async function loadMessages() {
      try {
        const res = await apiService.getCoachMessages();
        setMessages(res);
      } catch (err) {
        console.error("Failed to load coach messages", err);
      } finally {
        setLoading(false);
      }
    }
    loadMessages();
  }, []);

  // Scroll to bottom whenever messages or typing state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: CoachMessage = {
      id: String(Date.now()),
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputValue("");
    setIsTyping(true);

    try {
      const reply = await apiService.sendMessageToCoach(text);
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      console.error("Failed to send message", err);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend(inputValue);
    }
  };

  const suggestedPrompts = [
    { title: "Cycle Delayed", text: "Why is my cycle delayed this month?", icon: "calendar_month" },
    { title: "Skin Health", text: "Can I reduce acne naturally with my diet?", icon: "auto_awesome" },
    { title: "Lab Report", text: "Explain my recent hormone report in detail.", icon: "lab_research" },
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-md">
          <span className="material-symbols-outlined text-[48px] text-primary animate-spin">
            progress_activity
          </span>
          <p className="font-label-caps text-on-surface-variant">Connecting Hormonal Coach...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen flex flex-col relative overflow-hidden bg-background">
      {/* Atmospheric Background Blurs */}
      <div className="absolute top-[-10%] right-[-10%] w-[450px] h-[450px] bg-primary-fixed/15 blur-[120px] rounded-full -z-10"></div>
      <div className="absolute bottom-[-5%] left-[-5%] w-[350px] h-[350px] bg-tertiary-fixed/10 blur-[100px] rounded-full -z-10"></div>

      {/* Chat Container */}
      <div className="flex-grow flex flex-col max-w-4xl mx-auto w-full px-md md:px-lg py-lg md:py-xl justify-between h-[calc(100vh-64px)] md:h-screen">
        
        {/* Header Greeting */}
        <div className="mb-md text-center md:text-left shrink-0">
          <div className="mb-xs">
            <span className="bg-primary-container/10 border border-primary/20 text-primary px-sm py-xs rounded-full font-label-caps text-[9px] font-bold">
              AI CLINICAL COMPANION
            </span>
          </div>
          <h2 className="font-display-hero text-2xl md:text-3xl text-on-surface font-bold mb-xs">
            Hi Sarah, How can I help today?
          </h2>
          <p className="text-[13px] text-on-surface-variant leading-relaxed">
            I'm your AI Coach, here to help navigate your hormonal health with clinical accuracy, diet protocols, and lifestyle empathy.
          </p>
        </div>

        {/* Messages List Area */}
        <div className="flex-grow overflow-y-auto mb-md pr-xs space-y-lg flex flex-col py-sm">
          
          {messages.map((msg) => {
            const isCoach = msg.sender === "coach";
            return (
              <div key={msg.id} className={`flex items-start gap-md ${!isCoach ? "justify-end" : "justify-start"}`}>
                
                {isCoach && (
                  <div className="ai-orb-gradient w-10 h-10 rounded-full flex-shrink-0 mt-1 flex items-center justify-center text-white shadow-sm border border-white/20">
                    <span className="material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      smart_toy
                    </span>
                  </div>
                )}
                
                <div className={`p-lg rounded-2xl max-w-[85%] border shadow-sm ${
                  isCoach
                    ? "bg-white border-outline-variant/10 rounded-tl-none text-on-surface"
                    : "bg-primary text-on-primary border-primary rounded-tr-none"
                }`}>
                  <p className="text-[13.5px] leading-relaxed whitespace-pre-wrap">{msg.text}</p>
                  
                  {/* Visual UI Injection if AI gives clinical checklist tips (Matches simulated body content) */}
                  {isCoach && msg.text.includes("afternoon energy dip") && (
                    <div className="bg-surface-container-low border-l-4 border-primary p-md rounded-xl mt-md">
                      <ul className="text-on-surface-variant text-[12px] space-y-xs">
                        <li className="flex items-center gap-xs">
                          <span className="material-symbols-outlined text-[16px] text-primary">check_circle</span>
                          Afternoon energy dip noted 4 times this week
                        </li>
                        <li className="flex items-center gap-xs">
                          <span className="material-symbols-outlined text-[16px] text-primary">check_circle</span>
                          High carb intake logged during lunch
                        </li>
                      </ul>
                    </div>
                  )}

                  <span className={`text-[9px] uppercase tracking-wider block mt-sm font-label-caps opacity-50 ${
                    isCoach ? "text-on-surface-variant" : "text-on-primary"
                  }`}>
                    {isCoach ? "COACH" : "YOU"} • {msg.timestamp}
                  </span>
                </div>

                {!isCoach && (
                  <div className="w-10 h-10 rounded-full bg-surface-container-high flex items-center justify-center border border-outline-variant/30 flex-shrink-0 overflow-hidden shadow-sm">
                    <span className="material-symbols-outlined text-[20px] text-on-surface-variant">person</span>
                  </div>
                )}

              </div>
            );
          })}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex items-start gap-md justify-start animate-pulse">
              <div className="ai-orb-gradient w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center text-white shadow-sm border border-white/20">
                <span className="material-symbols-outlined text-[20px]">smart_toy</span>
              </div>
              <div className="bg-white border border-outline-variant/10 p-md rounded-2xl rounded-tl-none max-w-[85%] shadow-sm">
                <div className="flex gap-xs items-center py-sm px-md">
                  <span className="w-2.5 h-2.5 rounded-full bg-primary/40 animate-bounce" style={{ animationDelay: "0ms" }}></span>
                  <span className="w-2.5 h-2.5 rounded-full bg-primary/60 animate-bounce" style={{ animationDelay: "150ms" }}></span>
                  <span className="w-2.5 h-2.5 rounded-full bg-primary/80 animate-bounce" style={{ animationDelay: "300ms" }}></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Prompts Bento Grid (Only shows if there are few messages, or as helpers at bottom) */}
        {messages.length <= 3 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-md my-sm shrink-0">
            {suggestedPrompts.map((prompt) => (
              <button
                key={prompt.title}
                onClick={() => handleSend(prompt.text)}
                className="bg-white hover:bg-primary-fixed/30 border border-outline-variant/20 p-md rounded-2xl text-left transition-all duration-300 group hover:-translate-y-0.5 active:scale-[0.99] shadow-sm flex flex-col justify-between"
              >
                <div className="flex justify-between items-center w-full mb-xs">
                  <span className="material-symbols-outlined text-primary group-hover:scale-110 transition-transform">
                    {prompt.icon}
                  </span>
                  <span className="material-symbols-outlined text-[14px] text-outline opacity-0 group-hover:opacity-100 transition-opacity">
                    arrow_forward
                  </span>
                </div>
                <div>
                  <span className="font-title-card text-[13px] font-bold text-primary block mb-0.5">
                    {prompt.title}
                  </span>
                  <p className="text-[11px] text-on-surface-variant leading-snug">
                    "{prompt.text}"
                  </p>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Chat Input Bar */}
        <div className="glass-panel border border-outline-variant/20 rounded-[24px] p-2 flex items-center gap-md shadow-lg shrink-0 mt-sm">
          <button className="w-10 h-10 rounded-xl hover:bg-surface-container-low flex items-center justify-center text-on-surface-variant transition-colors active:scale-95 shrink-0">
            <span className="material-symbols-outlined text-[20px]">add</span>
          </button>
          
          <input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            className="flex-grow bg-transparent border-none focus:outline-none focus:ring-0 text-[13.5px] placeholder:text-on-surface-variant/40 px-xs"
            placeholder="Ask your AI coach anything about cycles, diet, labs..."
            type="text"
          />
          
          <button
            onClick={() => handleSend(inputValue)}
            className="bg-primary hover:bg-primary/95 text-on-primary w-10 h-10 rounded-xl flex items-center justify-center transition-all active:scale-95 shadow-md shrink-0"
          >
            <span className="material-symbols-outlined text-[20px]">send</span>
          </button>
        </div>

      </div>
    </main>
  );
}
