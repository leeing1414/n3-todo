import { create } from "zustand";
import type { AxiosError } from "axios";

import api from "@lib/api";
import type { AuthUser } from "@types/index";
import { UserDepartment } from "@types/index";
import { showToast } from "@store/useToastStore";

interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  error?: string;
  login: (input: { id: string; password: string }) => Promise<void>;
  signup: (input: {
    id: string;
    nickname: string;
    password: string;
    department: UserDepartment;
  }) => Promise<void>;
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

const applyAuthToken = (token: string | undefined) => {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
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
      const token = payload?.access_token ?? "";
      applyAuthToken(token);
      set({
        user: {
          id: payload?.user_id ?? id,
          nickname: payload?.nickname ?? "",
          department: getDepartmentValue(payload?.department),
          token,
        },
        loading: false,
      });
      showToast("로그인되었습니다.", "success");
    } catch (error) {
      console.error(error);
      const message = "로그인에 실패했습니다. 아이디와 비밀번호를 확인해 주세요.";
      set({
        error: message,
        loading: false,
      });
      showToast(message, "error");
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
      const fallback = "회원가입에 실패했습니다. 입력 정보를 확인해 주세요.";
      const firstError = errors && errors.length > 0 ? errors[0] : undefined;
      const message =
        detail ||
        (firstError
          ? `${firstError.label ?? firstError.field ?? "입력"}: ${firstError.message ?? fallback}`
          : undefined) ||
        fallback;
      set({
        error: message,
        loading: false,
      });
      showToast(message, "error");
    }
  },
  logout() {
    set({ user: null, error: undefined });
    applyAuthToken(undefined);
    showToast("로그아웃되었습니다.", "info");
  },
}));
