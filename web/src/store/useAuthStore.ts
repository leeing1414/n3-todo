import { create } from "zustand";
import type { AxiosError } from "axios";
import api from "@lib/api";
import type { AuthUser, UserDepartment } from "@types/index";

interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  error?: string;
  login: (input: { id: string; password: string }) => Promise<void>;
  signup: (input: { id: string; nickname: string; password: string; department: UserDepartment }) => Promise<void>;
  logout: () => void;
}

const getDepartmentValue = (value: string | undefined): UserDepartment => {
  if (!value) {
    return UserDepartment.Undefined;
  }
  const entries = Object.values(UserDepartment);
  return entries.includes(value as UserDepartment)
    ? (value as UserDepartment)
    : UserDepartment.Undefined;
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  async login({ id, password }) {
    set({ loading: true, error: undefined });
    try {
      const response = await api.post("/auth/login", {
        username: id,
        password,
      });
      const payload = response.data.data;
      set({
        user: {
          id: payload?.user_id ?? id,
          nickname: payload?.nickname ?? "",
          department: getDepartmentValue(payload?.department),
          token: payload?.access_token ?? "",
        },
        loading: false,
      });
    } catch (error) {
      console.error(error);
      set({
        error: "Login failed. Please check your ID and password.",
        loading: false,
      });
    }
  },
  async signup({ id, nickname, password, department }) {
    set({ loading: true, error: undefined });
    try {
      await api.post("/auth/register", {
        username: id,
        name: nickname,
        password,
        department,
      });
      await useAuthStore.getState().login({ id, password });
    } catch (error) {
      console.error(error);
      const axiosError = error as AxiosError<{
        detail?: string;
        data?: { errors?: Array<{ label?: string; field?: string; message?: string }> };
      }>;
      const detail = axiosError.response?.data?.detail;
      const errors = axiosError.response?.data?.data?.errors;
      const fallback = "Sign-up failed. Please verify the input information.";
      const firstError = errors && errors.length > 0 ? errors[0] : undefined;
      const formatted =
        detail ||
        (firstError
          ? `${firstError.label ?? firstError.field ?? "입력"}: ${firstError.message ?? fallback}`
          : undefined);
      set({
        error: formatted ?? fallback,
        loading: false,
      });
    }
  },
  logout() {
    set({ user: null, error: undefined });
  },
}));
