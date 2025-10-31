import { useMemo } from "react";
import { format, isToday, parseISO } from "date-fns";
import { ko } from "date-fns/locale";

import type { Task } from "@types/index";

interface TodayChecklistProps {
  tasks: Task[];
  assigneeId?: string;
}

const priorityBadge: Record<string, string> = {
  urgent: "bg-rose-500/20 text-rose-300 border border-rose-500/40",
  high: "bg-amber-500/20 text-amber-300 border border-amber-500/40",
  medium: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40",
  low: "bg-slate-500/20 text-slate-300 border border-slate-500/40",
};

const safeParseDate = (value?: string | null) => {
  if (!value) return null;
  try {
    const date = parseISO(value);
    if (Number.isNaN(date.getTime())) {
      return null;
    }
    return date;
  } catch (error) {
    console.error("Failed to parse date", error);
    return null;
  }
};

const TodayChecklist = ({ tasks, assigneeId }: TodayChecklistProps) => {
  const todayKey = useMemo(() => format(new Date(), "yyyy-MM-dd"), []);

  const todayTasks = useMemo(() => {
    const filtered = tasks.filter((task) => {
      if (assigneeId && task.assignee_id && task.assignee_id !== assigneeId) {
        return false;
      }
      const dueDate = safeParseDate(task.due_date);
      return dueDate && isToday(dueDate) && task.status !== "done";
    });

    const priorityOrder: Record<string, number> = { urgent: 0, high: 1, medium: 2, low: 3 };

    return filtered
      .sort((a, b) => (priorityOrder[a.priority] ?? 99) - (priorityOrder[b.priority] ?? 99))
      .slice(0, 10);
  }, [tasks, assigneeId]);

  const headline = useMemo(() => {
    try {
      return format(new Date(), "M월 d일 (EEE)", { locale: ko });
    } catch {
      return todayKey;
    }
  }, [todayKey]);

  return (
    <section className="glass-panel flex h-full flex-col rounded-3xl border border-slate-800 p-6">
      <header className="flex items-center justify-between">
        <div>
          <h4 className="text-lg font-semibold text-slate-100">오늘 할 일 체크리스트</h4>
          <p className="text-sm text-slate-400">{headline} 기준</p>
        </div>
        <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300">
          {todayTasks.length}건
        </span>
      </header>

      <ul className="mt-4 space-y-3">
        {todayTasks.map((task) => (
          <li
            key={task.id}
            className="flex items-start gap-3 rounded-2xl border border-slate-800/60 bg-slate-900/50 p-4"
          >
            <div className="mt-1">
              <input
                type="checkbox"
                checked={task.status === "done"}
                onChange={(event) => event.preventDefault()}
                className="h-4 w-4 cursor-not-allowed rounded border-slate-600 bg-slate-800 text-emerald-400 focus:ring-emerald-400"
              />
            </div>
            <div className="flex-1 space-y-2">
              <div className="flex items-center justify-between gap-3">
                <p className="text-sm font-semibold text-slate-100">{task.title}</p>
                <span
                  className={`rounded-full px-3 py-1 text-xs uppercase ${
                    priorityBadge[task.priority] ?? priorityBadge.low
                  }`}
                >
                  {task.priority}
                </span>
              </div>
              <p className="text-xs text-slate-400">
                {task.description?.trim() || "설명이 등록되지 않았습니다."}
              </p>
              {task.checklist && task.checklist.length > 0 && (
                <div className="space-y-1 rounded-2xl bg-slate-900/60 p-3">
                  {task.checklist.map((item, index) => (
                    <div
                      key={`${task.id}-item-${index}`}
                      className="flex items-center gap-2 text-xs text-slate-300"
                    >
                      <span className="block h-1.5 w-1.5 rounded-full bg-indigo-400" />
                      <span className="leading-tight">{item}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </li>
        ))}

        {!todayTasks.length && (
          <li className="rounded-2xl border border-dashed border-slate-700 bg-slate-900/30 p-6 text-center text-sm text-slate-400">
            오늘 마감 예정인 할 일이 없습니다. 긴급한 업무가 있다면 체크리스트에 추가해 보세요.
          </li>
        )}
      </ul>
    </section>
  );
};

export default TodayChecklist;
