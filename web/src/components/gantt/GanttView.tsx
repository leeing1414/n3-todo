import { useEffect, useRef } from 'react';
import type { Task } from '@types/index';

const GanttView = ({ tasks }: { tasks: Task[] }) => {
  const ganttRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ganttRef.current) return;

    (async () => {
      const { default: Gantt } = await import('frappe-gantt');
      const ganttTasks = tasks
        .filter((task) => task.start_date && task.due_date)
        .map((task) => ({
          id: task.id,
          name: task.title,
          start: task.start_date!,
          end: task.due_date!,
          progress: Math.round(task.progress ?? 0),
          custom_class: `status-${task.status}`,
        }));

      if (!ganttTasks.length) {
        ganttRef.current!.innerHTML = '<div class="text-sm text-slate-400">간트 차트로 표현할 일정 데이터가 없습니다.</div>';
        return;
      }

      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const gantt = new Gantt(ganttRef.current, ganttTasks, {
        view_mode: 'Week',
        custom_popup_html: (task: any) => `
          <div class="rounded-xl border border-slate-800 bg-slate-900/90 p-3 text-left text-sm">
            <h6 class="text-slate-100 font-semibold">${task.name}</h6>
            <p class="text-slate-400 mt-1">${task._start} ~ ${task._end}</p>
            <p class="text-indigo-300 mt-2">진척도 ${task.progress}%</p>
          </div>
        `,
      });
    })();
  }, [tasks]);

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">간트 차트</h4>
      <p className="text-sm text-slate-400">일정 기반 계획과 진척도</p>
      <div ref={ganttRef} className="gantt-container mt-4 overflow-x-auto" />
    </section>
  );
};

export default GanttView;
