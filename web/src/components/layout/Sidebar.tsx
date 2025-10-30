import type { Project } from '@types/index';

interface SidebarProps {
  projects: Project[];
}

const Sidebar = ({ projects }: SidebarProps) => {
  return (
    <aside className="hidden lg:flex w-72 flex-col border-r border-slate-800 bg-slate-900/70 glass-panel text-slate-100">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-semibold tracking-tight">N3 업무 허브</h1>
        <p className="mt-2 text-sm text-slate-400">조직 프로젝트와 업무를 한 화면에서</p>
      </div>
      <nav className="flex-1 overflow-y-auto p-4 space-y-6">
        <div>
          <h2 className="text-xs uppercase tracking-wide text-slate-500">프로젝트</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {projects.map((project) => (
              <li key={project.id} className="rounded-lg bg-slate-800/40 px-3 py-2 hover:bg-slate-700/40 transition">
                <p className="font-medium text-slate-200 line-clamp-1">{project.title}</p>
                <span className="text-xs text-slate-400">{project.status.replace('_', ' ')}</span>
              </li>
            ))}
            {!projects.length && (
              <li className="rounded-lg bg-slate-800/40 px-3 py-3 text-slate-500">등록된 프로젝트가 없습니다.</li>
            )}
          </ul>
        </div>
        <div>
          <h2 className="text-xs uppercase tracking-wide text-slate-500">빠른 작업</h2>
          <ul className="mt-3 space-y-2 text-sm text-slate-300">
            <li className="rounded-lg border border-slate-700 px-3 py-2 hover:border-indigo-400 hover:text-indigo-300 transition">새 프로젝트 생성</li>
            <li className="rounded-lg border border-slate-700 px-3 py-2 hover:border-indigo-400 hover:text-indigo-300 transition">업무 템플릿 관리</li>
            <li className="rounded-lg border border-slate-700 px-3 py-2 hover:border-indigo-400 hover:text-indigo-300 transition">팀 멤버 초대</li>
          </ul>
        </div>
      </nav>
      <div className="border-t border-slate-800 p-4 text-xs text-slate-500">
        © {new Date().getFullYear()} N3 Collaboration Platform
      </div>
    </aside>
  );
};

export default Sidebar;
