export default function SupportPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-lg py-xl">
      <div className="max-w-2xl bg-white border border-outline-variant/20 rounded-[32px] p-xl shadow-sm text-center">
        <div className="w-16 h-16 rounded-full bg-primary-container text-white flex items-center justify-center mx-auto mb-md">
          <span className="material-symbols-outlined text-[32px]">support_agent</span>
        </div>
        <h1 className="font-display-hero text-[32px] text-primary font-bold mb-xs">
          Help & Support
        </h1>
        <p className="font-body-main text-on-surface-variant text-lg leading-relaxed mb-lg">
          Our clinical support team is currently assisting other users. Please check back later, or email us at support@oviora.com for urgent inquiries.
        </p>
        <button className="bg-primary text-on-primary hover:bg-primary/95 font-bold py-sm px-xl rounded-xl transition-all shadow-sm">
          Return to Dashboard
        </button>
      </div>
    </div>
  );
}
