export default function LogoutPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-lg py-xl">
      <div className="max-w-md w-full bg-white border border-outline-variant/20 rounded-[32px] p-xl shadow-sm text-center">
        <div className="w-16 h-16 rounded-full bg-surface-variant text-on-surface-variant flex items-center justify-center mx-auto mb-md">
          <span className="material-symbols-outlined text-[32px]">logout</span>
        </div>
        <h1 className="font-display-hero text-[28px] text-on-surface font-bold mb-xs">
          Logging Out...
        </h1>
        <p className="font-body-main text-on-surface-variant leading-relaxed mb-lg">
          We are securely clearing your clinical session. See you next time!
        </p>
      </div>
    </div>
  );
}
