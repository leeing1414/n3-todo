import { useMemo, useState } from "react";

import type { Project } from "@types/index";
import CreateProjectModal from "@components/project/CreateProjectModal";

interface SidebarProps {
  projects: Project[];
}

const Sidebar = ({ projects }: SidebarProps) => {
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const sortedProjects = useMemo(() => {
    return [...projects].sort((a, b) => {
      const timeA = Number.isFinite(new Date(a.created_at).getTime())
        ? new Date(a.created_at).getTime()
        : 0;
      const timeB = Number.isFinite(new Date(b.created_at).getTime())
        ? new Date(b.created_at).getTime()
        : 0;
      return timeB - timeA;
    });
  }, [projects]);

  return (
    <>
      <aside className="hidden w-72 flex-col border-r border-slate-800 bg-slate-900/70 text-slate-100 lg:flex">
        <div className="border-b border-slate-800 p-6">
          <h1 className="text-xl font-semibold tracking-tight">N3 \uD611\uC5ED \uD50C\uB7AB\uD3FC</h1>
          <p className="mt-2 text-sm text-slate-400">\uD300\uACFC \uD504\uB85C\uC81D\uD2B8 \uC9C4\uD589 \uC0C1\uD669\uC744 \uD55C\uB208\uC5D0 \uC0B4\uD3B8\uBCF4\uC138\uC694.</p>
        </div>
        <nav className="flex-1 space-y-6 overflow-y-auto p-4">
          <div>
            <h2 className="text-xs uppercase tracking-wide text-slate-500">\uCD5C\uADFC \uD504\uB85C\uC81D\uD2B8</h2>
            <ul className="mt-3 space-y-2 text-sm">
              {sortedProjects.map((project) => (
                <li
                  key={project.id}
                  className="rounded-lg bg-slate-800/40 px-3 py-2 transition hover:bg-slate-700/40"
                >
                  <p className="line-clamp-1 font-medium text-slate-200">{project.title}</p>
                  <span className="text-xs text-slate-400">{project.status.replace("_", " ")}</span>
                </li>
              ))}
              {!sortedProjects.length && (
                <li className="rounded-lg bg-slate-800/40 px-3 py-3 text-slate-500">
                  \uB4F1\uB85D\uB41C \uD504\uB85C\uC81D\uD2B8\uAC00 \uC5C6\uC2B5\uB2C8\uB2E4.
                </li>
              )}
            </ul>
          </div>
          <div>
            <h2 className="text-xs uppercase tracking-wide text-slate-500">\uBE60\uB978 \uC791\uC5C5</h2>
            <ul className="mt-3 space-y-2 text-sm text-slate-300">
              <li>
                <button
                  type="button"
                  onClick={() => setIsCreateOpen(true)}
                  className="w-full rounded-lg border border-slate-700 px-3 py-2 text-left transition hover:border-indigo-400 hover:text-indigo-300"
                >
                  \uC0C8 \uD504\uB85C\uC81D\uD2B8 \uC0DD\uC131
                </button>
              </li>
              <li className="rounded-lg border border-slate-700 px-3 py-2 transition hover:border-indigo-400 hover:text-indigo-300">
                \uD300 \uB300\uC2DC\uBCF4\uB4DC \uC5F4\uAE30
              </li>
              <li className="rounded-lg border border-slate-700 px-3 py-2 transition hover:border-indigo-400 hover:text-indigo-300">
                \uB0B4 \uC5C5\uBB34 \uD55C\uB208\uC5D0 \uBCF4\uAE30
              </li>
            </ul>
          </div>
        </nav>
        <div className="border-t border-slate-800 p-4 text-xs text-slate-500">
          \u00A9 {new Date().getFullYear()} N3 Collaboration Platform
        </div>
      </aside>
      <CreateProjectModal open={isCreateOpen} onClose={() => setIsCreateOpen(false)} />
    </>
  );
};

export default Sidebar;