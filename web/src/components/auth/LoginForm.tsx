import { FormEvent, useState } from "react";

import { USER_DEPARTMENT_OPTIONS, UserDepartment } from "@types/index";
import { useAuthStore } from "@store/useAuthStore";

const LoginForm = () => {
  const { login, signup, loading, error } = useAuthStore((state) => ({
    login: state.login,
    signup: state.signup,
    loading: state.loading,
    error: state.error,
  }));
  const [mode, setMode] = useState<'login' | 'signup'>('login');
  const [form, setForm] = useState({
    id: '',
    nickname: '',
    password: '',
    department: UserDepartment.CloudSales,
  });

  const handleChange = (key: 'id' | 'nickname' | 'password', value: string) => {
    setForm((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleDepartmentChange = (value: UserDepartment) => {
    setForm((prev) => ({
      ...prev,
      department: value,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!form.id || !form.password) {
      alert('아이디와 비밀번호를 모두 입력해 주세요.');
      return;
    }

    if (mode === 'login') {
      await login({ id: form.id, password: form.password });
      return;
    }

    if (!form.nickname) {
      alert('닉네임을 입력해 주세요.');
      return;
    }

    await signup({
      id: form.id,
      nickname: form.nickname,
      password: form.password,
      department: form.department,
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md space-y-6 rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-slate-950/40 backdrop-blur"
      >
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-white">
            N3 업무 허브 {mode === 'login' ? '로그인' : '회원가입'}
          </h1>
          <p className="mt-2 text-sm text-slate-400">
            {mode === 'login'
              ? '사내 아이디로 로그인하여 프로젝트 대시보드를 확인하세요.'
              : '새 계정을 만들고 맞춤형 대시보드를 시작해 보세요.'}
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-slate-200" htmlFor="login-id">
              아이디
            </label>
            <input
              id="login-id"
              type="text"
              value={form.id}
              onChange={(event) => handleChange('id', event.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"
              placeholder="사내 아이디를 입력하세요"
              required
            />
          </div>

          {mode === 'signup' && (
            <>
              <div>
                <label className="text-sm font-medium text-slate-200" htmlFor="login-nickname">
                  닉네임
                </label>
                <input
                  id="login-nickname"
                  type="text"
                  value={form.nickname}
                  onChange={(event) => handleChange('nickname', event.target.value)}
                  className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"
                  placeholder="팀에서 사용하는 이름"
                  required
                />
              </div>

              <div>
                <label className="text-sm font-medium text-slate-200" htmlFor="login-department">
                  부서
                </label>
                <select
                  id="login-department"
                  value={form.department}
                  onChange={(event) => handleDepartmentChange(event.target.value as UserDepartment)}
                  className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 focus:border-indigo-400 focus:outline-none"
                >
                  {USER_DEPARTMENT_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          <div>
            <label className="text-sm font-medium text-slate-200" htmlFor="login-password">
              비밀번호
            </label>
            <input
              id="login-password"
              type="password"
              value={form.password}
              onChange={(event) => handleChange('password', event.target.value)}
              className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"
              placeholder="비밀번호를 입력하세요"
              required
            />
          </div>
        </div>

        {error && <p className="text-sm text-rose-400">{error}</p>}

        <button
          type="submit"
          className="flex w-full items-center justify-center rounded-xl bg-indigo-500 px-4 py-3 text-sm font-medium text-white shadow-lg shadow-indigo-500/40 transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-slate-600"
          disabled={loading}
        >
          {loading ? '처리 중...' : mode === 'login' ? '로그인' : '회원가입'}
        </button>

        <p className="text-center text-xs text-slate-500">
          {mode === 'login' ? '계정이 없으신가요?' : '이미 계정이 있으신가요?'}{' '}
          <button
            type="button"
            onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
            className="text-indigo-300 underline-offset-4 hover:underline"
          >
            {mode === 'login' ? '회원가입하기' : '로그인하기'}
          </button>
        </p>
      </form>
    </div>
  );
};

export default LoginForm;
