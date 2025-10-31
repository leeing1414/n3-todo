import { FormEvent, useEffect, useMemo, useState } from "react";

import { useDepartmentStore } from "@store/useDepartmentStore";
import { useProjectStore } from "@store/useProjectStore";

interface CreateProjectModalProps {
  open: boolean;
  onClose: () => void;
}

const CreateProjectModal = ({ open, onClose }: CreateProjectModalProps) => {
  const { departments, loading: departmentsLoading, error } = useDepartmentStore((state) => ({
    departments: state.departments,
    loading: state.loading,
    error: state.error,
  }));
  const fetchDepartments = useDepartmentStore((state) => state.fetchDepartments);
  const createProject = useProjectStore((state) => state.createProject);

  const [title, setTitle] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | undefined>();

  useEffect(() => {
    if (!open) {
      return;
    }
    void fetchDepartments();
  }, [open, fetchDepartments]);

  useEffect(() => {
    if (!open) {
      return;
    }
    if (!departmentId && departments.length > 0) {
      setDepartmentId(departments[0].id);
    }
  }, [open, departments, departmentId]);

  const isReady = useMemo(() => {
    return title.trim().length > 0 && departmentId.trim().length > 0;
  }, [title, departmentId]);

  const closeAndReset = () => {
    setTitle("");
    setDepartmentId("");
    setDescription("");
    setSubmitting(false);
    setFormError(undefined);
    onClose();
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!isReady) {
      setFormError("\uD504\uB85C\uC81D\uD2B8 \uC774\uB984\uACFC \uBD80\uC11C\uB97C \uC120\uD0DD\uD574 \uC8FC\uC138\uC694.");
      return;
    }
    setSubmitting(true);
    const result = await createProject({
      title: title.trim(),
      description: description.trim() || undefined,
      department_id: departmentId,
    });
    setSubmitting(false);
    if (result) {
      closeAndReset();
    }
  };

  if (!open) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-[1200] flex items-center justify-center bg-slate-950/70 px-4 backdrop-blur">
      <div className="w-full max-w-lg rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl shadow-black/40">
        <header className="mb-4">
          <h3 className="text-xl font-semibold text-slate-100">\uC0C8 \uD504\uB85C\uC81D\uD2B8 \uC0DD\uC131</h3>
          <p className="mt-1 text-sm text-slate-400">\uAE30\uBCF8 \uC815\uBCF4\uB9CC \uC785\uB825\uD558\uBA74 \uB098\uC911\uC5D0 \uC138\uBD80 \uB0B4\uC6A9\uC744 \uCD94\uAC00\uD560 \uC218 \uC788\uC5B4\uC694.</p>
        </header>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-200" htmlFor="project-title">
              \uD504\uB85C\uC81D\uD2B8 \uC774\uB984
            </label>
            <input
              id="project-title"
              type="text"
              value={title}
              onChange={(event) => {
                setTitle(event.target.value);
                setFormError(undefined);
              }}
              className="w-full rounded-2xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"
              placeholder="\uC608) \uC2E0\uADDC \uD611\uC5ED \uD50C\uB7AB\uD3FC \uB7F0\uCE6D"
              required
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-200" htmlFor="project-department">
              \uB2F4\uB2F9 \uBD80\uC11C
            </label>
            <select
              id="project-department"
              value={departmentId}
              onChange={(event) => setDepartmentId(event.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 focus:border-indigo-400 focus:outline-none"
              required
            >
              <option value="" disabled>
                \uBD80\uC11C\uB97C \uC120\uD0DD\uD574 \uC8FC\uC138\uC694
              </option>
              {departments.map((dept) => (
                <option key={dept.id} value={dept.id}>
                  {dept.name}
                </option>
              ))}
            </select>
            {(departmentsLoading || departments.length === 0) && (
              <p className="text-xs text-slate-500">\uBD80\uC11C \uC815\uBCF4\uB97C \uBD88\uB7EC\uC624\uB294 \uC911\uC785\uB2C8\uB2E4...</p>
            )}
            {error && <p className="text-xs text-rose-400">{error}</p>}
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-200" htmlFor="project-description">
              \uD504\uB85C\uC81D\uD2B8 \uC124\uBA85 (\uC120\uD0DD)
            </label>
            <textarea
              id="project-description"
              rows={3}
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-400 focus:outline-none"
              placeholder="\uD504\uB85C\uC81D\uD2B8\uC758 \uBAA9\uD45C\uB098 \uC8FC\uC694 \uC5C5\uBB34\uB97C \uAC04\uB2E8\uD788 \uC801\uC5B4 \uC8FC\uC138\uC694."
            />
          </div>
          {formError && <p className="text-sm text-rose-400">{formError}</p>}
          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={closeAndReset}
              className="rounded-2xl border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:border-slate-500 hover:text-white"
              disabled={submitting}
            >
              \uCDE8\uC18C
            </button>
            <button
              type="submit"
              className="rounded-2xl bg-indigo-500 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-indigo-500/40 transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:bg-slate-600"
              disabled={!isReady || submitting}
            >
              {submitting ? "\uC0DD\uC131 \uC911..." : "\uD504\uB85C\uC81D\uD2B8 \uC0DD\uC131"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateProjectModal;