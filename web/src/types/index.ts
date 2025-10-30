export type ProjectStatus = 'planned' | 'in_progress' | 'completed' | 'on_hold' | 'cancelled';
export type ProjectPriority = 'low' | 'medium' | 'high' | 'critical';
export type ProjectRisk = 'low' | 'medium' | 'high';
export type TaskStatus = 'todo' | 'in_progress' | 'review' | 'blocked' | 'done';
export type TaskPriority = 'low' | 'medium' | 'high' | 'urgent';
export type SubtaskStatus = 'todo' | 'in_progress' | 'done' | 'blocked';
export type UserRole = 'admin' | 'manager' | 'member';

export interface BaseEntity {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface Company extends BaseEntity {
  name: string;
  description?: string | null;
  domain?: string | null;
  tags: string[];
}

export enum UserDepartment {
  CloudSales = '클라우드 영업',
  CloudManagement = '클라우드 관리',
  TechnicalSupport = '기술지원본부',
  BusinessSupport = 'Business Support',
  SolutionTeam = '솔루션팀',
  CloudAI = '클라우드 AI',
  Undefined = '미지정',
}

export const USER_DEPARTMENT_OPTIONS: { label: string; value: UserDepartment }[] = [
  { label: '클라우드 영업', value: UserDepartment.CloudSales },
  { label: '클라우드 관리', value: UserDepartment.CloudManagement },
  { label: '기술지원본부', value: UserDepartment.TechnicalSupport },
  { label: 'Business Support', value: UserDepartment.BusinessSupport },
  { label: '솔루션팀', value: UserDepartment.SolutionTeam },
  { label: '클라우드 AI', value: UserDepartment.CloudAI },
  { label: '미지정', value: UserDepartment.Undefined },
];

export interface Department extends BaseEntity {
  company_id: string;
  name: string;
  description?: string | null;
  lead_id?: string | null;
  tags: string[];
}

export interface User extends BaseEntity {
  name: string;
  role: UserRole;
  department_id?: string | null;
  title?: string | null;
  phone?: string | null;
  avatar_url?: string | null;
  is_active: boolean;
  timezone?: string | null;
}

export interface Project extends BaseEntity {
  title: string;
  description?: string | null;
  department_id: string;
  status: ProjectStatus;
  priority: ProjectPriority;
  risk_level: ProjectRisk;
  progress: number;
  start_date?: string | null;
  end_date?: string | null;
  assignee_id?: string | null;
  content?: string | null;
  references: string[];
  tags: string[];
  member_ids: string[];
  watcher_ids: string[];
  department_name?: string | null;
}

export interface Task extends BaseEntity {
  project_id: string;
  title: string;
  description?: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  progress: number;
  start_date?: string | null;
  due_date?: string | null;
  assignee_id?: string | null;
  content?: string | null;
  references: string[];
  tags: string[];
  checklist: string[];
}

export interface Subtask extends BaseEntity {
  task_id: string;
  title: string;
  content?: string | null;
  status: SubtaskStatus;
  assignee_id?: string | null;
  order: number;
  due_date?: string | null;
}

export interface Activity extends BaseEntity {
  project_id?: string | null;
  task_id?: string | null;
  actor_id?: string | null;
  action: 'created' | 'updated' | 'status_changed' | 'comment' | 'attachment_added';
  detail?: string | null;
  occurred_at: string;
}

export interface DashboardSummary {
  project_total: number;
  active_projects: number;
  overdue_tasks: number;
  upcoming_deadlines: Array<Record<string, unknown>>;
  project_status_distribution: Array<Record<string, unknown>>;
  task_status_distribution: Array<Record<string, unknown>>;
  department_workload: Array<Record<string, unknown>>;
  recent_activities: Activity[];
}

export interface ApiResponse<T> {
  status_code: number;
  detail: string;
  data: T;
}

export interface AuthUser {
  id: string;
  nickname: string;
  department: UserDepartment;
  token: string;
}
