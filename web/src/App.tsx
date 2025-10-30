import { useEffect, useMemo } from 'react';

import LoginForm from '@components/auth/LoginForm';
import CalendarView from '@components/calendar/CalendarView';
import ActivityTimeline from '@components/dashboard/ActivityTimeline';
import DepartmentWorkloadChart from '@components/dashboard/DepartmentWorkloadChart';
import ProjectStatusChart from '@components/dashboard/ProjectStatusChart';
import SummaryCards from '@components/dashboard/SummaryCards';
import GanttView from '@components/gantt/GanttView';
import Sidebar from '@components/layout/Sidebar';
import Header from '@components/layout/Header';
import PersonalWorkPanel from '@components/personal/PersonalWorkPanel';
import KanbanBoard from '@components/kanban/KanbanBoard';
import TaskTable from '@components/table/TaskTable';
import { useAuthStore } from '@store/useAuthStore';
import { useProjectStore } from '@store/useProjectStore';

const DEMO_USER_ID = 'demo-user';

const App = () => {
  const { user, logout } = useAuthStore((state) => ({
    user: state.user,
    logout: state.logout,
  }));

  const {
    projects,
    dashboard,
    tasks,
    activities,
    loading,
    fetchDashboard,
    fetchProjects,
    fetchTasks,
  } = useProjectStore((state) => ({
    projects: state.projects,
    dashboard: state.dashboard,
    tasks: state.tasks,
    activities: state.activities,
    loading: state.loading,
    fetchDashboard: state.fetchDashboard,
    fetchProjects: state.fetchProjects,
    fetchTasks: state.fetchTasks,
  }));

  useEffect(() => {
    if (!user) return;
    void fetchDashboard();
    void fetchProjects();
  }, [fetchDashboard, fetchProjects, user]);

  useEffect(() => {
    if (!user) return;
    projects.slice(0, 4).forEach((project) => {
      if (!tasks[project.id]) {
        void fetchTasks(project.id);
      }
    });
  }, [projects, tasks, fetchTasks, user]);

  const allTasks = useMemo(() => Object.values(tasks).flat(), [tasks]);

  if (!user) {
    return <LoginForm />;
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <Sidebar projects={projects} />
      <div className="flex flex-1 flex-col">
        <Header userName={user.nickname} department={user.department} onLogout={logout} />
        <main className="flex-1 space-y-6 overflow-y-auto bg-transparent p-6">
          <SummaryCards summary={dashboard} loading={loading} />

          <section className="grid gap-6 xl:grid-cols-3">
            <div className="xl:col-span-1">
              <ProjectStatusChart data={dashboard?.project_status_distribution ?? []} />
            </div>
            <div className="xl:col-span-1">
              <DepartmentWorkloadChart data={dashboard?.department_workload ?? []} />
            </div>
            <div className="xl:col-span-1">
              <ActivityTimeline activities={activities} />
            </div>
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <KanbanBoard tasks={allTasks} />
            <GanttView tasks={allTasks} />
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <CalendarView tasks={allTasks} />
            <TaskTable tasks={allTasks} />
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <PersonalWorkPanel tasks={allTasks} currentUserId={DEMO_USER_ID} />
            <div className="glass-panel rounded-3xl border border-slate-800 p-6">
              <h4 className="text-lg font-semibold text-slate-100">AI 업무 요약 (준비 중)</h4>
              <p className="mt-2 text-sm text-slate-400">
                분석된 데이터를 기반으로 우선순위와 병목을 추천하는 AI 요약 기능이 곧 제공됩니다.
              </p>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default App;