import { useEffect, useMemo } from "react";

import LoginForm from "@components/auth/LoginForm";
import CalendarView from "@components/calendar/CalendarView";
import ActivityTimeline from "@components/dashboard/ActivityTimeline";
import DepartmentWorkloadChart from "@components/dashboard/DepartmentWorkloadChart";
import ProjectStatusChart from "@components/dashboard/ProjectStatusChart";
import SummaryCards from "@components/dashboard/SummaryCards";
import GanttView from "@components/gantt/GanttView";
import Sidebar from "@components/layout/Sidebar";
import Header from "@components/layout/Header";
import PersonalWorkPanel from "@components/personal/PersonalWorkPanel";
import TodayChecklist from "@components/personal/TodayChecklist";
import KanbanBoard from "@components/kanban/KanbanBoard";
import TaskTable from "@components/table/TaskTable";
import ToastContainer from "@components/ui/ToastContainer";
import { useAuthStore } from "@store/useAuthStore";
import { useProjectStore } from "@store/useProjectStore";
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

  const content = user ? (
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
            <PersonalWorkPanel tasks={allTasks} currentUserId={user.id} />
            <TodayChecklist tasks={allTasks} assigneeId={user.id} />
          </section>
        </main>
      </div>
    </div>
  ) : (
    <LoginForm />
  );

  return (
    <>
      {content}
      <ToastContainer />
    </>
  );
};

export default App;




