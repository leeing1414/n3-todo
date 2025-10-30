import { create } from 'zustand';
import api from '@lib/api';
import type {
  Activity,
  ApiResponse,
  DashboardSummary,
  Project,
  Subtask,
  Task,
} from '@types/index';

interface ProjectStoreState {
  projects: Project[];
  tasks: Record<string, Task[]>;
  subtasks: Record<string, Subtask[]>;
  activities: Activity[];
  dashboard?: DashboardSummary;
  loading: boolean;
  error?: string;
  fetchDashboard: () => Promise<void>;
  fetchProjects: (params?: { department_id?: string }) => Promise<void>;
  fetchTasks: (projectId: string) => Promise<void>;
  fetchSubtasks: (taskId: string) => Promise<void>;
}

export const useProjectStore = create<ProjectStoreState>((set) => ({
  projects: [],
  tasks: {},
  subtasks: {},
  activities: [],
  loading: false,
  async fetchDashboard() {
    set({ loading: true, error: undefined });
    try {
      const response = await api.get<ApiResponse<DashboardSummary>>('/projects/dashboard/summary');
      const recentActivities = response.data.data.recent_activities;
      set({ dashboard: response.data.data, activities: recentActivities, loading: false });
    } catch (error) {
      console.error(error);
      set({ error: '대시보드 데이터를 불러오지 못했습니다.', loading: false });
    }
  },
  async fetchProjects(params) {
    set({ loading: true, error: undefined });
    try {
      const response = await api.get<ApiResponse<Project[]>>('/projects', { params });
      set({ projects: response.data.data, loading: false });
    } catch (error) {
      console.error(error);
      set({ error: '프로젝트 목록을 불러오지 못했습니다.', loading: false });
    }
  },
  async fetchTasks(projectId) {
    try {
      const response = await api.get<ApiResponse<Task[]>>(`/projects/${projectId}/tasks`);
      set((state) => ({ tasks: { ...state.tasks, [projectId]: response.data.data } }));
    } catch (error) {
      console.error(error);
      set({ error: '태스크 정보를 불러오지 못했습니다.' });
    }
  },
  async fetchSubtasks(taskId) {
    try {
      const response = await api.get<ApiResponse<Subtask[]>>(`/subtasks/task/${taskId}`);
      set((state) => ({ subtasks: { ...state.subtasks, [taskId]: response.data.data } }));
    } catch (error) {
      console.error(error);
      set({ error: '서브태스크 정보를 불러오지 못했습니다.' });
    }
  },
}));
