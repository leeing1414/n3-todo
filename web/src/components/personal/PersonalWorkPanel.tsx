import type { Task } from '@types/index';

interface PersonalWorkPanelProps {
  tasks: Task[];
  currentUserId: string;
}

const priorityOrder: Record<string, number> = {
  urgent: 0,
  high: 1,
  medium: 2,
  low: 3,
};

const PersonalWorkPanel = ({ tasks, currentUserId }: PersonalWorkPanelProps) => {
  const personalTasks = tasks
    .filter((task) => task.assignee_id === currentUserId)
    .sort((a, b) => (priorityOrder[a.priority] ?? 99) - (priorityOrder[b.priority] ?? 99));

  const fallbackTasks = tasks
    .filter((task) => !task.assignee_id)
    .sort((a, b) => (priorityOrder[a.priority] ?? 99) - (priorityOrder[b.priority] ?? 99))
    .slice(0, 5);

  const items = personalTasks.length ? personalTasks : fallbackTasks;

  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">내 업무 스프린트</h4>
      <p className="text-sm text-slate-400">담당 업무와 개인 메모</p>
      <ul className="mt-4 space-y-3">
        {items.map((task) => (
          <li key={task.id} className="rounded-2xl border border-slate-800/60 bg-slate-900/40 p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-sm font-semibold text-slate-100">{task.title}</p>
                <p className="mt-1 text-xs text-slate-400 line-clamp-2">{task.description ?? '상세 설명이 없습니다.'}</p>
              </div>
              <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-indigo-300 uppercase">
                {task.priority}
              </span>
            </div>
            <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
              <span>진척도 {task.progress}%</span>
              <button className="rounded-full border border-slate-700 px-3 py-1 text-slate-300 hover:border-indigo-400 hover:text-indigo-200">
                메모 추가
              </button>
            </div>
          </li>
        ))}
        {!items.length && (
          <li className="rounded-2xl border border-slate-800/60 bg-slate-900/40 p-6 text-center text-sm text-slate-500">
            현재 담당 중인 업무가 없습니다.
          </li>
        )}
      </ul>
    </section>
  );
};

export default PersonalWorkPanel;
