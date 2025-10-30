import { format } from "date-fns";

import type { DashboardSummary } from "@types/index";

interface SummaryCardsProps {
  summary?: DashboardSummary;
  loading: boolean;
}

const SummaryCards = ({ summary, loading }: SummaryCardsProps) => {
  const today = format(new Date(), "yyyy-MM-dd");

  const cards = [
    {
      label: "Total Projects",
      value: summary?.project_total ?? 0,
      accent: "from-sky-500/20 to-sky-400/10",
      badge: "Projects",
    },
    {
      label: "Active Projects",
      value: summary?.active_projects ?? 0,
      accent: "from-emerald-500/20 to-emerald-400/10",
      badge: "Active",
    },
    {
      label: "Upcoming Deadlines",
      value: summary?.upcoming_deadlines?.length ?? 0,
      accent: "from-amber-500/20 to-amber-400/10",
      badge: "Due Soon",
    },
    {
      label: "Overdue Tasks",
      value: summary?.overdue_tasks ?? 0,
      accent: "from-rose-500/20 to-rose-400/10",
      badge: "Overdue",
    },
  ];

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6 shadow-lg shadow-slate-900/30">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-indigo-300">Daily Summary</p>
          <h3 className="mt-2 text-2xl font-semibold text-slate-50">Key Metrics as of {today}</h3>
        </div>
        <button className="inline-flex items-center gap-2 rounded-full bg-indigo-500/90 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-indigo-500/30 transition hover:bg-indigo-500">
          Refresh Data
        </button>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => (
          <article
            key={card.label}
            className={`rounded-2xl border border-slate-800 bg-gradient-to-br ${card.accent} p-4`}
          >
            <span className="text-xs uppercase tracking-wide text-slate-300">{card.badge}</span>
            <p className="mt-4 text-3xl font-semibold text-white">
              {loading ? "…" : card.value.toLocaleString()}
            </p>
            <p className="mt-1 text-sm text-slate-300">{card.label}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default SummaryCards;
