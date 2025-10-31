import { create } from "zustand";
import type { AxiosError } from "axios";

import api from "@lib/api";
import type { ApiResponse, Department } from "@types/index";

interface DepartmentStoreState {
  departments: Department[];
  loading: boolean;
  error?: string;
  fetchDepartments: () => Promise<void>;
}

export const useDepartmentStore = create<DepartmentStoreState>((set, get) => ({
  departments: [],
  loading: false,
  async fetchDepartments() {
    if (get().departments.length > 0) {
      return;
    }
    set({ loading: true, error: undefined });
    try {
      const response = await api.get<ApiResponse<Department[]>>("/departments");
      set({ departments: response.data.data, loading: false });
    } catch (error) {
      console.error(error);
      const axiosError = error as AxiosError<{ detail?: string }>;
      const message = axiosError.response?.data?.detail ?? "\uBD80\uC11C \uBAA9\uB85D\uC744 \uBD88\uB7EC\uC624\uC9C0 \uBABB\uD588\uC2B5\uB2C8\uB2E4.";
      set({ error: message, loading: false });
    }
  },
}));

