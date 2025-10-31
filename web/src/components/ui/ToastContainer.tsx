import clsx from "clsx";

import { useToastStore } from "@store/useToastStore";
import type { ToastType } from "@store/useToastStore";

const typeStyles: Record<ToastType, string> = {
  success: "bg-emerald-500/90",
  error: "bg-rose-500/90",
  info: "bg-slate-800/90",
};

const ToastContainer = () => {
  const toasts = useToastStore((state) => state.toasts);
  const removeToast = useToastStore((state) => state.removeToast);

  if (toasts.length === 0) {
    return null;
  }

  return (
    <div className="pointer-events-none fixed bottom-6 right-6 z-[1000] flex flex-col gap-3">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={clsx(
            "pointer-events-auto flex min-w-[220px] items-start gap-3 rounded-2xl px-4 py-3 text-sm font-medium text-white shadow-xl shadow-black/30 backdrop-blur",
            typeStyles[toast.type],
          )}
        >
          <span className="leading-snug">{toast.message}</span>
          <button
            type="button"
            onClick={() => removeToast(toast.id)}
            className="ml-auto text-white/70 transition hover:text-white"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
};

export default ToastContainer;
