import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

import type { Activity } from '@types/index';

interface ActivityTimelineProps {
  activities: Activity[];
}

const ActivityTimeline = ({ activities }: ActivityTimelineProps) => {
  return (
    <section className="glass-panel rounded-3xl border border-slate-800 p-6">
      <h4 className="text-lg font-semibold text-slate-100">최근 활동 로그</h4>
      <ul className="mt-4 space-y-4">
        {activities.map((activity) => (
          <li key={activity.id} className="relative pl-6">
            <span className="absolute left-0 top-1.5 h-1.5 w-1.5 rounded-full bg-indigo-400" />
            <p className="text-sm text-slate-200">{activity.detail ?? activity.action}</p>
            <p className="text-xs text-slate-500">
              {formatDistanceToNow(new Date(activity.occurred_at), { addSuffix: true, locale: ko })}
            </p>
          </li>
        ))}
        {!activities.length && <li className="text-sm text-slate-500">최근 활동 내역이 없습니다.</li>}
      </ul>
    </section>
  );
};

export default ActivityTimeline;
