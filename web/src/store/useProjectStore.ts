import { create } from 'zustand';
import type { AxiosError } from 'axios';

import api from '@lib/api';
import { showToast } from '@store/useToastStore';
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
  createProject: (input: { title: string; description?: string; department_id: string }) => Promise<Project | null>;
}

const DEFAULT_PROJECT_ERROR = "\uD504\uB85C\uC81D\uD2B8 \uC815\uBCF4\uB97C \uBD88\uB7EC\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4.";

export const useProjectStore = create<ProjectStoreState>((set) => ({
  projects: [],
  tasks: {},
  subtasks: {},
  activities: [],
  loading: false,
  async fetchDashboard() {
    set({ loading: true, error: undefined });
    try {
      const response = await api.get<ApiResponse<DashboardSummary>>("/projects/dashboard/summary");
      const recentActivities = response.data.data.recent_activities;
      set({ dashboard: response.data.data, activities: recentActivities, loading: false });
    } catch (error) {
      console.error(error);
      set({ error: "\uB300\uC2DC\uBCF4\uB4DC \uC694\uC57D\uC744 \uAC00\uC838\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4.", loading: false });
    }
  },
  async fetchProjects(params) {
    set({ loading: true, error: undefined });
    try {
      const response = await api.get<ApiResponse<Project[]>>("/projects", { params });
      set({ projects: response.data.data, loading: false });
    } catch (error) {
      console.error(error);
      set({ error: "\uD504\uB85C\uC81D\uD2B8 \uBAA9\uB85D\uC744 \uAC00\uC838\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4.", loading: false });
    }
  },
  async fetchTasks(projectId) {
    try {
      const response = await api.get<ApiResponse<Task[]>>(`/projects/${projectId}/tasks`);
      set((state) => ({ tasks: { ...state.tasks, [projectId]: response.data.data } }));
    } catch (error) {
      console.error(error);
      set({ error: "\uD0DC\uC2A4\uD06C \uC815\uBCF4\uB97C \uBD88\uB7EC\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4." });
    }
  },
  async fetchSubtasks(taskId) {
    try {
      const response = await api.get<ApiResponse<Subtask[]>>(`/subtasks/task/${taskId}`);
      set((state) => ({ subtasks: { ...state.subtasks, [taskId]: response.data.data } }));
    } catch (error) {
      console.error(error);
      set({ error: "\uC11C\uBE0C\uD0DC\uC2A4\uD06C \uC815\uBCF4\uB97C \uBD88\uB7EC\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4." });
    }
  },
  async createProject({ title, description, department_id }) {
    try {
      const response = await api.post<ApiResponse<Project>>("/projects", {
        title,
        description,
        department_id,
      });
      const project = response.data.data;
      set((state) => ({
        projects: [project, ...state.projects],
        error: undefined,
      }));
      showToast("\uD504\uB85C\uC81D\uD2B8\uB97C \uC0DD\uC131\uD588\uC2B5\uB2C8\uB2E4.", "success");
      return project;
    } catch (error) {
      console.error(error);
      const axiosError = error as AxiosError<{ detail?: string }>;
      const message = axiosError.response?.data?.detail ?? "\uD504\uB85C\uC81D\uD2B8 \uC0DD\uC131\uC5D0 \uC2E4\uD328\uD588\uC2B5\uB2C8\uB2E4.";
      set({ error: message || DEFAULT_PROJECT_ERROR });
      showToast(message || DEFAULT_PROJECT_ERROR, "error");
      return null;
    }
  },
}));